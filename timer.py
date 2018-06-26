"""
Simple clock that i can easily run in the console while i study
and record my time spent, excluding breaks or distractions
"""

from datetime import datetime, timedelta
import json
import requests

def maketimenice(input_time):

    """Formats time in a desired way"""

    nicetime = input_time.strftime("%H:%M:%S")
    
    return nicetime

def inputhandler(expected_inputs, msg=None):

    """Input sanitizer for Timer class"""
    while True:
        if msg:
            print (msg)
            
        user_choice = input("> ")
        
        if user_choice in expected_inputs:
            return user_choice
        else:
            print ("Wrong choice!")

def api_data_dump(data, runtime_test=False):
    try:
        if runtime_test == False:
            r = requests.post('http://127.0.0.1:5000/timer/v0.1/posttime', json=data)
        elif runtime_test == True:
            r = requests.post('http://127.0.0.1:5000/timer/v0.1/runtime_test', json=data)

        if r.status_code == 201 and runtime_test == False:
            print("Data postes succesfuly to endpoint.")
        elif r.status_code != 201:
            print("Problem encountered during data posting - {} status code from server".format(r.status_code))
            exit(1)
    except Exception as e:
        print("Encontered an exception:")
        print(e)
        exit(1)

            
class Timer():

    """ A clock and a heart of the program. It contains
    a pause/unpause functionality so i can better monitor 
    my true working time"""
    
    def __init__(self):
        self.starttime = datetime.now()
        self.pause_total = timedelta(0)
        self.pause_start = timedelta(0)
        self.totaltime = 0
        self.paused = False
        self.events = ["E", "P"]

    def pausehandle(self):
        if self.paused == False:
            self.pause_start = datetime.now()
            self.paused = True
        else:
            pause_time = datetime.now() - self.pause_start
            self.pause_total += pause_time
            self.paused = False

    def exithandle(self):
        if self.paused == True:
            pause_time = datetime.now() - self.pause_start
            self.pause_total += pause_time
        self.totaltime = datetime.now() - self.starttime - self.pause_total
        data_to_json = {"username":"main", "starttime":str(self.starttime), "worktime":str(self.totaltime)}
        api_data_dump(data_to_json)
        print (str(self.totaltime))
        exit(0)


    def eventhandle(self, input):

        if input == "E":
            self.exithandle()
        if input == "P":
            self.pausehandle()
            
if __name__ == "__main__":

    timer = Timer()


    api_data_dump({"test_data":"test data"}, runtime_test=True)
    
    print ("You have started at {}".format(maketimenice(datetime.now())))
    
    while True:
        user_choice = inputhandler(timer.events, "Input 'P' to pause/unpause or 'E' to exit and save")
        timer.eventhandle(user_choice)
    