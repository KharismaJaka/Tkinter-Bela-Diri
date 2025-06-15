import csv
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users = [
    {"id": 1, "username": "player1", "password_hash": hash_password("password")},
    {"id": 2, "username": "player2", "password_hash": hash_password("123456")},
    {"id": 3, "username": "player3", "password_hash": hash_password("qwerty")}
]

with open('users.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'username', 'password_hash']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for user in users:
        writer.writerow(user)

        import csv
from datetime import datetime, timedelta

scores = [
    {
        "id": 1,
        "user_id": 1,
        "ao_name": "Naruto",
        "aka_name": "Sasuke",
        "ao_score": 5,
        "aka_score": 3,
        "timestamp": (datetime.now() - timedelta(days=1, hours=9)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 2,
        "user_id": 1,
        "ao_name": "Goku",
        "aka_name": "Vegeta",
        "ao_score": 10,
        "aka_score": 8,
        "timestamp": (datetime.now() - timedelta(days=1, hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 3,
        "user_id": 2,
        "ao_name": "Luffy",
        "aka_name": "Zoro",
        "ao_score": 7,
        "aka_score": 9,
        "timestamp": (datetime.now() - timedelta(days=1, hours=7)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 4,
        "user_id": 3,
        "ao_name": "Ichigo",
        "aka_name": "Rukia",
        "ao_score": 12,
        "aka_score": 11,
        "timestamp": (datetime.now() - timedelta(days=1, hours=6)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 5,
        "user_id": 2,
        "ao_name": "Light",
        "aka_name": "Yagami",
        "ao_score": 15,
        "aka_score": 12,
        "timestamp": (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 6,
        "user_id": 3,
        "ao_name": "Eren",
        "aka_name": "Mikasa",
        "ao_score": 8,
        "aka_score": 6,
        "timestamp": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": 7,
        "user_id": 1,
        "ao_name": "Ash",
        "aka_name": "Pikachu",
        "ao_score": 20,
        "aka_score": 18,
        "timestamp": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    }
]

with open('scores.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'user_id', 'ao_name', 'aka_name', 'ao_score', 'aka_score', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for score in scores:
        writer.writerow(score)

        import csv
from collections import defaultdict

users = {}
with open('users.csv', 'r') as user_file:
    reader = csv.DictReader(user_file)
    for row in reader:
        users[row['id']] = row['username']

player_scores = defaultdict(dict)
with open('scores.csv', 'r') as score_file:
    reader = csv.DictReader(score_file)
    for row in reader:
        user_id = row['user_id']
        total = int(row['ao_score']) + int(row['aka_score'])
        timestamp = row['timestamp']
        
        
        if 'score' not in player_scores[user_id] or total > player_scores[user_id]['score']:
            player_scores[user_id] = {
                'username': users[user_id],
                'score': total,
                'timestamp': timestamp
            }

sorted_scores = sorted(
    player_scores.values(),
    key=lambda x: x['score'],
    reverse=True
)

with open('leaderboard.csv', 'w', newline='') as leaderboard_file:
    writer = csv.writer(leaderboard_file)
    writer.writerow(['rank', 'username', 'total_score', 'last_played'])
    
    for rank, data in enumerate(sorted_scores, 1):
        writer.writerow([
            rank,
            data['username'],
            data['score'],
            data['timestamp']
        ])
