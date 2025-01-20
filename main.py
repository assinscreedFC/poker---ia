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
import sys

console=Console()

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

def handle_key(event):
    print(f"Touche pressée : {event.name}")
    if event.name == "a":
        print("Action spéciale pour la touche 'a'.")
        return True  # Bloque la touche

# Ajouter un listener avec suppression
keyboard.on_press(handle_key, suppress=True)
# Fonction pour gérer le timer
def timer(game,tmm):
    
    more=""
    nbr=0
    if tmm!=20:
        
        nb=Prompt.ask("a")
        more=nb
        if(convert(nb)!=False):
            nbr=convert(nb)
    
    tm=tmm*100
    with Live(Table.print_choice(game.current_player,tmm),refresh_per_second=4) as live:
        
        while tm >= 0:
            
            if keyboard.is_pressed("r"): 
                nb=0
                keyboard.wait("a",suppress=False)
                while keyboard.is_pressed("r"):
                    pass
                
                more="raise"
                live.update("",refresh=True)
                live.stop()
                timer(game,tmm-1)
                return

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
    print("anis")
    return

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
    timer(game,20)

    while running:

        if keyboard.is_pressed("q"):
            while keyboard.is_pressed('p'): pass
            console.clear()
            console.print(Text("au revoir !"), justify="center" ,style="bold red")
            return
        
        
    
    

if __name__ == "__main__":
    main()