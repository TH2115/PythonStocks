import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

##################### get stock info for all 6 tickers #########################################
n_days = 120
today = datetime.date.today()
n_days_ago = today - datetime.timedelta(days=n_days)

d_1 = today.strftime("%Y-%m-%d")
d_0 = n_days_ago.strftime("%Y-%m-%d")

print("d current =", d_1)
print("d last month =", d_0)

mkt_data = yf.download("GSK.L PRTC.L OXB.L INDV.L GNS.L DPH.L", group_by = 'ticker', start=d_0, end=d_1)


# # GSK
# gsk_data = yf.download('GSK.L', d_0, d_1)
# #PURETECH
# prtc = yf.Ticker("PRTC")
# #OXFORD BIOMED
# oxb = yf.Ticker("OXB")
# #INDIVIOR
# indv = yf.Ticker("INDV")
# #GENUS
# gns = yf.Ticker("GNS")
# #DECHPRA PHARM
# dph = yf.Ticker("DPH")

print(mkt_data['GSK.L'].Close)
