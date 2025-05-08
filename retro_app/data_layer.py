"""
Data Layer for Terminal Dialogue System
Handles all file loading, saving, and data management
"""
import json
import os
from typing import Dict, List, Any, Optional, Union


class DialogueDataManager:
    """Handles loading, saving, and manipulating dialogue data"""
    
    def __init__(self, base_directory: str = None):
        """Initialize the data manager"""
        # If no base directory provided, use the directory this file is in
        self.base_directory = base_directory or os.path.dirname(__file__)
        self.conversations_directory = os.path.join(self.base_directory, "conversations")
        self.templates_directory = os.path.join(self.base_directory, "templates")
        
    def get_available_conversations(self) -> List[str]:
        """Get a list of available conversation files in the conversations directory"""
        if not os.path.exists(self.conversations_directory):
            return []
        
        return [f for f in os.listdir(self.conversations_directory) 
                if f.endswith(".json") and os.path.isfile(os.path.join(self.conversations_directory, f))]
    
    def get_available_templates(self) -> List[str]:
        """Get a list of available template files in the templates directory"""
        if not os.path.exists(self.templates_directory):
            return []
        
        return [f for f in os.listdir(self.templates_directory) 
                if f.endswith(".json") and os.path.isfile(os.path.join(self.templates_directory, f))]
    
    def load_dialogue_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load dialogue data from a JSON file.
        
        Args:
            file_path: Path to the JSON file (absolute or relative to conversations dir)
            
        Returns:
            A dictionary containing the dialogue data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        # Absolute path provided
        if os.path.isabs(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        
        # Try in conversations directory
        conversations_path = os.path.join(self.conversations_directory, os.path.basename(file_path))
        if os.path.exists(conversations_path):
            with open(conversations_path, 'r') as file:
                return json.load(file)
        
        # Try in templates directory
        templates_path = os.path.join(self.templates_directory, os.path.basename(file_path))
        if os.path.exists(templates_path):
            with open(templates_path, 'r') as file:
                return json.load(file)
        
        # Try direct path
        with open(file_path, 'r') as file:
            return json.load(file)
            
    def save_dialogue_data(self, data: Dict[str, Any], file_path: str) -> None:
        """
        Save dialogue data to a JSON file.
        
        Args:
            data: The dialogue data to save
            file_path: Path where to save the file
            
        Raises:
            IOError: If the file can't be written
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Write the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    
    def create_empty_dialogue_data(self) -> Dict[str, Any]:
        """Create an empty dialogue data structure"""
        return {
            "schema_version": "1.0",
            "metadata": {
                "title": "New Dialogue",
                "author": "Terminal Dialogue Creator",
                "creation_date": "2025-05-08",
                "description": "A new dialogue created with the Terminal Dialogue System"
            },
            "starting_dialogue": "dialogue_start",
            "dialogues": [
                {
                    "id": "dialogue_start",
                    "npc": "System",
                    "text": "This is a new dialogue. Edit this text to begin.",
                    "responses": [
                        {
                            "id": "response_end",
                            "text": "> End conversation",
                            "next_dialogue": None,
                            "script": None,
                            "condition": None
                        }
                    ],
                    "on_entry": None
                }
            ],
            "quests": [],
            "variables": {}
        }
    
    def get_dialogue_by_id(self, dialogue_data: Dict[str, Any], dialogue_id: str) -> Optional[Dict[str, Any]]:
        """Find a dialogue by its ID in the dialogue data"""
        for dialogue in dialogue_data.get("dialogues", []):
            if dialogue.get("id") == dialogue_id:
                return dialogue
        return None
    
    def get_quest_by_id(self, dialogue_data: Dict[str, Any], quest_id: str) -> Optional[Dict[str, Any]]:
        """Find a quest by its ID in the dialogue data"""
        for quest in dialogue_data.get("quests", []):
            if quest.get("id") == quest_id:
                return quest
        return None
    
    def get_quest_stage(self, dialogue_data: Dict[str, Any], quest_id: str, stage_id: int) -> Optional[Dict[str, Any]]:
        """Find a quest stage by quest ID and stage ID"""
        quest = self.get_quest_by_id(dialogue_data, quest_id)
        if quest:
            for stage in quest.get("stages", []):
                if stage.get("id") == stage_id:
                    return stage
        return None


# Singleton instance for easy import
dialogue_manager = DialogueDataManager()