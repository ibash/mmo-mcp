from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

# TODO(ibash) figure out user authentication

@mcp.tool
def play() -> str:
    pass

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
