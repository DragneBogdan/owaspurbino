# creazione della socket 

# imports
import socket
import sys
import requests
import time 
from time import perf_counter
import threading 

# def di thread - cosa fa il thread 
def ex_thread():
    
    # il thread invoca per un certo numero di volte il metodo per fare richiesta
    print("Processing...")
    for i in range(1,10):
        richiesta()
        
# richiesta al server 
def richiesta():

    r = requests.get("http://localhost/wordpress")
           
def comando(s):
    while True:
        comando = input("-> ")
        if comando == "exit":
            print("Disconnessione in corso...")
            s.close()
            time.sleep(2)
            sys.exit()
        
def connessione_server(indirizzo_server):
    try:
        s = socket.socket() # creazione socket
        s.connect(indirizzo_server)
        print(f"Connessione al server {indirizzo_server} stabilita")
       
    except socket.error as errore:
        print(f"Connessione al server non riuscita")
        
        # esco 
        sys.exit()
    
    threads = []
    for x in range(1,3):
        t = threading.Thread(target = ex_thread)
        
        # aggiungo il thread
        threads.append(t)
        
        # avvio il thread
        t.start()
        
    # mi metto in attesa della loro terminazione 
    for th in threads:
        th.join()
    
    # messaggio 
    comando(s)
    
# esecuzione passando il mio indirizzo locale
if __name__ == "__main__":
    connessione_server(("localhost",80))
    