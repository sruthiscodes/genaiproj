import os
import json
import random
from flask import Flask, render_template, request, jsonify, session
from game_logic import game, AdventureGame

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Game state class
class GameState:
    def __init__(self, player_name, character_class, initial_health=100):
        self.player_name = player_name
        self.character_class = character_class
        self.health = initial_health
        self.inventory = []
        self.location = "starting_point"
        self.history = []  # Track story progression
        self.visited_locations = set()
        self.quest_progress = {}
        
    def to_dict(self):
        return {
            "player_name": self.player_name,
            "character_class": self.character_class,
            "health": self.health,
            "inventory": self.inventory,
            "location": self.location,
            "history": self.history,
            "visited_locations": list(self.visited_locations),
            "quest_progress": self.quest_progress
        }
    
    @classmethod
    def from_dict(cls, data):
        state = cls(data["player_name"], data["character_class"], data["health"])
        state.inventory = data["inventory"]
        state.location = data["location"]
        state.history = data["history"]
        state.visited_locations = set(data["visited_locations"])
        state.quest_progress = data["quest_progress"]
        return state

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    data = request.json
    player_name = data.get('player_name', 'Adventurer')
    character_class = data.get('character_class', 'Warrior')
    
    # Initialize game state
    game_state = GameState(player_name, character_class)
    
    # Generate initial story introduction
    intro_text = game.generate_introduction(player_name, character_class)
    
    # Store in session
    session['game_state'] = game_state.to_dict()
    
    return jsonify({
        'message': intro_text,
        'health': game_state.health,
        'choices': game.generate_initial_choices(character_class)
    })

@app.route('/action', methods=['POST'])
def process_action():
    data = request.json
    action = data.get('action')
    
    # Get current game state
    game_state = GameState.from_dict(session.get('game_state'))
    
    # Check for special actions
    if action == "Restart":
        return jsonify({
            'message': "Game over. Please start a new game.",
            'health': 0,
            'choices': []
        })
    
    elif action == "Drink health potion":
        response = game.use_health_potion(game_state)
    else:
        # Process the action and generate response
        response = game.process_player_action(game_state, action)
    
    # Save updated game state
    session['game_state'] = game_state.to_dict()
    
    return jsonify(response)

@app.route('/save', methods=['POST'])
def save_game():
    # Save the current game state to a file
    game_state = session.get('game_state')
    if not game_state:
        return jsonify({'status': 'error', 'message': 'No game in progress'})
    
    save_id = f"{game_state['player_name']}_{random.randint(1000, 9999)}"
    
    with open(f"saves/{save_id}.json", 'w') as f:
        json.dump(game_state, f)
    
    return jsonify({'status': 'success', 'save_id': save_id})

@app.route('/load', methods=['POST'])
def load_game():
    data = request.json
    save_id = data.get('save_id')
    
    try:
        with open(f"saves/{save_id}.json", 'r') as f:
            game_state = json.load(f)
        
        session['game_state'] = game_state
        
        return jsonify({
            'status': 'success',
            'message': 'Game loaded successfully',
            'health': game_state['health'],
            'location': game_state['location']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    os.makedirs('saves', exist_ok=True)  # Create saves directory if it doesn't exist
    app.run(debug=True)
