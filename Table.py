from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from deuces import Card
from deuces import Deck
from rich.text import Text


def creation_terrain_de_jeu(game):
    # Créer un tableau principal
    table1 = Table(box=None)
    # Définir les couleurs pour chaque joueur
    colors = ["red", "blue", "green", "magenta", "cyan", "white"]

    for i in range(game.players):  # 6 cellules
        table1.add_column(
            Panel(
                Text("\n ")+ prerty_card_print(game.hand_of_players[i])+Text("\n\n")+Text("jeton: 123"),
                height=6,
                title=f"[bold {colors[i]}]player {i+1} {"D" if i==game.who_is_who[0] else "SM" if i==game.who_is_who[1] else "BB" if i==game.who_is_who[2] else "" }[/bold {colors[i]}]", 
                style=f"{colors[i]}"  
            ),
            vertical="middle",
            justify="center",
            width=20,
        )#n'ayant pas de meilleut solution pour les condition ternaire j'ai du faire comme ca
    
    table2 = Table(box=None)

    table2.add_column(Panel(Text("\n") + prerty_card_print(game.table)+Text("\n\n")+Text("pot: 123"), height=6, title="[bold yellow]table[/bold yellow]",style="yellow"), justify="center",min_width=120)

    

    console = Console()
    console.print(table1, justify="center")
    console.print(table2, justify="center")




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

# def deck_joueur():
#     deck= Deck()
#     hand = []
#     for i in range(6):
#         str_cards= [iint_to_str(card) for card in deck.draw(2)]
#         content= [afficher_carte(card[0],card[1]) for card in str_cards]
#         hand.append(content)
#     print(hand)

