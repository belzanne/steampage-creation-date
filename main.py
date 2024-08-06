import json
import requests
import sqlite3
import time
import csv

# Faire la requête GET
URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
response = requests.get(URL)    

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le JSON
    data = json.loads(response.text)
    
    # Extraire la liste des apps
    apps_list = data['applist']['apps']
    
    # Créer une liste pour stocker uniquement les ID
    game_ids = [app['appid'] for app in apps_list]
    game_ids.sort()
    
    # Afficher le nombre total de jeux
    print(f"Nombre total de jeux : {len(game_ids)}")

def fetch_steam_games():
    #response = requests.get(URL)
    if response.status_code == 200:
        return response.json()['applist']['apps']
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return None

# Remplacer la fonction update_database par update_csv_file
def update_csv_file(csv_file, games):
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        existing_ids = set(row[1] for row in reader)
    
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        last_id = max(int(row[0]) for row in reader) if reader else 0
    
    new_entries = []
    current_time = int(time.time())
    for game in games:
        if str(game['appid']) not in existing_ids:
            last_id += 1
            new_entries.append([last_id, game['appid'], current_time])
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_entries)
    
    print(f"CSV file updated. {len(new_entries)} new games added.")


def main(csv_file):
    # Récupérer la liste des jeux depuis l'API Steam
    games = fetch_steam_games()
    if games:
        # Mettre à jour la base de données avec les nouveaux jeux
        update_csv_file(csv_file, games)

if __name__ == "__main__":
    main("steam_games.csv")
    print("Le script a terminé son exécution et va maintenant se fermer.")