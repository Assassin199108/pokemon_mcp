# pokemon_mcp
Pokemon MCP SERVER，Feed the LLM with Pokémon information and knowledge。
Method: Query <a id="https://pokeapi.co/">Pokémon</a> information through an HTTP connection to the PokéAPI。
Built with FastMCP and @mcp.tool() decorators.

## 🚀 Features

- **6 Pokemon Tools**: Get Pokemon info, species, types, evolution chains, and search
- **FastMCP Integration**: Built with FastMCP for easy MCP server development
- **Async/await**: Fully async implementation for better performance
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Formatted Output**: Clean, readable text output with emoji formatting

## 📦 Requirements

- Python 3.8+
- fastmcp
- httpx

## ⚙️ Installation

### Using pip (recommended)
```bash
pip install fastmcp httpx
```

### Using uv
```bash
uv init
uv venv
source .venv/bin/activate
pip install fastmcp httpx
```

### Using pip with requirements.txt
```bash
pip install -r requirements.txt
```

## 🎮 MCP Server Configuration

### For Claude Desktop

Add the following configuration to your Claude Desktop `claude_desktop_config.json` file:

```json
{
    "pokemon": {
      "command": "uv",
      "args": [
            "--directory", 
            "/path/to/pokemon", 
            "run", 
            "pokemon_mcp.py"
        ],
      "env": {}
    }
}
```

**Note**: Replace `/path/to/your/pokemon_mcp` with the actual path to your project directory.

### For Claude Code

Add the MCP server to your Claude Code configuration:

1. Open Claude Code
2. Run `/init` to set up the project
3. Or manually add to your configuration:

```json
{
  "mcpServers": {
    "pokemon": {
      "command": "python",
      "args": ["./main.py"],
      "env": {}
    }
  }
}
```

### For Continue.dev

Add to your `config.json`:

```json
{
  "experimental": {
    "modelContextProtocol": true
  },
  "mcpServers": {
    "pokemon": {
      "command": "python",
      "args": ["./main.py"],
      "env": {}
    }
  }
}
```

## 🛠️ Available Tools

The server provides the following MCP tools:

### 1. get_pokemon_info
Get detailed Pokemon information by name or ID
- **Parameters**: `identifier` (string) - Pokemon name or ID
- **Example**: `get_pokemon_info("pikachu")` or `get_pokemon_info("25")`

### 2. get_pokemon_species
Get Pokemon species information including evolution details
- **Parameters**: `identifier` (string) - Pokemon name or ID
- **Example**: `get_pokemon_species("charizard")`

### 3. get_pokemon_types
Get all available Pokemon types
- **Parameters**: None
- **Example**: `get_pokemon_types()`

### 4. get_pokemon_by_type
Get all Pokemon of a specific type
- **Parameters**: `type_name` (string) - Pokemon type name
- **Example**: `get_pokemon_by_type("fire")`

### 5. search_pokemon
Search for Pokemon by name
- **Parameters**:
  - `query` (string) - Search query
  - `limit` (integer, optional) - Maximum results (default: 10)
- **Example**: `search_pokemon("char", 5)`

### 6. get_pokemon_evolution_chain
Get evolution chain by chain ID
- **Parameters**: `chain_id` (integer) - Evolution chain ID
- **Example**: `get_pokemon_evolution_chain(1)`

## 🧪 Testing

### 1. Start the Server
```bash
python main.py
```

### 2. Test with MCP Client

Create a test file `test_client.py`:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters

async def test_pokemon_mcp():
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
    )

    async with ClientSession(server_params) as session:
        await session.initialize()

        # Test getting Pokemon info
        result = await session.call_tool("get_pokemon_info", {"identifier": "pikachu"})
        print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(test_pokemon_mcp())
```

Run the test:
```bash
python test_client.py
```

### 3. Test API Connection
```python
import httpx
import asyncio

async def test_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon/pikachu")
        if response.status_code == 200:
            print("✅ API connection successful")
        else:
            print("❌ API connection failed")

asyncio.run(test_api())
```

## 🔧 Configuration Examples

### Claude Desktop Full Configuration
```json
{
  "mcpServers": {
    "pokemon": {
      "command": "/usr/bin/python3",
      "args": ["/Users/username/projects/pokemon_mcp/main.py"],
      "env": {
        "PYTHONPATH": "/Users/username/projects/pokemon_mcp"
      }
    }
  }
}
```

### Environment Variables
You can set environment variables for configuration:

```bash
export POKEMON_API_BASE_URL="https://pokeapi.co/api/v2"
export POKEMON_TIMEOUT="30"
```

## 📝 Usage Examples

### After Configuration
Once configured, you can use the tools directly in your LLM chat:

```
User: Get information about Pikachu
Assistant: I'll get the Pokemon information for Pikachu.
[Uses get_pokemon_info tool]

User: Show me all fire type Pokemon
Assistant: I'll get all fire type Pokemon for you.
[Uses get_pokemon_by_type tool]

User: Search for Pokemon starting with 'char'
Agent: I'll search for Pokemon matching that query.
[Uses search_pokemon tool]
```

## 🐛 Troubleshooting

### Common Issues

1. **ImportError: No module named 'fastmcp'**
   ```bash
   pip install fastmcp
   ```

2. **Server not starting**
   - Check Python path in configuration
   - Ensure all dependencies are installed
   - Check file permissions

3. **API connection errors**
   - Check internet connection
   - Verify PokéAPI status: https://pokeapi.statuspage.io/

4. **MCP server not connecting**
   - Verify configuration file path
   - Check command arguments
   - Ensure server starts successfully

### Debug Mode
Enable debug logging:
```bash
python main.py --log-level DEBUG
```

## 📄 License

This project is built for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 References

- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [PokéAPI Documentation](https://pokeapi.co/docs/v2)
- [MCP Specification](https://spec.modelcontextprotocol.io/)