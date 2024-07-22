import json
import requests
import sqlite3
import time

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

def create_database():
    conn = sqlite3.connect('steam_games.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        steam_game_id INTEGER UNIQUE NOT NULL,
        first_seen DATE NOT NULL
    )
    ''')
    conn.commit()
    return conn

def update_database(conn, games):
    cursor = conn.cursor()
    today = int(time.time())
    
    # Récupérer les steam_game_id existants
    cursor.execute("SELECT steam_game_id FROM games")
    existing_ids = set(row[0] for row in cursor.fetchall())
    
    # Identifier les nouveaux steam_game_id
    new_ids = set(game['appid'] for game in games) - existing_ids
    
    # Préparer les nouvelles entrées
    new_entries = [(game_id, today) for game_id in new_ids]
    
    # Insérer les nouvelles entrées
    cursor.executemany("INSERT INTO games (steam_game_id, first_seen) VALUES (?, ?)", new_entries)
    
    conn.commit()
    print(f"Base de données mise à jour. {len(new_entries)} nouveaux jeux ajoutés le {today}.")


def main():
    # Récupérer la liste des jeux depuis l'API Steam
    games = fetch_steam_games()
    if games:
        # Créer ou se connecter à la base de données
        conn = create_database()
        # Mettre à jour la base de données avec les nouveaux jeux
        update_database(conn, games)
        conn.close()

if __name__ == "__main__":
    main()
    print("Le script a terminé son exécution et va maintenant se fermer.")

