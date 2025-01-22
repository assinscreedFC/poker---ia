from deuces import Card # type: ignore
from deuces import Deck # type: ignore
from Table import Table
import asyncio



class Game:


    def __init__(self):
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.players = 6 #nombre de joueur sur la table 1-6
        self.hand_of_players = [self.deck.draw(2) for _ in range(self.players)] #pour avoir les cartes de chaque joueur
        self.coin =[1000 for _ in range(self.players)] #pour avoir le nombre de jeton de chaque joueur
        self.who_is_who=[0,1,2] #pour savoir qui est le bouton , le small blind et la big blind
        self.big_blind=10
        self.small_blind=5
        self.current_player=0
        self.pot = 0
        self.stop_to_player=5
        self.bet=self.big_blind
        self.nb=[0,3,4,5] # pour savoir combien de carte sont sur la table a chaque tour pre-flop, flop, turn, river
        self.etape=0

    
    def convert(nbr):
        # Fonction pour convertir une valeur en float ou en int
        if nbr.isdigit():
            return int(nbr) if int(nbr)>0 else False
        else:
            try:
            # Essayer de convertir la valeur en float
                return float(nbr) if float(nbr)>0 else False
            except ValueError:
            # Si une erreur se produit (valeur non convertible en float)
                return False

    def choix_joueur(self,choice=""):
        if choice=="fold":
            self.hand_of_players[self.current_player]=[]
            
        elif choice=="check" and self.bet==0:
            pass
        elif choice=="call":
            if(self.coin[self.current_player]>=self.bet):
                self.coin[self.current_player]-=self.bet
                self.pot+=self.bet
                               
        elif self.convert(choice):
            if self.coin[self.current_player]>=self.bet:
                self.coin[self.current_player]-=self.bet
                self.pot+=self.bet
                self.stop_to_player=self.current_player

        self.next_player()

    def check_if_stop_rounde(self):
        return self.stop_to_player==self.current_player
    def next_etape(self):
        self.etape+=1
        if self.etape==len(self.nb):
            self.check_winner_rounde()
        self.bet=0
    
    def check_winner_rounde(self):
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.hand_of_players = [self.deck.draw(2) for _ in range(self.players)]
        self.bet=self.big_blind
        self.current_player=self.who_is_who[0]
        self.stop_to_player=self.current_player-1 if self.current_player>0 else self.players-1
        for who in self.who_is_who:
            who=who+1 if who<self.players-1 else 0



    def next_player(self):
        self.current_player=(self.current_player+1) if self.current_player<self.players-1 else 0

    def rounde(self):
        # Fonction pour gérer le tour de jeu
        for etap in self.nb:

            
            self.choix_joueur()
    