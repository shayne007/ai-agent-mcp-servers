import os
import re
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data',
                        'daily_k')
os.makedirs(DATA_DIR, exist_ok=True)


def load_df(file: str) -> pd.DataFrame:
    df = pd.read_csv("{}/{}".format(DATA_DIR, file))
    if df.empty:
        raise Exception("文件不存在")
    df['日期'] = pd.to_datetime(df['日期'])
    df['股票代码'] = df['股票代码'].astype(str).str.zfill(
        6)  # Convert to string and pad with zeros to ensure 6 digits
    return df


def concat_csv(file_name: str):
    # 列出文件夹中的所有文件和目录
    files = os.listdir(DATA_DIR)
    # 定义一个正则表达式，匹配以数字开头的文件名
    pattern = re.compile(r'^\d+_.+\.csv$')
    # 遍历文件，筛选出符合条件的文件名
    filtered_files = [file for file in files if pattern.match(file)]
    ret = pd.DataFrame()
    # 打印结果
    for file in filtered_files:
        df = load_df(file)
        ret = pd.concat([ret, df])
    ret.to_csv("{}/{}".format(DATA_DIR, file_name))
    print("合并完成,文件名是{}".format(file_name))


if __name__ == "__main__":
    concat_csv("all_data.csv")
