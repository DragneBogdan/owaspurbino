# creazione della socket 

# imports
import socket
import sys
import requests
import time 
import threading 
from threading import Lock

# ---------------------------- 
# Variabili Globali per le richieste

inputRichieste = 0      # variabile che memorizza il numero di richieste preso in input dall'utente
richiesteOk = 0         # variabile che memorizza il numero di risposte con status 200
richiesteReinviate = 0  # variabile che memorizza il numero di richieste re-inviate 
totaleOk = 0            # variabile che memorizza la somma tra quelle re-inviate (con status 200) e le richiesteOk
durataSimulazione = 0   # variabile che memorizza la durata intera della simulazione

# -----------------------------
# Variabili Globali per l'intervallo tra una richiesta e l'altra
 
# time_To_sleep = 0.10     # variabile sulla quale si agisce per diminuire l'intervallo

# Funzione che definisce come si interfaccia il programma all'utente
def acquisizione_Comando():
    
    # serve per resettare il numero di richieste
    global inputRichieste 
    
    while True:
        comando = input("-> ")
        if comando == "exit":
            print("Disconnessione in corso...")
            time.sleep(0.2)
            sys.exit() 
            
        # se il comando è go acquisisco il programma va in esecuzione
        if comando == "go":
            inputRichieste = 0
            acquisizione_Richieste()
            
# Funzione che definisce il comportamento di un thread
def ex_thread():
    
    # variabili globali utilizzate 
    global richiesteOk
    global richiesteReinviate
    
    # creo un lock
    lock = Lock()
    
    try:
        # acquisizione del lock devo essere in mutua esclusione poichè agisco su variabili condivise
        lock.acquire()
    
        r = requests.get("http://localhost/wordpress")
        
        # incremento le richieste considerandola 200
        richiesteOk += 1
        
        # se il server non risponde e restituisce 500
        if r.status_code != 200:
      
            # decremento il valore delle richieste precedentemente incrementato
            richiesteOk -= 1
            
            # dormo relativamente poco e provo a rifare la richiesta
            time.sleep(0.1)
            rs = requests.get("http://localhost/wordpress")
            
            # se lo status è 200 incremento il contatore altrimenti rimane quello che e'
            if rs.status_code == 200:
                
               # aggiorno le richieste re-inviate 
               richiesteReinviate += 1
    finally:
        lock.release()
            
# Funzione che definisce la connessione al server
# Prima si crea la socket e si tenta la connessione, se è stabilita continua l'esecuzione
# altrimenti il programma termina con un messaggio d'errore
def connessione_server(indirizzo_server):
    
    try:
        # creazione socket
        s = socket.socket()
        s.connect(indirizzo_server)
        print(f"Connessione al server {indirizzo_server} stabilita")

        # continua l'esecuzione con l'acquisizione delle richieste
        acquisizione_Comando()
    except socket.error as errore:
        print(f"Connessione al server non riuscita")
        
        # esco 
        sys.exit()
    
# Funzione che definisce i thread che effettuano la richiesta
def acquisizione_Richieste():
    
    # variabile globale che memorizza il valore in input dell'utente
    global inputRichieste
    
    try:            
        # acquisizione del numero di richieste
        acquisizione = input("Inserire il numero di richieste da effettuare: ")
        
        # salvo il valore
        inputRichieste = int(acquisizione)
        
        # posso far partire i thread
        partenza_Thread()
    
    except:
        
        # faccio reinseire i valori 
        
        if acquisizione == "exit":
            sys.exit()
        else:
            print("Inserire valori coerenti oppure 'exit' per uscire")   
            print("")
            acquisizione_Richieste()

# Funzione che calcola le richieste con esito 200
def calcola_Richieste():
    
    # variabili globali utili a calcolare le prestazioni 
    global totaleOk, richiesteOk, inputRichieste, durataSimulazione, richiesteReinviate
    
    # calcolo il coeff.
    coef = ((richiesteOk + richiesteReinviate) / inputRichieste)
    
    # se il coef è maggiore rispetto al valore soglia posso invocare nuovamente i thread
    if coef >= 0.99:
        messaggio_Richieste()
        
        # setto a 0 le risposte ok dato che si ricomincia 
        richiesteOk = 0
        
        # raddoppio il numero di richieste 
        inputRichieste *= 2
        
        print("Nuove richieste da effettuare: ", inputRichieste)
        
        # tempo di attesa tra una richiesta e l'altra
        # time.sleep(time_To_sleep)
        
        # invoca nuovamente i thread 
        partenza_Thread()
        
    # se il coef. è inferiore al valore soglia la simulazione termina per evitare di mandare in crash il server 
    else: 
       messaggio_Richieste()
       print("Tempo di durata della simulazione: ", durataSimulazione)
       print("SIMULAZIONE TERMINATA")
    
def messaggio_Richieste():
    print("Richieste con successo: ", richiesteOk + richiesteReinviate)
    print("Rapporto richieste avvenute/richieste effettuate: ", ((richiesteOk + richiesteReinviate)/ inputRichieste))
    print("")
        
# Funzione che definisce la partenza dei thread in un ciclo 
def partenza_Thread():
    
    # calcolo le richieste
    global  inputRichieste, durataSimulazione
    
    # array di thread 
    threads = []
    
    # partenza del timer
    start = time.time()
            
     # faccio una richiesta
    print("Invio delle richieste in corso...")
    print("")
        
    # il ciclo for inserisce i thread nell'array e li fa partire
    for x in range(0,inputRichieste):
        
        # inizializzare i thread che andranno ad invocare la funzione che li definisce
        t = threading.Thread(target = ex_thread)

        # aggiungo il thread
        threads.append(t)
        
        # avvio i thread
        t.start()
        
    # mi metto in attesa della terminazione dei thread
    for th in threads:
        th.join()
      
    # stop timer - i thread sono finiti 
    stop = time.time()
    
    durataSimulazione += (stop - start)
    
    # valutazione delle prestazioni 
    calcola_Richieste()
    
def istruzioni():
    print("")
    print("--- TESTA LA TUA APPLICAZIONE ---")
    print("'go' per avviare la simulazione")
    print("'exit' per uscire dalla simulazione")
    print("")
    
# MAIN
if __name__ == "__main__":
    istruzioni()
    connessione_server(("localhost",80))
    