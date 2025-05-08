#!/usr/bin/env python3
"""
Terminal Dialogue CLI Parser

This script allows running dialogue trees from the command line interface,
making it possible for both humans and LLMs to interact with dialogue scenarios
without requiring the Streamlit interface.
"""

import json
import argparse
import sys
import os
import re
from pathlib import Path

# ANSI color codes for terminal output
GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"

class DialogueCLI:
    """Command-line interface for running dialogue trees"""
    
    def __init__(self, dialogue_file):
        """Initialize with a dialogue file"""
        self.dialogue_data = self._load_dialogue_file(dialogue_file)
        self.current_dialogue_id = self.dialogue_data.get("starting_dialogue")
        self.dialogue_history = []
        self.active_quests = {}
        self.variables = self.dialogue_data.get("variables", {}).copy()
        
    def _load_dialogue_file(self, file_path):
        """Load dialogue data from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"{RED}Error loading dialogue file: {e}{RESET}")
            sys.exit(1)
    
    def get_dialogue_by_id(self, dialogue_id):
        """Find a dialogue node by its ID"""
        for dialogue in self.dialogue_data.get("dialogues", []):
            if dialogue["id"] == dialogue_id:
                return dialogue
        return None
    
    def get_quest_by_id(self, quest_id):
        """Find a quest by its ID"""
        for quest in self.dialogue_data.get("quests", []):
            if quest["id"] == quest_id:
                return quest
        return None
    
    def process_script(self, script):
        """Process script commands"""
        if not script or script is None:
            return
        
        # StartQuest command
        if script.startswith("StartQuest_"):
            quest_id = script.replace("StartQuest_", "")
            quest = self.get_quest_by_id(quest_id)
            if quest:
                self.active_quests[quest_id] = 1  # Start at stage 1
                quest_stage = next((s for s in quest["stages"] if s["id"] == 1), None)
                if quest_stage:
                    print(f"\n{YELLOW}NEW QUEST: {quest['title']}{RESET}")
                    print(f"{YELLOW}> {quest_stage['journal_entry']}{RESET}\n")
        
        # UpdateQuest command
        elif script.startswith("UpdateQuest_"):
            parts = script.replace("UpdateQuest_", "").split("_")
            if len(parts) >= 2:
                quest_id = parts[0]
                try:
                    stage_id = int(parts[1])
                    quest = self.get_quest_by_id(quest_id)
                    if quest and quest_id in self.active_quests:
                        self.active_quests[quest_id] = stage_id
                        quest_stage = next((s for s in quest["stages"] if s["id"] == stage_id), None)
                        if quest_stage:
                            print(f"\n{YELLOW}QUEST UPDATED: {quest['title']}{RESET}")
                            print(f"{YELLOW}> {quest_stage['journal_entry']}{RESET}\n")
                except ValueError:
                    pass
        
        # CompleteQuest command
        elif script.startswith("CompleteQuest_"):
            quest_id = script.replace("CompleteQuest_", "")
            if quest_id in self.active_quests:
                quest = self.get_quest_by_id(quest_id)
                if quest:
                    print(f"\n{YELLOW}QUEST COMPLETED: {quest['title']}{RESET}")
                    if "rewards" in quest and quest["rewards"]:
                        print(f"{YELLOW}Rewards: {self._format_rewards(quest['rewards'])}{RESET}")
                    del self.active_quests[quest_id]
        
        # SetVariable command
        elif script.startswith("SetVariable_"):
            parts = script.replace("SetVariable_", "").split("_")
            if len(parts) >= 2:
                var_name = parts[0]
                value = parts[1]
                # Convert to appropriate type
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                elif value.isdigit():
                    value = int(value)
                self.variables[var_name] = value
    
    def _format_rewards(self, rewards):
        """Format quest rewards for display"""
        reward_parts = []
        if "xp" in rewards and rewards["xp"]:
            reward_parts.append(f"{rewards['xp']} XP")
        if "items" in rewards and rewards["items"]:
            reward_parts.append(f"Items: {', '.join(rewards['items'])}")
        
        return ", ".join(reward_parts)
    
    def evaluate_condition(self, condition):
        """Evaluate a condition expression"""
        if not condition or condition is None:
            return True
        
        # HasItem condition
        if condition.startswith("HasItem_"):
            item_id = condition.replace("HasItem_", "")
            # For now, we don't track inventory
            return False
        
        # QuestActive condition
        elif condition.startswith("QuestActive_"):
            quest_id = condition.replace("QuestActive_", "")
            return quest_id in self.active_quests
        
        # QuestStage condition
        elif condition.startswith("QuestStage_"):
            parts = condition.replace("QuestStage_", "").split("_")
            if len(parts) >= 2:
                quest_id = parts[0]
                try:
                    stage_id = int(parts[1])
                    return quest_id in self.active_quests and self.active_quests[quest_id] == stage_id
                except ValueError:
                    return False
            return False
        
        # VariableEquals condition
        elif condition.startswith("VariableEquals_"):
            parts = condition.replace("VariableEquals_", "").split("_")
            if len(parts) >= 2:
                var_name = parts[0]
                value = parts[1]
                
                # Convert value to appropriate type
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                elif value.isdigit():
                    value = int(value)
                
                return var_name in self.variables and self.variables[var_name] == value
            return False
        
        # Default to True for unknown conditions
        return True
    
    def show_dialogue(self):
        """Display the current dialogue"""
        dialogue = self.get_dialogue_by_id(self.current_dialogue_id)
        if not dialogue:
            print(f"{RED}Error: Dialogue with ID '{self.current_dialogue_id}' not found.{RESET}")
            return False
        
        # Process on_entry script if present
        if "on_entry" in dialogue and dialogue["on_entry"]:
            self.process_script(dialogue["on_entry"])
        
        # Add to history
        self.dialogue_history.append({
            "id": dialogue["id"],
            "npc": dialogue["npc"],
            "text": dialogue["text"]
        })
        
        # Display the dialogue
        print(f"\n{CYAN}{dialogue['npc']}{RESET}")
        print(f"{BRIGHT_GREEN}{dialogue['text']}{RESET}\n")
        
        # Get valid responses (filtering by conditions)
        valid_responses = []
        for i, response in enumerate(dialogue["responses"]):
            if self.evaluate_condition(response.get("condition")):
                valid_responses.append((i, response))
        
        # Check if there are no valid responses
        if not valid_responses:
            print(f"{YELLOW}[End of dialogue]{RESET}")
            return False
        
        # Display the responses
        for i, (_, response) in enumerate(valid_responses):
            print(f"{BOLD}{i+1}.{RESET} {GREEN}{response['text']}{RESET}")
        
        # Get user choice
        try:
            choice = input("\nEnter your choice (number): ")
            choice_idx = int(choice) - 1
            
            if choice_idx < 0 or choice_idx >= len(valid_responses):
                print(f"{RED}Invalid choice. Please enter a number between 1 and {len(valid_responses)}.{RESET}")
                return True
            
            # Process the selected response
            _, selected_response = valid_responses[choice_idx]
            
            # Add selected response to history
            self.dialogue_history.append({
                "text": selected_response["text"],
                "is_player": True
            })
            
            # Process any script command
            if "script" in selected_response and selected_response["script"]:
                self.process_script(selected_response["script"])
            
            # Set the next dialogue
            next_dialogue = selected_response["next_dialogue"]
            if next_dialogue is None:
                print(f"\n{YELLOW}End of conversation.{RESET}")
                return False
            
            self.current_dialogue_id = next_dialogue
            return True
            
        except ValueError:
            print(f"{RED}Please enter a valid number.{RESET}")
            return True
    
    def show_quest_log(self):
        """Display the quest log"""
        if not self.active_quests:
            print(f"\n{YELLOW}No active quests.{RESET}")
            return
        
        print(f"\n{YELLOW}=== ACTIVE QUESTS ==={RESET}")
        for quest_id, stage_id in self.active_quests.items():
            quest = self.get_quest_by_id(quest_id)
            if quest:
                print(f"\n{BOLD}{quest['title']}{RESET}")
                print(f"{quest['description']}")
                stage = next((s for s in quest["stages"] if s["id"] == stage_id), None)
                if stage:
                    print(f"{YELLOW}> {stage['journal_entry']}{RESET}")
    
    def show_variables(self):
        """Display the current variables (for debugging)"""
        if not self.variables:
            print(f"\n{BLUE}No variables set.{RESET}")
            return
        
        print(f"\n{BLUE}=== VARIABLES ==={RESET}")
        for var_name, value in self.variables.items():
            print(f"{var_name}: {value}")
    
    def run(self):
        """Run the dialogue tree"""
        print(f"\n{BOLD}==========================================={RESET}")
        print(f"{BOLD}  TERMINAL DIALOGUE SIMULATOR - CLI MODE  {RESET}")
        print(f"{BOLD}==========================================={RESET}")
        
        print("\nCommands:")
        print("  q - Quit")
        print("  help - Show commands")
        print("  quests - Show quest log")
        print("  vars - Show variables (debug)")
        
        while True:
            # Display prompt and get choice
            result = self.show_dialogue()
            
            if not result:
                # End of dialogue path reached
                choice = input("\nPlay again? (y/n): ")
                if choice.lower() != 'y':
                    break
                # Reset to starting dialogue
                self.current_dialogue_id = self.dialogue_data.get("starting_dialogue")
                self.dialogue_history = []
                # Don't reset quests or variables to allow for persistent state
            
            # Check for special commands
            last_input = input("\nCommand (or press Enter to continue): ")
            if last_input.lower() == 'q':
                break
            elif last_input.lower() == 'help':
                print("\nCommands:")
                print("  q - Quit")
                print("  help - Show commands")
                print("  quests - Show quest log")
                print("  vars - Show variables (debug)")
            elif last_input.lower() == 'quests':
                self.show_quest_log()
            elif last_input.lower() == 'vars':
                self.show_variables()
        
        print(f"\n{BOLD}Thank you for playing!{RESET}")

def main():
    parser = argparse.ArgumentParser(description='Run dialogue trees from the command line.')
    parser.add_argument('dialogue_file', help='Path to the dialogue JSON file')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        global GREEN, BRIGHT_GREEN, YELLOW, BLUE, CYAN, RED, RESET, BOLD
        GREEN = BRIGHT_GREEN = YELLOW = BLUE = CYAN = RED = RESET = BOLD = ""
    
    # Run the CLI
    cli = DialogueCLI(args.dialogue_file)
    cli.run()

if __name__ == "__main__":
    main()