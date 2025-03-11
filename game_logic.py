import random
from llm_integration import get_llm

# Initialize the LLM interface
llm = get_llm()

# Game content and mechanics
class AdventureGame:
    def __init__(self):
        self.story_context = ""
        self.character_traits = {
            "Warrior": {
                "strengths": ["combat", "strength", "endurance"],
                "weaknesses": ["magic", "stealth", "diplomacy"],
                "starting_items": ["sword", "shield", "light armor"]
            },
            "Mage": {
                "strengths": ["magic", "knowledge", "perception"],
                "weaknesses": ["physical combat", "endurance", "heavy armor"],
                "starting_items": ["staff", "spellbook", "potion"]
            },
            "Rogue": {
                "strengths": ["stealth", "agility", "traps"],
                "weaknesses": ["direct combat", "magic resistance", "heavy armor"],
                "starting_items": ["dagger", "lockpicks", "light armor"]
            }
        }
        
        # Game world locations and their descriptions
        self.locations = {
            "starting_point": "The crossroads where your journey begins.",
            "village": "A small, peaceful village with friendly inhabitants.",
            "dark_forest": "An ancient forest where light barely penetrates the canopy.",
            "mountain_pass": "A treacherous path through the mountains.",
            "ancient_ruins": "The crumbling remains of a once-great civilization.",
            "wizard_tower": "A tall tower where a powerful wizard resides.",
            "bandit_camp": "A hidden encampment used by local bandits.",
            "dragon_lair": "A cave system where a fearsome dragon has made its home.",
            "underground_city": "A vast city built beneath the surface, home to dwarves and other subterranean races.",
            "elven_forest": "A magical forest protected by ancient elven magic."
        }
        
        # Potential encounters for each location
        self.encounters = {
            "village": ["friendly_villager", "quest_giver", "merchant", "thief"],
            "dark_forest": ["wild_beast", "elf_scout", "lost_traveler", "magical_creature"],
            "mountain_pass": ["rock_slide", "mountain_troll", "eagle_nest", "abandoned_mine"],
            "ancient_ruins": ["skeleton_warrior", "treasure_chest", "trap", "ghost"],
            "wizard_tower": ["apprentice_wizard", "magical_experiment", "library", "portal"],
            "bandit_camp": ["bandit_guard", "prisoner", "bandit_leader", "loot_stash"],
            "dragon_lair": ["dragon_minion", "treasure_hoard", "trap", "sleeping_dragon"],
            "underground_city": ["dwarf_merchant", "mining_operation", "underground_tavern", "forge"],
            "elven_forest": ["elf_patrol", "ancient_tree", "fairy_circle", "elven_settlement"]
        }
        
        # Items that can be found or purchased
        self.items = {
            "health_potion": {"type": "consumable", "effect": "restore_health", "value": 20},
            "magic_scroll": {"type": "consumable", "effect": "spell", "value": 0},
            "gold_coins": {"type": "currency", "value": 1},
            "iron_sword": {"type": "weapon", "damage": 10, "value": 50},
            "steel_sword": {"type": "weapon", "damage": 15, "value": 100},
            "enchanted_sword": {"type": "weapon", "damage": 25, "value": 300},
            "leather_armor": {"type": "armor", "defense": 5, "value": 40},
            "chainmail": {"type": "armor", "defense": 10, "value": 120},
            "plate_armor": {"type": "armor", "defense": 20, "value": 250},
            "healing_herbs": {"type": "ingredient", "effect": "healing", "value": 5},
            "magical_gem": {"type": "quest_item", "value": 200},
            "ancient_key": {"type": "key", "value": 0},
            "treasure_map": {"type": "map", "value": 50}
        }
    
    def generate_introduction(self, player_name, character_class):
        """
        Generate a personalized introduction for the player based on their name and class.
        """
        strengths = ", ".join(self.character_traits[character_class]["strengths"])
        weaknesses = ", ".join(self.character_traits[character_class]["weaknesses"])
        items = ", ".join(self.character_traits[character_class]["starting_items"])
        
        prompt = f"""
        Create an engaging introduction for a text-based adventure game. The player's name is {player_name} and they are a {character_class}.
        
        As a {character_class}, they are skilled in {strengths}, but may struggle with {weaknesses}.
        They begin their journey with the following items: {items}.
        
        The introduction should welcome the player to the world, provide some background on their character,
        and hint at an upcoming adventure or threat they will face.
        Keep it concise but immersive.
        """
        
        # Get introduction from LLM
        introduction = llm.generate_text(prompt, max_length=400)
        
        # Store this in the context for future reference
        self.story_context = f"Player: {player_name}, a {character_class} who is skilled in {strengths} but weak in {weaknesses}. "
        self.story_context += f"Starting items: {items}. "
        self.story_context += introduction
        
        return introduction
    
    def generate_initial_choices(self, character_class):
        """
        Generate initial choices for the player based on their character class.
        """
        common_choices = [
            "Explore the nearby village",
            "Head into the dark forest",
            "Follow the mountain path"
        ]
        
        class_specific = {
            "Warrior": "Seek out the local garrison for work",
            "Mage": "Look for a wizard's tower or magical library",
            "Rogue": "Investigate rumors of a valuable treasure"
        }
        
        choices = common_choices.copy()
        if character_class in class_specific:
            choices.append(class_specific[character_class])
        
        # Shuffle to add variety
        random.shuffle(choices)
        return choices[:3]  # Return 3 choices
    
    def process_player_action(self, game_state, action):
        """
        Process the player's chosen action and generate the next part of the story.
        """
        player_name = game_state.player_name
        character_class = game_state.character_class
        current_location = game_state.location
        inventory = game_state.inventory
        health = game_state.health
        history = game_state.history
        
        # Add the chosen action to the history
        history_text = ", ".join(history[-3:] if len(history) > 3 else history)
        game_state.history.append(action)
        
        # Determine if this is a combat encounter (30% chance)
        is_combat = random.random() < 0.3
        
        # Generate a prompt for the LLM based on the current state and action
        prompt = f"""
        In a fantasy text adventure game:
        - Player: {player_name}, a {character_class} with {health} health points
        - Current location: {self.locations.get(current_location, current_location)}
        - Inventory: {', '.join(inventory) if inventory else 'empty'}
        - Recent history: {history_text}
        
        The player has chosen to: {action}
        
        {"This leads to a combat encounter. " if is_combat else ""}
        
        Generate a short, engaging continuation of the story (3-4 sentences) that:
        1. Describes what happens when the player chooses this action
        2. Includes sensory details and atmosphere
        3. {"Describes a combat situation and how much health the player loses (between 5-20 points)" if is_combat else "Describes what the player discovers or experiences"}
        4. Ends with a situation that leads to new choices
        
        Response:
        """
        
        # Get story continuation from LLM
        story_continuation = llm.generate_text(prompt, max_length=350)
        
        # Update the story context
        self.story_context += f"\nPlayer chose: {action}.\n" + story_continuation
        
        # Handle health changes in combat
        if is_combat:
            # Extract health loss from the response or generate a random one
            try:
                # Look for patterns like "lose X health" or "X damage" in the text
                import re
                health_loss_match = re.search(r'lose[s]?\s+(\d+)\s+health|(\d+)\s+damage|(\d+)\s+health\s+points', 
                                            story_continuation.lower())
                
                if health_loss_match:
                    # Use the first captured group that has a value
                    health_loss = next(int(g) for g in health_loss_match.groups() if g is not None)
                else:
                    # Random health loss if not specified in the text
                    health_loss = random.randint(5, 20)
                    
                game_state.health -= health_loss
                
                # Ensure health doesn't go below 0
                game_state.health = max(0, game_state.health)
                
                health_message = f"You lost {health_loss} health points!"
            except Exception as e:
                print(f"Error processing health loss: {e}")
                health_loss = random.randint(5, 15)
                game_state.health -= health_loss
                game_state.health = max(0, game_state.health)
                health_message = f"You lost {health_loss} health points in the encounter!"
        else:
            health_message = ""
            
            # Small chance to find a health potion
            if random.random() < 0.15:
                game_state.inventory.append("health_potion")
                health_message = "You found a health potion!"
        
        # Generate new choices based on the current situation
        new_choices = self.generate_new_choices(game_state, story_continuation)
        
        # Check if player has died
        if game_state.health <= 0:
            story_continuation += "\n\nYour vision fades to black as you collapse from your wounds. Your adventure has come to an end."
            new_choices = ["Restart", "Load Game"]
        
        # Add health message to the story if applicable
        if health_message and not health_message in story_continuation:
            story_continuation = f"{story_continuation}\n\n{health_message}"
        
        return {
            'message': story_continuation,
            'health': game_state.health,
            'choices': new_choices
        }
    
    def generate_new_choices(self, game_state, story_continuation):
        """
        Generate new choices based on the current situation.
        """
        # Extract potential keywords from the story continuation
        lower_story = story_continuation.lower()
        
        # Define some common actions based on keywords
        potential_choices = []
        
        # Combat-related choices
        if any(word in lower_story for word in ['fight', 'battle', 'enemy', 'attack', 'monster', 'creature']):
            potential_choices.extend([
                "Fight bravely", 
                "Attempt to flee", 
                "Look for a tactical advantage"
            ])
        
        # Exploration choices
        if any(word in lower_story for word in ['door', 'path', 'passage', 'tunnel', 'road', 'entrance']):
            potential_choices.extend([
                "Proceed carefully", 
                "Investigate further", 
                "Look for another way"
            ])
        
        # Social choices
        if any(word in lower_story for word in ['person', 'people', 'villager', 'man', 'woman', 'merchant', 'guard']):
            potential_choices.extend([
                "Talk to them", 
                "Observe from a distance", 
                "Offer assistance"
            ])
        
        # Item/treasure choices
        if any(word in lower_story for word in ['item', 'treasure', 'chest', 'gold', 'weapon', 'armor', 'potion']):
            potential_choices.extend([
                "Take it", 
                "Examine it carefully", 
                "Leave it alone"
            ])
        
        # Rest/recovery choices
        if game_state.health < 70:
            potential_choices.append("Rest to recover health")
        
        # Use health potion if available
        if "health_potion" in game_state.inventory:
            potential_choices.append("Drink health potion")
        
        # Always provide at least one direction choice
        direction_choices = [
            "Continue forward",
            "Turn back",
            "Go left",
            "Go right"
        ]
        
        # If we don't have enough choices, add some generic ones
        generic_choices = [
            "Wait and observe",
            "Search the area",
            "Move cautiously",
            "Call out",
            "Hide and observe"
        ]
        
        # Combine all choices and remove duplicates
        all_choices = potential_choices + direction_choices + generic_choices
        unique_choices = list(dict.fromkeys(all_choices))
        
        # Shuffle and select 3-4 choices
        random.shuffle(unique_choices)
        num_choices = min(len(unique_choices), random.randint(3, 4))
        
        return unique_choices[:num_choices]
    
    def use_health_potion(self, game_state):
        """
        Use a health potion from the inventory to restore health.
        """
        if "health_potion" in game_state.inventory:
            game_state.inventory.remove("health_potion")
            health_gain = 30
            game_state.health = min(100, game_state.health + health_gain)
            
            return {
                'message': f"You drink the health potion, feeling its magical energy spread through your body. You recover {health_gain} health points!",
                'health': game_state.health,
                'choices': self.generate_new_choices(game_state, "After drinking the potion, you feel refreshed and ready to continue your adventure.")
            }
        else:
            return {
                'message': "You don't have any health potions!",
                'health': game_state.health,
                'choices': self.generate_new_choices(game_state, "You search your inventory but find no health potions.")
            }

# Instantiate the game
game = AdventureGame()
