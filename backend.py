import csv
from datetime import datetime
import os

class CSVHandler:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # File paths
        self.team_members_file = os.path.join(self.data_dir, "team_members.csv")
        self.scoreboard_file = os.path.join(self.data_dir, "scoreboard_data.csv")
        self.settings_file = os.path.join(self.data_dir, "settings.csv")
        self.feedback_file = os.path.join(self.data_dir, "feedback_log.csv")
        self.history_file = os.path.join(self.data_dir, "game_history.csv")
        
        # Initialize files if they don't exist
        self._initialize_files()

    def _initialize_files(self):
        """Create CSV files with headers if they don't exist"""
        # Team members
        if not os.path.exists(self.team_members_file):
            with open(self.team_members_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'nim'])
                writer.writerows([
                    ['Elsy Aliffia Sirony Putri', '2417051025'],
                    ['Kharisma Jaka Harum', '2417051068'],
                    ['Rheal Iftiqar Rozak', '2417051029'],
                    ['Yulia Nuritnasari', '2457051008']
                ])
        
        # Scoreboard data
        if not os.path.exists(self.scoreboard_file):
            with open(self.scoreboard_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['team_name', 'score', 'last_updated'])
                writer.writerow(['Naruto', '0', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['Sasuke', '0', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        # Settings
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['setting_name', 'value'])
                writer.writerow(['theme', 'dark'])
                writer.writerow(['data_privacy', 'False'])
        
        # Feedback log (just create empty with header)
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'feedback_message'])
        
        # Game history (just create empty with header)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['start_time', 'end_time', 'winner', 'ao_score', 'aka_score'])

    def load_team_members(self):
        """Load team members from CSV"""
        team_members = []
        with open(self.team_members_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                team_members.append((row['name'], row['nim']))
        return team_members

    def load_scoreboard_data(self):
        """Load scoreboard data from CSV"""
        teams = {}
        with open(self.scoreboard_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                teams[row['team_name']] = {
                    'score': int(row['score']),
                    'last_updated': row['last_updated']
                }
        return teams

    def save_scoreboard_data(self, ao_name, ao_score, aka_name, aka_score):
        """Save current scoreboard data to CSV"""
        with open(self.scoreboard_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['team_name', 'score', 'last_updated'])
            writer.writerow([ao_name, ao_score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([aka_name, aka_score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    def load_settings(self):
        """Load settings from CSV"""
        settings = {}
        with open(self.settings_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert string 'False'/'True' to boolean
                if row['value'].lower() in ('true', 'false'):
                    settings[row['setting_name']] = row['value'].lower() == 'true'
                else:
                    settings[row['setting_name']] = row['value']
        return settings

    def save_settings(self, settings):
        """Save settings to CSV"""
        with open(self.settings_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['setting_name', 'value'])
            for key, value in settings.items():
                writer.writerow([key, str(value)])

    def log_feedback(self, message):
        """Log feedback message to CSV"""
        with open(self.feedback_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message])

    def log_game_result(self, start_time, end_time, winner, ao_score, aka_score):
        """Log game result to history CSV"""
        with open(self.history_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                start_time.strftime('%Y-%m-%d %H:%M:%S'),
                end_time.strftime('%Y-%m-%d %H:%M:%S'),
                winner,
                ao_score,
                aka_score
            ])

    def get_game_history(self):
        """Get all game history records"""
        history = []
        with open(self.history_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                history.append({
                    'start_time': row['start_time'],
                    'end_time': row['end_time'],
                    'winner': row['winner'],
                    'ao_score': row['ao_score'],
                    'aka_score': row['aka_score']
                })
        return history
