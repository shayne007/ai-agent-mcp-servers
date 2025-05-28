import logging
from mcp.server.fastmcp import FastMCP
from .register import StockAnalysisTools


class StockAnalysisMCPServer:
    def __init__(self):
        self.name = "job_hunting_server"
        self.mcp = FastMCP(self.name)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)

        # Initialize tools
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools."""
        # Initialize tool classes
        job_tools = StockAnalysisTools(self.logger)

        job_tools.register_tools(self.mcp)

    def run(self):
        """Run the MCP server."""
        self.mcp.run()


def main():
    server = StockAnalysisMCPServer()
    server.run()

