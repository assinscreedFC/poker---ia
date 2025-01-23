from deuces import Card # type: ignore
from deuces import Deck # type: ignore
from deuces import Evaluator # type: ignore
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
        self.under_bet=[]#who have coin < bet 
        self.stop_to_player=0
        self.bet=self.big_blind
        self.nb=[0,3,4,5] # pour savoir combien de carte sont sur la table a chaque tour pre-flop, flop, turn, river
        self.etape=0

    
    def convert(self,nbr):
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
        # Fonction pour gérer le choix du joueur
        if choice=="fold":
            self.hand_of_players[self.current_player]=[]
            self.increment()
            
        elif choice=="check" and self.bet==0:
            self.increment()
            pass

        elif choice=="call" and (self.coin[self.current_player]>=self.bet):
            
            self.coin[self.current_player]-=self.bet
            self.pot+=self.bet
            self.increment()   
                
        elif choice=="all":
                self.pot+=self.coin[self.current_player]
                self.coin[self.current_player]=0
                self.under_bet.append(self.current_player)
                self.increment()
        elif self.convert(choice):
            if self.coin[self.current_player]>=self.bet:
                self.bet=self.convert(choice)
                self.coin[self.current_player]-=self.bet
                self.pot+=self.bet
                self.stop_to_player=1
                
        
        
    def increment(self):
        self.stop_to_player+=1
    def nbr_current_player(self):
        # Fonction pour retourner le nombre du joueur actuel
        count=0
        for hand in self.hand_of_players:
            if len(hand)!=0:
                count+=1
        return count
        
    def check_if_stop_rounde(self):
        # Fonction pour vérifier si le tour est terminé
        print(f"stop {self.stop_to_player}")
        print(self.nbr_current_player())
        return self.stop_to_player==self.nbr_current_player()
    def next_etape(self):
        # Fonction pour passer à l'étape suivante
        self.stop_to_player=0
        self.etape+=1
        self.bet=0

    def next_player(self):
        
        # Fonction pour passer au joueur suivant
        self.current_player=(self.current_player+1) if self.current_player<self.players-1 else 0
        while len(self.hand_of_players[self.current_player])==0:
            self.current_player=(self.current_player+1) if self.current_player<self.players-1 else 0

    def check_winner_rounde(self):
        # Fonction pour vérifier le gagnant de la ronde
        evaluate=Evaluator()
        score_each_player=[evaluate(self.table,player) for player in self.hand_of_players]
        winner=score_each_player.index(min(score_each_player))
        self.coin[winner]+=self.pot
        self.pot=0
        self.etape=0
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.hand_of_players = [self.deck.draw(2) for _ in range(self.players)]
        self.bet=self.big_blind
        self.current_player=self.who_is_who[0]
        self.stop_to_player=self.current_player-1 if self.current_player>0 else self.players-1
        for who in self.who_is_who:
            who=who+1 if who<self.players-1 else 0
    