import pandas as pd
import akshare as ak

# stock symbol of "宁德时代" is "300750"
stock_symbol = "300750"

# we fetch daily history data between start and end date
# adjust 默认返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据
df = ak.stock_zh_a_hist(symbol=stock_symbol,
                        period="daily",
                        start_date="20250501",
                        end_date='20250520',
                        adjust="qfq")

print(df.dtypes)

# transfer the date format from object to datetime64
df['日期'] = pd.to_datetime(df['日期'])
print(df.dtypes)

df.set_index('日期', inplace=True)
df.sort_index(ascending=False, inplace=True)

df.to_csv('%s.csv' % stock_symbol)
