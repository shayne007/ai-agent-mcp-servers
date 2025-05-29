import asyncio
from typing import List
import akshare as ak
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)


async def save_daily_k(codes: List[str], start_date: str, end_date: str,
    prefix: str):
    all_data = pd.DataFrame()
    tasklist = []
    for code in codes:
        task = asyncio.create_task(load_data(code, start_date, end_date))
        tasklist.append(task)
    ret = await asyncio.gather(*tasklist)
    for r in ret:
        all_data = pd.concat([all_data, r], axis=0)
    filename = "{}{}_{}.csv".format(prefix, start_date, end_date)
    all_data.to_csv("{}/{}".format(DATA_DIR, filename))
    print("保存所有日线数据完成,文件名是:{}".format(filename))


async def load_data(symbol, start_date, end_date):
    # 由于 akshare 的 API 是同步的，我们需要在线程池中运行它
    loop = asyncio.get_event_loop()
    df = await loop.run_in_executor(None, lambda: ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"
    ))

    df['日期'] = pd.to_datetime(df['日期'])
    df.set_index('日期', inplace=True)
    df.sort_index(ascending=False, inplace=True)

    return df


if __name__ == "__main__":
    asyncio.run(save_daily_k(["300750", "600519"], "20250407", "20250411","test_"))
