from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table as tb
from rich.live import Live
from rich.prompt import Prompt
import sys
import keyboard # type: ignore
import Game
import Table
import time
import asyncio
#pour l'instant il ne faut pas laisser une touche appuyer trop longtemps
console=Console()
#event = keyboard.read_event()

def convert(nbr):
    if nbr.isdigit():
        return int(nbr)
    else:
        try:
        # Essayer de convertir la valeur en float
            return float(nbr)
            
        except ValueError:
        # Si une erreur se produit (valeur non convertible en float)
            return False

# Fonction pour gérer le timer
def timer(game):
    
    more=""

    tm=20*100
    tmm=20
    with Live(Table.print_choice(game.current_player,tmm),refresh_per_second=4) as live:
        
        while tm >= 0:
            
            if keyboard.is_pressed("r") and more!="raise\n":
                more="raise"
                nbr=0              
                nb=Prompt.ask("aa")
                more=nb
                if(convert(nb)!=False):
                    
                    
                    nbr=convert(nb)
                

            if keyboard.is_pressed("f") and more!="fold\n":
                more="fold\n"
            if keyboard.is_pressed("c") and more!="call\n":
                more="call\n"
            if keyboard.is_pressed("k") and more!="check\n":
                more="check\n"

            if tm%100==0:
                live.update(Table.print_choice(game.current_player,tmm,more),refresh=True)
                tmm-=1
            
                

            time.sleep(1/100)
            
            tm -= 1
    

# Fonction pour gérer l'input de l'utilisateur

def main():
    #la touche k a etait choisi pour check car c etait deja pris par call
    tx_intro=[Text("for raise click r",justify="right"),Text("for fold click f",justify="left"),Text("for call click c"),Text("for check click k")]
    
    console.print(Text("Bienvenue au jeu de poker\n"), justify="center",style="bold red")
    console.print(Text("je vous informe de certaine chose tout d'abord a toute instant pour mettre pause le jeux vous pouvez appuiez sur la touche p"), justify="center")
    merged_text =Text("\n").join(tx_intro)
    table1 = tb(box=None,padding=(2,2))
    table1.add_column(
    Panel(
                merged_text, 
            ),
            
            justify="center",
            min_width=30 
            
        )
    game=Game.game()
    console.print(table1, justify="center")
    
    running=False
    Table.creation_terrain_de_jeu(game)
    timer(game)

    while running:

        if keyboard.is_pressed("q"):
            console.clear()
            console.print(Text("au revoir !"), justify="center" ,style="bold red")
            time.sleep(0.1)
            return
        
        
    
    

if __name__ == "__main__":
    main()