import DetailsWrap from '@site/src/components/DetailsWrap';

# MCP Server for Databend

[mcp-databend](https://github.com/databendlabs/mcp-databend) is an MCP (Model Context Protocol) server that enables AI assistants to interact directly with your Databend database using natural language.

## What mcp-databend Can Do

- **execute_sql** - Execute SQL queries with timeout protection
- **show_databases** - List all available databases
- **show_tables** - List tables in a database (with optional filter)
- **describe_table** - Get detailed table schema information

## Build a ChatBI Tool

This tutorial shows you how to build a conversational Business Intelligence tool using mcp-databend and the Agno framework. You'll create a local agent that can answer data questions in natural language.

![Databend MCP ChatBI](@site/static/img/connect/databend-mcp-chatbi.png)

## Prerequisites

Before getting started, you'll need:

1. **Databend Database** - Either [Databend Cloud](https://app.databend.com) (free tier available) or a self-hosted instance
2. **DeepSeek API Key** - Get your key from [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

## Step-by-Step Tutorial

### Step 1: Setup Databend Connection

If you don't already have a Databend database:

1. **Sign up for [Databend Cloud](https://app.databend.com)** (free tier available)
2. **Create a warehouse and database**
3. **Get your connection string** from the console

For detailed DSN format and examples, see [Connection String Documentation](https://docs.databend.com/developer/drivers/#connection-string-dsn).

| Deployment         | Connection String Example                                     |
| ------------------ | ------------------------------------------------------------- |
| **Databend Cloud** | `databend://user:pwd@host:443/database?warehouse=wh`          |
| **Self-hosted**    | `databend://user:pwd@localhost:8000/database?sslmode=disable` |

### Step 2: Setup API Keys and Environment

Set up your API key and database connection:

```bash
# Set your DeepSeek API key
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# Set your Databend connection string
export DATABEND_DSN="your-databend-connection-string"
```

### Step 3: Install Dependencies

Create a virtual environment and install the required packages:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install packaging openai agno sqlalchemy fastapi mcp-databend
```

### Step 4: Create ChatBI Agent

Now create your ChatBI agent that uses mcp-databend to interact with your database.

Create a file `agent.py`:

```python
from contextlib import asynccontextmanager
import os
import logging
import sys

from agno.agent import Agent
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.mcp import MCPTools
from agno.models.deepseek import DeepSeek
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_env_vars():
    required = {
        "DATABEND_DSN": "https://docs.databend.com/developer/drivers/#connection-string-dsn",
        "DEEPSEEK_API_KEY": "https://platform.deepseek.com/api_keys"
    }

    missing = [var for var in required if not os.getenv(var)]

    if missing:
        print("❌ Missing environment variables:")
        for var in missing:
            print(f"  • {var}: {required[var]}")
        print("\nExample: export DATABEND_DSN='...' DEEPSEEK_API_KEY='...'")
        sys.exit(1)

    print("✅ Environment variables OK")

check_env_vars()

class DatabendTool:
    def __init__(self):
        self.mcp = None
        self.dsn = os.getenv("DATABEND_DSN")

    def create(self):
        env = os.environ.copy()
        env["DATABEND_DSN"] = self.dsn
        self.mcp = MCPTools(
            command="python -m mcp_databend",
            env=env,
            timeout_seconds=300
        )
        return self.mcp

    async def init(self):
        try:
            await self.mcp.connect()
            logger.info("✓ Connected to Databend")
            return True
        except Exception as e:
            logger.error(f"✗ Databend connection failed: {e}")
            return False

databend = DatabendTool()

agent = Agent(
    name="ChatBI",
    model=DeepSeek(),
    tools=[],
    instructions=[
        "You are ChatBI - a Business Intelligence assistant for Databend.",
        "Help users explore and analyze their data using natural language.",
        "Always start by exploring available databases and tables.",
        "Format query results in clear, readable tables.",
        "Provide insights and explanations with your analysis."
    ],
    storage=SqliteStorage(table_name="chatbi", db_file="chatbi.db"),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
    show_tool_calls=True,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    tool = databend.create()
    if not await databend.init():
        logger.error("Failed to initialize Databend")
        raise RuntimeError("Databend connection failed")

    agent.tools.append(tool)
    logger.info("ChatBI initialized successfully")

    yield

    if databend.mcp:
        await databend.mcp.close()

playground = Playground(
    agents=[agent],
    name="ChatBI with Databend",
    description="Business Intelligence Assistant powered by Databend"
)

app = playground.get_app(lifespan=lifespan)

if __name__ == "__main__":
    print("🤖 Starting MCP Server for Databend")
    print("Open http://localhost:7777 to start chatting!")
    playground.serve(app="agent:app", host="127.0.0.1", port=7777)

```

### Step 5: Start Your ChatBI Agent

Run your agent to start the local server:

```bash
python agent.py
```

You should see:

```
✅ Environment variables OK
🤖 Starting MCP Server for Databend
Open http://localhost:7777 to start chatting!
INFO Starting playground on http://127.0.0.1:7777
INFO:     Started server process [189851]
INFO:     Waiting for application startup.
INFO:agent:✓ Connected to Databend
INFO:agent:ChatBI initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:7777 (Press CTRL+C to quit)
```

### Step 6: Setup Web Interface

For a better user experience, you can set up Agno's web interface:

```bash
# Create the Agent UI
npx create-agent-ui@latest

# Enter 'y' when prompted, then run:
cd agent-ui && npm run dev
```

**Connect to Your Agent:**

1. Open [http://localhost:3000](http://localhost:3000)
2. Select "localhost:7777" as your endpoint
3. Start asking questions about your data!

**Try These Queries:**

- "Show me all databases"
- "What tables do I have?"
- "Describe the structure of my tables"
- "Run a query to show sample data"

## Resources

- **GitHub Repository**: [databendlabs/mcp-databend](https://github.com/databendlabs/mcp-databend)
- **PyPI Package**: [mcp-databend](https://pypi.org/project/mcp-databend)
- **Agno Framework**: [Agno MCP](https://docs.agno.com/tools/mcp/mcp)
- **Agent UI**: [Agent UI](https://docs.agno.com/agent-ui/introduction)
