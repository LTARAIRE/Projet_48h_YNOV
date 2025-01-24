import tkinter as tk

def dessiner_batterie(canvas, x, y, largeur, hauteur, pourcentage):
    """Dessine un rectangle représentant une cellule de batterie."""
    # Dessiner le contour de la batterie
    canvas.create_rectangle(x, y, x + largeur, y + hauteur, outline="black", width=2)
    # Calculer la hauteur du niveau de charge
    hauteur_charge = (hauteur - 4) * pourcentage / 100
    # Dessiner le niveau de charge
    canvas.create_rectangle(x + 2, y + (hauteur - 2 - hauteur_charge), x + largeur - 2, y + hauteur - 2, fill="green")

def mettre_a_jour_batterie(canvas, rect_id, pourcentage, x, y, largeur, hauteur):
    """Met à jour un rectangle représentant une cellule de batterie."""
    # Effacer l'ancien niveau de charge
    canvas.delete(rect_id)
    # Calculer la nouvelle hauteur du niveau de charge
    hauteur_charge = (hauteur - 4) * pourcentage / 100
    # Dessiner le nouveau niveau de charge
    rect_id = canvas.create_rectangle(x + 2, y + (hauteur - 2 - hauteur_charge), x + largeur - 2, y + hauteur - 2, fill="green")
    return rect_id

# Créer la fenêtre principale
root = tk.Tk()
root.title("Test Représentation de la charge des cellules")

# Créer un canvas pour dessiner les batteries
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

# Exemple de données de tension des cellules (en volts)
tensions = [3.5, 3.7, 3.6, 3.2, 3.9]
import tkinter as tk

def dessiner_batterie(canvas, x, y, largeur, hauteur, pourcentage):
    """Dessine un rectangle représentant une cellule de batterie."""
    # Dessiner le contour de la batterie
    canvas.create_rectangle(x, y, x + largeur, y + hauteur, outline="black", width=2)
    # Calculer la hauteur du niveau de charge
    hauteur_charge = (hauteur - 4) * pourcentage / 100
    # Dessiner le niveau de charge
    rect_id = canvas.create_rectangle(x + 2, y + (hauteur - 2 - hauteur_charge), x + largeur - 2, y + hauteur - 2, fill="green")
    return rect_id

def mettre_a_jour_batterie(canvas, rect_id, x, y, largeur, hauteur, pourcentage):
    """Met à jour un rectangle représentant une cellule de batterie."""
    # Effacer l'ancien niveau de charge
    canvas.delete(rect_id)
    # Calculer la nouvelle hauteur du niveau de charge
    hauteur_charge = (hauteur - 4) * pourcentage / 100
    # Dessiner le nouveau niveau de charge
    rect_id = canvas.create_rectangle(x + 2, y + (hauteur - 2 - hauteur_charge), x + largeur - 2, y + hauteur - 2, fill="green")
    return rect_id

# Callback pour mettre à jour le niveau de charge
def update_charge():
    try:
        # Récupérer la valeur entrée
        valeur = float(entry_tension.get())
        pourcentage = max(0, min(100, (valeur - tension_min) / (tension_max - tension_min) * 100))
        # Mettre à jour le rectangle
        global rect_id
        rect_id = mettre_a_jour_batterie(canvas, rect_id, x, y, largeur, hauteur, pourcentage)
    except ValueError:
        print("Veuillez entrer une valeur valide.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Test Représentation de la charge des cellules")

# Créer un canvas pour dessiner la batterie
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Définir les dimensions et la position du rectangle de la batterie
x = 150
y = 50
largeur = 100
hauteur = 200

# Valeurs de tension
tension_min = 3.0
tension_max = 4.2

# Dessiner une batterie initiale avec un pourcentage de charge de 50%
rect_id = dessiner_batterie(canvas, x, y, largeur, hauteur, 50)

# Champ pour entrer une nouvelle tension
frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

tk.Label(frame_controls, text="Tension (V) :").grid(row=0, column=0, padx=5)
entry_tension = tk.Entry(frame_controls)
entry_tension.grid(row=0, column=1, padx=5)

# Bouton pour mettre à jour la batterie
btn_update = tk.Button(frame_controls, text="Mettre à jour", command=update_charge)
btn_update.grid(row=0, column=2, padx=5)

# Lancer la boucle principale
root.mainloop()
tension_min = 3.0
tension_max = 4.2

# Dessiner les batteries
x = 50
y = 50
largeur = 80
hauteur = 200
espace = 20

for i, tension in enumerate(tensions):
    # Calculer le pourcentage de charge basé sur la tension
    pourcentage = max(0, min(100, (tension - tension_min) / (tension_max - tension_min) * 100))
    # Dessiner la batterie
    dessiner_batterie(canvas, x, y, largeur, hauteur, pourcentage)
    x += largeur + espace

# Lancer la boucle principale
root.mainloop()
