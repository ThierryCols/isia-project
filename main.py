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

    saved_data = get_data_from_file('btc')
    saved_data.append(to_save)

    save_data_to_file(saved_data, 'btc')

    response = requests.get('https://api.cryptonator.com/api/full/eth-usd')
    to_save = {
        'rates_date': time(),
        'rates': response.json()['ticker']['markets']
    }

    saved_data = get_data_from_file('eth')
    saved_data.append(to_save)

    save_data_to_file(saved_data, 'eth')


def get_data_from_file(crypto_name):
    """ load data from file and serve it """
    if (crypto_name == 'btc'):
        data_file = open(r'data', 'rb')
    else:
        data_file = open(r'data_eth', 'rb')
    try:
        saved_data = pickle.load(data_file)
    except EOFError:
        saved_data = []
    data_file.close()
    return saved_data


def save_data_to_file(data, crypto_name):
    """ save data in target file """
    if (crypto_name == 'btc'):
        file_to_save = open(r'data', 'wb')
    else:
        file_to_save = open(r'data_eth', 'wb')
    file_to_save.truncate()
    pickle.dump(data, file_to_save)
    file_to_save.close()


@hug.get('/btc-lovers')
def serve_btc_over_internet():
    data = get_data_from_file('btc')
    return data


@hug.get('/eth-lovers')
def serve_eth_over_internet():
    data = get_data_from_file('eth')
    return data


if __name__ == '__main__':
    fetch_data()
