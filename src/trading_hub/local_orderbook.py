import logging
import websocket
import json
from src.helpers.utils import *

SNAPSHOT_URL = "https://api.binance.com/api/v3/depth?symbol="
SOCKET = "wss://stream.binance.com:443/ws/"

LOGGER = logging.getLogger(__name__)


class LocalOrderBook:
    def __init__(self, symbol, snapshot_limit):
        self._symbol = symbol
        self._snapshot_limit = snapshot_limit
        self.start_updating = False
        self.last_message = dict()
        self.snapshot = dict()
        self.bids = dict()
        self.asks = dict()

        """
        :param _symbol: The ticker of interest
        :param _snapshot_limit: Depth of snapshot
        :param start_updating: The first update must comply different rules than the rest. This param is hence used to
            track its progress
        :param last_message: The latest updated from the stream
        :param snapshot: Stores latest snapshot
        :param bids: The order book for the bid side
        :param asks: The order book for the ask side
        
        """
    def get_params(self):
        """
        The get_params method aims to get the latest snapshot and pre-process it to bids and asks
        which are later updated separately
        """
        if not self.snapshot:
            self.snapshot = get_snapshot(SNAPSHOT_URL+self._symbol.upper()+"&limit="+self._snapshot_limit)
            self.bids, self.asks = preprocess_snapshot(self.snapshot)

    def set_up(self, new_update_massage):
        """
        The set_up method has 2 roles:
         1. Checks if the current update aligns with the requirements for starting the snapshot updates
         2. In case the updating process has not yet started, the method checks if there has been a 'jump'
            in the update message (e.g. first change of the updating message arrived 'too' late and hence
            some changes have been missed and a new snapshot is required)

        :param new_update_massage: The latest updated from the stream
        """

        if new_update_massage['U'] <= self.snapshot['lastUpdateId'] + 1 <= new_update_massage['u']:
            print("--------- Start --- Update ---------")
            self.last_message = new_update_massage
            self.start_updating = True
            self.bids, self.asks = update_book(bids=self.bids,
                                               asks=self.asks,
                                               json_message=new_update_massage)

        if new_update_massage['U'] > self.snapshot['lastUpdateId'] + 1 and not self.start_updating:
            raise Exception(f"First update was at {new_update_massage['U']} which "
                            f"is later than snapshot's final update"
                            f"at {self.snapshot['lastUpdateId']}")

    def update_snapshot(self, new_update_massage):
        """
        The update_snapshot method aims to update the prices and quantities of both the bids and the asks
        and sort them in the relevant order

        :param new_update_massage: The latest updated from the stream
        """
        if new_update_massage['U'] == self.last_message['u'] + 1:
            self.last_message = new_update_massage
            self.bids, self.asks = update_book(bids=self.bids,
                                               asks=self.asks,
                                               json_message=new_update_massage)
        else:
            raise Exception("A jump in the update occurred")

    def on_message(self, ws, message):
        """
        The on_message method processes and prints all the streaming I/O

        :param ws: The stream
        :param message: The latest stream message
        """

        self.get_params()
        new_update_massage = json.loads(message)

        if not self.start_updating:
            print('Current Update: ', new_update_massage)
            print('Latest Snapshot Update ID: ', self.snapshot['lastUpdateId'])
            try:
                self.set_up(new_update_massage=new_update_massage)
            except Exception as e:
                LOGGER.warning(f"The set up was interrupted by the following error: {e}")
        else:
            print('Current Update: ', new_update_massage)
            try:
                self.update_snapshot(new_update_massage=new_update_massage)
            except Exception as e:
                LOGGER.warning(f"The update was interrupted by the following error: {e}")

        print("Bids: ", self.bids)
        print("Asks: ", self.asks)
        print("___________")

    def on_close(self, ws):
        """
        The on_close method provides a message when the stream is closed

        :param ws: The stream
        """
        print(f"Connection closed")

    def main(self):
        """
        The main method triggers the whole workflow
        """
        ws = websocket.WebSocketApp(SOCKET + self._symbol + "@depth",
                                    on_message=self.on_message,
                                    on_close=self.on_close)
        ws.run_forever()


if __name__ == '__main__':

    try:
        Client = LocalOrderBook(symbol="bnbbtc", snapshot_limit='2')
        Client.main()
    except Exception as e:
        LOGGER.warning(f"Connection was interrupted due"
                       f"the following error: {e}."
                       f"Reconnecting again...")
