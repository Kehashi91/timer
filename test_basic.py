import unittest
from datetime import datetime, timedelta
import time
import json

from timer import Timer, inputhandler

class Test_basic_timer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()
        self.testime_tolerance = timedelta(seconds=2)

    def test_no_pause_5_seconds(self):
        testime_limit = timedelta(seconds=5)
        time.sleep(5)
        with self.assertRaises(SystemExit) as cm:
            self.timer.exithandle()
        self.assertTrue(testime_limit - self.testime_tolerance < self.timer.totaltime < testime_limit + self.testime_tolerance)

    def test_10_seconds_then_pause_5_seconds_then_exit(self):
        testime_limit = timedelta(seconds=10)
        time.sleep(10)
        self.timer.eventhandle("P")
        time.sleep(5)
        with self.assertRaises(SystemExit) as cm:
            self.timer.exithandle()
        self.assertTrue(testime_limit - self.testime_tolerance < self.timer.totaltime < testime_limit + self.testime_tolerance)
        
    def test_10_seconds_then_pause_5_seconds_then_unpase_for_5_seconds_exit(self):
        testime_limit = timedelta(seconds=15)
        time.sleep(10)
        self.timer.eventhandle("P")
        time.sleep(5)
        self.timer.eventhandle("P")
        time.sleep(5)
        with self.assertRaises(SystemExit) as cm:
            self.timer.exithandle()
        self.assertTrue(testime_limit - self.testime_tolerance < self.timer.totaltime < testime_limit + self.testime_tolerance)

    def test_json_synchronization(self):
        time.sleep(5)
        with self.assertRaises(SystemExit) as cm:
            self.timer.exithandle()
        with open('data.json', 'r') as f:
            json_data = json.load(f)
        self.assertEqual(json_data["work_time"], str(self.timer.totaltime))

if __name__ == '__main__':
    unittest.main()