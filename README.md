# Projet d'Apprentissage renforcé par le jeu-vidéo

## Objectif du projet

Le but du projet est de réaliser un jeu mono ou multijoueur, où un agent automatique apprend à jouer puis joue (seul ou contre l'humain) en optimisant son niveau de jeu.

## Technique

- Langage: Python
- Environnement graphique: TBD
- Algorithme d'apprentissage par renforcementavec prise en charge complete de l'état du joueur
- Stockage de l'évaluation(Q-table, NN, etc.) et rechargement
- Possibilité de refaire l'apprentissage

## Jeu

### But

En se basant sur le jeu du dinosaure disponible lors de la perte de connexion sur les differents navigateurs web, l'objectif de notre jeu est d'atteindre la fin du niveau en esquivant les differents obstacles sur le chemin.

### Actions

Pour éviter les obstacles lui faisant face, le joueur à 2 actions possibles:

- Sauter(JUMP)
- S'accroupir(CROUCH)

Le personnage se deplace vers l'avant automatiquement et ne peut pas aller vers l'arrière.

### Obstacles

Le joueur devra utiliser les 2 actions qui lui sont à disposition afin d'éviter les obstacles sur sa route. Il y a 2 types d'obstacles:

- Obstacles au sol(GROUND_OBSTACLES): Le joueur doit sauter pour les esquiver

- Obstacles dans les airs(SKY_OBSTACLES): Le joueur doit s'accroupir pour les esquiver
