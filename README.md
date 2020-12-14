# archiefDemo

De historische kring waarvan ik lid ben, heeft de beschrijvingen van al haar gedigitaliseerde foto's en documenten (ongeveer 100.000) opgeslagen in een Excelbestand. Het gaat om zeven categorieën (foto's, documenten, geboorte- en trouwaktes e.d.). Voor elke categorie wordt een apart blad gebruikt. Elke categorie heeft haar eigen nummering omdat de bestaande nummering (uit het analoge tijdperk) tijdens het opzetten van de database ongewijzigd is gebleven.
Op dit moment wordt de rubriek afbeeldingen, die onderverdeeld was in subcategorieën, heringedeeld, aangevuld en opnieuw genummerd.

Ik heb een programma geschreven om in dat bestand te kunnen zoeken: zoekenDemo.py.
De procedure:

1. De database wordt na het opstarten van het programma geladen (workbook = xlrd.open_workbook(...)).
2. De gebruiker typt een zoekwoorden in.
3. Het programma zoekt achtereenvolgens in alle bladen in alle cellen naar het zoekwoord en slaat een aantal gegevens van elk gevonden record op in de list 'zoekresultaten': nummer van de categorie, rijnummer in Excel en een korte beschrijving van de scan.
4. Als alle bladen doorzocht zijn, worden deze gegevens als 'zoekresultaatregels' onder elkaar op het scherm geprint.
5. Als de gebruiker op een regel dubbelklikt, worden in de functie foto_of_pdf_tonen het nummer van de categorie en het rijnummer eruit gefilterd en met deze gegevens worden in andere functies alle bijbehorende gegevens gelezen.
6. In de functie toon_scan wordt bepaald hoe de scan van het record op het scherm wordt getoond: de pdf's in een pdf-reader, geboorte- en trouwaktes in een foto-viewer en foto's in een fotopresentatie. Voor die fotpresentatie wordt een aparte module gebruikt.

De fotopresentatiemodule wordt aangeroepen met drie parameters: het nummer van de eerste foto, een list met de nummers van alle foto's in de juiste volgorde en een dictionary met alle bijbehorende gegevens. 

Het programma en het bijbehorende Excelbestand staan in afgeslankte vorm in de map archiefDemo. Het programma zoekt in vier categorieën in een Excelbestand met zestien records. Het zoekwoord 'archief' levert een overzicht op van alle zestien records.
