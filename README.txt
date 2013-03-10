Programmi testimiseks kasutan Ubuntu Desktop 12.04 LTS 32-bit operatsioonisüsteemi.
Tehtud on puhas install VirtuaBoxi virtuaalmasinale.

Repo kloonimiseks kasutasin testimisel programmi Cola Git GUI, mis on saadaval Ubuntu Software Center'i kaudu.

NB!! Märkused järgnevates sammudes toodud käsurea näitete kohta:
	Käsud on antud ropo juurkaustast (Alman_thesis, ehk siis 'ls' käsk peaks näitama kasutasid 'Baaslahendus', 'L6pplahendus' jne)
	Käsud kasutavad ettevalmistatud testandmeid



Lühike testimisjuhend (sh vajalikud moodulid ja installeerimis juhendid ubuntu keskkonnas)
========================
Gitis olevad programmid on seadistatud jooksma kasutas "Testandmed" toodud failidega.

1. Klooni Git repo endale meelepärase vahendiga (aadress: https://github.com/FableBlazeII/Alman_thesis.git)
2. Ava "Terminal"
3. Navigeeri repo juurkausta (ls näitab kaustu "Testandmed", "Naiivne_lahendus" jne, edasised käsud sooritame sealt)
4. Vajadusel muuda järgmiste failide õigused (chmod 775 FAILI_NIMI):
		* ./Naiivne_lahendus/createMotifSummary.1.1.py
		* ./Baaslahendus/MotSum_manager.1.0.py
		* ./Baaslahendus/MotSum_submit.1.1.py
		* ./L6pplahendus/MotSum_manager
		* ./L6pplahendus/MotSum_submit
		* ./Testandmed/generateTestData.py
5. Käivita naiivne lahendus käsuga './Naiivne_lahendus/createMotifSummary.1.1.py -i ./Testandmed/inputSummary.txt -m ./Testandmed/inputRegex.txt -o ./Testandmed/naiveResult.txt --processes 5'

6. Installeeri python-pip (teeb pythoni moodulite installeerimise kergemaks)
		'sudo apt-get install python-pip'
7. Installeeri Pythoni Pyro4 moodul
		'sudo pip install Pyro4'
8. Installeeri python-dev moodul (vajalik järgmise sammu õnnestumiseks)
		'sudo apt-get install python-dev'
9. Installeeri Pythoni bitarray 0.8.0 moodul
		'sudo pip install bitarray'
10. Käivita baaslahenduse manager
		'nohup ./Baaslahendus/MotSum_manager.1.0.py  > ./Baaslahendus/MotSum_manager.log 2>&1&'
		(Märkus: logifaili tekib hoiatus "HMAC_KEY not set", see hoiatus ei mõjuta programmi tööd)
11. Lisa baaslahendusele loendamiseks üks töö
		'./Baaslahendus/MotSum_submit.1.1.py -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'

12. Installeeri g++
		sudo apt-get install g++
13. Installeeri libsqlite3-dev
		sudo apt-get install libsqlite3-dev
14. Kompileeri programm
		'make -C L6pplahendus/'
		(Märkus: Suuremahulise koondtabeli korral tuleb muuta faili '.L6pplahendus/Makefile' kolmas rida järgmiseks: 'CFLAGS = -O3 -mcmodel=medium', mis nõuab 64-bit operatsioonisüsteemi)
15. Käivita lõpplahenduse manager
		'nohup ./L6pplahendus/MotSum_manager  > ./L6pplahendus/MotSum_manager.log 2>&1&'
16. Lisa lõpplahendusele loendamiseks üks töö
		'./L6pplahendus/MotSum_submit -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'



Repos olevad programmid on seadistatud jooksma ettevalmistatud testandmetega
Järgnevad lõigud on toodud juhuks, kui on vajadus programmi kasutada mõne teise koondtabeliga
Tulevikus on plaanis kasutada koodis olevate muutujate asemel käsurealt antavaid parameetreid
Lisaks võiks vabaneda nohup käsu kasutamisest (double-fork abil)


Kaust "Testandmed"
========================
Selles kaustas olevad failid ja programmid on loodud testimise lihtsustamise eesmärgiga peale bakalaureusetöö valmimist.
Programmide puhul ei ole pandud rõhku kasutajamugavusele (parameetrite muutmisel) ega optimiseerimisele.
Programmide väljundfailid on lähtekoodis relatiivse failiteega, seega tuleb jälgida kust neid käivitada.

* inputSummary.txt - Programmiga 'generateTestData.py' loodud koondtabel
	10000 sõna
	50 proovi
	sagedused vahemikus 0-500
	enamus sagedustest on nullid

* inputRegex.txt - Programmiga 'generateTestRegex.py' loodud regulaaravaldiste fail
	50 avaldist
	iga avaldis on pikkusega 2-12 tähemärki

* generateTestData.py - Pythonis kirjutatud programm, mis loob suvalise koondtabeli testimise jaoks
	programm käivitatakse parameetriteta
	väljundfail './Testandmed/inputSummary.txt' (lähtekoodis rida 9)
	väljundiks oleva koondtabeli muutmiseks tuleb muuta järgmiseid ridu lähtekoodis:
		# wordCount (rida 5) - sõnade arv koondtabelis
		# sampleCount (rida 6) - proovide arv koondtabelis
		# countMax (rida 7) - maksimaalne sagedus
	käivitada käsuga './Testandmed/generateTestData.py'

* generateTestRegex.py - Pythonis kirjutatud programm, mis loob suvalise regulaaravaldiste faili testimise jaoks
	programm käivitatakse parameetriteta
	väljundfail './Testandmed/inputRegex.txt'  (lähtekoodis rida 9)
	väljundiks oleva regulaaravaldiste muutmiseks tuleb muuta järgmiseid ridu lähtekoodis:
		# expressionsCount (rida 5) - regulaaravaldiste arv väljundis
		# minLen (rida 6) - minimaalne regulaaravaldise pikkus väljundis (vahemikus 1-12)
		# maxLen (rida 7) - maksimaalne regulaaravaldise pikkus väljundis (vahemikus 1-12)
	käivitada käsuga './Testandmed/generateTestRegex.py'


Kaust "Naiivne_lahendus"
========================
Selles kaustas sisaldub ülesande lahendamiseks loodud esialgne naiivne lahendus.
Testitud Pythoni versioonidega 2.6 ja 2.7 ning ei vaja lisatarkvara installeerimist.

* createMotifSummary.1.1.py - leiab sisendiks antud regulaaravaldiste sagedused igas proovis
	parameetrite kohta saab infot käsuga './Naiivne_lahendus/createMotifSummary.1.1.py -h'
	programm käivitab loendamiseks alamprotsesse (vaikimisi 10)
	
	testandmetega loendamise käivitamiseks kasutada näiteks järgmist käsku:
		'./Naiivne_lahendus/createMotifSummary.1.1.py -i ./Testandmed/inputSummary.txt -m ./Testandmed/inputRegex.txt -o ./Testandmed/naiveResult.txt --processes 5'


Kaust "Baaslahendus"
========================
Selles kaustas sisaldub ülesande lahendamiseks Pythonis kirjutatud baaslahendus.
Mitmed baaslahenduse vead on parandamata, kuna otsustasin minna C++ keelele üle.
Järjekorras saab korraga olla maksimaalselt 1000 tööd (parandamata viga: peale seda hakatakse tööde infot üle kirjutama).
Testitud Pythoni versioonidega 2.6 ja 2.7 ning vajab lisamooduleid Pyro4 ja bitarray 0.8.8

NB! Lahendus tekitab iga loendustöö kohta zombie protsesse, mis püsivad kuni vastav 'MotSum_manager.1.0.py' protsess on lõppenud.
NB! Ettevaatust suure mälukasutusega mahukate koondtabelite korral.

* MotSum_manager.1.0.py - lahenduse keskne komponent
	käivitatakse ilma parameetriteta
	peab olema käivitatud ja koondabeli laadimise lõpetanud, et saaks töid järjekorda lisada
	
	käivitamiseks kasutada näiteks järgmist käsku (logi kirjutatakse faili 'MotSum_manager.log'):
		'nohup ./Baaslahendus/MotSum_manager.1.0.py  > ./Baaslahendus/MotSum_manager.log 2>&1&'
	alternatiivselt võib kasutada käsku (logi ilmub terminali aknasse, Manager väljub akna sulgemisel):
		'./Baaslahendus/MotSum_manager.1.0.py'
	
	Vajadusel tuleb muuta lähtekoodis järgmised read:
		# maxActiveWorks (rida 11) - Maksimaalne samaaegselt jooksvate tööde arv
		# PepCount (rida 20) - Kasutatavas koondtabelis olevate sõnade (ridade) arv
		# SUMMARY (rida 21) - Kasutatav koondtabel
		# daemon (rida 204) - Pyro4.Daemon(port=X), kus X on suhtluseks kasutatava pordi number
		# uri (rida 205) - daemon.register(manager, "Y"), kus Y on suhtluseks kasutatav objekti nimi
	

* MotSum_submit.1.1.py - programm, mille abil saab kasutaja uusi töid järjekorda lisada
	parameetrite kohta saab infot käsuga './Baaslahendus/MotSum_submit.1.1.py -h'
	käivitamiseks kasutada käsku:
		'./Baaslahendus/MotSum_submit.1.1.py -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'
	
	Vajadusel tuleb muuta lähtekoodis järgmised read:
		# motifCountManager (rida 35) - Pyro4.Proxy('PYRO:Y@localhost:X'), kus Y on suhtluseks kasutatav objekti nimi ja X on suhtluseks kasutatava pordi number

* MotSum_worker.py - loendamist teostav komponent
	manager kasutab seda faili kui ühte moodulit
	
	Vajadusel tuleb muuta lähtekoodis järgmised read:
		MAX_PROCESSES (rida 5) - Maksimaalne alamprotsesside arv loendustöö kohta
		sampleCount (rida 6) - Proovide arv koondtabelis



Kaust "L6pplahendus"
========================
Selles kaustas sisaldub ülesande lahendamiseks C++ keeles kirjutatud lõpplik lahendus.
Makefile eeldab g++ kompilaatori olemasolu
Vajab Linuxi lisapaketti libsqlite3-dev

* Makefile - kompileerimist lihtsustav fail, mis lubab 'make' kasutamist
	väga mahukate koondtabelite puhul tuleb muuta kolmas rida järgmiseks: 'CFLAGS = -O3 -mcmodel=medium', mis nõuab 64-bit operatsioonisüsteemi
	'make clean' kustutab vajadusel kompileeritud failid (andmebaasi faili ei kustutata)

* MotSum_manager.cpp - manageri komponendi lähtekood
	käivitatakse ilma parameetriteta
	töid saab lisada kohe kui andmebaas on loodud (koondtabel ei pea olema veel mällu laetud)
	
	käivitamiseks kasutada näiteks järgmist käsku (logi kirjutatakse faili 'MotSum_manager.log'):
		'nohup ./L6pplahendus/MotSum_manager  > ./L6pplahendus/MotSum_manager.log 2>&1&'
	alternatiivselt võib kasutada käsku (logi ilmub terminali aknasse, Manager väljub akna sulgemisel):
		'/L6pplahendus/MotSum_manager'
	
	Vajadusel tuleb muuta lähtekoodis järgmised read:
		# pepCount (rida 13) - Kasutatavas koondtabelis olevate sõnade (ridade) arv
		# sampleCount (rida 14) - Proovide arv koondtabelis
		# worksLimit (rida 15) - Maksimaalne samaaegselt jooksvate tööde arv
		# processesLimit (rida 16) - Maksimaalne alamprotsesside arv loendustöö kohta
		# ifstream (rida 275) - ifstream BS ("X"), kus X on kasutatava koondtabeli asukoht

* MotSum_submitter.cpp - submitteri komponendi lähtekood
	parameetrite kohta saab infot käsuga './L6pplahendus/MotSum_submit -h'
	käivitamiseks kasutada käsku:
		'./L6pplahendus/MotSum_submit -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'