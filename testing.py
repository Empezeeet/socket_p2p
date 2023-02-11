import random
import threading
import time
def waitForInput():
    while True:
        print(input("Enter Message > "))
        time.sleep(0.5)

def printOutput():
    while True:
        print(f"\n{random.randint(0, 100)}")
        time.sleep(random.randint(0, 5))


IThread = threading.Thread(target=waitForInput)
OThread = threading.Thread(target=printOutput)
IThread.start()
OThread.start()
