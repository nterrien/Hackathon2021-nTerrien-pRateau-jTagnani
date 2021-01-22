# Journal de l'avancement du Hackaton

## 19/01/2021 12h15

Nous avions plusieurs plans concernant l'utilisation d'une API externe :
Plan A : La CARAE
    Nous avons contacté la CARAE concernant une API pour la reservation des salles.
    Réponse : Carae nous a dit qu'ils utilisaient le service général de réservation de l'école pour la réservation de salles : [Grr](https://reservation.imt-atlantique.fr/). Malheureusement ce service ne dispose pas d'API pour y accéder...
    Nous avons donc décidé de simuler l'utilisation de l'API de Grr pour les réservations de salle dans l'enceinte de l'école.
Plan B : Faire une fausse API permettant de reserver les sandwiches : 
    Probleme : D'autre groupe s'occupe déjà de cette problématique et cela risque de faire une redondance
Plan C : Utiliser l'API d'un autre groupe pour la reservation des sandwiches :
    L'autre groupe ne compte pas faire d'API.

Nous avons codé :

* Début de la mise en place du front end pour l'interface de reservation des machines à laver. Ce code pourra surement être réutiliser pour la reservation de salle
* Adaptation de la bdd pour stocker des réservations
    * Création d'une classe "WashingMachine" pour s'occuper spécifiquement de la réservation d'une machine à laver
    * Ajout dans la bdd d'une table User pour l'authentification
* Authentification
    * interface de login
    * interface d'inscription
    * devoir s'authentifier avant toute chose

Nous avons prévu de faire : 

* Finir le Frontend Machine à laver et le connecter à la BDD
* Faire le Frontend poru la reservation des salle de la MDE
* Finir l'authentification


## 20/01/2021 17h45

Nous avons codé :
* Coté BDD :
    * Ajout de la gestion de plusieurs machines
    * Le code est plus modulaire pour pouvoir reserver autre chose que les machines à laver
    * Ajout de la gestion des salles en BDD
* L'authentification :
    * Page de connexion et gestion de la connexion
* API :
    * Developpement d'un fausse API connecter avec Grr. Cette API est deployée sur Scalingo
* FrontEnd Machine à laver:
    * Les fonctionnalités fonctionnent presque toute. L'affichage est prévu pour les smartphone et le bureau. 

Nous avons prévu de faire :
* Fonctionnalié manquante frontend :
    * Faire que le nav soit adapté au mobile
    * Mettre avant le creneau qui nous appartient (cela demande un peu de travail du coté backend pour enregistrer l'id de la personne qui a pris la reservation)
    * La page de connexion est pas responsive (c'est trop petit en mode portable)
    * Toute la reservation de salle
* Autre :
    * Verifier si la BDD disparait sur SCALINGO
    * Deployement automatique sur develop
* Fonctionnalité manquante backend :
    * merge l'API
    * relier l'utilisateur et les réservations
    * réorganiser le code dans plus de dossiers

## 22/01/2021 12h15

* L'authentification :
    * Les pages sont adaptés pour le format mobile
    * Possibilité de changer son mdp et nom d'utilisateur via l'onglet profil
* Base de données :
    * Les réservations sont maintenant faites par un utilisateur
* FrontEnd :
    * Rajout d'un onglet contact avec nos informations
    * La page de reservation des salles a été faites en entier en factorisant le code pour l'affichage de l'agenda des machines à laver avec celui des salles
    * Mise en avant des créneaux réservés par l'utilisateur et affichage de l'utilisateur ayant réservé un creneau 
    * Ajustement concernant la responsivité de la page de login, de la barre de navigation et de l'agenda
* Autre :
    * Nous avons merge l'API dans develop
    * Nous avons constaté qu'apres + d'un jour le base de donnée sur Scalingo n'avais pas disparu
    * Nous avons mis en place le deploiement automatique de la branche develop
    * Grosse refactorisation et réorganisation du code
    * Correction de bugs divers

## 22/01/2021 15h30
* FrontEnd :
    * Petit changement graphique de l'agenda
    * Correction d'un bug qui concerne l'ajout d'une reservation dépassant minuit
    * Amélioration de l'apparence de l'agenda lorsque que le téléphone est en mode paysage
    * Amélioration du champs de selection de l'heure
    * Corrections de bug (authentification, changement de nom)
* Bdd :
    * Lorsqu'on change son nom, les réservations à notre nom sont elles aussi mise à jour
    * réorganisation de fonctions
* Autre :
    * Mise en production et merge de develop sur le main



Lien vers le site deployé sur Scalingo : https://hackaton2021jnp.osc-fr1.scalingo.io/

Lien vers le Github : https://github.com/nterrien/Hackathon2021-nTerrien-pRateau-jTagnani
