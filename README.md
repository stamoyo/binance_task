# Binance Local Orderbook Management

Abstract:

        The repository is dedicated to solve a technical interview challenge
 

Folder 1: 
        src/trading_hub
        
        local_orderbook.py - this is the main file where the process happens. It contains
        the LocalOrderBook class which is accountable for the general structure and workflow
        
Folder 2:
        src/helpers

        utils.py - the file contains some helper functions that are being called mulitple times
        by the local_orderbook.py 

        
Folder 3:
        tests

        test_utils.py - this is where functions are being tested
        test_trading_hub.py - tests the behaviour of methods
        mock_data.py - the file contains mock data that is used by the test.py file


Objective:
        
        The aim is to update live data from the Binance websocket and print it in
        the required format (sorted by decending for bids and by ascending for asks

Instructions: 

        In order to run the program, please, go to src/trading_hub/local_order.py and 
        scroll down to the botom of the page. You can then modify the method params and
        run it. In order to make it more dynamic, it could use sys for example to fetch
        user input from the terminal

        Next, you can run the test_utils.py and test_traind_hub.py to make sure that the
        methods behave the way they are expect to and stress test some edge cases

Solution:

        The solution works as follows: takes a snap_shot form the Binance API and fetches
        new streams from the websocket. It begins by examining whether the updates align
        with the conditions explained in the Binance API page 
        (see https://binance-docs.github.io/apidocs/spot/en/#partial-book-depth-streams)
        Once the streamed message complies with the conditions the updating begins by
        altering the snap_shot with the update. Then, the solution examines every next
        streamed message and updates the snap_shot appropriately. If an update is invalid,
        e.g. the first change of the message is later than the previous' message latest
        update + 1 the code rasies an error to indicate probable missed changes

        Each new update from the stream is printed regardless of whether the updading has
        started or not. --------- Start --- Update --------- is printed once the first
        update takes place and following the altered bids and asks dictionaries


