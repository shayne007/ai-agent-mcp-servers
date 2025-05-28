import logging
from typing import Any

from financial_mcp_server.llms.llm import OpenAiCompatibleClient
from financial_mcp_server.tools.stock_price import get_stock_info


class StockAnalysisTools(OpenAiCompatibleClient):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self.name = "stock_analysis_tools"

    def register_tools(self, mcp: Any):
        """Register stock analysis tools."""

        @mcp.tool(
            description="可以根据传入的股票代码或股票名称获取股票实时行情信息")
        def mcp_get_stock_info(name: str, code: str) -> str:
            """可以根据传入的股票代码或股票名称获取股票实时行情信息"""
            tools = [get_stock_info]
            tools_by_name = {tool.name: tool for tool in tools}
            response_text = tools_by_name['get_stock_info'].invoke(
                {"code": code, "name": name})
            self.logger.info(response_text)
            return response_text
