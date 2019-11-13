import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os.path
import math
import numpy as np
import pytz


def converttimezone(latest_time, tzfrom, tzto):
    old_timezone = pytz.timezone(tzfrom)
    new_timezone = pytz.timezone(tzto)
    my_timestamp_in_new_timezone = old_timezone.localize(latest_time).astimezone(new_timezone)
    return my_timestamp_in_new_timezone

def parsedata(stocks, currency):
    #loop through all stocks and get 30 min of last day
    for i in range(len(stocks)):
        ticker_data = yf.Ticker(stocks[i]).history(period="1d", interval="1m")
        close_price = ticker_data.Close.tail(1)

        df = pd.DataFrame({'Date': [close_price.index.values[0]],
                           'Bought Price': [close_price.iat[0]],
                           'Shares': [0],
                           'Cash Available': [0],
                           'Net Invested': [0]})

        df.set_index('Date', inplace=True)
        fx_rate = ccyconversion(currency[i], "USD")
        df1 = df.copy()
        bought_price_loc = df1.columns.get_loc('Bought Price')
        bought_price = df1.iloc[0, bought_price_loc]
        bought_price_fx = fx_rate * bought_price
        df1.iloc[0, bought_price_loc] = bought_price_fx
        buystock(df1, stocks[i])

    return 1




def buystock(df, stock_name):

    path = "StockTracker/" + "Ledger_" + stock_name + ".csv"
    initial_injection = 10000
    daily_injection = 1000

    if os.path.exists(path):
        df_read = pd.read_csv(path)
        df_read.set_index('Date', inplace=True)
        df1 = injectcash(df_read.tail(1), daily_injection)
        cash_left_loc = df1.columns.get_loc('Cash Available')
        cash_left = df1.iloc[0, cash_left_loc]
        net_invested_loc = df1.columns.get_loc('Net Invested')
        net_invested = df1.iloc[0, net_invested_loc]

        df.iloc[0, cash_left_loc] = cash_left
        df.iloc[0, net_invested_loc] = net_invested
        df_updated = sharestobuy(df)


        with open(path, 'a+') as writeFile:
            df_updated.to_csv(writeFile, header=False, float_format='%.2f')
        writeFile.close()
        print("Bought " + stock_name)
    else:
        df1 = injectcash(df, initial_injection)
        df_updated = sharestobuy(df1)
        with open(path, 'a+') as writeFile:
            df_updated.to_csv(writeFile, header=True, float_format='%.2f')
            writeFile.close()
        print("Bought " + stock_name)
    return 1


def injectcash(df, cash_in):
    df1 = df.copy()
    cash_left_loc = df1.columns.get_loc('Cash Available')
    cash_left = df1.iloc[0,cash_left_loc]
    cash_net = cash_left + cash_in
    df1.iloc[0,cash_left_loc] = cash_net
    return df1


def sharestobuy(df):
    df1 = df.copy()
    cash_left_loc = df1.columns.get_loc('Cash Available')
    cash_left = df1.iloc[0, cash_left_loc]
    bought_price_loc = df1.columns.get_loc('Bought Price')
    bought_price = df1.iloc[0, bought_price_loc]
    shares_loc = df1.columns.get_loc('Shares')
    shares = math.floor(cash_left / bought_price)
    net_invested_loc = df1.columns.get_loc('Net Invested')
    net_invested = df1.iloc[0, net_invested_loc]

    left_over_cash = cash_left - shares*bought_price

    if(shares < 1):
        df1.iloc[0,net_invested_loc] = net_invested
        df1.iloc[0, cash_left_loc] = cash_left
        df1.iloc[0, shares_loc] = 0
    else:
        df1.iloc[0,net_invested_loc] = net_invested + cash_left - left_over_cash
        df1.iloc[0, cash_left_loc] = left_over_cash
        df1.iloc[0, shares_loc] = shares

    return df1


def ccyconversion(ccy_from, ccy_to):
    fx_pair = ccy_from + ccy_to + "=X"
    if ccy_to != ccy_from:
        fx_data = yf.Ticker(fx_pair).history(period="1d", interval="1m")
        fx_close = fx_data.Close.tail(1).iat[0]
    else:
        fx_close = 1
    return fx_close


def main():
    print("Buying session begins: ")
    # healthcare stocks NYSE, HKEX, LSE
    stocks = ["GEN", "CHCT", "1521.HK", "2616.HK", "DPH.L", "GSK.L"]
    currency = ["USD", "USD", "HKD", "HKD", "GBP", "GBP", ]
    parsedata(stocks, currency)


if __name__ == "__main__":
    main()














