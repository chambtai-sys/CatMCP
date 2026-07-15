# CatMCP

```text
       /\_/\
      ( o.o )   [ BETA ]
       > ^ <
     _ /   \ _
    ( )     ( )
    ` `     ` `
     \__/\_/
```

**CatMCP** is a lightweight, playful, and fully standard-compliant **Model Context Protocol (MCP)** server that serves a curated collection of hilarious cat jokes to LLM clients (like Claude Desktop, Cursor, VS Code, Windsurf, and more). Whether you need tech puns, classic question-and-answers, silly scenarios, or workplace meow-ments, CatMCP has you covered!

---

## 🌟 Features

- **Purr-fect Joke Database**: Hand-crafted collection of 24 cat jokes categorized by themes.
- **Categorized Selections**: Easily request jokes filtered by category (`tech`, `classic`, `puns`, `silly`, `work`).
- **Flexible Searching**: Full-text case-insensitive search across the entire joke database.
- **Rich Resources**:
  - `jokes://all`: Read the complete dataset in JSON format.
  - `jokes://categories`: Read a summary of all categories and their joke counts.
  - `jokes://random`: Fetch a dynamic random joke in raw text format.
- **Creative Prompts**: Integrate interactive prompt templates like `tell_cat_joke` to turn LLMs into cat-loving stand-up comedians.
- **Robustly Tested**: Built using `fastmcp` with comprehensive unit tests for high reliability.

---

## 🚀 Quick Start

### Prerequisites
- **Python**: `>=3.12`
- **uv** (Recommended package manager): [Install uv](https://github.com/astral-sh/uv)

### Installation
Clone the repository and install dependencies using `uv`:

```bash
# Clone the repository
git clone https://github.com/Perseu/catmcp.git
cd catmcp

# Install dependencies and create a virtual environment
uv sync
```

### Running the Server
You can start the MCP server using standard IO (stdio) transport:

```bash
uv run python main.py
```

---

## 🛠️ MCP Capabilities

### 1. Tools

- **`get_random_joke(category: Optional[str])`**: Retrieve a random cat joke. You can filter by category: `tech`, `classic`, `puns`, `silly`, or `work`.
- **`list_categories()`**: Get a sorted list of all available joke categories.
- **`search_jokes(keyword: str)`**: Case-insensitive text search across joke setups, punchlines, and categories.

### 2. Resources

- **`jokes://all`**: Serves the entire joke database as a static JSON resource.
- **`jokes://categories`**: Serves the category distribution and count summary as a JSON resource.
- **`jokes://random`**: Serves a dynamic random cat joke in plain text format.

### 3. Prompts

- **`tell_cat_joke(category: Optional[str], tone: Optional[str])`**: Generates a standard instruction set directing the AI client to perform the joke under a specified persona (e.g. `CatComedian`) and tone (e.g. `sarcastic`, `enthusiastic`, `dry`).

---

## ⚙️ Host Configuration

To integrate CatMCP with your favorite LLM client, add the server configuration using the paths and snippets below.

### 1. Claude Desktop
Add this to your `claude_desktop_config.json` (located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "catmcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/catmcp",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

### 2. Cursor
1. Go to **Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Fill in the fields:
   - **Name**: `CatMCP`
   - **Type**: `command`
   - **Command**: `uv --directory "/absolute/path/to/catmcp" run python main.py`

### 3. VS Code (via Cline / Roo Code)
If you use popular AI coding assistants like **Cline** or **Roo Code** in VS Code, add the following to your `cline_mcp_settings.json` (located at `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` on macOS or `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json` on Windows):

```json
{
  "mcpServers": {
    "catmcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/catmcp",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

### 4. Windsurf
Windsurf supports MCP natively. You can configure CatMCP by editing your global `mcp_config.json` (located at `~/.codeium/windsurf/mcp_config.json` on macOS/Linux or `%USERPROFILE%\.codeium\windsurf\mcp_config.json` on Windows):

```json
{
  "mcpServers": {
    "catmcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/catmcp",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

---

## 🧪 Testing

CatMCP uses `pytest` for testing. You can run all 11 unit tests to verify server tools, resources, and prompts:

```bash
uv run pytest
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
*Created with 🐾 by Perseu.*
