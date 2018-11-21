# Attacco al decryption exponent in RSA

Implementazione dell'attacco al decryption exponent in RSA mediante l'algoritmo probabilsitico di tipo Las Vegas.

Esercizio di programmazione 3.2 per il Corso Data Security and Privacy - Set 3

# Come Utilizzarlo

Il codice sviluppato per questo programma richiede il file RSA.py, ovvero il file python contenente il codice per
l'esercizio 3.1 di programmazione del Set 3, tale file viene reso già disponibile nella cartella del progetto, quindi
non è neccessario eseguire nessun tipo di azione.
Per testare il codice è sufficente avviare tramite un interprete python il file decryption_exponent_attack.py

# Come Funziona

Una volta avviato, il programma stampa a video un piccolo menù dove vengono indicate le tre possibili funzioni che
l'utente può eseguire. L'utente può eseguire una funzione semplicemete inserendo nella console il numero relativo alla
funzione scelta. Di seguito viene riportata una breve descrizione delle tre funzioni e cosa richiedono in input.

1. Execute Decryption Exponent Attack.
   Funzione che consente di eseguire l'algoritmo dell'attacco al decryption exponent in RSA.
   - All'utente viene richiesto di inserire il modulo n, l'esponente privato d e l'esponente pubblico e sui cu basare
     l'attacco. Si assume che l'esponente e sia fornito dall'utente.
   - La funzione restituisce un fattore non banale di n e il numero totale di iterazioni impiegate dall'algoritmo.
2. Test Decryption Exponent Attack.
   Funzione che consente all'utente di testare le prestazioni dell'algoritmo per l'attacco al decryption exponent in
   RSA basandosi sulla generazione casuale di i moduli RSA realistici con k bits e usando il modulo RSA.py sviluppato
   per l'es. 3.1.
   - All'utente viene richiesta la dimensione in bits k dei moduli RSA che verranno generati casualmente durante
     il test e il numero di iterazioni totali i del test (numero totale di moduli RSA da testare).
   - La funzione restituisce il numero medio di iterazione dell'algoritmo di attacco, il tempo medio di esecuzione
     dell'attacco (in secondi) e la varianza di tale tempo.
3. Quit.
   Funzione che consente la chiusura del programmma.

# Test di Esempio Effettuato

Per eseguire un test realistico con numeri di dimensione > 10^100 ho deciso di far generare casualmente al programma 100
moduli RSA formati da 1024 bit.

I risultati ottenuti sono i seguenti:

- Test Results -
Average Algorithm Iterations: 1.41
Average Execution Time: 0.037960051671092725 seconds
Variance of Execution Time: 0.0003401957817046251 seconds^2

Possiamo dunque notare come l'algoritmo sia molto efficente nel trovare un fattore non banale del modulo RSA n se si
conosce l'esponente privato d, riuscendo a mantenere sempre un numero di iterazaioni medio minore o uguale a 2. Nel
nostro test abbiamo ottenuto un numero medio di iteraioni pari a 1.41 ma anche effettuando altri test con moduli di
dimensione diversa si ottiene sempre un numero medio di iterazioni minore o uguale a 2 (in generale vicino a 1.4 o 1.3).

# Author
Elia Mercatanti