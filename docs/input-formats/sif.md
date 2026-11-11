# SASTA Input Format (SIF)

## Het bestand
Het transcript dient te worden aangeleverd als een Microsoft Word  `.docx`-bestand. Een `.txt`-bestand met `utf-8`-encoding wordt ook geaccepteerd. De naam van het bestand wordt gebruikt als titel van het transcript binnen SASTA. Zo zal het bestand `sample 12.docx` het transcript `sample_12` opleveren.

## Sprekers
Het transcript kan uitingen van meerdere sprekers bevatten. Ken elke spreker een unieke drieletterige code toe; bijvoorbeeld CHI (child), INV (interviewer) of PMA (patient met afasie).


##  Metadata
### Uitingen selecteren
SASTA werkt optimaal wanneer het volledige transcript wordt aangeleverd. Dus ook uitingen van sprekers die niet geanalyseerd hoeven te worden, kunnen de resultaten verbeteren. Het is nodig om in dit volledige transcript de uitingen te markeren waarin je geinterresseerd bent. Je kunt dit mechanisme gebruiken om de analyse te baseren op een vast aantal uitingen, bijvoorbeeld 50.

Er zijn twee manieren om een zin te markeren voor analyse:

1. De spreker van de uiting
2. De uiting nummeren, zie [uitingen](#uitingen)

Om alle uitingen van spreker PMA te analyseren, voeg je de volgende regel in:

```
##TARGET SPEAKER PMA
```

Om alleen de genummerde uitingen te analyseren:

```
##TARGET UTTIDS
```

Wanneer uitingen van een spreker worden gemarkeerd, **én** er zijn gemarkeerde uitingen aanwezig, worden alleen de genummerde uitingen van de spreker geanalyseerd.

### Samplenaam
Het is mogelijk de titel van een transcript te overschrijven aan de hand van het metadata-veld `samplenaam`:
```##META text samplenaam = ASTA-13```
Als dit veld aanwezig is wordt de bestandsnaam genegeerd.

### Overige metadata
Alle metadata volgens het [PAQU-formaat](https://paqu.let.rug.nl:8068/info.html#credits) zijn geldige invoer. deze worden echter door niet door SASTA verwerkt.

## Uitingen

Elke uiting begint op een nieuwe regel. Ze kunnen doorlopen op de volgende regel, maar mogen niet onderbroken worden met een regeleinde. Uitingen hebben een vaste vorm:

```
SPK:<tab of spatie(s)>Inhoud van de uiting
```

Optioneel zijn ze ook genummerd:
```
<nummer> | SPK:<tab of spatie(s)>Inhoud van de uiting
```

```

INV: Waar ben je vandaag geweest?
1 | PMA: In de dierentuin.
2 | INV: Oh wat leuk!
```



### Annoteren
Uitingen kunnen geannoteerd worden volgens de [CHAT handleiding][chat-manual].

[Voor lijsten met veel gebruikte annotaties, zie TODO: ASTA, STAP, TARSP-specifieke annotaties.]: #


## Voorbeeldbestanden
Zie [link](./voorbeelden.md) voor downloadbare voorbeeldbestanden.

[chat-manual]: https://talkbank.org/manuals/CHAT.pdf
