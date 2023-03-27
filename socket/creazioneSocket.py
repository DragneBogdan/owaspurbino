# creazione della socket 

# imports
import socket
import sys
import requests
import time 
import threading 
from threading import Lock

# variabile globale che identifica il numero di risposte 200
richiesteOk = 0

# numero di richieste re-inviate 
richiesteReinviate = 0

# variabile che memorizza gli status complessivi 200
totaleOk = 0

# costante e variabile temporale 
val_default = 0.10 # ogni 100 mili sec 
time_To_sleep = val_default

# def di thread - cosa fa il thread 
def ex_thread():
    
    # variabile globale
    global richiesteOk
    global richiesteReinviate
    
    # creo un lock
    lock = Lock()
    
    try:
        lock.acquire()
        
        # faccio una richiesta
        print("Sending request...")
        r = requests.get("http://localhost/wordpress")
        
        # se il server non risponde
        if r.status_code != 200:
      
            # decremento il valore delle richieste
            richiesteOk -= 1
            
            # dormo relativamente poco e rifaccio la richiesta 
            time.sleep(0.1)
            rs = requests.get("http://localhost/wordpress")
            
            if rs.status_code == 200:
               richiesteOk += 1
               richiesteReinviate += 1
        else:
        # incremento il valore delle richieste
            richiesteOk += 1
    finally:
        lock.release()
    
# COMANDO 
def comando(cmd):
    
    global richiesteOk
    
    while True:
        comando = input("-> ")
        if comando == "exit":
            print("Disconnessione in corso...")
            cmd.close()
            time.sleep(0.2)
            sys.exit() 
            
        # se il comando è go acquisisco i nuovamente i valori 
        if comando == "go":
            
            # reset dei valori 
            richiesteOk = 0
            partenza_Thread(cmd)
        
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
    
def partenza_Thread(s):
    try:
        
        # acquisizione del numero di richieste
        acquisizione = input("Inserire il numero di richieste: ")
        n_THREAD = int(acquisizione)
        
    except:
        print("Inserire valori coerenti!")   
        sys.exit
    
    # array di thread che effettuano la richiesta
    threads = []

    # verifico quanto tempo ci impiegano per terminare 
    start = time.time()
    
    # il ciclo for inserisce i thread nell'array e li fa partire
    for x in range(0,n_THREAD):
        
        t = threading.Thread(target = ex_thread)

        # aggiungo il thread
        threads.append(t)
        
        # avvio il thread
        t.start()
        
        # tempo di attesa 
        # time.sleep(time_To_sleep)
        
    # verifico com è la situazione 
    totaleOk = richiesteOk + richiesteReinviate
        
    # se il totale è un certo valore v -> se è piccolo la simulazione termina se è grande
    # allora conviene provare con un intervallo più ristretto cioè sempre lo stesso numero 
    # di thread ma con un intervallo più piccolo
        
    # mi metto in attesa della loro terminazione 
    for th in threads:
        th.join()
      
    # stop timer  
    stop = time.time()
    
    # messaggio
    print("Richieste andate a buon fine: ",richiesteOk)
    print("Richieste re-inviate: ", richiesteReinviate)
    print("Tempo impiegato: ",(stop - start))
        
    # ritorno ad acquisire il comando
    comando(s)
        
# esecuzione passando il mio indirizzo locale
if __name__ == "__main__":
    print("")
    print("Comandi:")
    print("--------")
    print("")
    print("'go': per avviare il programma")
    print("'exit': per uscire")
    print("")
    connessione_server(("localhost",80))
    
# STAMPARE REPORT 