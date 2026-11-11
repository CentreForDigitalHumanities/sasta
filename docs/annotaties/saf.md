# SASTA Output formaat (SAF)

## Het bestand
Een bestand in het SASTA Output formaat representeert de uitingen en annotaties van één transcript. Het bestand wordt opgeleverd als een Excel spreadsheet (`.xlsx`).

## Kolommen
### Uiting
In deze kolom staat het uitingsnummer van de uiting. Let op: dit zijn alleen de uitingen die geselecteerd zijn voor analyse. De `ID` kolom loopt dus altijd van `1` tot `<hoeveelheid gemarkeerde uitingen>`.
### Level
In deze kolom word de naam van de verschillende niveaus getoond, zie [levels](#levels).

### Hele uiting
Deze kolom is bedoeld voor niet-gealigneerde annotaties. Een voorbeeld zijn annotaties die niet bij een specifiek woord of woordgroep horen, maar bij de gehele uiting.

### Word1, Word2, ...WordN
De `Word`-kolommen zijn bedoeld voor annotaties behorende bij een specifiek woord in de uiting. Wanneer annotaties behoren bij woordgroepen, worden deze genoteerd onder het eerste woord van de woordgroep. De kolommen lopen door tot het aantal woorden van de langste geanalyseerde uiting in het transcript.

### Fases
In deze kolom wordt automatisch een opsomming gemaakt van alle fases die horen bij de annotaties van de uiting, in Romeinse cijfers.

### Opmerkingen
In deze kolom kunnen opmerkingen worden opgenomen, behorende bij de gehele zin. Deze worden niet door SASTA verwerkt. Voor commentaar over een specifiek woord word het level `Opmerkingen` gebruikt.

## Rijen
Eén uiting bestaat uit meerdere rijen, elk beginnende met hetzelfde uitingsnummer. Voor een uiting zijn steeds de `Uiting`-rij, `level`-rijen, en de `Opmerkingen`-rij opgenomen.

### Uiting
Op deze rij staan de woorden van uiting. Als een woord in het invoerbestand bijvoorbeeld voorzien is van een CHAT-annotatie, wordt deze verwerkt en wordt het woord opgeschoond getoond.

### Levels
Annotaties kunnen op verschillende niveaus worden gemaakt.
Voor elk niveau is er een aparte rij opgenomen.

