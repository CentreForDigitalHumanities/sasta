# Transcript pagina
Op de transcriptpagina vindt u informatie over het gekozen transcript, en kunt u de analyse uitvoeren. De pagina is verdeeld in een aantal panelen.

## Titelbalk
In de titelbalk vindt u de titel van het transcript. Onder de titel vindt u relevante informatie over het transcript en de SASTA bewerkingen:

- Status: de status van de SASTA bewerkingen
- Analysing: hoeveel uitingen (van het totaal aantal uitingen) door SASTA genalyseerd worden [link naar selecting speakers]
- Analysing speakers: de codes van de sprekers wiens uitingen worden geanalyseerd
- Method: de methode waarmee het transcript geanalyseerd wordt
- Created on: de datum waarop het transcript is toegevoegd

## Scoring
In dit paneel bevindt zich de hoofdfunctionaliteit van SASTA: het genereren van automatische analyses.
Er is een drietal opties. De onderliggende analyse is steeds dezelfde, maar het uitvoerformaat verschilt:

- Annotate (xlsx)
	- Genereert een bestand in het Sasta Annotatie Formaat (SAF) [link]
	- Dit bestandsformaat wordt ook gebruikt voor handmatige verbetering van de analyse
- Annotate (CHAT)
	- Genereert een CHAT bestand, met daaraan toegevoegd de annotaties voor elke genalyseerde uiting. Dit bestand kan bijvoorbeeld gebruikt worden in STAMPER.
- Generate form
	- Genereert het (gedeeltelijk) ingevulde formulier voor de gekozen methode. Dit uitvoerformaat bootst analyse middels handmatige analyse na.

## Annotations
- Download annotations: download een `xlsx` bestand met annotaties volgens de laatste analyse
- Upload (corrected) annotations: hier kunt u een verbeterd annotatiebestand uploaden (zie [link])
- Reset corrections: zet het bestand terug naar de eerste versie, zonder handmatige verbeteringen

## Utterances
U kunt het paneel met uitingen openklikken door op de balk te klikken. Per uiting in het transcript wordt weergeven:

- Speaker: de code van de spreker
- Sentence: de (opgeschoonde) uiting
- For analysis: een vinkje wanneer SASTA de uiting analyseert, een streepje wanneer dit niet het geval is
- Parse tree: een visuele representatie van de geparseerde uiting. Hier kunt u bekijken hoe Alpino de uiting heeft geparseerd

## Files
In dit paneel heeft u toegang tot enkele van de bestanden die SASTA gebruikt voor een transcript:

- CHAT: het door SASTA bewerkte inputbestand, in CHAT formaat
- Alpino parse: het Alpino geparseerde bestand, in LASSY XML formaat
- corrected Alpino parse: het door SASTA verbeterde geparseerde bestand, in LASSY XML formaat
