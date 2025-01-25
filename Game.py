from deuces import Deck # type: ignore
from deuces import Evaluator # type: ignore

class Game:

    def __init__(self):
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.players = [i for i in range(6) ] #nombre de joueur sur la table 1-6
        self.hand_of_players = [self.deck.draw(2) for _ in self.players] #pour avoir les cartes de chaque joueur
        self.coin ={index:1000 for index in self.players} #pour avoir le nombre de jeton de chaque joueur
        self.btn=0 #pour savoir qui est le bouton , le small blind btn+1 et la big blind btn+2
        self.big_blind=10
        self.small_blind=5
        self.pots = [0 for _ in self.players] #pour avoir le pots de chaque joueur
        self.stop_to_player=0
        self.bet=self.big_blind
        self.nb=[0,3,4,5] # pour savoir combien de carte sont sur la table a chaque tour pre-flop, flop, turn, river
        self.etape=0
        self.coin[self.btn+1]-=self.small_blind
        self.coin[self.btn+2]-=self.big_blind
        self.pots[self.btn+2]=self.big_blind
        self.pots[self.btn+1]=self.small_blind
        self.current_player=self.btn+3
    
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
                 
        elif choice=="check":
            self.increment()
            pass

        elif choice=="call" and (self.coin[self.current_player]>=self.bet):
            self.coin[self.current_player]-=self.bet
            self.pots[self.current_player]+=self.bet
            self.increment()   
                
        elif choice=="all":
                self.pots[self.current_player]+=self.coin[self.current_player]
                self.coin[self.current_player]=0
                self.increment()

        elif self.convert(choice):
            if self.coin[self.current_player]>=self.bet:
                self.bet=self.convert(choice)
                self.coin[self.current_player]-=self.bet
                self.pots[self.current_player]+=self.bet
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
        self.current_player=(self.players.index(self.current_player)+1) if self.players.index(self.current_player)<len(self.players)-1 else 0
        while len(self.hand_of_players[self.current_player])==0:
            self.current_player=(self.players.index(self.current_player)+1) if self.players.index(self.current_player)<len(self.players)-1 else 0


    def check_winner_rounde(self):
        # Fonction pour vérifier le gagnant de la ronde et 
        evaluator= Evaluator()
        self.pots=self.calcul_des_pots()
        score_each_player=[(index,evaluator.evaluate(self.table,player)) 
                           for index, player in enumerate(self.hand_of_players) if (len(player))!=0]
        for pot in self.pots:
            score_each_player_in_pot=[(index,score) 
                                      for index,score in score_each_player if index in pot['players']]
            winner = min(score_each_player_in_pot, key=lambda x: x[1])[0]
            self.coin[winner]+=pot['amount']
        self.init()
    
    def calcul_des_pots(self):
        #au poker on peut avoir plusieurs potss si un joueur n'a pas assez de jeton pour suivre cette fonction calcul les potss
        index_bets=[(index,bet) for index,bet in enumerate(self.pots) if bet>0]
        pots=[]
        while len(index_bets)!=0:
            pot=0
            involved_players = []
            min_bet_tuple = min(index_bets, key=lambda x: x[1])
            for index,bet in index_bets:
                pot+=min_bet_tuple[1]
                new_bet=bet-min_bet_tuple[1]
                if new_bet >= 0:
                    involved_players.append((index, new_bet))
            
            pots.append({'amount':pot,'players':[index for index,new_bet in involved_players]})
            index_bets = [(index, new_bet) for index, new_bet in involved_players if new_bet > 0]
        return pots
    def init(self):
        # Fonction pour initialiser le jeu
        players_to_remove = [player for player, coin in self.coin.items() if coin <= 0]

        # Supprimer les joueurs de self.players
        for player in players_to_remove:
            self.players.remove(player)
        self.coin = {key: value for key, value in self.coin.items() if value > 0}
        self.pots={index: 0 for index in self.players}
        self.etape=0
        self.deck = Deck()
        self.table = self.deck.draw(5)
        self.hand_of_players = [self.deck.draw(2) for _ in range(len(self.players))]
        self.bet=self.big_blind
        self.stop_to_player=0
        self.btn=self.btn+1 if self.btn<len(self.players)-1 else 0
        self.coin[self.players[self.btn+1%len(self.players)]]-=self.small_blind
        self.coin[self.players[self.btn+2%len(self.players)]]-=self.big_blind
        self.current_player=self.players[self.btn+3%len(self.players)]

    # def calcule_du_prochain(self,nbr):
    #     # Fonction pour calculer le prochain joueur BB, SB, BTN
    #     index=self.who_is_who[nbr]
    #     index=self.players.index(index)
    #     index=index+1 if index<len(self.players)-1 else 0
    #     return index