import asyncio
from typing import List
import akshare as ak
import pandas as pd
import os
from requests.exceptions import RequestException

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'daily_k')
os.makedirs(DATA_DIR, exist_ok=True)

MAX_RETRIES = 3
INITIAL_DELAY = 5  # seconds

async def save_daily_k(codes: List[str], start_date: str, end_date: str,
    prefix: str):
    all_data = pd.DataFrame()
    tasklist = []
    for code in codes:
        task = asyncio.create_task(load_data(code, start_date, end_date))
        tasklist.append(task)
    ret = await asyncio.gather(*tasklist, return_exceptions=True)
    for r in ret:
        if isinstance(r, Exception):
            print(f"Error occurred: {str(r)}")
            continue
        if not r.empty:
            all_data = pd.concat([all_data, r], axis=0)
    if not all_data.empty:
        filename = "{}{}_{}.csv".format(prefix, start_date, end_date)
        all_data.to_csv("{}/{}".format(DATA_DIR, filename))
        print("保存所有日线数据完成,文件名是:{}".format(filename))
    else:
        print("没有获取到任何数据")


async def load_data(symbol, start_date, end_date):
    loop = asyncio.get_event_loop()
    retry_count = 0
    delay = INITIAL_DELAY

    while retry_count < MAX_RETRIES:
        try:
            df = await loop.run_in_executor(None, lambda: ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            ))
            
            if df.empty:
                return pd.DataFrame()
                
            df['日期'] = pd.to_datetime(df['日期'])
            df.set_index('日期', inplace=True)
            df.sort_index(ascending=False, inplace=True)
            return df
            
        except RequestException as e:
            retry_count += 1
            if retry_count == MAX_RETRIES:
                print(f"Failed to fetch data for {symbol} after {MAX_RETRIES} attempts: {str(e)}")
                return pd.DataFrame()
                
            print(f"Attempt {retry_count} failed for {symbol}, retrying in {delay} seconds...")
            await asyncio.sleep(delay)
            delay *= 2  # Exponential backoff
        except Exception as e:
            print(f"Unexpected error for {symbol}: {str(e)}")
            return pd.DataFrame()
    return None


if __name__ == "__main__":
    asyncio.run(save_daily_k(["300750", "600519"], "20250407", "20250411","test_"))
