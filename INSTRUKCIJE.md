## Ubuntu
1. Instalacija Ubuntu: 
-	Win key + R 
-	u „Pokreni“ prozoru upišemo optionalfeatures.exe
-	U „Uključivanju i isključivanju značajki sustava Windows“ pronađemo i uključimo „Podsustav Windows za Linux“ („Windows Subsystems for Linux“)
-	Kliknemo OK
-	 Instaliramo Ubuntu sa Windows Store-a ili sa browsera
-	Ponovno pokrenemo računalo
2. Instalacija Apache Airflowa u Ubuntu CLI
-	U Ubuntu CLI okruženju unesemo komandu „Sudo apt-get install software-properties-common“ koja nam omogućuje da instaliramo paket „software-properties-common“ za upravljanje repozitorija softvera kao i dodavanjem novih repozitorija
-	Unosimo komandu za dodavanje repozitorija universe, „Sudo apt-add-repository universe“
-	Te ažuriramo pakete repozitorija sa komandom – „Sudo apt-get update“
-	Nakon toga instaliramo python package manager (pip) sa komandom „sudo apt-get install python3-pip“
-	Sada napokon možemo instalirati Apache airflow sa komandom „pip install 'apache-airflow[amazon]'
-	Incijaliziramo bazu podataka sa komndom „airflow db init“
-	Pokrenemo webserver sa komandom „airflow webserver“ koja nam pokreće web server na portu 8080
-	Za kreiranje administratora za Airflow koristimo sljedeću naredbu „airflow users create \ --username admin \ --password xxxx \ --firstname admin \ --lastname admin \ --role Admin \ --email xxx@email.com“
-	Putem naredbe „cd airflow“ i nakon naredbe „nano airflow.cfg“ možete postaviti željenu DAG mapu pod imenom dags_folder = „putanja dag direktorija“, ili je ostavite kakva je pa u taj direktorij postaviti svoje DAG python skripe
-	Nakon postavljenog DAG direktorija i DAG skripte unutar direktorija možemo ugasiti webserver, ponovno inicijalizirati bazu podataka sa naredbom „airflow db init“ i naredbom „airflow webserver“ naš DAG bi trebao biti vidljiv na Airflow UI-u koji se nalazi na localhost/8080
3. Kreiranje i pokretanje skripte DAGA u Ubuntu CLI
- Alternativa postavljanju skripte unutar DAG direktorija bi bila kreiranje python skripte unutar Ubuntu CLI-a.
- Putem naredbe „cd airflow“ stižemo u airflow direktorij gdje bi se trebao nalaziti DAG direktorij. Ako se ne nalazi unutar airflow direktorija možemo ga kreirati naredbom „mkdir DAG“. 
- Unutar DAG direktorija kreiramo python skriptu „vim <naziv_skripte.py> i zatim uređujemo našu python skriptu unutar Ubuntu CLI-a, prije toga trebamo pritisnuti tipku „I“ za uređivanje skripte.
- Nakon što smo je uredili pritisnemo esc tipku i upižemo „:wq“ kako bi izašli i spremili promjene
- Sada pokrenemo naš airflow webserver i u novom Ubuntu terminalu navigiramo do DAG direktorija gdje se nalazi naša python DAG skripta i unesemo naredbu „Airflow test tasks <id_daga> <task_uploada> i naš DAG se pokreće
- Pripazite u pisanju koda na ispravljanje putanje datoteka da budu prilagođene za Linux sustave. Recimo umjesto C:/put_do_datoteke treba pisati /mnt/c/put_do_datoteke. 
## Konfiguracija S3 bucketa

1. Napravite S3 bucket:
-	Idite na AWS upravljačku konzolu i idite na S3.
-	Kliknite na "Create bucket" i navedite jedinstveni naziv za svoju kantu.
-	Ostale opcije ostavite kao zadane i stvorite kantu.


2. Stvorite AWS pristupne ključeve:
-	U AWS konzoli za upravljanje idite na sigurnosne ključeve vašeg korisnika.
-	Pod "Pristupni ključevi", kliknite na "Stvori novi pristupni ključ" i zabilježite ID pristupnog ključa i tajni pristupni ključ.

3. Postavite vezu na Airflow-u:
-	Otvorite Airflow UI i idite na Administrator -> Veze.
-	Kliknite na gumb "+" za stvaranje nove veze.
-	Postavite ID veze na „s3_conn“.
-	Postavite vrstu veze na "Amazon Web Services".
-	Zamijenite „YOUR_ACCESS_KEY_ID“ i „YOUR_SECRET_ACCESS_KEY“ odgovarajućim ključevima iz vaših AWS pristupnih ključeva



## Objašnjenje DAG skripte
- Uvoz potrebnih modula: Uvezeni su potrebni Python moduli kao što su datetime, DAG, PythonOperator, S3Hook, pandas i matplotlib.pyplot.

- upload_to_s3 Funkcija: Ova funkcija upravlja učitavanjem datoteka u Amazon S3 spremnik. Koristi klasu S3Hook za uspostavljanje veze i učitava datoteke navedene u popisu putova datoteka s odgovarajućim ključevima S3 s popisa ključeva.

-analiza Funkcija: Ova funkcija izvodi analizu skupa podataka glazbene ankete. Čita skup podataka s navedene lokacije datoteke, grupira podatke prema omiljenom žanru, izračunava srednje rezultate i rezultate standardne devijacije i generira vizualizacije trakastog grafikona pomoću matplotlib.pyplot.

-Konfiguracija DAG-a: DAG se stvara pomoću klase DAG, navodeći ID DAG-a, interval rasporeda i datum početka.

-Definicija zadatka: Zadatak task_upload_to_s3 definiran je kao PythonOperator koji poziva funkciju upload_to_s3 s navedenim argumentima.


