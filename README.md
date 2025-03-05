# Poker AI

## Description
Poker AI est un projet visant à développer un agent IA capable de jouer au poker contre différents types de joueurs, jusqu'à 6 participants. Actuellement, la partie jeu est déjà développée : il est possible de jouer via le terminal ou d'utiliser la classe du jeu pour permettre à une IA de jouer automatiquement.

La prochaine étape consiste à développer l'IA en utilisant **Monte Carlo Counterfactual Regret Minimization (MCCFR)**. Des recherches sont en cours pour affiner cette approche. À terme, d'autres techniques de machine learning pourraient être testées et comparées à MCCFR.

## Technologies Utilisées
- **Python 3.12**
- **Deuces** (bibliothèque d'évaluation des mains de poker)

## Installation
1. Assurez-vous d'avoir **Python 3.12** installé sur votre système.
2. Clonez ce dépôt :
   ```sh
   git clone https://github.com/assinscreedFC/poker---ia.git
   cd poker-ai
   ```
3. Installez les dépendances :
   ```sh
   pip install -r requirements.txt
   ```

## Utilisation
- Pour jouer manuellement via le terminal :
  ```sh
  python main.py
  ```
- Pour intégrer une IA, il suffit de passer la classe du jeu à l'agent IA en cours de développement.

## Prochaines étapes
- Implémentation de **Monte Carlo CFR** pour la prise de décision IA.
- Comparaison avec d'autres modèles de machine learning.
- Améliorations et optimisations de l'algorithme.

## Contributions
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## Licence
MIT License

