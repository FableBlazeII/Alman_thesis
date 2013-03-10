Programmi testimiseks kasutan Ubuntu Desktop 12.04 LTS 32-bit operatsioonis�steemi.
Tehtud on puhas install VirtuaBoxi virtuaalmasinale.

Repo kloonimiseks kasutasin testimisel programmi Cola Git GUI, mis on saadaval Ubuntu Software Center'i kaudu.

NB!! M�rkused j�rgnevates sammudes toodud k�surea n�itete kohta:
	K�sud on antud ropo juurkaustast (Alman_thesis, ehk siis 'ls' k�sk peaks n�itama kasutasid 'Baaslahendus', 'L6pplahendus' jne)
	K�sud kasutavad ettevalmistatud testandmeid



L�hike testimisjuhend (sh vajalikud moodulid ja installeerimis juhendid ubuntu keskkonnas)
========================
Gitis olevad programmid on seadistatud jooksma kasutas "Testandmed" toodud failidega.

1. Klooni Git repo endale meelep�rase vahendiga (aadress: https://github.com/FableBlazeII/Alman_thesis.git)
2. Ava "Terminal"
3. Navigeeri repo juurkausta (ls n�itab kaustu "Testandmed", "Naiivne_lahendus" jne, edasised k�sud sooritame sealt)
4. Vajadusel muuda j�rgmiste failide �igused (chmod 775 FAILI_NIMI):
		* ./Naiivne_lahendus/createMotifSummary.1.1.py
		* ./Baaslahendus/MotSum_manager.1.0.py
		* ./Baaslahendus/MotSum_submit.1.1.py
		* ./L6pplahendus/MotSum_manager
		* ./L6pplahendus/MotSum_submit
		* ./Testandmed/generateTestData.py
5. K�ivita naiivne lahendus k�suga './Naiivne_lahendus/createMotifSummary.1.1.py -i ./Testandmed/inputSummary.txt -m ./Testandmed/inputRegex.txt -o ./Testandmed/naiveResult.txt --processes 5'

6. Installeeri python-pip (teeb pythoni moodulite installeerimise kergemaks)
		'sudo apt-get install python-pip'
7. Installeeri Pythoni Pyro4 moodul
		'sudo pip install Pyro4'
8. Installeeri python-dev moodul (vajalik j�rgmise sammu �nnestumiseks)
		'sudo apt-get install python-dev'
9. Installeeri Pythoni bitarray 0.8.0 moodul
		'sudo pip install bitarray'
10. K�ivita baaslahenduse manager
		'nohup ./Baaslahendus/MotSum_manager.1.0.py  > ./Baaslahendus/MotSum_manager.log 2>&1&'
		(M�rkus: logifaili tekib hoiatus "HMAC_KEY not set", see hoiatus ei m�juta programmi t��d)
11. Lisa baaslahendusele loendamiseks �ks t��
		'./Baaslahendus/MotSum_submit.1.1.py -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'

12. Installeeri g++
		sudo apt-get install g++
13. Installeeri libsqlite3-dev
		sudo apt-get install libsqlite3-dev
14. Kompileeri programm
		'make -C L6pplahendus/'
		(M�rkus: Suuremahulise koondtabeli korral tuleb muuta faili '.L6pplahendus/Makefile' kolmas rida j�rgmiseks: 'CFLAGS = -O3 -mcmodel=medium', mis n�uab 64-bit operatsioonis�steemi)
15. K�ivita l�pplahenduse manager
		'nohup ./L6pplahendus/MotSum_manager  > ./L6pplahendus/MotSum_manager.log 2>&1&'
16. Lisa l�pplahendusele loendamiseks �ks t��
		'./L6pplahendus/MotSum_submit -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'



Repos olevad programmid on seadistatud jooksma ettevalmistatud testandmetega
J�rgnevad l�igud on toodud juhuks, kui on vajadus programmi kasutada m�ne teise koondtabeliga
Tulevikus on plaanis kasutada koodis olevate muutujate asemel k�surealt antavaid parameetreid
Lisaks v�iks vabaneda nohup k�su kasutamisest (double-fork abil)


Kaust "Testandmed"
========================
Selles kaustas olevad failid ja programmid on loodud testimise lihtsustamise eesm�rgiga peale bakalaureuset�� valmimist.
Programmide puhul ei ole pandud r�hku kasutajamugavusele (parameetrite muutmisel) ega optimiseerimisele.
Programmide v�ljundfailid on l�htekoodis relatiivse failiteega, seega tuleb j�lgida kust neid k�ivitada.

* inputSummary.txt - Programmiga 'generateTestData.py' loodud koondtabel
	10000 s�na
	50 proovi
	sagedused vahemikus 0-500
	enamus sagedustest on nullid

* inputRegex.txt - Programmiga 'generateTestRegex.py' loodud regulaaravaldiste fail
	50 avaldist
	iga avaldis on pikkusega 2-12 t�hem�rki

* generateTestData.py - Pythonis kirjutatud programm, mis loob suvalise koondtabeli testimise jaoks
	programm k�ivitatakse parameetriteta
	v�ljundfail './Testandmed/inputSummary.txt' (l�htekoodis rida 9)
	v�ljundiks oleva koondtabeli muutmiseks tuleb muuta j�rgmiseid ridu l�htekoodis:
		# wordCount (rida 5) - s�nade arv koondtabelis
		# sampleCount (rida 6) - proovide arv koondtabelis
		# countMax (rida 7) - maksimaalne sagedus
	k�ivitada k�suga './Testandmed/generateTestData.py'

* generateTestRegex.py - Pythonis kirjutatud programm, mis loob suvalise regulaaravaldiste faili testimise jaoks
	programm k�ivitatakse parameetriteta
	v�ljundfail './Testandmed/inputRegex.txt'  (l�htekoodis rida 9)
	v�ljundiks oleva regulaaravaldiste muutmiseks tuleb muuta j�rgmiseid ridu l�htekoodis:
		# expressionsCount (rida 5) - regulaaravaldiste arv v�ljundis
		# minLen (rida 6) - minimaalne regulaaravaldise pikkus v�ljundis (vahemikus 1-12)
		# maxLen (rida 7) - maksimaalne regulaaravaldise pikkus v�ljundis (vahemikus 1-12)
	k�ivitada k�suga './Testandmed/generateTestRegex.py'


Kaust "Naiivne_lahendus"
========================
Selles kaustas sisaldub �lesande lahendamiseks loodud esialgne naiivne lahendus.
Testitud Pythoni versioonidega 2.6 ja 2.7 ning ei vaja lisatarkvara installeerimist.

* createMotifSummary.1.1.py - leiab sisendiks antud regulaaravaldiste sagedused igas proovis
	parameetrite kohta saab infot k�suga './Naiivne_lahendus/createMotifSummary.1.1.py -h'
	programm k�ivitab loendamiseks alamprotsesse (vaikimisi 10)
	
	testandmetega loendamise k�ivitamiseks kasutada n�iteks j�rgmist k�sku:
		'./Naiivne_lahendus/createMotifSummary.1.1.py -i ./Testandmed/inputSummary.txt -m ./Testandmed/inputRegex.txt -o ./Testandmed/naiveResult.txt --processes 5'


Kaust "Baaslahendus"
========================
Selles kaustas sisaldub �lesande lahendamiseks Pythonis kirjutatud baaslahendus.
Mitmed baaslahenduse vead on parandamata, kuna otsustasin minna C++ keelele �le.
J�rjekorras saab korraga olla maksimaalselt 1000 t��d (parandamata viga: peale seda hakatakse t��de infot �le kirjutama).
Testitud Pythoni versioonidega 2.6 ja 2.7 ning vajab lisamooduleid Pyro4 ja bitarray 0.8.8

NB! Lahendus tekitab iga loendust�� kohta zombie protsesse, mis p�sivad kuni vastav 'MotSum_manager.1.0.py' protsess on l�ppenud.
NB! Ettevaatust suure m�lukasutusega mahukate koondtabelite korral.

* MotSum_manager.1.0.py - lahenduse keskne komponent
	k�ivitatakse ilma parameetriteta
	peab olema k�ivitatud ja koondabeli laadimise l�petanud, et saaks t�id j�rjekorda lisada
	
	k�ivitamiseks kasutada n�iteks j�rgmist k�sku (logi kirjutatakse faili 'MotSum_manager.log'):
		'nohup ./Baaslahendus/MotSum_manager.1.0.py  > ./Baaslahendus/MotSum_manager.log 2>&1&'
	alternatiivselt v�ib kasutada k�sku (logi ilmub terminali aknasse, Manager v�ljub akna sulgemisel):
		'./Baaslahendus/MotSum_manager.1.0.py'
	
	Vajadusel tuleb muuta l�htekoodis j�rgmised read:
		# maxActiveWorks (rida 11) - Maksimaalne samaaegselt jooksvate t��de arv
		# PepCount (rida 20) - Kasutatavas koondtabelis olevate s�nade (ridade) arv
		# SUMMARY (rida 21) - Kasutatav koondtabel
		# daemon (rida 204) - Pyro4.Daemon(port=X), kus X on suhtluseks kasutatava pordi number
		# uri (rida 205) - daemon.register(manager, "Y"), kus Y on suhtluseks kasutatav objekti nimi
	

* MotSum_submit.1.1.py - programm, mille abil saab kasutaja uusi t�id j�rjekorda lisada
	parameetrite kohta saab infot k�suga './Baaslahendus/MotSum_submit.1.1.py -h'
	k�ivitamiseks kasutada k�sku:
		'./Baaslahendus/MotSum_submit.1.1.py -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'
	
	Vajadusel tuleb muuta l�htekoodis j�rgmised read:
		# motifCountManager (rida 35) - Pyro4.Proxy('PYRO:Y@localhost:X'), kus Y on suhtluseks kasutatav objekti nimi ja X on suhtluseks kasutatava pordi number

* MotSum_worker.py - loendamist teostav komponent
	manager kasutab seda faili kui �hte moodulit
	
	Vajadusel tuleb muuta l�htekoodis j�rgmised read:
		MAX_PROCESSES (rida 5) - Maksimaalne alamprotsesside arv loendust�� kohta
		sampleCount (rida 6) - Proovide arv koondtabelis



Kaust "L6pplahendus"
========================
Selles kaustas sisaldub �lesande lahendamiseks C++ keeles kirjutatud l�pplik lahendus.
Makefile eeldab g++ kompilaatori olemasolu
Vajab Linuxi lisapaketti libsqlite3-dev

* Makefile - kompileerimist lihtsustav fail, mis lubab 'make' kasutamist
	v�ga mahukate koondtabelite puhul tuleb muuta kolmas rida j�rgmiseks: 'CFLAGS = -O3 -mcmodel=medium', mis n�uab 64-bit operatsioonis�steemi
	'make clean' kustutab vajadusel kompileeritud failid (andmebaasi faili ei kustutata)

* MotSum_manager.cpp - manageri komponendi l�htekood
	k�ivitatakse ilma parameetriteta
	t�id saab lisada kohe kui andmebaas on loodud (koondtabel ei pea olema veel m�llu laetud)
	
	k�ivitamiseks kasutada n�iteks j�rgmist k�sku (logi kirjutatakse faili 'MotSum_manager.log'):
		'nohup ./L6pplahendus/MotSum_manager  > ./L6pplahendus/MotSum_manager.log 2>&1&'
	alternatiivselt v�ib kasutada k�sku (logi ilmub terminali aknasse, Manager v�ljub akna sulgemisel):
		'/L6pplahendus/MotSum_manager'
	
	Vajadusel tuleb muuta l�htekoodis j�rgmised read:
		# pepCount (rida 13) - Kasutatavas koondtabelis olevate s�nade (ridade) arv
		# sampleCount (rida 14) - Proovide arv koondtabelis
		# worksLimit (rida 15) - Maksimaalne samaaegselt jooksvate t��de arv
		# processesLimit (rida 16) - Maksimaalne alamprotsesside arv loendust�� kohta
		# ifstream (rida 275) - ifstream BS ("X"), kus X on kasutatava koondtabeli asukoht

* MotSum_submitter.cpp - submitteri komponendi l�htekood
	parameetrite kohta saab infot k�suga './L6pplahendus/MotSum_submit -h'
	k�ivitamiseks kasutada k�sku:
		'./L6pplahendus/MotSum_submit -m ./Testandmed/inputRegex.txt -o ./Testandmed/baseResult.txt'