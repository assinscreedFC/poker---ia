from deuces import Deck # type: ignore
from deuces import Evaluator # type: ignore

class Game:

    def __init__(self,players=[1,2,3,4,5,6]):
        self.deck = Deck()
        self.table = self.deck.draw(5)
         
        #pour avoir les cartes de chaque joueur
        #self.info_players contient les informations de chaque joueur notamment son index, ses cartes et ses jetons
        self.info_players = [{"index": index, "hand": self.deck.draw(2), "coin": 1000 ,"btn":False} for index in players]

         #pour savoir qui est le bouton , le small blind btn+1 et la big blind btn+2
        self.big_blind=10
        self.small_blind=5
        self.pots = {index:0 for index in players} #pour avoir le pots de chaque joueur
        self.stop_to_player=0
        self.bet=self.big_blind
        self.nb=[0,3,4,5] # pour savoir combien de carte sont sur la table a chaque tour pre-flop, flop, turn, river
        self.etape=0
        self.info_players[len(players) - 1]["btn"]=True
        self.info_players[self.index_sb()]["coin"]-=self.small_blind
        self.info_players[(self.index_bb())]["coin"]-=self.big_blind
        self.pots[self.info_players[self.index_bb()]["index"]]+=self.big_blind
        self.pots[self.info_players[self.index_sb()]["index"]]+=self.small_blind
        self.current_player=self.index_utg()
    
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
    
    def index_btn(self):
        # Fonction pour retourner l'index du joueur qui est le bouton
        return next((index for index, player in enumerate(self.info_players) if player["btn"]), None)

    def index_sb(self):
        # Fonction pour retourner l'index du joueur qui est le small blind
        return (self.index_btn()+1)%len(self.info_players)
    
    def index_bb(self):
        # Fonction pour retourner l'index du joueur qui est le big blind
        return (self.index_btn()+2)%len(self.info_players)
    def index_utg(self):
        # Fonction pour retourner l'index du joueur qui est l'under the gun
        return (self.index_btn()+3)%len(self.info_players)
    
    def index_current_player(self):
        return self.info_players[self.current_player]["index"]
    
    def choix_joueur(self,choice=""):
        # Fonction pour gérer le choix du joueur
        if choice=="fold":
            self.info_players[self.current_player]["hand"]=[]
            
        elif choice=="check":
            self.increment()
            pass

        elif choice=="call" and (self.info_players[self.current_player]["coin"]>=self.bet):
            self.info_players[self.current_player]["coin"]-=self.bet
            self.pots[self.index_current_player()]+=self.bet
            self.increment()   
                
        elif choice=="all":
                self.pots[self.index_current_player()]+=self.info_players[self.current_player]["coin"]
                self.info_players[self.current_player]["coin"]=0
                self.increment()

        elif self.convert(choice):
            if self.info_players[self.current_player]["coin"]>=self.bet:
                self.bet=self.convert(choice)
                self.info_players[self.current_player]["coin"]-=self.bet

                self.pots[self.index_current_player()]+=self.bet
                self.stop_to_player=1
                
    def increment(self):
        # fonction pour calculer le nombre de joueur apres le dernier raise ou le under the gun
        self.stop_to_player+=1
    def nbr_current_player(self):
        # Fonction pour retourner le nombre du joueur actuel qui n'ont pas fold
        return sum(1 for player in self.info_players if len(player["hand"]) != 0)
        
    def check_if_stop_rounde(self):
        # Fonction pour vérifier si le tour est terminé
        # print(f"stop {self.stop_to_player}")
        # print(self.nbr_current_player())
        return self.stop_to_player==self.nbr_current_player()
    def next_etape(self):
        # Fonction pour passer à l'étape suivante
        #au poker qaunnd on a plus que deux joueur a l'etape 1 l'under the gun jouer puis le bouton a chaque etape suivante en premier
        if len(self.info_players)==2 :
            if self.etape==1:
                self.current_player=(self.index_btn()+1)%len(self.info_players)
        self.stop_to_player=0
        self.etape+=1
        self.bet=0

    def next_player(self):
        # Fonction pour passer au joueur suivant
        self.current_player=(self.current_player+1)%len(self.info_players)
        while len(self.info_players[self.current_player]["hand"])==0:
            self.current_player=(self.current_player+1)%len(self.info_players)



    def check_winner_rounde(self):
        # Fonction pour vérifier le gagnant de la ronde et 
        evaluator= Evaluator()
        self.pots=self.calcul_des_pots()
        score_each_player = [
                            (player["index"], evaluator.evaluate(self.table, player["hand"]))
                            for player in self.info_players
                            if len(player["hand"]) != 0
                        ]
        #parcours la liste des pots et donne le pot au joueur qui a la meilleur main dans le pot
        for pot in self.pots:
            score_each_player_in_pot=[(index,score) 
                                      for index,score in score_each_player if index in pot['players']]
            winner = min(score_each_player_in_pot, key=lambda x: x[1])[0]

            self.update_player(winner,"coin",pot['amount'])
        self.init()
    
    def update_player(self, target_index, key, value):
        """
        Met à jour un champ spécifique dans un joueur donné par son index.
        """
        for player in self.info_players:
            if player["index"] == target_index:
                player[key] += value
                break

    
    def calcul_des_pots(self):
        #au poker on peut avoir plusieurs potss si un joueur n'a pas assez de jeton pour suivre cette fonction calcul les potss
        index_bets= [(index, bet) for index, bet in self.pots.items() if bet > 0]
        pots=[]
        #cree plusieurs pots si un joueur n'a pas assez de jeton pour suivre
        #pots est une liste de dictionnaire contenant le montant du pot et les joueurs qui ont contribué
        """
            il ya autant de pots differents que de valeur different dans self.pots
            chaque pot contient le montant du pot et les joueurs qui ont contribué
            un joueur contribue a un pot si il a misé une valeur superieur ou egale a la valeur minimale des mises des joueurs
            dans le pot
            et a chaque fois on retire la valeur minimale des mises des joueurs dans le pot
            et on recalcule les pots
            jusqua ce que toute les valeurs dans self.pots soient nulles
        """
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
    
    def next_btn(self):
        # passer le bouton au joueur suivant sur la table
        index_btn=self.index_btn()
        self.info_players[index_btn].update({"btn":False})
        index_btn=(index_btn+1)%len(self.info_players)

        while self.info_players[index_btn]["coin"]<=0:
            index_btn=(index_btn+1)%len(self.info_players)
            
        self.info_players[index_btn].update({"btn": True})
    def init(self):
        
        self.next_btn()
        self.info_players=[player for player in self.info_players if player["coin"]>0]
        self.pots={player["index"]:0 for player in self.info_players}
        self.etape=0
        self.deck = Deck()
        self.table = self.deck.draw(5)
        for player in self.info_players:
            player["hand"] = self.deck.draw(2)
        self.bet=self.big_blind
        self.stop_to_player=0
        self.info_players[self.index_sb()]["coin"]-=self.small_blind
        self.info_players[(self.index_bb())]["coin"]-=self.big_blind
        self.pots[self.info_players[self.index_bb()]["index"]]+=self.big_blind
        self.pots[self.info_players[self.index_sb()]["index"]]+=self.small_blind
        self.current_player=self.index_utg()

    