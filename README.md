# Progetto per il corso di Reti di Calcolatori 2023

## Tool per testare le vulnerabilità di una Web App

### OWASP 
L'idea di progetto si basa sulla politica di OWASP che mette a disposizione un insieme di tool per testare le vulnerabilità delle proprie applicazioni web. 

### OWASP Urbino 
#### Tecnologie usate
1. XAMPP: per avere la disponibilità di un'application server e un DB; 
2. Wordpress: per la creazione di un sito sul quale simulare gli attacchi.
La simulazione quindi si concentra sulla stessa macchina che svolge il ruolo di client - server (auto - attacco).

### Istruzioni d'uso
Per utilizzare il tool è sufficiente inserire la chiave di avvio 'go' altrimenti 'exit' per terminare la simulazione. Il programma prende in input il numero di richieste da effettuare (> 0) altrimenti viene generato un messaggio d'errore e viene richiesto il reinserimento. 

### L'algoritmo 

#### Input
All'avvio del programma, si tenta di effettuare la connessione al server, in questo caso la porta corrispondendte è la PORTA 80 ovvero la porta dedicata al server Web (HTTP).
Se la connessione al server non è riuscita allora l'esecuzione termina altrimenti prosegue in attesa della parola chiave "go" per avviare le richieste altrimenti "exit" per uscire dal programma.
Quando il programma richiede il numero di richieste da effettuare si aspetta un numero intero - positivo altrimenti chiede il reinserimento oppure "exit" per uscire.
Supponiamo che l'utente abbia inserito un valore coerente con quanto richiesto dal programma, questo non fa altro che generare un numero di THREAD quante sono le richieste inserite dall'utente.

#### Comportamento dei Thread
Una volta che i Thread sono pariti iniziano ad effettuare richieste al server.
All'interno della funzione che definisce il comportamento dei Thread (ex_thread()) si hanno due variabili globali: richiesteOK e richiesteReinviate. La prima variabile viene incrementata dal Thread in questione poi viene fatto un controllo sull'esito della richiesta. Se il server ha risposto con un esito diverso da 200 (cioè non è andata a buon fine), la variabile viene decrementata e attende un lasso di tempo molto piccolo (0.1s) per effettuare nuovamente la richiesta. Nel caso in cui questa volta il server ha risposto, viene incrementa la seconda variabile globale che memorizza le richieste reinviate.
Tutte queste operazioni si svolgono in MUTUA ESCLUSIONE mediante l'utilizzo dei semafori binari (MUTEX).

#### Valutazione delle risposte 
Quando i Thread sono finiti viene invocata una funzione (calcola_Richieste()) che valuta il rapporto tra le richieste andate a buon fine (somma delle due variabili globali sopra menzionate) e quelle prese in input.
Se questo rapporto è maggiore o uguale a 0.99 significa che il server ha risposto bene e quindi il programma riparte raddoppiando il numero delle richieste inizialmente prese in input.

NOTA: Per essere più coerenti con l'esecuzione, in realtà bisognerebbe aspettare un lasso di tempo più o meno lungo in modo da dare la possibilità al Sistema Operativo di effettuare lo SWAP e aggiornare la tabella delle pagine per quanto riguarda la memoria. Ma nella simulazione si dà per assodato che le prestazioni del server siano di gran lunga superiori alla macchina sulla quale sono stati effettuati i test. 

#### Output
Se il rapporto tra le richieste avvenute e quelle richieste è minore di 0.99 allora il programma termina e stampa a video la durata della simulazione.
(Il timer è stato inizializzato all'avvio dei thread e fermato al termine dell'esecuzione dei thread).



