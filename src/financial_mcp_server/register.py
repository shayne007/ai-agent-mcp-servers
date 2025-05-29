import logging
from typing import Any

from financial_mcp_server.llms.llm import OpenAiCompatibleClient
from financial_mcp_server.tools.stock_price import get_stock_info,get_hk_stock_hist,get_stock_real_time_data,get_macro_economic_data


class StockAnalysisTools(OpenAiCompatibleClient):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self.name = "stock_analysis_tools"

    def register_tools(self, mcp: Any):
        """Register stock analysis tools."""

        @mcp.tool(
            description="可以根据传入的股票代码或股票名称获取股票实时行情信息")
        def mcp_get_stock_real_time_data(name: str, code: str) -> str:
            """可以根据传入的股票代码或股票名称获取股票实时行情信息"""
            tools = [get_stock_real_time_data]
            tools_by_name = {tool.name: tool for tool in tools}
            response_text = tools_by_name['get_stock_real_time_data'].invoke(
                {"code": code, "name": name})
            self.logger.info(response_text)
            return response_text
        @mcp.tool(
            description="可以根据传入的股票代码及日期范围获取股票历史数据")
        def mcp_get_hk_stock_hist(code: str, start_date: str, end_date: str) -> str:
            """可以根据传入的股票代码及日期范围获取股票历史数据"""
            tools = [get_hk_stock_hist]
            tools_by_name = {tool.name: tool for tool in tools}
            response_text = tools_by_name['get_hk_stock_hist'].invoke(
                {"code": code, "start_date": start_date, "end_date": end_date})
            self.logger.info(response_text)
            return response_text
        @mcp.tool(
            description="可以根据指标类型获取宏观经济数据")
        def mcp_get_macro_economic_data(indicator: str) -> str:
            """可以根据指标类型获取宏观经济数据"""
            tools = [get_macro_economic_data]
            tools_by_name = {tool.name: tool for tool in tools}
            response_text = tools_by_name['get_macro_economic_data'].invoke(
                {"indicator": indicator})
            self.logger.info(response_text)
            return response_text
        @mcp.tool(
            description="可以根据传入的股票代码获取股票信息")
        def mcp_get_stock_info(code: str) -> str:
            """可以根据传入的股票代码获取股票信息"""
            tools = [get_stock_info]
            tools_by_name = {tool.name: tool for tool in tools}
            response_text = tools_by_name['get_stock_info'].invoke(
                {"code": code})
            self.logger.info(response_text)
            return response_text
