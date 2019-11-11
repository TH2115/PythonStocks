import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import csv

##################### get stock info for all 6 tickers #########################################

n_days = 120
today = datetime.date.today()
n_days_ago = today - datetime.timedelta(days=n_days)

d_1 = today.strftime("%Y-%m-%d")
d_0 = n_days_ago.strftime("%Y-%m-%d")

#GSK PURETECH OXFORD BIOMED INDIVIOR GENUS DECHPRA PHARM
stocks = ["GSK", "PRTC", "OXB", "INDV", "GNS", "DPH"]
# formatting stocks into 1 string for data download

allstocks = ""
for stock in stocks:
    allstocks = allstocks + stock + ".L" + " "

mkt_data = yf.download(allstocks, group_by = 'ticker', start=d_0, end=d_1)

# reading and appending to file

for stock in stocks:
    close_price = mkt_data[stock + ".L"].Close.tail(1)
    with open("StockTracker/" + stock + ".csv", 'a+') as writeFile:
        close_price.to_csv(writeFile, header=True)
    writeFile.close()












