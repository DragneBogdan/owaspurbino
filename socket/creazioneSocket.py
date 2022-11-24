# creazione della socket 

# imports
import socket
import sys
import requests

# richiesta al server 
def richiesta():
    r = requests.get("http://localhost/wordpress")
    print("Esito:",r.status_code)

def comando(s):
    while True:
        comando = input("-> ")
        if comando == "exit":
            print("Disconnessione in corso...")
            s.close()
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
    
    # faccio una richiesta al server
    richiesta() 
    
    # messaggio 
    comando(s)
    
# esecuzione passando il mio indirizzo locale
if __name__ == "__main__":
    connessione_server(("192.168.1.51",80))
    