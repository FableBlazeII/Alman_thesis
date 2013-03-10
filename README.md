NB! Täpsem info ja testimisjuhend failis README.txt!



Alman_thesis
============

Piiratud võimsusega regulaaravaldistele sobituave sõnade leidmine


Repositoorium sisaldab Anti Almani bakalaureusetöö käigus välja arendatud kolme programmi.
Need programmid täidavad sama ülesannet, aga erinevad tugevalt kiiruse poolest. Programmide nõuded on erinevad


Järgnevalt on toodud põgus ülevaade repos olevatest programmidest


Naiivne lahendus
============
* Kirjuatud programeerimiskeeles Python
* Vajab kasutamiseks Pythoni versiooni 2.6+. Ei tööta versioonidel 3.0+
* Programm on testitud vaid Linuxi keskonnas (CentOS release 5.9 (Final))
* Peaks töötama ka Windowsi keskonnas, aga see ei ole garanteeritud

Baaslahendus
============
* Kirjutatud programeerimiskeeles Python
* Vajab kasutamiseks Pythoni versiooni 2.6+. Ei tööta versioonidel 3.0+
* Kasutamiseks tuleb instaleerida Pythoni moodul bitarray 0.8.0 (https://pypi.python.org/pypi/bitarray)
* Kasutamiseks tuleb instaleerida Pythoni moodul Pyro4 ja programmi koodis määrata kasutamiseks sobiv port (https://pypi.python.org/pypi/Pyro4)
* Programm on testitud vaid Linuxi keskonnas (CentOS release 5.9 (Final))
* Ei tööta Windowsi keskonnas kuna kasutab forkimist
* Koondtabeli asukoht, protsesside, samaaegsete tööde, proovide ja koondtabeli ridade arvud on kmanageri koodi siise kirjutatud

Lõpplahendus
============
* Kirjutatud programeerimiskeeles C++
* Programm on testitud vaid Linuxi keskonnas (CentOS release 5.9 (Final))
* Programi kompileerimine on testitud vaid gcc 4.1.2 kompilaatoriga (kaasas on kompileerimiseks Makefile)
* Ei tööta Windowsi keskonnas kuna kasutab forkimist
* Eeldab, et arvutis on instaleeritud sqlite3 andmebaasi tarkvara, selliselt et kompilaator on võimeline selle ülese leidma
* * Koondtabeli asukoht, protsesside, samaaegsete tööde, proovide ja koondtabeli ridade arvud on kmanageri koodi siise kirjutatud
