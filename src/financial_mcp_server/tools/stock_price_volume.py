from langchain_core.tools import tool
import pandas as pd
from financial_mcp_server.tools.load import load_df

@tool
def stock_price(target_date:str):
    """
    获取股票指定日期前三天与后三天（包含指定日期）的收盘价
    param target_date: str，指定日期
    return: float，最新价格
    """
    df = load_df('600600.csv')
    
    # 将目标日期转换为datetime
    target_date = pd.to_datetime(target_date)
    
    # 获取目标日期在数据中的位置
    date_mask = df['日期'] == target_date
    if not date_mask.any():
        return f"未找到日期 {target_date}"
    
    # 获取目标日期的索引
    target_idx = df[date_mask].index[0]
    
    # 获取前后的数据并合并
    combined_data = pd.concat([
        df.iloc[target_idx-3:target_idx][['日期', '收盘']],
        df.iloc[target_idx:target_idx+3][['日期', '收盘']]
    ])
    
    # 格式化日期为字符串
    combined_data['日期'] = combined_data['日期'].dt.strftime('%Y-%m-%d')
    
    # 返回结果
    return combined_data.to_string(index=False)

if __name__ == '__main__':
    result = stock_price.invoke({"target_date":"2024-09-26"})
    print(result)
