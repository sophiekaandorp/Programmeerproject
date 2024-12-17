Reviewers: Ronan Philips & Sean Park

1. **Locatie van vragen en antwoorden in create.py:**
Mijn vragen en antwoorden staan momenteel in create.py. Dit is een onhandige plek, omdat dit bestand vooral gericht is op het aanmaken van nieuwe items. Een goede oplossing hiervoor zou zijn om een nieuw bestand te maken, zoals import.py, en hierin de code voor het toevoegen van de vragen en antwoorden aan de database te zetten. Hiermee verbeter ik de structuur en logica van mijn bestanden. Hierdoor is mijn project ook beter te begrijpen voor anderen. 

2. **Onduidelijkheid bij het invoeren van de Instagram-gebruikersnaam:**
Bij "Mijn Profiel" is er een mogelijkheid om je Instagram-gebruikersnaam in te voeren. Bij het invoeren is het onduidelijk of je *@gebruikersnaam* moet invoeren of *gebruikersnaam*. Dit is erg onhandig, want als de gebruiker *@gebruikersnaam* invoert zal de webapplicatie leiden naar een Instagram account dat niet bestaat. Ik heb hiervoor aan meerdere oplossingen gedacht, zoals als placeholder in plaats van "Voer je Instagram-gebruikersnaam in..." het volgende neer te zetten: "@...", alleen dit maakt het naar mijn idee juist nog onduidelijker. Ik denk dat daarom de beste oplossing is om in plaats van een tijdelijke placeholder, standaard "@" in het tekstvak te plaatsen. Hierdoor staat een "@" al klaar en is het dan ook duidelijk voor de gebruikers dat zij deze niet zelf hoeven in te typen.

3. **Geen efficiënte rank functie:**
In mijn rank functie vraag ik rang 1 tot en met rang 5 afzonderlijk op en voeg ik deze één voor één toe aan een lijst. Dit is een onnodige herhaling, en zou veel efficiënter zijn als ik dit in een for loop had geplaatst. Dit maakt de code korter en overzichtelijker. Bovendien zou dit later ook veel handiger zijn als ik bijvoorbeeld meer rangen zou willen toevoegen. 

4. **Onduidelijk opslaan van profielgegevens:**
Wanneer je na het aanpassen van je profielgegevens op opslaan drukt, gebeurt er visueel niks. De gegevens worden uiteraard opgeslagen, maar de gebruiker ziet hier niks van. Dit kan ertoe leiden dat het voor de gebruiker niet duidelijk is of de gegevens succesvol zijn opgeslagen. Dit vond ik een erg goed verbeterpunt, en heb dit daarom ook gelijk aangepast. Ik heb er nu voor gezorgd dat de gebruiker nadat er op de "Opslaan" knop is gedrukt, terug gaat naar de homepagina en een flashbericht krijgt die aangeeft dat de profielgegevens succesvol zijn opgeslagen. 

5. **Restrictie lengte tekst biografie/gebruikersnaam/wachtwoord:**
Bij verschillende tekstvakken heb ik geen restricties, zoals bij de gebruikersnaam en het wachtwoord. Ook is er bij de biografie geen restrictie voor de lengte van de tekst. Dit kan de webapplicatie minder gebruiksvriendelijk maken. Als een gebruiker bijvoorbeeld een erg lange biografie invoert, is het voor de andere gebruiker die op dat profiel klikt totaal niet overzichtelijk. Dan verschijnt er ineens een enorme hoeveelheid tekst waar je doorheen moet scrollen. Het zou beter zijn om aan te geven dat de biografie bijvoorbeeld maximaal 100 tekens kan zijn. Dit zou een goede aanpassing zijn en de website gebruiksvriendelijker maken.


