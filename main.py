from rich.console import Console
from rich.text import Text
import keyboard # type: ignore
import Game
import Table

TIME_OF_ROUNDE=20

console=Console()




# Fonction pour gérer l'input de l'utilisateur

def main():
    Table.intro_jeu(console)
    keyboard.wait("Enter")
    console.clear()
    game=Game.game()
    
    
    running=False
    Table.creation_terrain_de_jeu(console,game)
    Table.timer(console,game,TIME_OF_ROUNDE)

    while running:

        if keyboard.is_pressed("q"):

            while keyboard.is_pressed('p'): pass
            console.clear()
            console.print(Text("au revoir !"), justify="center" ,style="bold red")
            return
        
        
    
    

if __name__ == "__main__":
    main()