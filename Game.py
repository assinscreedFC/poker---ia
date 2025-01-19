from deuces import Card
from deuces import Deck



class game:


    def __init__(self):
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.players = 6 #nombre de joueur sur la table 1-6
        self.hand_of_players = [self.deck.draw(2) for _ in range(self.players)] #pour avoir les cartes de chaque joueur
        self.coin =[1000 for _ in range(self.players)] #pour avoir le nombre de jeton de chaque joueur
        self.current_player = 0
        self.who_is_who=[0,1,2] #pour savoir qui est le bouton , le small blind et la big blind
        self.big_blind=10
        self.small_blind=5
        self.pot = 0
        self.nb=[0,3,4,5] #pour savoir combien de carte sont sur la table a chaque tour pre-flop, flop, turn, river


    def get_hand(self):
        return self.hand_of_players

    def get_table(self):
        return self.table
    
    def get_players(self):
        return self.players
    