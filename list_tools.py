
import asyncio
from src.midi_mcp.core.server import MCPServer
from src.midi_mcp.config.settings import ServerConfig

async def main():
    config = ServerConfig()
    server = MCPServer(config)
    tools = server.get_registered_tools()
    print("Available MCP Tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())
