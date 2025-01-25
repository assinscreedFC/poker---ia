from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import keyboard # type: ignore
from rich.live import Live
from rich.prompt import Prompt
import time
import asyncio



def intro_jeu(console):
    #afficher l'introduction du jeu
    #la touche k a etait choisi pour check car c etait deja pris par call
    tx_intro=[Text("for raise click r",justify="right"),Text("for fold click f",justify="left"),Text("for call click c"),Text("for check click k")]
    
    console.print(Text("Bienvenue au jeu de poker\n"), justify="center",style="bold red")
    console.print(Text("je vous informe de certaine chose tout d'abord a toute instant pour mettre pause le jeux vous pouvez appuiez sur la touche p"), justify="center")
    merged_text =Text("\n").join(tx_intro)
    table1 = Table(box=None,padding=(2,2))
    table1.add_column(
    Panel(
                merged_text, 
            ),
            
            justify="center",
            min_width=30 
            
        )
    console.print(table1, justify="center")




def creation_terrain_de_jeu(console,game):
    # Créer un tableau principal
    table1 = Table(box=None)
    # Définir les couleurs pour chaque joueur
    colors = ["red", "blue", "green", "magenta", "cyan", "white"]

    for i in range(len(game.players)):  # 6 cellules
        table1.add_column(
            Panel(
                Text("\n ")+ prerty_card_print(game.hand_of_players[i])+Text("\n\n")+Text(f"jeton: {game.coin[i]}"),
                height=6,
                title=f"[bold {colors[i]}]player {i+1} {"D" if i==game.who_is_who[0] else "SM" if i==game.who_is_who[1] else "BB" if i==game.who_is_who[2] else "" }[/bold {colors[i]}]", 
                style=f"{colors[i]}"  
            ),
            vertical="middle",
            justify="center",
            width=20,
        )#n'ayant pas de meilleut solution pour les condition ternaire j'ai du faire comme ca
    
    table2 = Table(box=None)

    table2.add_column(Panel(Text("\n") + prerty_card_print(game.table[i] for i in range(game.nb[game.etape]) )+Text("\n\n")+Text(f"pots: {sum(game.pots)}"), height=6, title="[bold yellow]table[/bold yellow]",style="yellow"), justify="center",min_width=120)

    

    
    console.print(table1, justify="center")
    console.print(table2, justify="center")

def print_choice(player,bet,coin,tm,more_text=None):
    #afficher les choix des joueurs
    table2 = Table(box=None,expand=True)
    table2.add_column(
            Panel(
                Text(f"\n{"Raise (r)" if coin>bet else "all in (A)"}\tFold (f)\t{"Call (c)" if coin>=bet else""}\t{"Check (k)" if bet==0 else ""} \n \n"
                     f"{""if more_text==None else more_text + "\n"}"
                     f"seconds remaining: {tm}\n"
                     
                     ,justify="center",style="yellow white",),
                style="yellow white",
                title=f"[bold yellow]choice for player {player+1}[/bold yellow]"
            ),
            justify="center",
            max_width=120
        )
    return table2

#---------------------------------fonction pour afficher les cartes jolie---------------------------------

INT_SUIT_TO_CHAR_SUIT = 'xshxdxxxc'
STR_RANKS = '23456789TJQKA'
def iint_to_str(card_int):
        rank_int = gget_rank_int(card_int)
        suit_int = gget_suit_int(card_int)
        return STR_RANKS[rank_int] + INT_SUIT_TO_CHAR_SUIT[suit_int]

def gget_rank_int(card_int):
        return (card_int >> 8) & 0xF

    
def gget_suit_int(card_int):
        return (card_int >> 12) & 0xF


#couleurs = {"h": "red", "d": "red", "c": "green", "s": "blue"}
def afficher_carte(valeur, couleur):
    symboles = {"h": "♥", "d": "♦", "c": "♣", "s": "♠"}
    couleurs = {"h": "red", "d": "black", "c": "green", "s": "blue"}
    if valeur == "T":
        valeur = "10"
    texte = Text(f"{valeur} {symboles[couleur]}", style=couleurs[couleur])
    return texte


def prerty_card_print(hand):
    str_cards= [iint_to_str(card) for card in hand]
    content= [afficher_carte(card[0],card[1]) for card in str_cards]
    combined_text = Text()
        
    combined_text=Text(" | ", ).join(content) 
    # Créer un panel avec le texte combiné

    return combined_text
#---------------------------------------------------------------------------------------------------
# def deck_joueur():
#     deck= Deck()
#     hand = []
#     for i in range(6):
#         str_cards= [iint_to_str(card) for card in deck.draw(2)]
#         content= [afficher_carte(card[0],card[1]) for card in str_cards]
#         hand.append(content)
#     print(hand)


def place_the_bet(console,game):
    nbr=""#initialise comme chaine de caractere pour que la boucle while se lance
    keyboard.send("Enter")
    input()
    console.clear()
    nbr=Prompt.ask("entrer la valeur de la mise")
    console.clear()
    while game.convert(nbr)==False or game.convert(nbr)<=game.bet:

        nbr=Prompt.ask("entrer une valeur reel positif s'il vous plait superieur strictement a la dernier mise",default="0")
        console.clear()
        more=nbr

    return nbr
    

def timer(console,game,tmm):
    # Fonction pour gérer le timer du jeu et permettre aux joueurs de choisir leur action
    more=""
    keyboard.block_key("r")
    tm=tmm*100
    with Live(print_choice(game.current_player,game.bet,game.coin[game.current_player],tmm),refresh_per_second=4) as live:
        if game.coin[game.current_player]<=0:
                return "check"
        while tm >= 0:
            
            if keyboard.is_pressed("r") and game.coin[game.current_player]>game.bet: 
                while keyboard.is_pressed("r"):
                    pass
                keyboard.unblock_key("r")
                more="raise"
                stop_live(live)
                
                return place_the_bet(console,game)

            if keyboard.is_pressed("a") and game.coin[game.current_player]<=game.bet:
                more="all"
                stop_live(live)
                return "all"
            
            if keyboard.is_pressed("f") and more!="fold\n":
                more="fold\n"
                stop_live(live)

                return "fold"
            if keyboard.is_pressed("c") and more!="call\n":
                more="call\n"
                stop_live(live)
                return "call"
            if keyboard.is_pressed("k") and more!="check\n" and game.bet==0:
                more="check\n"
                stop_live(live)
                return "check"

            if tm%100==0:
                live.update(print_choice(game.current_player,game.bet,game.coin[game.current_player],tmm,more),refresh=True)
                tmm-=1
            
            time.sleep(1/100)
            tm -= 1
    return "fold"

def stop_live(live):
    live.update("",refresh=True)
    live.stop()
    live.console.clear()
