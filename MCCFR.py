import random
from collections import defaultdict
from Game import Game

class MCCFRTrainer:
    def __init__(self, game, iterations=10000):
        self.game = game
        self.iterations = iterations
        self.regret_sum = defaultdict(lambda: defaultdict(float))
        self.strategy_sum = defaultdict(lambda: defaultdict(float))
    
    def get_strategy(self, info_set):
        strategy = {}
        normalizing_sum = 0
        
        for action in self.game.get_action():
            strategy[action] = max(self.regret_sum[info_set][action], 0)
            normalizing_sum += strategy[action]
        
        if normalizing_sum > 0:
            for action in strategy:
                strategy[action] /= normalizing_sum
        else:
            for action in strategy:
                strategy[action] = 1 / len(strategy)
        
        return strategy
    
    def get_average_strategy(self, info_set):
        strategy = {}
        normalizing_sum = sum(self.strategy_sum[info_set].values())
        
        for action in self.strategy_sum[info_set]:
            if normalizing_sum > 0:
                strategy[action] = self.strategy_sum[info_set][action] / normalizing_sum
            else:
                strategy[action] = 1 / len(self.strategy_sum[info_set])
        
        return strategy
    
    def train(self):
        for _ in range(self.iterations):
            self.cfr()
    
    def cfr(self, pr_1=1, pr_2=1):
        history = ""  # À définir selon l'état du jeu
        return self.cfr_recursive(history, pr_1, pr_2)
    
    def cfr_recursive(self, history, pr_1, pr_2):
        # Convertir l'état du jeu en un information set
        info_set = str(self.game.info_players)  # Peut être amélioré
        
        if self.game.check_if_stop_rounde():
            return self.get_terminal_value()
        
        strategy = self.get_strategy(info_set)
        util = {}
        node_utility = 0
        
        for action in strategy:
            self.game.choix_joueur(action)
            util[action] = -self.cfr_recursive(history + action, pr_1, pr_2)
            node_utility += strategy[action] * util[action]
            self.game.undo_last_action()  # Nécessite une fonction pour annuler une action
        
        for action in strategy:
            regret = util[action] - node_utility
            self.regret_sum[info_set][action] += regret
            self.strategy_sum[info_set][action] += strategy[action] * (pr_1 if self.game.current_player == 1 else pr_2)
        
        return node_utility
    
    def get_terminal_value(self):
        # Déterminer le gain final d'un joueur
        return 1  # Placeholder, à calculer avec l'évaluation de la main

trainer = MCCFRTrainer(Game())
trainer.train()
print("Training Complete.")
