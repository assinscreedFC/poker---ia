from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table as tb
from rich.live import Live
from rich.prompt import Prompt
import keyboard # type: ignore
import Game
import Table
import time
import asyncio
#pour l'instant il ne faut pas laisser une touche appuyer trop longtemps
console=Console()

def print_choice(player,tm):
    table2 = tb(box=None,expand=True)
    table2.add_column(
            Panel(
                Text(f"\nRaise (r)\tFold (f)\tCall (c)\tCheck (k)\n \nseconds remaining: {tm}",justify="center",style="yellow white",),
                style="yellow white",
                title=f"[bold yellow]choice for player {player}[/bold yellow]"
            ),
            justify="center",
            width=120
        )
    return table2

# Fonction pour gérer le timer
async def timer(game):
    tm=20
    with Live(print_choice(game.current_player,tm),refresh_per_second=1) as live:
        while tm >= 0:
            live.update(print_choice(game.current_player,tm))
            if keyboard.is_pressed("r"):
                pr=await Prompt.ask("how much do you want to raise",default="0")
                console.print(f"player {game.current_player} raised {pr}")
                break
                time.sleep(0.2)

            time.sleep(1)
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
    async timer(game)

    while running:

        if keyboard.is_pressed("q"):
            console.clear()
            console.print(Text("au revoir !"), justify="center" ,style="bold red")
            time.sleep(0.1)
            return
        
        
    
    

if __name__ == "__main__":
    main()