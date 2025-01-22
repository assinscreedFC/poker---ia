from rich.console import Console
from rich.text import Text
import keyboard # type: ignore
from Game import Game
import Table
import asyncio
from time import sleep

TIME_OF_ROUNDE=20

console=Console()




# Fonction pour gérer l'input de l'utilisateur

async def main():
    Table.intro_jeu(console)
    keyboard.wait("Enter")
    console.clear()
    game=Game()
    
    
    running=True
    Table.creation_terrain_de_jeu(console,game)
    

    while running:

        if keyboard.is_pressed("q"):
    
            while keyboard.is_pressed('p'): pass
            console.clear()
            console.print(Text("au revoir !"), justify="center" ,style="bold red")
            return
        
        
        
        choice= Table.timer(console,game,TIME_OF_ROUNDE)
        game.choix_joueur(choice)
        Table.creation_terrain_de_jeu(console,game)
        sleep(0.2)
        if game.check_if_stop_rounde():
            game.next_etape()
    

if __name__ == "__main__":
    asyncio.run(main())