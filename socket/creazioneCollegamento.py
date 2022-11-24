# creazione del collegamento tra la socket e la porta

# imports
import socket
import sys
import requests

# richiesta al server 
def richiesta():
    r = requests.get("http://localhost/wordpress")
    print("Esito:",r.status_code)
       
def sub_server(indirizzo): # connessioni ammesse
    try:
        s = socket.socket()
        s.bind(indirizzo)   # collegamento vero e proprio
        s.listen()
        print("Server inizializzato correttamente")
        richiesta()
    
    except socket.error as errore:
        print("Server non inizializzato")
        print()
        sys.exit()
            
if __name__ == "__main__":
    sub_server(("",8080))
    
    