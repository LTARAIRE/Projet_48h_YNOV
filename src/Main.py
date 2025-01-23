from UI import BMSInterface
import tkinter as tk

def main():
    # Initialiser Tkinter
    root = tk.Tk()

    # Lancer l'application BMS Interface
    app = BMSInterface(root)

    # Boucle principale de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
