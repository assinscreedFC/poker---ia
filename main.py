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

def main():
    Table.intro_jeu(console)
    
    keyboard.wait("Enter")
    console.input()
    console.clear()
    game=Game()
    
    
    running=True
    Table.creation_terrain_de_jeu(console,game)
    

    while running:

        if keyboard.is_pressed("q"):
            keyboard.block_key("q")
            while keyboard.is_pressed('p'): pass
            keyboard.unblock_key("q")
            console.clear()
            console.print(Text("au revoir !"), justify="center" ,style="bold red")
            return
        
        
        
        choice= Table.timer(console,game,TIME_OF_ROUNDE)
        game.choix_joueur(choice)
        game.next_player()
        sleep(0.5)
        print(game.current_player)
        if game.check_if_stop_rounde():
            game.next_etape()
            if game.etape==len(game.nb):
                game.check_winner_rounde()
            game.nbr_current_player()
            print(game.stop_to_player)
        
        sleep(0.5)
        Table.creation_terrain_de_jeu(console,game)
        
        
        
    

if __name__ == "__main__":
    main()