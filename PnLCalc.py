#!/usr/bin/env python3
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os.path
import math
import numpy as np
import pytz

def ccyconversion(ccy_from, ccy_to):
    fx_pair = ccy_from + ccy_to + "=X"
    if ccy_to != ccy_from:
        fx_data = yf.Ticker(fx_pair).history(period="1d", interval="1m")
        fx_close = fx_data.Close.tail(1).iat[0]
    else:
        fx_close = 1
    return fx_close


def getactivestocks(stocks, currency):

    dt_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    df = pd.DataFrame({'Date': [dt_now]})
    df_ptc = pd.DataFrame({'Date': [dt_now]})

    net_invested = 0
    left_over = 0
    for i in range(len(stocks)):
        path = "StockTracker/" + "Ledger_" + stocks[i] + ".csv"
        df_read = pd.read_csv(path)
        df_read.set_index('Date', inplace=True)


        ticker_data = yf.Ticker(stocks[i]).history(period="1d", interval="1m")
        current_price = ticker_data.Close.tail(1).iat[0]


        fx_rate = ccyconversion(currency[i], "USD")

        current_price_fx = current_price * fx_rate

        pnl = pnlcalc(df_read, current_price_fx)

        pnl_ptc = pnlcalcptc(df_read, current_price_fx)

        df[stocks[i]] = [pnl]
        df_ptc[stocks[i]] = [pnl_ptc]

        net_invested_loc = df_read.columns.get_loc('Net Invested')
        net_invested += df_read.tail(1).iloc[0, net_invested_loc]

        left_over_loc = df_read.columns.get_loc('Cash Available')
        left_over += df_read.tail(1).iloc[0, left_over_loc]



    df.set_index('Date', inplace=True)
    df_ptc.set_index('Date', inplace=True)

    df2 = df.copy()




    df2['Net Invested ($)'] = [net_invested]
    df2['Available Cash ($)'] = [left_over]
    df2['Total PnL ($)'] = [df.sum(axis=1).iat[0]]


    df_ptc['Net Invested ($)'] = [net_invested]
    df_ptc['Available Cash ($)'] = [left_over]
    df_ptc['Total PnL (%)'] = [(df.sum(axis=1).iat[0] / net_invested)*100]

    return [df2, df_ptc]




def pnlcalc(df, currentprice):
    PnL = 0
    for index, row in df.iterrows():
        PnL += row['Shares'] * (currentprice - row['Bought Price'] )
        # print(row['Bought Price'], currentprice, row['Shares'], PnL)
    return PnL

def pnlcalcptc(df, currentprice):
    PnL = 0
    for index, row in df.iterrows():
        PnL += row['Shares'] * (currentprice - row['Bought Price'])

    net_invested_loc = df.columns.get_loc('Net Invested')
    net_invested = df.tail(1).iloc[0,net_invested_loc]
    PnL_ptc = 100*(PnL/net_invested)

    return PnL_ptc

def writepnl(df,df_ptc):

    path = "PNL/" + "PnL" + ".csv"
    if os.path.exists(path):
        with open(path, 'a+') as writeFile:
            df.to_csv(writeFile, header=False, float_format='%.2f')
        writeFile.close()
    else:
        with open(path, 'a+') as writeFile:
            df.to_csv(writeFile, header=True, float_format='%.2f')
            writeFile.close()

    path = "PNL/" + "PnL_pct" + ".csv"
    if os.path.exists(path):
        with open(path, 'a+') as writeFile:
            df_ptc.to_csv(writeFile, header=False, float_format='%.2f')
        writeFile.close()
    else:
        with open(path, 'a+') as writeFile:
            df_ptc.to_csv(writeFile, header=True, float_format='%.2f')
            writeFile.close()

    return 1

def main():
    #healthcare stocks NYSE, HKEX, LSE
    stocks = ["GEN", "CHCT", "1521.HK", "2616.HK", "DPH.L", "GSK.L"]
    currency = ["USD", "USD", "HKD", "HKD", "GBP", "GBP", ]
    [df, df_ptc] = getactivestocks(stocks, currency)
    writepnl(df,df_ptc)


if __name__ == "__main__":
    print("Calculating PnL...")
    main()

