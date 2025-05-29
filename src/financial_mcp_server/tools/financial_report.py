from langchain_core.tools import tool
import pandas as pd
import os
from typing import List
from pydantic import BaseModel, Field
from financial_mcp_server.akshare.financial_report_by_code import load_data

class FinancialReportInput(BaseModel):
    stock_codes: List[str] = Field(
        description="List of stock codes to get financial reports for")
    yjbb_date: str = Field(
        default="20241231",
        description="Date of the financial report in format YYYYMMDD")


@tool(args_schema=FinancialReportInput)
def get_financial_report(stock_codes: List[str], yjbb_date: str = "20241231"):
    """
    根据股票代码列表获取财报数据

    Parameters:
    -----------
    stock_codes : list
        股票代码列表
    yjbb_date : str
        财报日期，格式为YYYYMMDD

    Returns:
    --------
    dict
        包含每个股票代码对应的财报数据的字典
    """
    # 确保数据目录存在
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data',
                            'financial_report')
    os.makedirs(data_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, 'financial_report.csv')
    
    # 如果文件不存在，先加载数据
    if not os.path.exists(csv_path):
        print("财务数据文件不存在，正在从网络获取...")
        load_data(yjbb_date)
        if not os.path.exists(csv_path):
            print("获取数据失败")
            return None

    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        print("从本地文件读取数据成功")

        # 确保股票代码列是字符串类型
        df['股票代码'] = df['股票代码'].astype(str).str.zfill(6)

        # 创建结果字典
        result = {}

        # 为每个股票代码获取数据
        for code in stock_codes:
            # 确保股票代码格式一致（6位数字）
            code = str(code).zfill(6)
            # 筛选该股票的数据
            stock_data = df[df['股票代码'] == code]

            if not stock_data.empty:
                # 将数据转换为字典格式，包含列名
                result[code] = {
                    'data': stock_data.to_dict('records')
                }
            else:
                result[code] = {
                    'data': []
                }

        return result

    except Exception as e:
        print(f"读取数据时出错: {str(e)}")
        return None

# 示例使用
if __name__ == "__main__":
    # 测试用的股票代码列表
    test_codes = ['600600', '002461', '000729', '600573']
    
    # 使用invoke而不是直接调用
    tool = get_financial_report
    result = tool.invoke({"stock_codes": test_codes,"yjbb_date": "20241231"})

    if result:
        # 打印结果
        for code, data in result.items():
            print(f"\n股票代码: {code}")
            print("数据内容:")
            for row in data['data']:
                print(row)
    else:
        print("获取数据失败")
