import asyncio
import akshare as ak
from daily_k_by_code import save_daily_k


def get_all_codes():
    df = ak.stock_zh_a_spot_em()
    codes = df['代码']
    bool_list = df['代码'].str.startswith(('60', '30', '00', '68'))
    return codes[bool_list].to_list()


def save_all_data():
    codes = get_all_codes()
    print("共有{}个股票需要抓取".format(len(codes)))
    n = 100
    for i in range(0, len(codes), n):
        subset = codes[i:i + n]
        if len(subset) > 0:
            asyncio.run(save_daily_k(subset, '20230422', '20250422',
                                     prefix=f"{i}_"))
            print("抓取了{}".format(i))


if __name__ == "__main__":
    save_all_data()
