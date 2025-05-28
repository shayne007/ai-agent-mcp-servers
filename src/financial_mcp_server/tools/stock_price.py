from langchain_core.tools import tool
from financial_mcp_server.llms.DeepSeek import DeepSeekV3
import akshare as ak
import pandas as pd
import os
from datetime import datetime
import json

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

@tool
def get_stock_info(code: str, name: str) -> str:
    """可以根据传入的股票代码或股票名称获取股票实时行情信息
    Args:
        code: 股票代码
        name: 股票名称
    """
    code_isempty = (code == "" or len(code) <= 2)
    name_isempty = (name == "" or len(name) <= 2)

    if code_isempty and name_isempty:
        return []

    try:
        # Try to get fresh data from akshare
        df = ak.stock_zh_a_spot_em()
        # Save to cache if successful
        save_to_cache(df)
    except Exception as e:
        print(f"Error fetching from akshare: {e}")
        # If akshare fails, try to load from cache
        df = load_from_cache()
        if df is None:
            return {"error": "无法获取股票数据，且本地缓存不可用"}

    try:
        ret = None
        if code_isempty and not name_isempty:
            ret = df[df['名称'].str.contains(name)]
        elif not code_isempty and name_isempty:
            ret = df[df['代码'].str.contains(code)]
        else:
            ret = df[df['代码'].str.contains(code) & df['名称'].str.contains(name)]
        
        if ret is None or ret.empty:
            return {"error": "未找到匹配的股票信息"}
            
        return ret.to_dict(orient='records')
    except Exception as e:
        print(f"Error processing data: {e}")
        return {"error": f"处理数据时出错: {str(e)}"}


tools = [get_stock_info]
tools_by_name = {tool.name: tool for tool in tools}
llm = DeepSeekV3()
llm_with_tools = llm.bind_tools(tools)

if __name__ == "__main__":
    print(tools_by_name['get_stock_info'].invoke({"code": "002594", "name": "比亚迪"}))

