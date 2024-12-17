# Programmeerproject
## **Musicmatch**
Sophie Kaandorp

### Visualisaties van de Webapplicatie
![Home](home.png)
![Rang](rang.png)
![Mijn Profiel](mijn_profiel.png)
![Matches](matches.png)

### Beschrijving
Muziekmatch is een webapplicatie die muziekliefhebbers met elkaar verbindt door hun muziekvoorkeuren te matchen. Deze webapplicatie is dan ook bedoeld voor mensen die houden van muziek en graag nieuwe mensen willen ontmoeten met dezelfde muziekstijl. Door middel van een quiz met meerkeuzevragen en ranking-vragen berekent de webapplicatie het matchpercentage tussen gebruikers. Het doel is om gebruikers met overeenkomende muziekinteresses (meer dan 60% match) te koppelen, zodat ze nieuwe mensen leren kennen met dezelfde muzieksmaak. Gebruikers kunnen elkaars profielen bekijken, met een bio en een Instagram-link. 

### Instructies voor Installatie
1. **Zorg ervoor dat python3 en PostgreSQL zijn geïnstalleerd**. Voor PostgreSQL:
    - On a Mac with homebrew simply run brew install postgresql. Just for reference: https://wiki.postgresql.org/wiki/Homebrew
    - On WSL on Windows follow these instructions: https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database#install-postgresql

2. **Start de PostgreSQL-service:**
    - On a Mac with homebrew run: `brew services start postgresql`
    - On WSL on Windows run: `sudo service postgresql start`

3. **Installeer de vereiste packages:**
Run `python3 -m pip install -r requirements.txt`

4. **Stel de database-URL in:** Run `export DATABASE_URL="postgresql://postgres:jouw_wachtwoord@localhost/musicmatch"`
    - Vervang *jouw_wachtwoord* door je eigen PostgreSQL-wachtwoord.

5. **Maak de database aan:** Zorg ervoor dat de database musicmatch bestaat. Voer de volgende commando in in de PostgreSQL-shell:
`CREATE DATABASE musicmatch;`

6. **Run create.py:**
Run 
`python3 create.py`

7. **Start de Flask-applicatie:**
Run 
`python3 -m flask run --debug`

8. **Ga naar de webiste: http://127.0.0.1:5000**


