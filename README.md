# 💗 MiryoLove AI

### An Independent AI Project by Miryo Bun

[🇬🇧 English](README.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md)

[🤗 Hugging Face](https://huggingface.co/MiryoBun) · [💗 MiryoLove-7B](https://huggingface.co/MiryoBun/MiryoLove-7B) · [💻 GitHub](https://github.com/Miryo-Bun/MiryoLove-AI)

---

## ✨ About the Project

**MiryoLove AI** is an independent AI project created by Miryo Bun, focused on developing a friendly AI assistant and exploring language model development.

The project focuses on programming assistance, educational support, technical explanations, and multilingual interaction.

## 💗 MiryoLove-7B

MiryoLove-7B is based on **Qwen2.5-7B-Instruct**, originally developed by Qwen / Alibaba Cloud.

- **Base model:** Qwen2.5-7B-Instruct
- **Fine-tuning:** LoRA
- **Published weights:** Merged FP16
- **Parameters:** Approximately 7 billion
- **Languages:** English, Russian, Ukrainian

These details reflect the project's current description and should be verified against the model files and training records.

MiryoLove AI is an independent project and is not an official Qwen or Alibaba Cloud release.

## 🌟 Features

- 💻 **Programming:** Python, C, C++, Java, and Assembly.
- 📚 **Learning:** Programming explanations and practice exercises.
- 🌍 **Languages:** English, Russian, and Ukrainian.
- 📖 **Knowledge:** Planned integration with MiryoWiki and Wikipedia.
- 🧠 **AI Development:** Experimentation with language models and fine-tuning.

## 📂 Project Structure

| File | Description |
|---|---|
| `miryolove_ai.py` | Main AI chat script |
| `.gitignore` | Excludes local files, model weights, datasets, logs, and secrets from Git |

## 🚀 Getting Started

### 1. Requirements

- Python 3.10 or newer
- PyTorch
- Transformers
- Accelerate
- Bitsandbytes
- Compatible hardware and model-loading configuration

### 2. Install Dependencies

```bash
pip install torch transformers accelerate bitsandbytes
```

### 3. Configure the Model

```bash
export MIRYO_MODEL=MiryoBun/MiryoLove-7B
```

### 4. Run MiryoLove AI

```bash
python miryolove_ai.py
```

The required hardware depends on the inference configuration, quantization, context length, and available memory. Check the model repository for current instructions.

### 📖 MiryoWiki Integration

The `MIRYOWIKI_API` environment variable can specify the MediaWiki API address.

Default address:

```text
http://127.0.0.1:8081/api.php
```

Example:

```bash
export MIRYOWIKI_API=http://127.0.0.1:8081/api.php
```

## 🌐 Languages and Tasks

MiryoLove AI is intended to support:

- English-language interaction
- Russian-language interaction
- Ukrainian-language interaction
- Programming education
- Technical explanations
- Technical translation

Generated code, translations, and explanations should be reviewed for accuracy.

## ⚠️ Limitations

AI-generated responses may contain mistakes, incomplete explanations, or inaccurate translations.

Comprehensive benchmark results are not documented here. Model capabilities should be evaluated on relevant tasks.

## 📜 License and Attribution

### MiryoLove AI

Original project code and documentation may be distributed under the **Apache License 2.0**, where the project owner has the necessary rights to apply that license.

- **License:** Apache-2.0
- **License file:** [`LICENSE`](LICENSE)
- **Official license:** [Apache.org](https://www.apache.org/licenses/LICENSE-2.0.txt)
- **SPDX:** [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)

Third-party models, datasets, and components may have separate licensing terms. Their licenses must be reviewed independently.

MiryoLove AI is not officially affiliated with or endorsed by Qwen or Alibaba Cloud.

## 🔮 Future Development

Potential development directions include:

- Improving programming assistance.
- Expanding the fine-tuning dataset.
- Evaluating model quality.
- Improving local installation instructions.
- Developing MiryoWiki integration.
- Continuing independent AI research and development.

These are potential future directions, not claims of completed features.

## 🤝 Contact and Community

- 💻 [GitHub Repository](https://github.com/Miryo-Bun/MiryoLove-AI)
- 🤗 [Hugging Face Profile](https://huggingface.co/MiryoBun)
- 💗 [MiryoLove-7B Model](https://huggingface.co/MiryoBun/MiryoLove-7B)

Use GitHub Issues and Discussions if they are enabled in the repository.

---

<p align="center">
  💗 <strong>MiryoLove AI</strong>
  <br />
  <em>Created and independently developed by Miryo Bun.</em>
  <br />
  An independent AI project exploring language models and AI assistance.
</p>
