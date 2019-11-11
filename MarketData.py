import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import csv
import os.path


def AddToFile(stock_name, mkt_data):

    close_price = mkt_data[stock_name + ".L"].Close.tail(1)

    df = pd.DataFrame({'Date': [close_price.index.values[0]],
                       'Closing Price': [close_price.iat[0]],
                       'Cash': [0]})

    df.set_index('Date', inplace=True)

    print(df)


    if(os.path.exists("StockTracker/" + stock_name + ".csv")):
        with open("StockTracker/" + stock_name + ".csv", 'a+') as writeFile:
            df.to_csv(writeFile, header=False)
        writeFile.close()
        return 1
    else:
        with open("StockTracker/" + stock_name + ".csv", 'a+') as writeFile:
            df.to_csv(writeFile, header=True)
            writeFile.close()
        return 0


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
    AddToFile(stock, mkt_data)














