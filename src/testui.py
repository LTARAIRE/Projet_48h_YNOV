import customtkinter as ctk
from tkinter import DoubleVar

# Configuration de CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Thèmes: "blue", "green", "dark-blue"

class BMSInterface(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre principale
        self.title("BMS Interface")
        self.geometry("1200x800")
        self.bind("<Configure>", self.resize_widgets)

        # Création des widgets
        self.create_sidebar()
        self.create_ui()

    def create_sidebar(self):
        """Créer une barre latérale pour naviguer entre les écrans."""
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        sidebar_title = ctk.CTkLabel(self.sidebar, text="Menu", font=("Arial", 20))
        sidebar_title.pack(pady=20)

        self.sidebar_buttons = []
        menu_items = ["Cell Voltages", "Alerts", "Temperatures", "Hardware/Software Versions", "Serial Number", "Battery Stats"]
        for item in menu_items:
            button = ctk.CTkButton(self.sidebar, text=item, command=lambda name=item: self.show_frame(name))
            button.pack(pady=10, padx=20, fill="x")
            self.sidebar_buttons.append(button)

    def create_ui(self):
        """Créer l'interface utilisateur."""
        self.frames = {}

        # Section des voltages des cellules
        self.cell_frame = ctk.CTkFrame(self)
        self.frames["Cell Voltages"] = self.cell_frame

        # Barres de progression pour les cellules
        self.cell_bars = []
        self.cell_voltages = []  # Liste pour les tensions des cellules
        for i in range(13):
            row, col = divmod(i, 2)  # Ajustement pour une meilleure lisibilité (2 colonnes)
            label = ctk.CTkLabel(self.cell_frame, text=f"Cell {i+1}", font=("Arial", 16))
            label.grid(row=row * 2, column=col * 2, pady=20, padx=10, sticky="w")

            # Jauge de progression plus épaisse
            progress_bar = ctk.CTkProgressBar(self.cell_frame, orientation="horizontal", width=300, height=20)
            progress_bar.set(0.5)  # Exemple: 50%
            progress_bar.grid(row=row * 2, column=col * 2 + 1, pady=20, padx=10)
            self.cell_bars.append(progress_bar)

            # Tension associée
            voltage_label = ctk.CTkLabel(self.cell_frame, text="Voltage: 3.7V", font=("Arial", 14))
            voltage_label.grid(row=row * 2 + 1, column=col * 2, columnspan=2, pady=10)
            self.cell_voltages.append(voltage_label)

        # Section des alertes
        self.alert_frame = ctk.CTkFrame(self)
        self.frames["Alerts"] = self.alert_frame
        alert_title = ctk.CTkLabel(self.alert_frame, text="Alerts", font=("Arial", 20))
        alert_title.pack(pady=10)

        self.alert_lights = []
        for i in range(5):
            frame = ctk.CTkFrame(self.alert_frame, height=80)
            frame.pack(pady=10, padx=20, fill="x")

            label = ctk.CTkLabel(frame, text=f"Alert {i+1}", font=("Arial", 18))
            label.pack(side="top", pady=5)

            light = ctk.CTkLabel(frame, text=" ", width=40, height=40, bg_color="red", corner_radius=20)
            light.pack(side="top", pady=5)
            self.alert_lights.append(light)

            # Section des températures
            self.temp_frame = ctk.CTkFrame(self)
            self.frames["Temperatures"] = self.temp_frame
            temp_title = ctk.CTkLabel(self.temp_frame, text="Temperatures", font=("Arial", 20))
            temp_title.pack(pady=10)

            self.temp_vars = []
            self.temp_gauges = []
            for i in range(3):
                frame = ctk.CTkFrame(self.temp_frame, height=100)
                frame.pack(pady=20, padx=20, fill="x")

                # Barres de progression horizontales
                temp_var = DoubleVar(value=25)
                self.temp_vars.append(temp_var)

                temp_gauge = ctk.CTkProgressBar(frame, orientation="horizontal", width=300, height=20)
                temp_gauge.set(temp_var.get() / 100)  # Normaliser la température pour la jauge
                temp_gauge.pack(side="left", padx=20)
                self.temp_gauges.append(temp_gauge)

                # Curseur pour démo
                slider = ctk.CTkSlider(frame, from_=0, to=100, variable=temp_var, orientation="horizontal", width=300)
                slider.pack(side="right", padx=20)

                label = ctk.CTkLabel(frame, text=f"NTC {i + 1}: {temp_var.get()} °C", font=("Arial", 16))
                label.pack(side="top", pady=5)

                # Mettre à jour la jauge et l'étiquette
                temp_var.trace("w", lambda *args, idx=i: self.update_temperature(idx))

        # Section des versions HW/SW
        self.version_frame = ctk.CTkFrame(self)
        self.frames["Hardware/Software Versions"] = self.version_frame
        version_title = ctk.CTkLabel(self.version_frame, text="Hardware / Software Versions", font=("Arial", 20))
        version_title.pack(pady=10)

        self.version_label = ctk.CTkLabel(self.version_frame, text="HW: 1.0, SW: 2.3")
        self.version_label.pack()

        # Section pour le numéro de série
        self.serial_frame = ctk.CTkFrame(self)
        self.frames["Serial Number"] = self.serial_frame
        serial_title = ctk.CTkLabel(self.serial_frame, text="Serial Number", font=("Arial", 20))
        serial_title.pack(pady=10)

        self.serial_label = ctk.CTkLabel(self.serial_frame, text="SN123456789")
        self.serial_label.pack()

        # Section des statistiques de la batterie
        self.stats_frame = ctk.CTkFrame(self)
        self.frames["Battery Stats"] = self.stats_frame
        stats_title = ctk.CTkLabel(self.stats_frame, text="Battery Stats", font=("Arial", 20))
        stats_title.pack(pady=10)

        self.stats_labels = {
            "Capacity": ctk.CTkLabel(self.stats_frame, text="Capacity: 100%"),
            "Health": ctk.CTkLabel(self.stats_frame, text="Health: 95%"),
            "Cycles": ctk.CTkLabel(self.stats_frame, text="Cycles: 300"),
            "Voltage": ctk.CTkLabel(self.stats_frame, text="Voltage: 48.0V")
        }
        for label in self.stats_labels.values():
            label.pack(pady=5)

        # Afficher le premier écran
        self.show_frame("Cell Voltages")

    def update_temperature(self, idx):
        """Mettre à jour la jauge circulaire et l'étiquette en fonction du curseur."""
        temp = self.temp_vars[idx].get()
        self.temp_gauges[idx].set(temp / 100)  # Normaliser pour la jauge
        self.temp_labels[idx].config(text=f"NTC {idx + 1}: {temp:.1f} °C")

    def show_frame(self, frame_name):
        """Afficher une frame spécifique."""
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(pady=20, padx=20, fill="both", expand=True)

    def resize_widgets(self, event):
        """Redimensionner les widgets en fonction de la fenêtre."""
        pass  # Placeholder si besoin de redimensionner les widgets dynamiquement

if __name__ == "__main__":
    app = BMSInterface()

    app.mainloop()
