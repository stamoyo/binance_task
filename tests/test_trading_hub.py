from tests import mock_data
from unittest import TestCase
from src.trading_hub.local_orderbook import LocalOrderBook


class TestTradingHub(TestCase):

    def testSetUpException(self,):
        """
        Testing when the earliest change in update message is later than the snapshot
        and the updating has not yet started
        """

        Client = LocalOrderBook(symbol="bnbbtc", snapshot_limit='2')
        Client.start_updating = False
        Client.snapshot = mock_data.SNAPSHOT_DATA

        new_update_massage = mock_data.JSON_EXCEPTION_MESSAGE

        self.assertRaises(
            Exception,
            lambda: Client.set_up(new_update_massage=new_update_massage),
        )

    def testSetUpValidInput(self,):
        """
        Testing the set_up method with a valid input when the updating has started
        """

        Client = LocalOrderBook(symbol="bnbbtc", snapshot_limit='2')
        Client.start_updating = True
        Client.snapshot = mock_data.SNAPSHOT_DATA

        new_update_massage = mock_data.JSON_NORMAL_MESSAGE
        Client.set_up(new_update_massage=new_update_massage)

        self.assertEqual(Client.bids, mock_data.SETUP_BIDS)
        self.assertEqual(Client.asks, mock_data.SETUP_ASKS)
        self.assertEqual(Client.start_updating, mock_data.SETUP_START_UPDATING)
        self.assertEqual(Client.last_message, mock_data.SETUP_LAST_MESSAGE)

    def testUpdateSnapshotException(self,):
        """
        Testing the update_snapshot method when earliest change in the new message is not
        the latest + 1 from the previous message
        """

        Client = LocalOrderBook(symbol="bnbbtc", snapshot_limit='2')
        Client.last_message = 300

        new_update_massage = mock_data.JSON_EXCEPTION_MESSAGE

        self.assertRaises(
            Exception,
            lambda: Client.update_snapshot(new_update_massage=new_update_massage),
        )

    def testUpdateSnapshotValidInput(self,):
        """
        Testing the update_snapshot method when a valid input must trigger the bids and asks update
        from the latest message
        """

        Client = LocalOrderBook(symbol="bnbbtc", snapshot_limit='2')
        Client.last_message['u'] = 94

        new_update_massage = mock_data.JSON_NORMAL_MESSAGE
        Client.update_snapshot(new_update_massage=new_update_massage)

        self.assertEqual(Client.bids, mock_data.SETUP_BIDS)
        self.assertEqual(Client.asks, mock_data.SETUP_ASKS)
        self.assertEqual(Client.last_message, mock_data.SETUP_LAST_MESSAGE)
