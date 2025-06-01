from langchain_core.tools import tool
import pandas as pd
from financial_mcp_server.tools.load import load_df

def calc_vol_ratio_around_date(df, target_date, days_before=3, days_after=3):
    """
    计算指定日期前后的成交量比值
    :param df: DataFrame，包含股票数据
    :param target_date: str，目标日期，格式：'YYYY-MM-DD'
    :param days_before: int，目标日期前的天数
    :param days_after: int，目标日期后的天数
    :return: float，成交量比值
    """
    # 将目标日期转换为datetime
    target_date = pd.to_datetime(target_date)
    
    # 获取目标日期在数据中的位置
    date_mask = df['日期'] == target_date
    if not date_mask.any():
        print(f"未找到日期 {target_date}")
        return None
    
    # 获取目标日期的索引
    target_idx = df[date_mask].index[0]
    
    # 获取前后的数据
    before_data = df.iloc[target_idx-days_before:target_idx]['成交量']
    after_data = df.iloc[target_idx:target_idx+days_after]['成交量']

    # 计算比值
    if len(before_data) == days_before and len(after_data) == days_after:
        return after_data.mean() / before_data.mean()
    else:
        print("数据不足，无法计算比值")
        return None

@tool
def vol_info(target_date:str):
    """
    计算指定日期后3天（含指定日期）与前3天的成交量比值
    param target_date: str，指定日期，格式：'YYYY-MM-DD'
    return: float，成交量比值
    """
    df = load_df('600600.csv')
    ratio = calc_vol_ratio_around_date(df, target_date)

    return ratio

if __name__ == '__main__':
    # 可以在这里修改目标日期
    ratio =vol_info.invoke({"target_date":"2024-09-26"})

    print(f"日期 2024-09-26 后3天与前3天的成交量比值: {ratio:.2f}")
