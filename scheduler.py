from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import pickle
from time import time

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def fetch_data():
    """ grab data from crypto server """
    response = requests.get('https://api.cryptonator.com/api/full/btc-usd')
    to_save = {
        'rates_date': time(),
        'rates': response.json()['ticker']['markets']
    }

    data_file = open(r'./data', 'rb')
    try:
        saved_data = pickle.load(data_file)
    except EOFError:
        saved_data = []
    data_file.close()

    saved_data.append(to_save)

    file_to_save = open(r'./data', 'wb')
    file_to_save.truncate()
    pickle.dump(saved_data, file_to_save)
    file_to_save.close()


sched.start()
