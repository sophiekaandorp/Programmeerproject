# Programmeerproject
## **Musicmatch**
Sophie Kaandorp

### Screencast van de Webapplicatie
[Screencast bekijken](https://drive.google.com/file/d/1zk1511V--9kYxBMl9p6w5vkTzcQjSwGv/preview)


### Visualisaties van de Webapplicatie
![Home](home.png)
![Rang](rang.png)
![Mijn Profiel](mijn_profiel.png)
![Matches](matches.png)

### Beschrijving van de Webapplicatie
Muziekmatch is een webapplicatie die muziekliefhebbers met elkaar verbindt door hun muziekvoorkeuren te matchen. Deze webapplicatie is dan ook bedoeld voor mensen die houden van muziek en graag nieuwe mensen willen ontmoeten met dezelfde muziekstijl. Door middel van een quiz met meerkeuzevragen en ranking-vragen berekent de webapplicatie het matchpercentage tussen gebruikers. Het doel is om gebruikers met overeenkomende muziekinteresses (meer dan 60% match) te koppelen, zodat ze nieuwe mensen leren kennen met dezelfde muzieksmaak. Gebruikers kunnen elkaars profielen bekijken, met een biografie en een Instagram-link.

### Instructies voor Installatie
1. **Zorg ervoor dat python3 en PostgreSQL zijn geïnstalleerd**. Voor PostgreSQL:
    - Mac: run `brew install postgresql`. Zie hier informatie: https://wiki.postgresql.org/wiki/Homebrew
    - WSL of Window: volg de volgende instructies: https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database#install-postgresql

2. **Start de PostgreSQL-service:**
    - Mac: met homebrew run: `brew services start postgresql`
    - WSL of Windows: run: `sudo service postgresql start`

3. **Installeer de vereiste packages:**
Run `python3 -m pip install -r requirements.txt`

4. **Stel de database-URL in:** Run `export DATABASE_URL="postgresql://postgres:jouw_wachtwoord@localhost/musicmatch"` Vervang *jouw_wachtwoord* door je eigen PostgreSQL-wachtwoord.

5. **Maak de database aan:** Zorg ervoor dat de database musicmatch bestaat. Voer de volgende commando in in de PostgreSQL-shell:
`CREATE DATABASE musicmatch;`

6. **Run create.py:**
Run 
`python3 create.py`

7. **Start de Flask-applicatie:**
Run 
`python3 -m flask run --debug`

8. **Ga naar de webiste: http://127.0.0.1:5000**


