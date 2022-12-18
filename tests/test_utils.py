from src.helpers.utils import *
from unittest import TestCase
from tests import mock_data


class TestUtils(TestCase):

    def testUpdateBidsAsksBookValidInput(self):
        """
        Testing the update_bids, update_asks and update_book methods with valid non-empty input
        """
        json_message = mock_data.JSON_MESSAGE

        bids, asks = mock_data.BIDS, mock_data.ASKS
        result_bids, result_asks, result_book = mock_data.RESULT_BIDS, mock_data.RESULT_ASKS, mock_data.RESULT_BOOK

        self.assertEqual(update_bids(bids, json_message), result_bids)
        self.assertEqual(update_asks(asks, json_message), result_asks)
        self.assertEqual(update_book(bids, asks, json_message), result_book)

    def testUpdateBidsAsksBookValidEmptyInput(self):
        """
        Testing the update_bids, update_asks and update_book methods with valid empty input
        """
        json_message = mock_data.JSON_EMPTY_MESSAGE

        bids, asks = mock_data.BIDS, mock_data.ASKS
        result_bids, result_asks, result_book = mock_data.RESULT_BIDS_EMPTY, mock_data.RESULT_ASKS_EMPTY, mock_data.RESULT_BOOK_EMPTY

        self.assertEqual(update_bids(bids, json_message), result_bids)
        self.assertEqual(update_asks(asks, json_message), result_asks)
        self.assertEqual(update_book(bids, asks, json_message), result_book)

    def testPreProcessSnapShot(self):
        """
        Testing preprocess_snapshot with valid input
        """
        snapshot_data = mock_data.SNAPSHOT_DATA
        snapshot_bids = mock_data.SNAPSHOT_BIDS
        snapshot_asks = mock_data.SNAPSHOT_ASKS

        bids, asks = preprocess_snapshot(snapshot_data)

        self.assertEqual(bids, snapshot_bids)
        self.assertEqual(asks, snapshot_asks)
