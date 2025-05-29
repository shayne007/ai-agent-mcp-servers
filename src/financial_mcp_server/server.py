import logging
from mcp.server.fastmcp import FastMCP
from financial_mcp_server.registers.stock_analysis import StockAnalysisTools
from financial_mcp_server.registers.stock_news import StockNewsTools


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
        analysis_tools = StockAnalysisTools(self.logger)
        news_tools = StockNewsTools(self.logger)

        analysis_tools.register_tools(self.mcp)
        news_tools.register_tools(self.mcp)

    def run(self):
        """Run the MCP server."""
        self.mcp.run("sse")


def main():
    server = StockAnalysisMCPServer()
    server.run()

