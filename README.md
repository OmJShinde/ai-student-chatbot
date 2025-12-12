# AI Student Support Chatbot 🎓🤖

A production-ready AI chatbot designed to handle student queries efficiently using **FastAPI**, **Sentence Transformers**, and **MongoDB**. It features semantic search, spell correction, and an admin dashboard for flexible knowledge base management.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![AI](https://img.shields.io/badge/AI-Sentence%20Transformers-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🚀 Features

- **🧠 Intelligent Semantic Search**: Uses `sentence-transformers/paraphrase-MiniLM-L6-v2` to understand the *meaning* of questions, not just keywords.
- **✨ Spell Correction**: Automatically fixes typos (e.g., "wfi" -> "wifi") using `pyspellchecker`.
- **🔍 Fuzzy Matching & Suggestions**: If the bot isn't sure, it suggests the top 3 closest questions instead of giving up.
- **⚡ Real-time Interface**: Clean, responsive chat UI with typing indicators and quick-suggestion chips.
- **🛠 Admin Dashboard**: Secure panel to add, edit, or delete FAQs without touching code.
- **💾 Flexible Database**: Works with **MongoDB** (Production) or a local **JSON file** (Testing/Dev).
- **🐳 Dockerized**: Easy deployment with `docker-compose`.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **NLP**: Sentence Transformers, NLTK/TextBlob (Concepts), PySpellChecker
- **Database**: MongoDB (Motor async driver) / JSON
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **DevOps**: Docker, Docker Compose

## 📦 Installation

### Option 1: Local Development (Quick Start)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/OmJShinde/ai-student-chatbot.git
    cd ai-student-chatbot
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    *First run will take a moment to download the AI model (~80MB).*

5.  **Access the App**
    *   Chatbot: [http://localhost:8000](http://localhost:8000)
    *   Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)
        *   **User**: `admin`
        *   **Pass**: `admin123`

### Option 2: Docker (Recommended for Production)

1.  Ensure Docker Desktop is running.
2.  Run:
    ```bash
    docker-compose up --build
    ```

## 📚 Knowledge Base Seeding

To quickly populate the bot with sample university data (35+ FAQs):

```bash
python seed_bulk.py
```

## 📸 Screenshots

*(Add screenshots of your Chat Interface and Admin Panel here)*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Developed by [OmJShinde](https://github.com/OmJShinde)**
