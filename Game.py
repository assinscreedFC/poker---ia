from deuces import Card
from deuces import Deck


class game:


    def __init__(self):
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.players = 6
        self.hand_of_players = [self.deck.draw(2) for _ in range(self.players)] #pour avoir les cartes de chaque joueur
        self.coin =[1000 for _ in range(self.players)] #pour avoir le nombre de jeton de chaque joueur
        self.big_blinde_player =1
        self.small_blinde_player = 2
        self.big_blind=10
        self.small_blind=5
        self.pot = 0
        self.nbr_tour=0


    def get_hand(self):
        return self.hand_of_players

    def get_table(self):
        return self.table
    
    def get_players(self):
        return self.players