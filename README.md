# DevBuddy 🧑‍💻

### Your AI-powered companion for understanding codebases.

DevBuddy is an AI-powered developer assistant designed to make exploring, understanding, and debugging codebases easier.

It combines **Retrieval-Augmented Generation (RAG)**, conversational memory, and AI agents to provide context-aware answers based on project documentation and source files.

Instead of relying entirely on an LLM's general knowledge, DevBuddy retrieves relevant information from uploaded project files and uses it to generate more accurate, contextual responses.

The goal is simple: make working with unfamiliar codebases feel less overwhelming.

---

## ✨ Features

- **Context-aware conversations** — Ask questions about your project and receive answers grounded in its documentation.
- **Document ingestion** — Upload and process files such as PDF, Markdown, and TXT.
- **Semantic search** — Find relevant information using embeddings and vector similarity.
- **Conversational memory** — Maintain context across multiple messages.
- **AI-powered debugging** — Analyze errors and receive explanations based on available project context.
- **Code explanations** — Understand unfamiliar functions, concepts, and implementation details.
- **AI agents and tools** — Use specialized tools to search documentation and analyze code.
- **Source references** — Trace generated answers back to the relevant documents.
- **Execution monitoring** — Track model calls, retrieval activity, latency, and token usage.

---

## 🧠 How It Works

DevBuddy follows a Retrieval-Augmented Generation architecture combined with an agent-based workflow.

### Document Processing

1. Documents are loaded using LangChain document loaders.
2. Text is divided into smaller chunks using text splitters.
3. Embeddings are generated for each chunk.
4. Vectors are stored in a vector database.
5. Relevant information can later be retrieved through semantic search.

### Question Answering

1. A user submits a question.
2. Conversational memory provides relevant chat context.
3. An agent determines which tools or information are needed.
4. A retriever searches the vector database for relevant context.
5. An LCEL pipeline combines the retrieved context, prompt, and language model.
6. An output parser structures the generated response.
7. Callbacks monitor and log the execution process.

---

## 🏗️ Architecture & Technologies

| Component | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| LLM Framework | LangChain |
| Language Models | OpenAI / Gemini |
| Prompt Management | LangChain Prompt Templates |
| Output Processing | LangChain Output Parsers |
| Pipeline Composition | LCEL / Runnables |
| Document Processing | LangChain Loaders & Splitters |
| Embeddings | OpenAI Embeddings |
| Vector Database | ChromaDB |
| Retrieval | LangChain Retrievers |
| Agents & Tools | LangChain |
| Conversational Memory | LangChain Chat History |
| Monitoring | LangChain Callbacks |
| Frontend | React + Tailwind CSS |
| Database | SQLite |

---

## 🔗 LangChain Components

DevBuddy explores the core building blocks of the LangChain ecosystem:

- **Models:** LLM integration and generation.
- **Prompts:** Reusable, structured prompt templates.
- **Output Parsers:** Structured response extraction.
- **Runnables / LCEL:** Composable execution pipelines.
- **Memory:** Context management across conversations.
- **Document Loaders & Splitters:** Document ingestion and processing.
- **Embeddings & Vector Stores:** Semantic representation and storage.
- **Retrievers:** Contextual information retrieval.
- **Chains:** Multi-step LLM workflows.
- **Agents & Tools:** Tool selection and autonomous task execution.
- **Callbacks:** Execution tracking, logging, and monitoring.

---

## 📁 Project Structure

```text
devbuddy/
│
├── backend/
│   ├── ingestion/
│   ├── retrieval/
│   ├── chains/
│   ├── agents/
│   ├── prompts/
│   ├── memory/
│   ├── parsers/
    ├── tools/
│   ├── callbacks/
│   ├── config.py
│   └── main.py
│
├── frontend/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

## 🎯 Project Goals

- Explore the practical implementation of LLM-powered applications.
- Understand how RAG systems work beyond basic chatbot implementations.
- Build modular and reusable LangChain pipelines.
- Experiment with agent-based workflows and tool calling.
- Combine semantic retrieval with conversational context.
- Develop an application with a clean and intuitive user interface.

---

## 🚀 Vision

DevBuddy aims to bring together document intelligence, conversational AI, and developer productivity in one place.

It's an exploration of how different LLM application components can work together to create something genuinely useful.

---

*Built with curiosity, Python, and a little too much AI.*
