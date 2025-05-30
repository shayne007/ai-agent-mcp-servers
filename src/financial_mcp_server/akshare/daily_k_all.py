import asyncio
import akshare as ak
from financial_mcp_server.akshare.daily_k_by_code import save_daily_k
import time


def get_all_codes():
    try:
        df = ak.stock_zh_a_spot_em()
        codes = df['代码']
        bool_list = df['代码'].str.startswith(('60', '30', '00', '68'))
        return codes[bool_list].to_list()
    except Exception as e:
        print(f"Error getting stock codes: {str(e)}")
        return []


def save_all_data(start_date: str, end_date: str):
    codes = get_all_codes()
    if not codes:
        print("No stock codes found")
        return

    print("共有{}个股票需要抓取".format(len(codes)))
    n = 500  # Process 500 stocks at a time
    total_batches = (len(codes) + n - 1) // n

    for i in range(0, len(codes), n):
        batch_num = i // n + 1
        subset = codes[i:i + n]
        if len(subset) > 0:
            print(
                f"Processing batch {batch_num}/{total_batches} ({len(subset)} stocks)")
            try:
                asyncio.run(save_daily_k(subset, start_date, end_date,
                                         prefix=f"batch_{batch_num}_"))
                print(f"Completed batch {batch_num}/{total_batches}")
                # Add a small delay between batches to avoid overwhelming the server
                time.sleep(1)
            except Exception as e:
                print(f"Error processing batch {batch_num}: {str(e)}")
                continue


if __name__ == "__main__":
    save_all_data(start_date='20250101', end_date='20250530')
