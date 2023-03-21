import time 

# avvio il tempo 
start = time.perf_counter()

def myFunction():
    print("Sto dormendo...")
    time.sleep(1)
    print("Mi sono svegliato")
    
# invocandola 2 volte dorme risveglia poi torna a dormire...
myFunction()
myFunction()

# stop 
finish = time.perf_counter()
