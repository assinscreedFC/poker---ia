import random
from collections import defaultdict
from Game import Game
# Importe votre classe Game telle que vous l’avez définie.
# Par exemple, si elle est dans le fichier game.py, vous pouvez faire :
# from game import Game

# --- Classe MCCFRTrainer ---
class MCCFRTrainer:
    def __init__(self, game, iterations=10000):
        """
        :param game: Une instance de votre classe Game
        :param iterations: Nombre d’itérations d’entraînement
        """
        self.game = game
        self.iterations = iterations
        # regret_sum et strategy_sum sont indexés par info_set (la représentation de l'état pour le joueur)
        # et par action.
        self.regret_sum = defaultdict(lambda: defaultdict(float))
        self.strategy_sum = defaultdict(lambda: defaultdict(float))
    
    def get_strategy(self, info_set):
        """
        Calcule la stratégie (distribution de probabilités sur les actions) 
        pour un info_set donné, basée sur les regrets positifs.
        """
        strategy = {}
        normalizing_sum = 0.0
        # On parcourt toutes les actions possibles fournies par la méthode get_action() de Game.
        for action in self.game.get_action():
            # On utilise le regret positif (ou 0 si négatif)
            r = self.regret_sum[info_set][action]
            strategy[action] = r if r > 0 else 0.0
            normalizing_sum += strategy[action]
        
        # Si la somme des regrets positifs est nulle, on retourne une stratégie uniforme.
        if normalizing_sum > 0:
            for action in strategy:
                strategy[action] /= normalizing_sum
        else:
            num_actions = len(strategy)
            for action in strategy:
                strategy[action] = 1.0 / num_actions
        return strategy

    def get_average_strategy(self, info_set):
        """
        Retourne la stratégie moyenne apprise pour un info_set.
        """
        avg_strategy = {}
        normalizing_sum = sum(self.strategy_sum[info_set].values())
        if normalizing_sum > 0:
            for action in self.strategy_sum[info_set]:
                avg_strategy[action] = self.strategy_sum[info_set][action] / normalizing_sum
        else:
            num_actions = len(self.strategy_sum[info_set])
            for action in self.strategy_sum[info_set]:
                avg_strategy[action] = 1.0 / num_actions
        return avg_strategy

    def get_terminal_value(self):
        """
        Fonction utilitaire pour définir l’utilité terminale de la simulation.
        Ici, nous choisissons aléatoirement un gagnant parmi les joueurs
        qui n’ont pas fold (c'est-à-dire dont la main n'est pas vide).
        Le gagnant reçoit 1.0 et les autres –0.2.
        Cette fonction retourne un dictionnaire avec pour clé l’index du joueur.
        """
        active_players = [player for player in self.game.info_players if player["hand"]]
        utilities = {}
        if active_players:
            winner = random.choice(active_players)
            for player in self.game.info_players:
                if player["hand"]:
                    if player["index"] == winner["index"]:
                        utilities[player["index"]] = 1.0
                    else:
                        utilities[player["index"]] = -0.2
                else:
                    # Un joueur qui a fold obtient 0
                    utilities[player["index"]] = 0.0
        else:
            # Aucun joueur actif
            for player in self.game.info_players:
                utilities[player["index"]] = 0.0
        return utilities

    def train(self):
        """
        Lance l'entraînement sur le nombre d’itérations spécifié.
        Pour chaque itération, l'état du jeu est réinitialisé via la méthode d'initialisation (ici, on utilise game.init()).
        """
        for i in range(self.iterations):
            # Réinitialiser le jeu pour une nouvelle simulation.
            self.game.init()
            # Initialisation des probabilités de portée pour chaque joueur.
            # Les clés correspondent aux index des joueurs (player["index"]).
            pr = {player["index"]: 1.0 for player in self.game.info_players}
            self.cfr_recursive("", pr)
        print("Entraînement terminé.")

    def cfr_recursive(self, history, pr):
        """
        Algorithme de CFR récursif adapté à un jeu multi-joueurs.
        :param history: Chaîne représentant l'historique (peut être utilisée pour distinguer les branches de l'arbre)
        :param pr: Dictionnaire des probabilités de portée pour chaque joueur.
        :return: Un dictionnaire des utilités pour chaque joueur (clé = index du joueur).
        """
        # Identifiez le joueur courant via son index dans la liste.
        current_index = self.game.info_players[self.game.current_player]["index"]
        # Construire l'info_set à partir des informations du joueur courant.
        info_set = str(self.game.info_players[self.game.current_player])
        
        # Vérifier si le tour (ou l'étape) est terminé.
        if self.game.check_if_stop_rounde():
            # Passer à l'étape suivante.
            self.game.next_etape()
            # Si on a atteint la dernière étape (par exemple, river), c'est un état terminal.
            if self.game.etape >= len(self.game.nb):
                # Dans notre exemple, nous utilisons get_terminal_value() pour définir les utilités.
                return self.get_terminal_value()
        
        # Récupérer la stratégie courante pour cet info_set.
        strategy = self.get_strategy(info_set)
        # Préparer un dictionnaire pour accumuler l'utilité pondérée de chaque action.
        util = {}
        # node_util accumulera l’utilité moyenne pour chaque joueur sur ce nœud.
        node_util = {pid: 0.0 for pid in pr}
        
        # Pour chaque action possible
        for action in strategy:
            # Appliquer l'action dans le jeu.
            self.game.choix_joueur(action)
            # Copier le dictionnaire de probabilités pour la branche de l'action.
            new_pr = pr.copy()
            new_pr[current_index] *= strategy[action]
            # Appel récursif sur le nouvel état
            util[action] = self.cfr_recursive(history + action, new_pr)
            # Combiner les utilités pondérées pour chaque joueur.
            for pid in node_util:
                node_util[pid] += strategy[action] * util[action].get(pid, 0.0)
            # Annuler l'action pour revenir à l'état précédent.
            self.game.undo_last_action()
        
        # Mise à jour des regrets pour le joueur courant.
        for action in strategy:
            # Pour le joueur courant, le regret est la différence entre l'utilité obtenue en jouant l'action
            # et l'utilité moyenne du nœud.
            regret = util[action].get(current_index, 0.0) - node_util[current_index]
            self.regret_sum[info_set][action] += regret
            # Mise à jour de la somme de stratégie pondérée par la probabilité de portée.
            self.strategy_sum[info_set][action] += strategy[action] * pr[current_index]
        
        return node_util

# --- Point d'entrée du programme ---
if __name__ == '__main__':
    # Supposons que votre classe Game est déjà définie et importée.
    # Créez une instance du jeu.
    game = Game(players=[1, 2, 3, 4, 5, 6])
    
    # Créez l'entraîneur MCCFR avec par exemple 1000 itérations (pour la démo).
    trainer = MCCFRTrainer(game, iterations=1000)
    
    # Lancez l'entraînement.
    trainer.train()
    
    # Affichage des stratégies moyennes apprises pour chaque info_set rencontré.
    print("\nStratégies moyennes apprises :")
    for info_set in trainer.strategy_sum:
        avg_strategy = trainer.get_average_strategy(info_set)
        print("Info_set :", info_set, "-> Stratégie :", avg_strategy)
