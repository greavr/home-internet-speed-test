import speedtest
import sqlite3
import threading
import time
import datetime
import logging

import my_db

# App variables:
## Todo move to config
PingFrequency = 1
FullTestFrequency = 10
debug_level = 2

# Counters
PingCount = 0
FullTestCount = 0

# Speed test 
s = speedtest.Speedtest()
s.get_servers()

#Execution Flags
isPing = False
isFull = False

def PingTest():
    s.get_best_server()
    return round(s.results.dict()["ping"],1)

def PingTask():
    # Perform Ping test and save results to local DB
    global PingCount, isPing

    # Check for Gate
    if (not isPing):
        #Enable Gate
        isPing=True

        # Run Tests
        thisResult = PingTest()
        # Save Values to DB
        my_db.SavePing(thisResult)
        PingCount += 1

        # Debug Info
        
        #Disable Gate
        isPing=False
    else:
        logging.debug("Ping Test Already Running")


def FullTest():
    # Function To run full test
    global FullTestCount, isFull

    # Check for Gate
    if (not isFull):
        #Enable Gate
        isFull = True

        my_db.SetNotification("Full Test Running","True")

        # Run Tests
        st = speedtest.Speedtest()
        st.get_servers()
        st.get_best_server()
        st.download()
        st.upload()
        res = st.results.dict()

        # Save Values to DB
        my_db.SaveValue(round(res["download"],2), round(res["upload"],2), round(res["ping"],2))        

        # Debug Info
        logging.debug("Full Test: " + str(datetime.datetime.now()) + ": " + str(res))

        FullTestCount += 1
        my_db.SetNotification("Full Test Running","False")

        #Disable Gate
        isFull = False
    else:
        logging.debug("Full Test Already Running")
    
    
# Function to dump main thread
def PrintInfo():
    print("Home Internet Checker v0.0")
    print("Ping Frequency {0} secs".format(PingFrequency))
    print("Full Test Frequency {0} secs".format(FullTestFrequency))
    print("Target DB: {0}".format(my_db.localDB))


# Main App thread (Tick)
def Main():
    # Thread ticks over with a 1 second delay

    # Used to count
    PingTick = 0
    FullTestTick = 0
    tickCount = 0
    while True:

        # Check if Time To Ping
        if PingTick == PingFrequency:
            PingTask()
            PingTick = 0
        else:
            PingTick += 1

        # Check if Time to do Full Test
        if FullTestTick == FullTestFrequency:
            fulltest_thread = threading.Thread(name='fulltest', target=FullTest())
            fulltest_thread.daemon = True
            fulltest_thread.start()
            FullTestTick = 0
        else:
            FullTestTick += 1


        #Debug check db:
        if __debug__:  
            allResults = my_db.AllPings()
            logging.debug(allResults)
            logging.debug("Tick: " + str(tickCount) )
            logging.debug("Total Pings: {0}, Total Full Tests: {1}".format(str(PingCount),str(FullTestCount)))

        # Keeping Sync
        tickCount += 1


if __name__ == "__main__":
    #Check for debug
    if __debug__:
        print ('Debug ON')
    else:
        print ('Debug OFF')

    # Output info:
    PrintInfo()
    # Required to bootstrap DB
    my_db.CreateConn()

    # Now run Main Thread
    Main()