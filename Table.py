from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Créer un tableau principal
table1 = Table(box=None)

# Définir les couleurs pour chaque joueur
colors = ["red", "blue", "green", "magenta", "cyan", "white"]

# Ajouter des colonnes avec des couleurs différentes pour le texte et la bordure
for i in range(1, 7):  # 6 cellules
    table1.add_column(
        Panel(
            f"\nColonne {i} : Joueur {i}",
            height=7,
            title=f"[bold {colors[i-1]}]player[/bold {colors[i-1]}]", 
            style=f"{colors[i-1]}"  
        ),
        vertical="middle",
        justify="center",
        width=20,
    )

# Créer un second tableau
table2 = Table(box=None)

# Ajouter des colonnes au second tableau
table2.add_column(Panel("\n[white]Colonne 2 : Joueur 2[/white]", height=5, title="[bold yellow]table[/bold yellow]", style="yellow"), justify="center",min_width=120)


# Configurer un affichage dans la console
console = Console()
console.print(table1, justify="center")
console.print(table2, justify="center")
