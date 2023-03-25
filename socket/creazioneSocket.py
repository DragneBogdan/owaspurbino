# creazione della socket 

# imports
import socket
import sys
import requests
import time 
from time import perf_counter
import threading 
from threading import Lock
 
# def di thread - cosa fa il thread 
def ex_thread():
    
    # il thread invoca per un certo numero di volte il metodo per fare richiesta
    lock = Lock()
    
    try:
        # acquisisco il lock 
        lock.acquire()
        
        # calcolo il tempo 
    
        print("Processing...")
        r = requests.get("http://localhost/wordpress")
        
    finally:
        # rilascio il lock 
        lock.release()
          
# COMANDO 
def comando(cmd):
    while True:
        comando = input("-> ")
        if comando == "exit":
            print("Disconnessione in corso...")
            cmd.close()
            time.sleep(0.2)
            sys.exit() 
            
        # se il comando è go acquisisco i nuovamente i valori 
        if comando == "go":
            acquisizione(cmd)
        
def connessione_server(indirizzo_server):
    try:
        
        # creazione socket
        s = socket.socket()
        s.connect(indirizzo_server)
        print(f"Connessione al server {indirizzo_server} stabilita")

        # posso acquisire i valori
        comando(s)
    except socket.error as errore:
        print(f"Connessione al server non riuscita")
        
        # esco 
        sys.exit()
    
def acquisizione(s):
    try:
        
        # acquisizione del numero di richieste
        acquisizione = input("Inserire il numero di richieste: ")
        n_THREAD = int(acquisizione)
        
        # acquisizione dell'intervallo di tempo 
        acq_Time = input("Inserire l'intervallo di tempo(nel formato 0.#): ")
        time_To_sleep = float(acq_Time)
        
    except:
        print("Inserire valori coerenti!")   
        sys.exit
    
    # array di thread che effettuano la richiesta
    threads = []
    i = 0
    
    # il ciclo for inserisce i thread nell'array e li fa partire
    for x in range(0,n_THREAD):
        t = threading.Thread(target = ex_thread)
        
        # aggiungo il thread
        threads.append(t)
        
        # avvio il thread
        t.start()
        
        # incremento il numero di richieste 
        i += 1
        print("Richieste: ", i)
        
        # prima di fare un'altra richiesta attende un certo t
        time.sleep(time_To_sleep)
        
    # verifico quanto tempo ci impiegano per terminare 
    start = perf_counter()
    
    # mi metto in attesa della loro terminazione 
    for th in threads:
        th.join()
        
    stop = perf_counter()
    
    print("Tempo impiegato: ",(stop - start))
        
    # ritorno ad acquisire il comando
    comando(s)
        
# esecuzione passando il mio indirizzo locale
if __name__ == "__main__":
    print("")
    print("Comandi:")
    print("--------")
    print("Go: per avviare il programma")
    print("exit: per uscire")
    print("")
    connessione_server(("localhost",80))
    