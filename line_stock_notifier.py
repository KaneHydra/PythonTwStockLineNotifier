# -*- coding=utf-8 -*-
import pytz
import requests
import pandas as pd
from rich import print
from datetime import datetime

url_twse = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
response = requests.get(url_twse)
stocks = response.json()

df = pd.DataFrame(stocks)
numeric_columns = [
    "TradeVolume",
    "TradeValue",
    "OpeningPrice",
    "HighestPrice",
    "LowestPrice",
    "ClosingPrice",
    "Change",
    "Transaction",
]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, downcast="integer")
df["ChangeRate"] = round(df["Change"] / df["ClosingPrice"] * 100, 2)
df.sort_values(by="TradeVolume", ascending=False, inplace=True)
df.set_index("Code", inplace=True)

msg = (
    "25-黃葵昇\n"
    f"時　　間：{datetime.now(pytz.timezone('Asia/Taipei')):%Y-%m-%d %H:%M:%S}\n"
    "每日成交量最高前5支股票/ETF：\n"
)
for idx, row in df.head(5).iterrows():
    msg += (
        f"{(10 * '—')}\n"
        f"代　　碼：{idx}\n"
        f"名　　稱：{row.Name}\n"
        f"成交　量：{int(row.TradeVolume):,d}\n"
        f"成交股數：{int(row.TradeValue):,d}\n"
        f"開盤　價：{row.OpeningPrice:.2f}\n"
        f"最高　價：{row.HighestPrice:.2f}\n"
        f"最低　價：{row.LowestPrice:.2f}\n"
        f"收盤　價：{row.ClosingPrice:.2f}\n"
        f"漲跌　幅：{row.ChangeRate:.2f}%\n"
        f"交易筆數：{int(row.Transaction):,d}\n"
    )

print(msg)

with open("./line_token.txt", mode="r") as f:
    LINE_TOKEN = f.read().strip()


def sendtoLine(msg):
    urline = "https://notify-api.line.me/api/notify"
    token = LINE_TOKEN
    headers = {
        "Authorization": "Bearer " + token  # 設定權杖
    }
    data = {
        "message": "\n" + msg.strip()  # 設定要發送的訊息
    }
    requests.post(urline, headers=headers, data=data)


sendtoLine(msg)

