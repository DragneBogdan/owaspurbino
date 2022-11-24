# creazione della socket 

# imports
import socket
import sys

def messaggio(s):
    while True:
        comando = input("-> ")
        if comando == "exit":
            print("Connessione in corso...")
            s.close()
            sys.exit()
        
        else:
            s.send(comando.encode())
            data = s.recv(4096) # dimensione del buffer
            print(str(data,"utf-8"))
    
def connessione_server(indirizzo_server):
    try:
        s = socket.socket() # creazione socket
        s.connect(indirizzo_server)
        print(f"Connessione al server {indirizzo_server} stabilita")
        
    except socket.error as errore:
        print(f"Connessione al server non riuscita")
        
        # esco 
        sys.exit()
        
    # messaggio d'errore
    messaggio(s)
    
# esecuzione passando il mio indirizzo locale
if __name__ == "__main__":
    connessione_server(("192.168.1.51",80))
    