import logging
from datetime import datetime
from typing import Any

import akshare as ak
from dotenv import load_dotenv

from financial_mcp_server.llms.llm import OpenAiCompatibleClient

load_dotenv()  # load environment variables from .env


class StockNewsTools(OpenAiCompatibleClient):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self.name = "stock_news_tools"

    @staticmethod
    def register_tools(mcp: Any):
        """Register stock news tools."""

        @mcp.tool(description="获取沪深京 A 股日频率数")
        def stock_zh_a_hist(stock_code: str,
                            start_date: str =datetime.now().strftime("%Y-%m-%d") ,
                            end_date: str = datetime.now().strftime("%Y-%m-%d")) -> str:
            """  沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
            Args:
                stock_code (str): 股票代码,例如 symbol="000001";
                start_date(str):	开始查询的日期,例如start_date='20210301';
                end_date(str): 结束查询的日期,例如end_date ='20210616';
            Returns:
                str: 返回包含股票行情信息的字符串,
            Raises:
                Exception: 当查询股票数据发生异常时抛出
            """
            try:
                stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="hfq")
                if stock_zh_a_hist_df.empty:
                    return "未找到该股票的行情信息。"
                else:
                    return stock_zh_a_hist_df.to_json(orient='records', force_ascii=False)
            except Exception as e:
                return f"查询股票行情时出现错误: {e}"

        @mcp.tool(description="获取指定个股的新闻资讯数据")
        def stock_news_em(stock_code: str) -> str:
            """  指定个股的新闻资讯数据
            Args:
                stock_code (str): 股票代码,例如 symbol="000001";
            Returns:
                str: 指定 symbol 当日最近 100 条新闻资讯数据,
            Raises:
                Exception: 当查询股票数据发生异常时抛出
            """
            try:
                stock_news_em_df = ak.stock_news_em(symbol=stock_code)
                if stock_news_em_df.empty:
                    return "未找到该股票的信息。"
                else:
                    return stock_news_em_df.to_json(orient='records', force_ascii=False)
            except Exception as e:
                return f"查询股票信息时出现错误: {e}"

        @mcp.tool(description="获取财新数据通-股票精选新闻内容")
        def  stock_news_main_cx():
            """  财新数据通-股票精选新闻内容
            Returns:
                str: 返回所有历史新闻数据
            Raises:
                Exception: 当查询股票数据发生异常时抛出
            """
            try:
                stock_news_main_cx_df = ak.stock_news_main_cx()
                if stock_news_main_cx_df.empty:
                    return "未找到该股票的信息。"
                else:
                    return stock_news_main_cx_df.head(20).to_json(orient='records', force_ascii=False)
            except Exception as e:
                return f"查询股票信息时出现错误: {e}"

        @mcp.tool(description="获取指定股票代码的行情信息,单次返回指定股票的行情报价数据")
        def stock_bid_ask_em(stock_code: str) -> str:
            """获取指定股票代码的行情信息,单次返回指定股票的行情报价数据。
            获取 A 股股票的实时行情数据,包括股票名称、最新价格和涨跌幅信息。
            Args:
                stock_code (str): 股票代码,例如 symbol="000001";
            Returns:
                str: 返回包含股票行情信息的字符串,
            Raises:
                Exception: 当查询股票数据发生异常时抛出
            """
            try:
                stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol=stock_code)
                if stock_bid_ask_em_df.empty:
                    return "未找到该股票的行情信息。"
                else:
                    return stock_bid_ask_em_df.to_json(orient='records', force_ascii=False)
            except Exception as e:
                return f"查询股票行情时出现错误: {e}"
            