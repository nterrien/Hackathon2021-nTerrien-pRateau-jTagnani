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
- Si Scalingo vous demande de faire l'étape "SSH KEY" suivez les instructions suivantes : 
  - Générer une clef SSH (vous en avez peut etre déjà une (voir : https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/checking-for-existing-ssh-keys), si c'est le cas cette sous-étape n'est pas necessaire) en suivant la partie "Generating a new SSH key" du tutoriel : https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key
  - Dans le champs Name mettez ce que vous voulez, et dans le champs Content copier-coller l'intégralité du contenu du fichier généré (id_rsa.pub, id_ecdsa.pub ou id_ed25519.pub). Ce fichier devrait se trouver dans /c/Users/**_Nom_utilisateur_**/.ssh/ sous Windows, /home/**_Nom_utilisateur_**/.ssh/ sous Linux ou dans /Users/**_Nom_utilisateur_**/.ssh sous MAC (Nom_utilisateur etant le nom d'utilisateur de votre PC)
- Écrire le nom que vous voulez puis Cliquer sur Next
- Cliquer sur Next
- Suivez les instructions à l'écran, qui devraient être :
  - Dans le répertoire de travail copier coller les deux lignes ```git remote add scalingo git@ssh.osc-fr1.scalingo.com:nomdelapp.git``` (le nomdelapp est ce que vous avez à la deuxieme étape, la commande exact est trouvable sur le site)
  - Dans le répertoir de travail lancer la commande ```git push scalingo main:master``` (On précise ici que la commande utilise main et pas master)
  - Aller sur l'adresse donnée par le site.

## Demonstration 

Le site est déployé à l'adresse suivante : https://hackaton2021jnp.osc-fr1.scalingo.io/
