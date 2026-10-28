# Privacy- en gegevensverklaring

*Laatst bijgewerkt: 28 oktober 2026*

Deze verklaring beschrijft hoe SASTA omgaat met de bestanden die u uploadt, de resultaten die SASTA daaruit genereert, en de gegevens van uw gebruikersaccount. Deze verklaring geldt voor de door de Universiteit Utrecht beheerde installatie op [sasta.hum.uu.nl](https://sasta.hum.uu.nl/). Als u SASTA zelf host, bent u zelf verantwoordelijk voor de gegevens in uw installatie.

## Wie is waarvoor verantwoordelijk?

SASTA wordt ontwikkeld en beheerd door het Research Software Lab van het Centre for Digital Humanities (CDH), Universiteit Utrecht.

- **Accountgegevens**: de Universiteit Utrecht is verantwoordelijk voor de gegevens die nodig zijn om uw account te beheren (zie [Accountgegevens](#accountgegevens)).
- **Geüploade transcripten**: u bent zelf verantwoordelijk voor de transcripten die u uploadt. Dat betekent dat u ervoor zorgt dat u deze gegevens mag verwerken, bijvoorbeeld omdat u toestemming heeft van de spreker(s) of hun wettelijk vertegenwoordiger. SASTA verwerkt deze gegevens uitsluitend om de analyse voor u uit te voeren.

## Welke gegevens slaat SASTA op?

Wanneer u een transcript uploadt, slaat SASTA de volgende gegevens op:

- **Het transcript zelf.** Word-bestanden (`.docx`) worden omgezet naar platte tekst en dit bestand wordt bewaard; het oorspronkelijke Word-bestand wordt daarna verwijderd. CHAT-bestanden worden bewaard.
- **Afgeleide bestanden.** Een CHAT-versie van het transcript, de grammaticale analyse (Alpino XML), en een automatisch gecorrigeerde versie daarvan.
- **Uitingen.** De afzonderlijke uitingen in het transcript, met de bijbehorende sprekercode, worden in de database opgeslagen.
- **Analyseresultaten.** De bestanden die SASTA genereert (zoals het SAF-bestand, het methode-formulier en het geannoteerde CHAT-bestand), en eventuele gecorrigeerde SAF-bestanden die u zelf weer uploadt.
- **Metagegevens.** De namen van uw corpora en transcripten, de gekozen analysemethode, de verwerkingsstatus en de datum van uploaden.

## Waar en hoe worden de gegevens verwerkt?

- Alle gegevens worden opgeslagen en verwerkt op servers van de Universiteit Utrecht.
- De grammaticale analyse wordt uitgevoerd met [Alpino](https://www.ineo.tools/resources/alpino). Alpino draait op dezelfde infrastructuur van de Universiteit Utrecht; uw tekst wordt hiervoor **niet** naar externe partijen gestuurd.
- Ook de overige bewerkingen (zoals conversie naar CHAT en de analyse volgens TARSP, STAP of ASTA) vinden volledig plaats op de servers van de Universiteit Utrecht.
- SASTA deelt uw gegevens niet met derden.
- SASTA gebruikt geen analyse- of trackingdiensten. Er worden alleen cookies geplaatst die nodig zijn om in te loggen en om de website te beveiligen (een sessiecookie en een CSRF-cookie).

## Wie heeft toegang tot uw gegevens?

- **U.** U heeft alleen toegang tot de corpora en transcripten die u zelf heeft aangemaakt. Andere gebruikers kunnen uw gegevens niet inzien.
- **Beheerders.** Systeembeheerders en ontwikkelaars van het Research Software Lab hebben technisch toegang tot de opgeslagen gegevens. Zij bekijken uw gegevens alleen wanneer dat nodig is voor onderhoud of het oplossen van problemen, of wanneer u zelf om ondersteuning vraagt.

## Beveiliging

Wij nemen de beveiliging van SASTA en uw gegevens serieus:

- SASTA wordt beheerd door een team van systeembeheerders van de Universiteit Utrecht, dat de servers en software onderhoudt en up-to-date houdt.
- Wij volgen actief beveiligingsproblemen in SASTA en de software waarop SASTA is gebouwd, en verhelpen deze zo snel mogelijk.
- Alleen ingelogde gebruikers hebben toegang tot de applicatie, en elke gebruiker kan alleen zijn of haar eigen gegevens inzien.

Heeft u een beveiligingsprobleem gevonden? Meld dit dan via [dh.developers@uu.nl](mailto:dh.developers@uu.nl?subject=[SASTA]%20Beveiliging).

## Anonimiseer uw transcripten

Transcripten bevatten vaak gevoelige informatie over sprekers, zoals namen, woonplaatsen of zorginstellingen. Wij raden u **met klem** aan uw transcripten te anonimiseren voordat u ze uploadt. SASTA ondersteunt hiervoor speciale anonimisatiecodes (zoals `NAAM1` of `PLAATS1`), die tijdens de analyse worden vervangen door grammaticaal gelijkwaardige woorden. Zie [Anonimisatie](input-formats/anonimisatie.md) voor een overzicht van de beschikbare codes.

Let ook op de **bestandsnamen** en **corpusnamen** die u kiest: deze worden zichtbaar in de applicatie en in technische logbestanden van de server. Gebruik hierin geen namen of andere herleidbare gegevens van sprekers.

SASTA controleert niet of een transcript geanonimiseerd is. Het anonimiseren blijft uw eigen verantwoordelijkheid.

## Hoe lang worden gegevens bewaard?

Uw transcripten en analyseresultaten worden bewaard totdat u ze zelf verwijdert, of totdat uw account wordt verwijderd.

### Gegevens verwijderen

- **Transcript verwijderen**: op de corpuspagina kiest u bij het transcript voor het prullenbak-icoon. Het transcript, alle afgeleide bestanden, de opgeslagen uitingen en alle analyseresultaten worden dan verwijderd.
- **Corpus verwijderen**: in het corpusoverzicht kunt u een volledig corpus verwijderen. Alle transcripten en bestanden in dat corpus worden dan verwijderd.
- **Account verwijderen**: u kunt uw account niet zelf verwijderen. Neem hiervoor [contact met ons op](mailto:dh.developers@uu.nl?subject=[SASTA]%20Account%20verwijderen). Wij verwijderen dan uw account en alle bijbehorende corpora, transcripten en resultaten.

### Back-ups

Van de server worden back-ups gemaakt. Gegevens die u verwijdert, kunnen daardoor nog een beperkte tijd in deze back-ups aanwezig zijn, totdat de back-ups worden overschreven. Back-ups worden niet gebruikt om verwijderde gegevens in te zien.

## Gebruik voor andere doeleinden

Uw geüploade gegevens worden uitsluitend gebruikt om de analyse voor u uit te voeren. Ze worden niet gebruikt voor de ontwikkeling van SASTA, voor onderzoek, of voor andere doeleinden.

Mocht SASTA in de toekomst een mogelijkheid bieden om gegevens te delen, dan gebeurt dat alleen met uw uitdrukkelijke toestemming. Deze verklaring wordt dan aangepast.

## Accountgegevens

Om SASTA te gebruiken heeft u een account nodig. Hiervoor slaan wij de volgende gegevens op:

- uw gebruikersnaam;
- uw e-mailadres;
- uw wachtwoord (versleuteld opgeslagen; wij kunnen uw wachtwoord niet inzien);
- de datum van registratie en van uw laatste login.

Uw e-mailadres wordt alleen gebruikt om uw account te bevestigen, om uw wachtwoord te herstellen, en om contact met u op te nemen als dat nodig is voor het gebruik van SASTA. Wij sturen geen nieuwsbrieven of reclame.

## Uw rechten

Op grond van de Algemene Verordening Gegevensbescherming (AVG) heeft u onder andere het recht om:

- uw gegevens in te zien;
- onjuiste gegevens te laten corrigeren;
- uw gegevens te laten verwijderen;
- uw gegevens in een gangbaar formaat te ontvangen. Via de functie `download` op de corpuspagina kunt u uw transcripten en analyses zelf downloaden.

Voor het uitoefenen van deze rechten kunt u contact opnemen via [dh.developers@uu.nl](mailto:dh.developers@uu.nl?subject=[SASTA]%20Privacy).

## Vragen en klachten

Heeft u vragen over deze verklaring of over hoe SASTA met uw gegevens omgaat? Neem dan contact op met het Research Software Lab via [dh.developers@uu.nl](mailto:dh.developers@uu.nl?subject=[SASTA]%20Privacy).

U kunt ook contact opnemen met de privacy officer van de Universiteit Utrecht: [privacy.gw@uu.nl](mailto:privacy.gw@uu.nl?subject=[SASTA]%20Privacy).

Bent u niet tevreden over hoe wij met uw vraag of klacht omgaan, dan kunt u een klacht indienen bij de [Autoriteit Persoonsgegevens](https://autoriteitpersoonsgegevens.nl/).

## Wijzigingen

Deze verklaring kan worden aangepast, bijvoorbeeld wanneer SASTA nieuwe functionaliteit krijgt. De datum bovenaan geeft aan wanneer de verklaring voor het laatst is bijgewerkt.
