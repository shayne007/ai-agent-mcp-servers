from langchain_core.tools import tool
from financial_mcp_server.llms.DeepSeek import DeepSeekV3
import akshare as ak
import pandas as pd
import os
from datetime import datetime
import json
import concurrent.futures
import logging
from typing import Dict, Any,List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Create cache directory if it doesn't exist
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def save_to_cache(df, filename='stock_data.csv'):
    """Save stock data to cache"""
    cache_path = os.path.join(CACHE_DIR, filename)
    # Ensure string columns are saved as strings
    for col in ['代码', '名称']:
        if col in df.columns:
            df[col] = df[col].astype(str)
    df.to_csv(cache_path, index=False)
    # Save timestamp
    timestamp_path = os.path.join(CACHE_DIR, 'timestamp.json')
    with open(timestamp_path, 'w') as f:
        json.dump({'last_update': datetime.now().isoformat()}, f)

def load_from_cache(filename='stock_data.csv'):
    """Load stock data from cache"""
    cache_path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(cache_path):
        df = pd.read_csv(cache_path)
        # Ensure string columns are loaded as strings
        for col in ['代码', '名称']:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    return None

def fetch_stock_data_with_timeout(timeout=5):
    """Fetch stock data with timeout"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(ak.stock_zh_a_spot_em)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(f"获取股票数据超时，超过{timeout}秒")

@tool("get_macro_economic_data")
def get_macro_economic_data(indicator: str) -> List[Dict[str, Any]]:
    """获取宏观经济数据
    Args:
        indicator: 指标名称，如'GDP'、'CPI'等
    """
    indicator_map = {
        'GDP': ak.macro_china_gdp,
        'CPI': ak.macro_china_cpi,
        'PMI': ak.macro_china_pmi
    }
    if indicator not in indicator_map:
        raise ValueError(f"Unsupported indicator: {indicator}")
    
    logger.info(f"Fetching macroeconomic data for {indicator}")
    df = indicator_map[indicator]()
    return df.to_dict('records')

@tool("get_stock_real_time_data")
def get_stock_real_time_data(code: str, name: str) -> str:
    """可以根据传入的股票代码或股票名称获取股票实时行情信息
    Args:
        code: 股票代码
        name: 股票名称
    """
    try:
        # Fetch Hong Kong stock data
        logger.info("Fetching Hong Kong stock data...")
        df = ak.stock_hk_spot()
        
        if df is None or df.empty:
            return {"error": "无法获取股票数据"}
            
        # Remove .HK suffix if present
        code = str(code).replace('.HK', '').lstrip('0')
        code_isempty = (code == "" or len(code) <= 2)
        name_isempty = (name == "" or len(name) <= 2)

        if code_isempty and name_isempty:
            return {"error": "股票代码和名称不能同时为空"}

        try:
            ret = None
            if code_isempty and not name_isempty:
                ret = df[df['name'].str.contains(name, case=False, na=False)]
            elif not code_isempty and name_isempty:
                ret = df[df['symbol'].str.contains(code, case=False, na=False)]
            else:
                ret = df[df['symbol'].str.contains(code, case=False, na=False) & 
                        df['name'].str.contains(name, case=False, na=False)]
            
            if ret is None or ret.empty:
                return {"error": "未找到匹配的股票信息"}
                
            return ret.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return {"error": f"处理数据时出错: {str(e)}"}
            
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return {"error": f"获取股票数据失败: {str(e)}"}

@tool("get_stock_info")
def get_stock_info(code: str) -> Dict[str, Any]:
    """获取股票基本信息
    Args:
        code: 股票代码
    """
    try:
        logger.info(f"Fetching stock info for {code}")
        df = ak.stock_hk_spot()
        # Remove .HK suffix if present
        code = code.replace('.HK', '')
        logger.info(f"Available stock codes: {df['symbol'].unique()[:5]}")  # Show first 5 codes
        matching_stocks = df[df['symbol'] == code]
        
        if matching_stocks.empty:
            return {"error": f"未找到股票代码 {code} 的信息"}
            
        stock_info = matching_stocks.iloc[0].to_dict()
        return stock_info
    except Exception as e:
        logger.error(f"Error fetching stock info: {str(e)}")
        return {"error": f"获取股票信息失败: {str(e)}"}

@tool("get_hk_stock_hist")
def get_hk_stock_hist(code: str, start_date: str, end_date: str) -> str:
    """获取股票历史数据
    Args:
        code: 股票代码，如'00700'（腾讯控股）
        start_date: 开始日期，格式'YYYYMMDD'
        end_date: 结束日期，格式'YYYYMMDD'
    """
    try:
        # Remove .HK suffix if present and ensure proper format
        code = code.replace('.HK', '').zfill(5)
        logger.info(f"Fetching stock history for {code} from {start_date} to {end_date}")
        
        stock_hk_hist_df = ak.stock_hk_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="")
        if stock_hk_hist_df.empty:
            return {"error": "未找到股票历史数据"}
            
        return stock_hk_hist_df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error fetching stock history: {str(e)}")
        return {"error": f"获取股票历史数据失败: {str(e)}"}

tools = [get_macro_economic_data, get_stock_real_time_data, get_stock_info, get_hk_stock_hist]
tools_by_name = {tool.name: tool for tool in tools}
llm = DeepSeekV3()
llm_with_tools = llm.bind_tools(tools)

if __name__ == "__main__":
    # Test the tools
    print(tools_by_name['get_macro_economic_data'].invoke({"indicator": "GDP"}))
    # print(tools_by_name['get_stock_real_time_data'].invoke({"code": "00700", "name": "腾讯"}))
    # print(tools_by_name['get_stock_info'].invoke({"code": "00700"}))
    # print(tools_by_name['get_hk_stock_hist'].invoke({"code": "0700.HK", "start_date": "20250101", "end_date": "20250201"}))

