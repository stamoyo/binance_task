import requests


def update_bids(bids, json_message):
    """
    The update_bids function updates the existing bids dictionary

    :param bids: The bids dictionary to be updated
    :param json_message: The latest message from the stream
    :return: Bids updated to the latest stream
    """
    if json_message['b']:
        for i in json_message['b']:
            bids[i[0]] = i[1]
            if i[1] == '0.00000000':
                del bids[i[0]]
    return dict(sorted(bids.items(), reverse=True))


def update_asks(asks, json_message):
    """
    The update_asks function updates the existing asks dictionary

    :param asks: The asks dictionary to be updated
    :param json_message: The latest message from the stream
    :return: Asks updated to the latest stream
    """
    if json_message['a']:
        for i in json_message['a']:
            asks[i[0]] = i[1]
            if i[1] == '0.00000000':
                del asks[i[0]]
    return dict(sorted(asks.items()))


def update_book(bids, asks, json_message):
    """
    The update_book function returns Bids and Asks

    :param bids: The bids dictionary to be updated
    :param asks: The asks dictionary to be updated
    :param json_message: The latest message from the stream
    :return: Bids and Asks
    """
    return update_bids(bids, json_message), update_asks(asks, json_message)


def preprocess_snapshot(snapshot_data):
    """
    The preprocess_snapshot aims to convert the input snapshot from dictionary of
    multiple list values to two separate dictionaries - bid and ask - each having
    price as key and quantity as value

    :param snapshot_data: Latest snapshot
    :return: Bid and ask dictionaries
    """
    bid = {}
    ask = {}

    for i in snapshot_data['bids']:
        bid[i[0]] = i[1]
    for i in snapshot_data['asks']:
        ask[i[0]] = i[1]

    bid = dict(reversed(sorted(bid.items())))
    ask = dict(sorted(ask.items()))
    return bid, ask


def get_snapshot(snapshot_url):
    """
    The get_snapshot function makes a request to collect the latest snapshot
    from the exchange

    :param snapshot_url: The desired URL (api endpoint)
    :return: Snapshot in JSON format
    """
    return requests.get(snapshot_url).json()
