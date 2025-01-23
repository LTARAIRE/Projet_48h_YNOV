import tkinter as tk
from tkinter import ttk
from Trame import GestionTrames, decoder_trame
import can

class BMSInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("BMS Interface")
        self.root.geometry("1200x800")
        self.root.config(background='#C1DBD8')

        # Gestionnaire de trames
        self.gestionnaire = GestionTrames()

        # Références des widgets pour mise à jour dynamique
        self.entries = {}

        # Initialiser l'interface utilisateur
        self.create_ui()

        # Configurer le bus CAN
        self.bus = can.interface.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000)

        # Lancer la mise à jour périodique
        self.update_values()

    def create_ui(self):
        """Créer l'interface utilisateur."""
        # Frame: Cell voltages
        cell_frame = tk.LabelFrame(self.root, text="Cell Voltages", font=("Arial", 10, "bold"), background='#C1DBD8')
        cell_frame.place(x=20, y=20, width=500, height=250)

        for i in range(13):
            row, col = divmod(i, 4)
            tk.Label(cell_frame, text=f"V{i + 1}", background='#C1DBD8').grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")
            entry_voltage = tk.Entry(cell_frame, width=10, state="readonly")
            entry_voltage.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            self.entries[f"Cellule {i + 1}"] = entry_voltage

        # Frame: Temperatures
        temp_frame = tk.LabelFrame(self.root, text="Temperatures", font=("Arial", 10, "bold"), background='#C1DBD8')
        temp_frame.place(x=20, y=280, width=500, height=100)

        for i in range(3):
            tk.Label(temp_frame, text=f"NTC {i + 1}", background='#C1DBD8').grid(row=0, column=i * 2, padx=5, pady=5, sticky="w")
            entry_temp = tk.Entry(temp_frame, width=15, state="readonly")
            entry_temp.grid(row=0, column=i * 2 + 1, padx=5, pady=5)
            self.entries[f"Température {i + 1}"] = entry_temp

        # Frame: Global measures
        global_frame = tk.LabelFrame(self.root, text="Global Measures", font=("Arial", 10, "bold"), background='#C1DBD8')
        global_frame.place(x=20, y=390, width=500, height=120)

        measures = ["Vpack", "Vmin", "Vmax", "Tmin", "Tmax"]
        for i, measure in enumerate(measures):
            tk.Label(global_frame, text=measure, background='#C1DBD8').grid(row=i // 2, column=(i % 2) * 2, padx=5, pady=5, sticky="w")
            entry_measure = tk.Entry(global_frame, width=15, state="readonly")
            entry_measure.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=5)
            self.entries[measure] = entry_measure

        # Frame: Alerts
        alert_frame = tk.LabelFrame(self.root, text="Alerts", font=("Arial", 10, "bold"), background='#C1DBD8')
        alert_frame.place(x=600, y=20, width=450, height=200)

        alert_types = ["Vmin", "Vmax", "Tmin", "Tmax", "Vbatt", "SN"]
        for i, alert in enumerate(alert_types):
            tk.Label(alert_frame, text=f"Alarme {alert}", background='#C1DBD8').grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry_alert = tk.Entry(alert_frame, width=15, state="readonly")
            entry_alert.grid(row=i, column=1, padx=5, pady=5)
            self.entries[f"Alarme {alert}"] = entry_alert

        # Frame: Hardware/Software Versions
        version_frame = tk.LabelFrame(self.root, text="Hardware/Software Versions", font=("Arial", 10, "bold"), background='#C1DBD8')
        version_frame.place(x=600, y=240, width=450, height=100)

        versions = ["Version HW", "Version SW"]
        for i, version in enumerate(versions):
            tk.Label(version_frame, text=version, background='#C1DBD8').grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry_version = tk.Entry(version_frame, width=20, state="readonly")
            entry_version.grid(row=i, column=1, padx=5, pady=5)
            self.entries[version] = entry_version

        # Frame: Serial Number
        serial_frame = tk.LabelFrame(self.root, text="Serial Number", font=("Arial", 10, "bold"), background='#C1DBD8')
        serial_frame.place(x=600, y=360, width=450, height=80)

        tk.Label(serial_frame, text="Numéro de Série", background='#C1DBD8').grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_serial = tk.Entry(serial_frame, width=30, state="readonly")
        entry_serial.grid(row=0, column=1, padx=5, pady=5)
        self.entries["Numéro de Série"] = entry_serial

    def update_values(self):
        """Met à jour les valeurs affichées dans l'interface."""
        try:
            message = self.bus.recv(timeout=0.1)  # Lecture non bloquante
            if message:
                trame_id, valeurs = decoder_trame(message)
                if trame_id is not None:
                    self.gestionnaire.mettre_a_jour(trame_id, valeurs)

            # Mettre à jour les champs
            valeurs = self.gestionnaire.recuperer_valeurs()
            for trame_id, cellules in valeurs.items():
                for cellule, valeur in cellules.items():
                    if cellule in self.entries:
                        entry = self.entries[cellule]
                        entry.config(state="normal")
                        entry.delete(0, tk.END)
                        entry.insert(0, str(valeur))
                        entry.config(state="readonly")

        except can.CanError as e:
            print(f"Erreur CAN : {e}")

        # Replanifie cette méthode pour une exécution continue
        self.root.after(100, self.update_values)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMSInterface(root)
    root.mainloop()