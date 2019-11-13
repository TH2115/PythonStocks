from datetime import datetime
import time
import os
import PnLCalc
import MarketData

from apscheduler.schedulers.background import BackgroundScheduler

def job1():
    MarketData.main()
    print("Job Completed: Buying more stocks")

def job2():
    PnLCalc.main()
    print("Job Completed: Calculating PnL")

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(job1, 'cron', day_of_week='mon-fri', hour=18, minute=0, end_date='2021-01-01')
    scheduler.add_job(job2, 'cron', day_of_week='mon-fri', hour=17, minute=0, end_date='2021-01-01')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()