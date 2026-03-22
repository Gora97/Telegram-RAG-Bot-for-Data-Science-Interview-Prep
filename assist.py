import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

# ================================
# 🔹 LOGGER SETUP
# ================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),   # save to file
        logging.StreamHandler()           # print to console
    ]
)

logger = logging.getLogger(__name__)

# ================================
# 🔹 LOAD ENV
# ================================
load_dotenv()

# ================================
# 🔹 INIT CLIENTS
# ================================
logger.info("Initializing OpenAI client...")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logger.info("Initializing ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="Document")

embedding_cache = {}

# ================================
# 🔹 EMBEDDING FUNCTION
# ================================
def get_openai_embedding(text: str):
    if text in embedding_cache:
        logger.info("Using cached embedding")
        return embedding_cache[text]

    logger.info("Generating embedding for query...")

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )

    embedding = response.data[0].embedding

    embedding_cache[text] = embedding  # store in cache

    return embedding


# ================================
# 🔹 RAG QUERY
# ================================
def query_rag(question):
    logger.info(f"Running RAG query for: {question}")

    query_embedding = get_openai_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    logger.info("Retrieved top 3 documents from vector DB")

    return results


# ================================
# 🔹 CONTEXT EXTRACTION
# ================================
def get_context(results):
    logger.info("Extracting context from results...")

    documents = results.get("documents", [[]])[0]

    if not documents:
        logger.warning("No documents found in retrieval")
        return "No relevant context found."

    context = "\n\n".join(documents)

    logger.info(f"Context length: {len(context)} characters")

    return context


# ================================
# 🔹 ANSWER GENERATION
# ================================
def generate_answer(question,history=None):
    logger.info("Generating answer from LLM...")

    results = query_rag(question)
    context = get_context(results)

    prompt = f"""
You are a helpful assistant.

Answer the question based ONLY on the context below.
If the answer is not in the context, say "I don't know based on the provided context."

Context:
{context}

Question:
{question}
"""

    logger.info("Sending request to OpenAI model...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise and helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content.strip()

    logger.info("Received response from OpenAI")

    return answer


# ================================
# 🔹 MAIN ENTRY FUNCTION
# ================================
def ask_question(question: str, history=None) -> str:
    logger.info(f"Received user question: {question}")

    try:
        answer = generate_answer(question)
        logger.info("Answer generated successfully")
        return answer

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return f"⚠️ Error: {str(e)}"