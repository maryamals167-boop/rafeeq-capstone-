"""MCP stdio server exposing the read-only synthetic policy search tool."""
from mcp.server.fastmcp import FastMCP
from tools import search_policy, list_required_documents

mcp = FastMCP("rafeeq-madar-tools")

@mcp.tool()
def search_madar_policy(query: str) -> str:
    """Search synthetic Madar municipality policy context."""
    return search_policy(query)

@mcp.tool()
def required_documents(permit_type: str) -> list[str]:
    """List synthetic required documents for a permit type."""
    return list_required_documents(permit_type)

if __name__ == "__main__":
    mcp.run()
