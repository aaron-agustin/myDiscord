from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Toplevel, Text, Scrollbar
from hashlib import sha256
import mysql.connector
from datetime import datetime


# Configurations de la base de données
db_config = {
    'user': 'root',
    'password': 'Mot de Passe',
    'host': 'localhost',
    'database': 'MyDiscord'
}

# Fonction pour gérer l'inscription
def inscription():
    nom = nom_var.get()
    prenom = prenom_var.get()
    mail = mail_var.get()
    mot_de_passe = sha256(mot_de_passe_var.get().encode()).hexdigest()

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Vérifiez d'abord si l'utilisateur avec le même e-mail existe
        cursor.execute("SELECT * FROM information_utilisateur WHERE mail=%s", (mail,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Erreur d'inscription", "Un utilisateur avec cet e-mail existe déjà.")
        else:
            # S'il n'existe pas, procédez à l'inscription
            cursor.execute("INSERT INTO information_utilisateur (nom, prenom, mail, mot_de_passe) VALUES (%s, %s, %s, %s)", (nom, prenom, mail, mot_de_passe))
            connection.commit()
            messagebox.showinfo("Inscription réussie", "Votre compte a été créé avec succès.")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur d'inscription", f"Erreur MySQL: {err}")


# Fonction pour gérer la connexion
def connexion():
    mail = mail_var.get()
    mot_de_passe = sha256(mot_de_passe_var.get().encode()).hexdigest()

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM information_utilisateur WHERE mail=%s AND mot_de_passe=%s", (mail, mot_de_passe))
        utilisateur = cursor.fetchone()

        if utilisateur:
            messagebox.showinfo("Connexion réussie", "Vous êtes connecté avec succès.")
            # Redirigez l'utilisateur vers la nouvelle interface du canal
            canal_interface()
        else:
            messagebox.showerror("Erreur de connexion", "L'adresse e-mail ou le mot de passe est incorrect.")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur de connexion", f"Erreur MySQL: {err}")

# Fonction pour afficher l'interface du canal
def canal_interface():
    canal_window = Toplevel(root)
    canal_window.title("Canal")

    # Zone de texte pour afficher les messages
    message_history = Text(canal_window, wrap="word", height=20, width=50)
    message_history.pack(pady=10)

    # Champ de texte pour saisir un nouveau message
    new_message_entry = Text(canal_window, wrap="word", height=3, width=50)
    new_message_entry.pack(pady=10)

    # Bouton pour envoyer un message
    send_button = Button(canal_window, text="Envoyer", command=lambda: envoyer_message(message_history, new_message_entry))
    send_button.pack(pady=10)

def envoyer_message(message_history, new_message_entry):
    message = new_message_entry.get("1.0", "end-1c").strip()
    if message:
        # Obtenez l'heure actuelle
        now = datetime.now()
        
        # Ajoutez le nouveau message à l'historique
        message_history.insert("1.0", f"{now.strftime('%H:%M:%S')} - {message}\n")
        
        # Effacez le champ de texte pour un nouveau message
        new_message_entry.delete("1.0", "end")
    else:
        messagebox.showwarning("Envoyer un message", "Veuillez entrer un message avant d'envoyer.")

# Configuration de l'interface graphique principale
root = Tk()
root.title("MyDiscord")

# Variables pour stocker les données du formulaire
nom_var = StringVar()
prenom_var = StringVar()
mail_var = StringVar()
mot_de_passe_var = StringVar()

# Labels et Entrées pour les informations utilisateur
Label(root, text="Nom:").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nom_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Prénom:").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=prenom_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="E-mail:").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=mail_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Mot de passe:").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=mot_de_passe_var, show="*").grid(row=3, column=1, padx=10, pady=5)

# Boutons pour l'inscription et la connexion
Button(root, text="S'inscrire", command=inscription).grid(row=4, column=0, columnspan=2, pady=10)
Button(root, text="Se connecter", command=connexion).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()