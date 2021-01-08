# Hackathon2021-nTerrien-pRateau-jTagnani

## Lancer le site en local
### Installation

#### Python:

https://wiki.python.org/moin/BeginnersGuide/Download

#### Pip

https://pip.pypa.io/en/stable/installing/#

Il est possible d'installer python à partir du microsoft store et pip s'installe automatiquement

#### Vérifier que python et pip sont bien installés :

python --version

pip --version

####  installer les dépendances :

Dans le répertoire de travail, executer :

```$ pip install flask Flask-WTF flask_sqlalchemy requests```

OU

```$ pip install -r requirements.txt```

### Execution

Dans le répertoire de travail lancer :
```python app.py```

Puis aller sur : http://127.0.0.1:5000

## Deployer le site sur Scalingo

- Se connecter sur le site Scalingo
- Créer une nouvelle app avec le bouton "CREATE A NEW APP"
- Écrire le nom que vous voulez puis Cliquer sur Next
- Cliquer sur Next
- Suivez les instructions à l'écran, qui devraient être :
 - Dans le répertoire de travail copier coller les deux lignes ```git remote add scalingo git@ssh.osc-fr1.scalingo.com:nomdelapp.git``` (le nomdelapp est ce que vous avez à la deuxieme étape, la commande exact est trouvable sur le site)
 - Dans le répertoir de travail lancer la commande ```git push scalingo master```
 - Aller sur l'adresse donné par le site.
