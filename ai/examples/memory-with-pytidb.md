---
title: AI Agent Memory Example
summary: Implement conversation memory for chatbots and conversational AI applications.
---

# AI Agent Memory Example

This example showcases how to build an intelligent AI agent with persistent memory powered by TiDB's vector search capabilities.

With just a few lines of code, you can create a conversational AI that remembers past interactions and builds context over time.

- **Persistent Memory**: The AI remembers conversations across sessions and user interactions
- **Interactive Chat**: Both web interface and command-line options for flexible interaction
- **Multi-User Support**: Different users can have separate memory contexts
- **Real-Time Memory Viewing**: Visual display of all stored memories in the web interface

<p align="center">
    <img src="https://github.com/user-attachments/assets/b57ae0fb-9075-43a9-8690-edaa69ca9f40" alt="AI Agent with memory powered by TiDB" width="700"/>
    <p align="center"><i>AI Agent with memory powered by TiDB</i></p>
</p>

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster**: Create a free cluster here: [tidbcloud.com ↗️](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme)
- **OpenAI API Key**: Get your API key at [OpenAI Platform ↗️](https://platform.openai.com/api-keys)

## How to run

### Step 1. Clone the repository

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

### Step 3. Set up environment variables

Go to [TiDB Cloud console](https://tidbcloud.com/clusters) and get the connection parameters, then set up the environment variable like this:

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

### Option 1. Launch Web Application:

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser and follow the instructions in the [Interact with memory in Web Application](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-web-application) section to start interacting with the memory-enabled AI assistant.

### Option 2. Run Command Line Application:

```bash
python main.py
```

Follow the instructions in the [Interact with memory in Command Line Application](https://github.com/pingcap/pytidb/tree/main/examples/memory/#interact-with-memory-in-command-line-application) section to start interacting with the memory-enabled AI assistant.

## Interact with memory in web application

In the web application, you can interact with the AI assistant, the user interface includes:

- **Sidebar**: User settings and chat list.
- **Main chat area**: Chat interface with the AI assistant.
- **Memory viewer**: Real-time memory viewer showing stored facts.

You can follow the following steps to check how the memory works:

1. Introduce yourself in the default chat session. For example, "Hello, I am John. I work as a software engineer and love guitar."
2. You can see the information you provided in the memory viewer.
3. Click **New chat** in the sidebar to start a new chat session.
4. Ask "Who am I?" in the new chat session. The AI will recall your information from previous conversations.

## Interact with memory in command line application

In the command line application, you can interact with the AI assistant and introduce yourself.

**Example conversation:**

```plain
Chat with AI (type 'exit' to quit)
You: Hello, I am Mini256.
AI: Hello, Mini256! How can I assist you today?
You: I am working at PingCAP.
AI: That's great to hear, Mini256! PingCAP is known for its work on distributed databases, particularly TiDB. How's your experience been working there?
You: I am developing pytidb (A Python SDK for TiDB) which helps developers easy to connect to TiDB.
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