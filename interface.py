
from tkinter import *
from tkinter import Tk, Label, Button

def create_interface():
    root = Tk()
    root.title("Interface Graphique")
    label = Label(root, text="Bienvenue dans l'interface graphique !")
    label.pack()
    button = Button(root, text="Fermer", command=root.destroy)
    button.pack()
    root.mainloop()
# Configuration du thème sombre
dark_theme = {
    'background': '#000000',  # Noir pour le fond
    'foreground': '#00FF00',  # Vert pour le texte
}
# Fonction pour créer et afficher l'interface graphique
def create_gui():
    root = Tk()
    root.title("MyDarkApp")
    root.config(bg=dark_theme['background'])
    label = Label(root, text="Bienvenue dans l'application sombre !", bg=dark_theme['background'], fg=dark_theme['foreground'])
    label.pack(pady=20)
    button = Button(root, text="Cliquez-moi", bg=dark_theme['background'], fg=dark_theme['foreground'], command=root.destroy)
    button.pack(pady=10)
    root.mainloop()
# Appel de la fonction pour créer et afficher l'interface graphique
create_gui()

