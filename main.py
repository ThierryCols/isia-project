import requests
import pickle
from time import time
import hug


def fetch_data():
    """ grab data from crypto server """
    response = requests.get('https://api.cryptonator.com/api/full/btc-usd')
    to_save = {
        'rates_date': time(),
        'rates': response.json()['ticker']['markets']
    }

    saved_data = get_data_from_file()
    saved_data.append(to_save)

    save_data_to_file(saved_data)


def get_data_from_file():
    """ load data from file and serve it """
    data_file = open(r'./data', 'rb')
    try:
        saved_data = pickle.load(data_file)
    except EOFError:
        saved_data = []
    data_file.close()
    return saved_data


def save_data_to_file(data):
    """ save data in target file """
    file_to_save = open(r'./data', 'wb')
    file_to_save.truncate()
    pickle.dump(data, file_to_save)
    file_to_save.close()


@hug.get('/crypto-lovers')
def serve_data_over_internet():
    data = get_data_from_file()
    return data


if __name__ == '__main__':
    fetch_data()
