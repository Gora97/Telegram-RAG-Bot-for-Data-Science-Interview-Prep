# Telegram-RAG-Bot-for-Data-Science-Interview-Prep
A Retrieval-Augmented Generation (RAG) powered Telegram bot designed to help users prepare for data science interviews by providing accurate, context-aware answers from a custom knowledge base.
🚀 Features
🔍 Semantic Search (RAG) using vector embeddings
🧠 Context-Aware Conversations (last 3 interactions memory)
⚡ Embedding Caching (faster & cost-efficient)
🧾 Summarization Command (/summarize) for quick revision
💬 Telegram Bot Interface
🗂️ ChromaDB Persistent Vector Database
📜 Detailed Logging (app.log)
🏗️ Project Structure
project/
│
├── app.py              # Entry point
├── bot.py              # Telegram bot logic
├── Assist.py     # RAG pipeline (embedding + retrieval + generation)
├── chroma_db/          # Persistent vector database
├── .env                # API keys (not committed)
├── app.log             # Logs
├── Notebook.ipynb           # My Notebook 
└── README.md
⚙️ Setup Instructions
1️⃣ Clone the repository
cd your-repo-name
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate    # Mac/Linux
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Setup environment variables

Create a .env file:

OPENAI_API_KEY=your_openai_api_key
TELEGRAM_TOKEN=your_telegram_bot_token

Ensure:

collection.count() > 0
▶️ Run the Application
python app.py
💬 How to Use
Open Telegram and search your bot
Start chatting:
What is overfitting?
Explain bias vs variance
🧾 Available Commands
Command	Description
/start	Start the bot
/summarize	Summarize recent conversation
/reset	Clear chat memory
🧠 How It Works
User Query
   ↓
Telegram Bot (bot.py)
   ↓
RAG Pipeline (assist.py)
   ↓
Embedding → Vector Search (ChromaDB)
   ↓
Context + Query → OpenAI LLM
   ↓
Response → User
📊 Logging

Logs are stored in:

app.log

Example:

INFO | Received user question
INFO | Retrieved top 3 documents
WARNING | No documents found
⚠️ Common Issues
❌ No documents found
Run ingest.py
Check collection name (Document)
Ensure persistence is enabled
❌ Invalid Telegram Token
Verify .env file
Run using:
python app.py

(not Jupyter Notebook)


Python
OpenAI API
ChromaDB
python-telegram-bot
python-dotenv


👨‍💻 Author

Gourab Som

⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
