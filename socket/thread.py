import time 
import threading

# avvio il tempo 
start = time.perf_counter()

def myFunction():
    print("Sto dormendo...")
    time.sleep(1)
    print("Mi sono svegliato")

thread1 = threading.Thread(target = myFunction)

# avvio il thread
thread1.start()

# aspetto 3 secondi prima di terminare 
time.sleep(3)

# mi metto in attesa della sua terminazione 
thread1.join()

# stop 
stop = time.perf_counter()

print("Time: ", stop - start)
