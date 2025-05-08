"""
Logic Layer for Terminal Dialogue System
Handles dialogue navigation, game state, and quest tracking
"""
from typing import Dict, List, Any, Optional, Union, Tuple
from data_layer import dialogue_manager


class GameState:
    """Manages the state of the dialogue game"""
    
    def __init__(self):
        """Initialize the game state"""
        self.dialogue_data = None
        self.current_dialogue_id = None
        self.conversation_history = []
        self.quest_state = {}
        self.variables = {}
    
    def load_dialogue(self, file_path: str) -> bool:
        """
        Load dialogue data from a file and initialize the game state
        
        Args:
            file_path: Path to the dialogue file
            
        Returns:
            True if loading was successful, False otherwise
        """
        try:
            self.dialogue_data = dialogue_manager.load_dialogue_data(file_path)
            self.current_dialogue_id = self.dialogue_data.get("starting_dialogue")
            # Initialize variables from the dialogue data if present
            self.variables = self.dialogue_data.get("variables", {}).copy()
            return True
        except Exception:
            return False
    
    def reset_state(self) -> None:
        """Reset the game state but keep the dialogue data"""
        if self.dialogue_data:
            self.current_dialogue_id = self.dialogue_data.get("starting_dialogue")
            self.conversation_history = []
            self.quest_state = {}
            self.variables = self.dialogue_data.get("variables", {}).copy()
    
    def get_current_dialogue(self) -> Optional[Dict[str, Any]]:
        """Get the current dialogue object"""
        if not self.dialogue_data or not self.current_dialogue_id:
            return None
        
        return dialogue_manager.get_dialogue_by_id(self.dialogue_data, self.current_dialogue_id)
    
    def select_response(self, response_id: str) -> Tuple[bool, Optional[str]]:
        """
        Process a player's response selection
        
        Args:
            response_id: ID of the selected response
            
        Returns:
            Tuple of (success, error_message)
        """
        current_dialogue = self.get_current_dialogue()
        if not current_dialogue:
            return False, "No current dialogue"
        
        # Find the selected response
        selected_response = None
        for response in current_dialogue.get("responses", []):
            if response.get("id") == response_id:
                selected_response = response
                break
        
        if not selected_response:
            return False, f"Response {response_id} not found"
        
        # Add response to history
        self.conversation_history.append({
            "id": response_id,
            "speaker": "Player",
            "text": selected_response.get("text", ""),
            "is_player": True
        })
        
        # Execute script if present
        if "script" in selected_response and selected_response["script"]:
            self.execute_script(selected_response["script"])
        
        # Move to next dialogue
        next_dialogue_id = selected_response.get("next_dialogue")
        if next_dialogue_id is not None:
            self.current_dialogue_id = next_dialogue_id
            # Add new dialogue to history after processing on_entry
            new_dialogue = self.get_current_dialogue()
            if new_dialogue:
                # Execute on_entry script if present
                if "on_entry" in new_dialogue and new_dialogue["on_entry"]:
                    self.execute_script(new_dialogue["on_entry"])
                
                # Add to history
                self.conversation_history.append({
                    "id": new_dialogue.get("id", ""),
                    "speaker": new_dialogue.get("npc", "System"),
                    "text": new_dialogue.get("text", ""),
                    "is_player": False,
                    "image_url": new_dialogue.get("image_url")
                })
        
        return True, None
    
    def execute_script(self, script: str) -> None:
        """
        Execute a script command
        
        Args:
            script: The script command to execute
        """
        if not script:
            return
        
        # Quest commands
        if script.startswith("StartQuest_"):
            quest_id = script.replace("StartQuest_", "")
            self.quest_state[quest_id] = {"current_stage": 1}
        
        elif script.startswith("UpdateQuest_"):
            parts = script.replace("UpdateQuest_", "").split("_")
            if len(parts) >= 2:
                quest_id = parts[0]
                try:
                    stage = int(parts[1])
                    if quest_id in self.quest_state:
                        self.quest_state[quest_id]["current_stage"] = stage
                except ValueError:
                    pass
        
        elif script.startswith("CompleteQuest_"):
            quest_id = script.replace("CompleteQuest_", "")
            if quest_id in self.quest_state:
                self.quest_state[quest_id]["completed"] = True
        
        # Variable commands
        elif script.startswith("SetVariable_"):
            parts = script.replace("SetVariable_", "").split("_")
            if len(parts) >= 2:
                var_name = parts[0]
                var_value = parts[1]
                
                # Convert value to appropriate type
                if var_value.lower() == "true":
                    var_value = True
                elif var_value.lower() == "false":
                    var_value = False
                elif var_value.isdigit():
                    var_value = int(var_value)
                
                self.variables[var_name] = var_value
    
    def evaluate_condition(self, condition: str) -> bool:
        """
        Evaluate a condition string
        
        Args:
            condition: The condition to evaluate
            
        Returns:
            True if the condition is met, False otherwise
        """
        if not condition:
            return True
        
        # Variable conditions
        if condition.startswith("VariableEquals_"):
            parts = condition.replace("VariableEquals_", "").split("_")
            if len(parts) >= 2:
                var_name = parts[0]
                var_value = parts[1]
                
                # Convert value to appropriate type
                if var_value.lower() == "true":
                    var_value = True
                elif var_value.lower() == "false":
                    var_value = False
                elif var_value.isdigit():
                    var_value = int(var_value)
                
                return var_name in self.variables and self.variables[var_name] == var_value
        
        # Quest conditions
        if condition.startswith("QuestActive_"):
            quest_id = condition.replace("QuestActive_", "")
            return quest_id in self.quest_state
        
        if condition.startswith("QuestCompleted_"):
            quest_id = condition.replace("QuestCompleted_", "")
            return quest_id in self.quest_state and self.quest_state[quest_id].get("completed", False)
        
        if condition.startswith("QuestStage_"):
            parts = condition.replace("QuestStage_", "").split("_")
            if len(parts) >= 2:
                quest_id = parts[0]
                try:
                    stage = int(parts[1])
                    return (quest_id in self.quest_state and 
                            self.quest_state[quest_id].get("current_stage") == stage)
                except ValueError:
                    return False
        
        return False
    
    def get_quest_title(self, quest_id: str) -> str:
        """Get the title of a quest by its ID"""
        if not self.dialogue_data:
            return quest_id
        
        quest = dialogue_manager.get_quest_by_id(self.dialogue_data, quest_id)
        if quest:
            return quest.get("title", quest_id)
        
        return quest_id
    
    def get_current_quest_stages(self) -> List[Dict[str, Any]]:
        """Get the current stages of all active quests"""
        result = []
        
        if not self.dialogue_data:
            return result
        
        for quest_id, quest_state in self.quest_state.items():
            quest = dialogue_manager.get_quest_by_id(self.dialogue_data, quest_id)
            if not quest:
                continue
            
            # For completed quests
            if quest_state.get("completed", False):
                result.append({
                    "quest_id": quest_id,
                    "quest_title": quest.get("title", quest_id),
                    "completed": True
                })
                continue
            
            # For active quests
            current_stage_id = quest_state.get("current_stage")
            if current_stage_id is None:
                continue
                
            for stage in quest.get("stages", []):
                if stage.get("id") == current_stage_id:
                    result.append({
                        "quest_id": quest_id,
                        "quest_title": quest.get("title", quest_id),
                        "stage_id": current_stage_id,
                        "stage_text": stage.get("journal_entry", ""),
                        "completed": False
                    })
                    break
        
        return result


# Singleton instance for easy import
game_state = GameState()