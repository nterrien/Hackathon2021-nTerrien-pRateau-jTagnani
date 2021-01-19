#Journal de l'avancement du Hackaton

##19/01/2021 12h15

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


