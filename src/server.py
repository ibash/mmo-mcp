from dotenv import load_dotenv

load_dotenv()

from fastmcp import FastMCP  # noqa: E402

from .auth import AuthMiddleware  # noqa: E402
from . import tools  # noqa: E402
from . import prompts  # noqa: E402

mcp = FastMCP("My MCP Server")
mcp.add_middleware(AuthMiddleware())

app = mcp.http_app()

tools.register(mcp)
prompts.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
