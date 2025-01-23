import can

# Configuration des trames à surveiller et leurs cellules associées
TRAMES_CONFIG = {
    0x200: ['Cellule 1', 'Cellule 2', 'Cellule 3', 'Cellule 4'],
    0x201: ['Cellule 5', 'Cellule 6', 'Cellule 7', 'Cellule 8'],
    0x202: ['Cellule 9', 'Cellule 10', 'Cellule 11', 'Cellule 12'],
    0x203: ['Cellule 13'],
    0x204: ['Température 1', 'Température 2', 'Température 3'],
    0x205: ['Vpack', 'Vmin', 'Vmax', 'Vbatt'],
    0x206: ['Alarme Vmin', 'Alarme Vmax', 'Alarme Tmin', 'Alarme Tmax', 'Alarme Vbatt', 'Alarme SN'],
    0x300: ['Numéro de Série'],
    0x301: ['Version HW', 'Version SW']
}

# Classe pour gérer le stockage des trames
def initialiser_valeurs_par_defaut():
    valeurs = {}
    for trame_id, cellules in TRAMES_CONFIG.items():
        valeurs[trame_id] = {cellule: '-' for cellule in cellules}
    return valeurs

class GestionTrames:
    def __init__(self):
        self.valeurs_trames = initialiser_valeurs_par_defaut()

    def mettre_a_jour(self, trame_id, valeurs):
        if trame_id in self.valeurs_trames:
            self.valeurs_trames[trame_id].update(valeurs)

    def recuperer_valeurs(self):
        return self.valeurs_trames

    def afficher_valeurs(self):
        print("\n--- État actuel des trames ---")
        for trame_id, cellules in self.valeurs_trames.items():
            print(f"Trame {hex(trame_id)} :")
            for cellule, valeur in cellules.items():
                print(f"  - {cellule} : {valeur}")
        print("------------------------------\n")

# Fonction pour décoder une trame avec gestion des erreurs
def decoder_trame(message):
    trame_id = message.arbitration_id
    if trame_id in TRAMES_CONFIG:
        cellules = TRAMES_CONFIG[trame_id]
        valeurs = {}

        # Validation de la longueur de la trame
        if len(message.data) < 8:
            print(f"Erreur : Trame {hex(trame_id)} malformée (données insuffisantes : {len(message.data)} octets).")
            return trame_id, {cellule: 'Erreur' for cellule in cellules}

        try:
            if trame_id == 0x200 or trame_id == 0x201 or trame_id == 0x202:
                # Décodage des tensions
                for i, cellule in enumerate(cellules):
                    start_byte = i * 2
                    end_byte = start_byte + 2
                    if end_byte <= len(message.data):
                        valeurs[cellule] = int.from_bytes(message.data[start_byte:end_byte], byteorder='big') * 0.001
                    else:
                        valeurs[cellule] = '-'

            elif trame_id == 0x203:
                # Décodage de la tension unique V13
                valeurs['Cellule 13'] = int.from_bytes(message.data[6:8], byteorder='big') * 0.001

            elif trame_id == 0x204:
                # Décodage des températures
                for i, cellule in enumerate(cellules):
                    start_byte = (2 + i * 2)
                    end_byte = start_byte + 2
                    valeurs[cellule] = int.from_bytes(message.data[start_byte:end_byte], byteorder='big') * 0.1

            elif trame_id == 0x205:
                # Décodage des statistiques batterie
                for i, cellule in enumerate(cellules):
                    start_byte = i * 2
                    end_byte = start_byte + 2
                    valeurs[cellule] = int.from_bytes(message.data[start_byte:end_byte], byteorder='big') * 0.001

            elif trame_id == 0x206:
                # Décodage des alarmes (bits spécifiques)
                valeurs['Alarme Vmin'] = 'Actif' if message.data[0] & 0x01 else 'Inactif'
                valeurs['Alarme Vmax'] = 'Actif' if message.data[0] & 0x02 else 'Inactif'
                valeurs['Alarme Tmin'] = 'Actif' if message.data[1] & 0x01 else 'Inactif'
                valeurs['Alarme Tmax'] = 'Actif' if message.data[1] & 0x02 else 'Inactif'
                valeurs['Alarme Vbatt'] = 'Actif' if message.data[2] & 0x01 else 'Inactif'
                valeurs['Alarme SN'] = 'Actif' if message.data[2] & 0x02 else 'Inactif'

            elif trame_id == 0x300:
                # Décodage du numéro de série
                valeurs['Numéro de Série'] = message.data.hex()

            elif trame_id == 0x301:
                # Décodage des versions HW et SW
                valeurs['Version HW'] = f"{message.data[3]}.{message.data[4]}"
                valeurs['Version SW'] = f"{message.data[5]}.{message.data[6]}.{message.data[7]}"

        except (IndexError, ValueError) as e:
            print(f"Erreur lors du décodage de la trame {hex(trame_id)} : {e}")
            valeurs = {cellule: 'Erreur' for cellule in cellules}

        return trame_id, valeurs

    print(f"Trame inconnue : {hex(trame_id)}")
    return None, None

# Fonction principale
def main():
    gestionnaire = GestionTrames()

    with can.interface.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000) as bus:
        print("En attente des trames...")

        # Afficher immédiatement les valeurs par défaut
        gestionnaire.afficher_valeurs()

        try:
            while True:
                message = bus.recv(timeout=1)
                if message:
                    # Décoder la trame et mettre à jour les valeurs
                    trame_id, valeurs = decoder_trame(message)
                    if trame_id is not None:
                        gestionnaire.mettre_a_jour(trame_id, valeurs)

                    # Afficher immédiatement les valeurs mises à jour
                    gestionnaire.afficher_valeurs()

        except can.CanError as e:
            print(f"Erreur CAN : {e}")
        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur.")
        finally:
            print("Connexion fermée proprement.")

if __name__ == "__main__":
    main()