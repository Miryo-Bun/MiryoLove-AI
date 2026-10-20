#!/usr/bin/env python3
"""MiryoLove AI.
- Programming: MiryoWiki, then English Wikipedia, then Wikipedia in the question's language.
- Homework: short explanation plus one task (statement only, no solution).
- Examples: short code with comments (Python, C, C++, Java, Assembly).
- History and general topics: Wikipedia in the question's language (ru, uk, en).
- Translation: question starts with 'переведи', 'переклади' or 'translate'.
Prompts are in English; answers follow the question's language.
"""
import json
import os
import re
import urllib.parse
import urllib.request

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_PATH = os.environ.get("MIRYO_MODEL", "/mnt/Tears/MiryoLove AI/Qwen/miryo_merged_7b")
MIRYOWIKI_API = os.environ.get("MIRYOWIKI_API", "http://127.0.0.1:8081/api.php")
USER_AGENT = "MiryoLoveAI/1.0 (personal project)"
MAX_CHARS = 8000
MAX_NEW_TOKENS = 1700
LANG_NAMES = {"ru": "Russian", "uk": "Ukrainian", "en": "English"}
NOT_FOUND = {
    "ru": "Не нашёл статью по этому вопросу. Попробуй другие слова.",
    "uk": "Не знайшов статтю за цим запитанням. Спробуй інші слова.",
    "en": "No article found for this question. Try other keywords.",
}

PROGRAMMING = re.compile(
    r"python|java|c\+\+|cpp|\bc\b|assembly|ассемблер|код|функци|массив|список|стек|очеред|"
    r"цикл|класс|указател|переменн|алгоритм|рекурс|словар|кортеж|linux|программ|"
    r"code|function|array|stack|queue|loop|pointer|algorithm|program",
    re.IGNORECASE,
)
HOMEWORK = re.compile(r"задани|домашк|\bдз\b|задач|завдання|домашн|homework|exercise", re.IGNORECASE)
EXAMPLE = re.compile(r"^\s*(пример|приклад|example)\b", re.IGNORECASE)
TRANSLATE = re.compile(r"^\s*(переведи|переклади|translate)\b", re.IGNORECASE)
DISAMBIG = re.compile(r"\((прізвище|значення|фамилия|значение|disambiguation)\)", re.IGNORECASE)

STOP_WORDS = {
    "хто", "такий", "така", "таке", "що", "який", "яка", "як", "про", "розкажи", "расскажи",
    "истории", "история", "кто", "такой", "такая", "что", "такое", "какой", "о", "об",
    "who", "what", "is", "was", "tell", "about", "the", "a", "an",
}


def detect_lang(text):
    t = text.lower()
    if re.search(r"[іїєґ]", t):
        return "uk"
    if re.search(r"[а-яё]", t):
        return "ru"
    return "en"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def clean_query(query):
    words = [w for w in re.findall(r"\w+", query.lower()) if w not in STOP_WORDS and len(w) > 1]
    return " ".join(words) or query.strip()


def fetch_article(api, query, url_base):
    """Return (title, text, url) for the first hit whose title matches the name."""
    try:
        q = clean_query(query)
        params = urllib.parse.urlencode({"action": "query", "list": "search",
                                         "srsearch": q, "srlimit": 10, "format": "json"})
        hits = get_json(f"{api}?{params}").get("query", {}).get("search", [])
        stems = [w[:5] for w in q.split()]
        for hit in hits:
            title = hit["title"]
            if stems and not any(st in title.lower() for st in stems):
                continue
            if DISAMBIG.search(title):
                continue
            params = urllib.parse.urlencode({"action": "query", "prop": "extracts|info",
                                             "explaintext": 1, "inprop": "url",
                                             "titles": title, "format": "json"})
            pages = get_json(f"{api}?{params}").get("query", {}).get("pages", {})
            page = next(iter(pages.values()))
            text = page.get("extract", "")
            if not text:
                continue
            url = page.get("fullurl") or f"{url_base}/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
            return title, text, url
        return None
    except Exception:
        return None


def wikipedia(lang, query):
    return fetch_article(f"https://{lang}.wikipedia.org/w/api.php", query, f"https://{lang}.wikipedia.org")


def miryowiki(query):
    return fetch_article(MIRYOWIKI_API, query, "http://127.0.0.1:8081")


def first_found(sources):
    return next((s for s in sources if s and s[1]), None)


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, quantization_config=bnb,
                                                 device_map="auto", trust_remote_code=True)
    return tokenizer, model


def generate(tokenizer, model, messages):
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS, do_sample=False)
    return tokenizer.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()


def ask(tokenizer, model, system, user):
    return generate(tokenizer, model, [{"role": "system", "content": system},
                                       {"role": "user", "content": user}])


def article_answer(tokenizer, model, question, name, title, text, url):
    system = (f"You are MiryoLove AI. Answer in {name}, in 3-4 sentences. "
              f"Use ONLY the article text below. If the article does not contain the answer, say so in {name}.")
    user = f"Question: {question}\n\nArticle: {title}\n---\n{text[:MAX_CHARS]}\n---"
    short = urllib.parse.unquote(url).replace(" ", "_")
    return f"{title} — {short}", ask(tokenizer, model, system, user)


def handle(tokenizer, model, question):
    lang = detect_lang(question)
    name = LANG_NAMES[lang]

    if TRANSLATE.match(question):
        system = "You are a precise translator. Translate exactly, with no commentary."
        return None, ask(tokenizer, model, system, question)

    if EXAMPLE.match(question):
        system = (f"You are MiryoLove AI, a programming tutor. Answer in {name}. "
                  "Give a short code example (up to 10 lines) in the language named in the question "
                  "(Python, C, C++, Java or Assembly; default is Python). Add brief comments. "
                  "For Assembly output ONLY assembly instructions (for example: mov eax, 5 or add eax, ebx). "
                  "Never write C syntax (no int, no semicolons, no braces) for Assembly. "
                  "Then explain the example in 2-3 sentences.")
        return None, ask(tokenizer, model, system, question)

    if HOMEWORK.search(question):
        system = (f"You are MiryoLove AI, a programming tutor. Answer in {name}. "
                  "Explain the topic in 1-2 sentences. Then give ONE homework task: "
                  "the task statement only, no solution, no code, no hints with the answer.")
        return None, ask(tokenizer, model, system, question)

    if PROGRAMMING.search(question):
        topic = re.sub(r"\bassembly\b", "assembly language", question, flags=re.IGNORECASE)
        sources = [miryowiki(topic), wikipedia("en", topic), wikipedia(lang, question)]
        found = first_found(sources)
        if found:
            title, text, url = found
            return article_answer(tokenizer, model, question, name, title, text, url)
        system = (f"You are MiryoLove AI, a programming tutor. Answer in {name}, 3-5 sentences, "
                  "with a short code snippet if useful. If you are not sure, say so.")
        return None, ask(tokenizer, model, system, question)

    # History and general topics: Wikipedia in the question's language first
    sources = [wikipedia(lang, question)]
    if lang == "uk":
        sources.insert(0, wikipedia("uk", question))
    if lang != "ru":
        sources.append(wikipedia("ru", question))
    found = first_found(sources)
    if not found:
        return None, NOT_FOUND[lang]
    title, text, url = found
    return article_answer(tokenizer, model, question, name, title, text, url)


def main():
    print("Loading MiryoLove AI...")
    tokenizer, model = load_model()
    print("Ready. Write in Russian, Ukrainian or English.")
    print("Programming, homework, examples, history, translation (start with 'переведи'). exit to quit.")
    while True:
        question = input("\n👤 Вы: ").strip()
        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            break
        source, reply = handle(tokenizer, model, question)
        if source:
            print(f"📖 Источник: {source}")
        print(f"🤖 {reply}")


if __name__ == "__main__":
    main()
