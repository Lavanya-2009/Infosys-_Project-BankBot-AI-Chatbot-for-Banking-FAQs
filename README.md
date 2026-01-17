# BankBot – AI Chatbot for Banking FAQs 🤖🏦

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![AI/NLP](https://img.shields.io/badge/AI-NLP-success.svg)
![LLM](https://img.shields.io/badge/LLM-Transformer--based-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)

## 📌 Project Description

**BankBot** is an AI-powered banking chatbot designed to assist users by answering common **banking-related FAQs** quickly and efficiently.
It simulates a real-time support assistant that can respond to customer queries related to banking services such as account support, card-related help, and general banking information.

This project is created as part of an **Infosys Certification / Project Submission**, and it is built using **Streamlit** for an interactive UI and smooth local execution.

---

## ✨ Features

✅ Interactive chatbot UI using **Streamlit**
✅ Banking FAQ chatbot experience
✅ User-friendly conversation interface
✅ Intelligent responses using **AI + NLP** techniques
✅ Supports natural language queries like:

* “How do I check my balance?”
* “How can I block my debit card?”
* “What are the bank working hours?”
* “How to apply for a new card?”

✅ Designed for **project presentation and certification evaluation**
✅ Easily extendable with new intents, FAQs, and AI models

---

## 🧠 Techniques Used

### ✅ Natural Language Processing (NLP)

BankBot uses NLP concepts to understand user input and generate meaningful responses, such as:

* Text cleaning & normalization
* Tokenization
* Intent detection / FAQ matching
* Keyword & pattern-based understanding (for basic flows)

### ✅ Prompt Engineering

To improve chatbot response quality, prompt engineering can be applied such as:

* Clear role-based instructions (system prompts)
* Context-aware prompts
* Controlled response formatting for professional chatbot replies

### ✅ LLM-based Text Generation

BankBot supports integration with **Transformer-based LLMs** for advanced conversations:

* Better answer generation
* More natural, human-like responses
* Ability to handle variations of user questions

---

## 🛠️ Tech Stack

### ✅ Programming Language

* **Python 3.x**

### ✅ Libraries / Frameworks

This project may use:

* `streamlit` (interactive chatbot UI)
* `nltk` (text preprocessing)
* `scikit-learn` (optional: intent classification)
* `transformers` (optional: LLM integration)
* `json` (FAQ/intents storage)
* `re` (pattern matching)

### ✅ AI / ML Technologies

* Natural Language Processing (NLP)
* Intent Recognition
* Transformer-based LLM Support

---

## 🤖 LLM Details

This project supports **Transformer-based LLMs**, such as:

* GPT-style LLMs
* BERT-based models (for classification / retrieval)
* Other transformer-based text generation models

✅ **Configurable LLM Support**
The chatbot is designed so that the **LLM can be changed or upgraded** easily based on availability and use case:

* Open-source models (via Hugging Face Transformers)
* API-based models (configurable through environment variables / config files)

---

## 📂 Project Structure

A typical structure for this project may look like:

* `app.py` → Streamlit chatbot application
* `requirements.txt` → Required dependencies
* `data/`

  * `faq.json` / `intents.json` → Banking FAQ dataset
* `models/`

  * `model.pkl` (optional ML model)
* `README.md`

> The exact structure may vary slightly depending on updates in the repository.

---

## ✅ Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Lavanya-2009/Infosys-_Project-BankBot-AI-Chatbot-for-Banking-FAQs.git
cd Infosys-_Project-BankBot-AI-Chatbot-for-Banking-FAQs
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, you can install manually:

```bash
pip install streamlit nltk scikit-learn transformers
```

---

## ▶️ How to Run the Project Locally (Streamlit)

Run the Streamlit app using:

```bash
streamlit run app.py
```

After running, open the link shown in the terminal (usually):

* [http://localhost:8501/](http://localhost:8501/)

---

## 🎓 Certification Use Case (Infosys Project Submission)

This project is suitable for **Infosys Certification Evaluation** because it demonstrates:

✅ Understanding of AI chatbot systems
✅ Practical implementation of **NLP + AI-based responses**
✅ Real-world banking support automation scenario
✅ Streamlit-based interactive working prototype
✅ Expandability using **Transformer-based LLMs**

### Suggested Certification Demonstration Flow

1. Show the chatbot interface
2. Ask multiple banking questions
3. Explain how intents/FAQs are mapped
4. Highlight AI/NLP techniques
5. Present future scope with LLM integration

---

## 🚀 Future Enhancements

🔹 Add voice input/output support (Speech-to-Text & Text-to-Speech)
🔹 Multi-language support (English + regional languages)
🔹 Connect to real banking APIs securely
🔹 Add authentication for user-specific queries
🔹 Improve response quality using advanced retrieval + LLM (RAG)

---

## 📜 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute this project for learning and educational purposes.

---

## 👩‍💻 Author

**Lavanya Yandapalli**
GitHub: [https://github.com/Lavanya-2009](https://github.com/Lavanya-2009)

---

## ⭐ Support

If you found this project useful for learning or certification purposes, please consider giving it a ⭐ on GitHub! ⭐
