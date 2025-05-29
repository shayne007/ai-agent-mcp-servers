import os
import akshare as ak

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data',
                            'financial_report')
os.makedirs(data_dir, exist_ok=True)

def load_data(yjbb_date="20241231"):
    """从网络获取最新的财务报告数据"""
    try:
        print("正在从网络获取财务报告数据...")
        df = ak.stock_yjbb_em(date=yjbb_date)
        csv_path = os.path.join(data_dir, 'financial_report.csv')
        df.to_csv(csv_path, index=False)
        print(f"数据已保存到: {csv_path}")
        return True
    except Exception as e:
        print(f"获取数据时出错: {str(e)}")
        return False

