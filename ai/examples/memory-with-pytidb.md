---
title: AI Agent Memory Example
summary: Implement conversation memory for chatbots and conversational AI applications.
---

# AI Agent Memory Example

This example shows how to build an AI agent with persistent memory powered by TiDB's vector search capabilities.

With just a few lines of code, you can create a conversational AI that remembers past interactions and builds context over time.

- **Persistent memory**: Remembers conversations across sessions and user interactions
- **Interactive chat**: Uses either a web UI or a command-line interface
- **Multi-user support**: Keeps separate memory contexts per user
- **Real-time memory viewing**: Shows stored memories in the web interface

<p align="center">
    <img src="https://github.com/user-attachments/assets/b57ae0fb-9075-43a9-8690-edaa69ca9f40" alt="AI Agent with memory powered by TiDB" width="700"/>
    <p align="center"><i>AI Agent with memory powered by TiDB</i></p>
</p>

## Prerequisites

Before you begin, ensure you have the following:

- **Python (>=3.10)**: Install [Python](https://www.python.org/downloads/) 3.10 or a later version.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).
- **OpenAI API key**: Get an OpenAI API key from [OpenAI](https://platform.openai.com/api-keys).

## How to run

### Step 1. Clone the `pytidb` repository

[`pytidb`](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB, designed to help developers build AI applications efficiently.

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/memory/
```

### Step 2. Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r reqs.txt
```

### Step 3. Set environment variables

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.
3. Set environment variables according to the connection parameters as follows:

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test

OPENAI_API_KEY={your-openai-api-key}
EOF
```

### Step 4. Run the application

Choose one of the following options:

### Option 1. Launch the web application

```bash
streamlit run app.py
```

Open your browser, visit `http://localhost:8501`, and then follow [Interact with memory in Web Application](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application) to start using the memory-enabled AI assistant.

### Option 2. Run the command-line application

```bash
python main.py
```

Follow [Interact with memory in Command Line Application](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application) to start using the memory-enabled AI assistant.

## Interact with memory in web application

In the web application, you can interact with the AI assistant. The UI includes the following components:

- **Sidebar**: User settings and chat list.
- **Main chat area**: Chat interface with the AI assistant.
- **Memory viewer**: Real-time memory viewer showing stored facts.

Follow these steps to see how memory works:

1. Introduce yourself in the default chat session. For example, "Hello, I am John. I work as a software engineer and love guitar."
2. You can see the information you provided in the memory viewer.
3. Click **New chat** in the sidebar to start a new chat session.
4. Ask "Who am I?" in the new chat session. The AI will recall your information from previous conversations.

## Interact with memory in command line application

In the command-line application, you can chat with the AI assistant and introduce yourself.

**Example conversation:**

```plain
Chat with AI (type 'exit' to quit)
You: Hello, I am Mini256.
AI: Hello, Mini256! How can I assist you today?
You: I am working at PingCAP.
AI: That's great to hear, Mini256! PingCAP is known for its work on distributed databases, particularly TiDB. How's your experience been working there?
You: I am developing pytidb (A Python SDK for TiDB) which helps developers easily connect to TiDB.
AI: That sounds like a great project, Mini256! Developing a Python SDK for TiDB can make it much easier for developers to integrate with TiDB and interact with it using Python. If you need any advice on best practices, libraries to use, or specific features to implement, feel free to ask!
You: exit
Goodbye!
```

After the first conversation, the AI assistant will remember the information you provided and use it to answer future questions.

Now, you can start a new chat session and ask the AI assistant "Who am I?".

**Example conversation in another chat session:**

```plain
Chat with AI (type 'exit' to quit)
You: Who am I?
AI: You are Mini256, and you work at PingCAP, where you are developing pytidb, a Python SDK for TiDB to assist developers in easily connecting to TiDB.
You: exit
Goodbye!
```

As you can see, the AI assistant remembers you across sessions!

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/memory)