#!/usr/bin/env python
"""
Create a new dialogue file from a template.
This script helps users create a new dialogue file with proper structure.
"""
import os
import sys
import json
import argparse
from datetime import datetime

def create_dialogue_file(template_path, output_path, title, author, description):
    """Create a new dialogue file from a template with custom metadata"""
    try:
        # Load template file
        with open(template_path, 'r') as f:
            dialogue_data = json.load(f)
        
        # Update metadata
        if "metadata" not in dialogue_data:
            dialogue_data["metadata"] = {}
            
        dialogue_data["metadata"]["title"] = title
        dialogue_data["metadata"]["author"] = author
        dialogue_data["metadata"]["creation_date"] = datetime.now().strftime("%Y-%m-%d")
        dialogue_data["metadata"]["description"] = description
        
        # Ensure schema_version exists
        if "schema_version" not in dialogue_data:
            dialogue_data["schema_version"] = "1.0"
            
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write to output file
        with open(output_path, 'w') as f:
            json.dump(dialogue_data, f, indent=2)
            
        print(f"Created new dialogue file: {output_path}")
        return True
    except Exception as e:
        print(f"Error creating dialogue file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create a new dialogue file from a template')
    parser.add_argument('--template', default='dialogue_default.json', 
                        help='Template file name (from templates directory)')
    parser.add_argument('--output', required=True, 
                        help='Output file path (in conversations directory)')
    parser.add_argument('--title', required=True, 
                        help='Title for the dialogue')
    parser.add_argument('--author', default='Terminal Dialogue Creator', 
                        help='Author name')
    parser.add_argument('--description', default='A dialogue created from template', 
                        help='Description of the dialogue')
    
    args = parser.parse_args()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Construct paths
    template_path = os.path.join(script_dir, args.template)
    
    # Handle relative or absolute output path
    if os.path.isabs(args.output):
        output_path = args.output
    else:
        output_path = os.path.join(root_dir, 'conversations', args.output)
        
    # Add .json extension if not present
    if not output_path.endswith('.json'):
        output_path += '.json'
    
    # Create the dialogue file
    success = create_dialogue_file(
        template_path, 
        output_path, 
        args.title, 
        args.author, 
        args.description
    )
    
    # Suggest validation
    if success:
        validator_path = os.path.join(root_dir, 'dialogue_validator.py')
        print(f"\nTo validate your new dialogue file, run:")
        print(f"  {validator_path} --file {output_path}")
        
    # Return status code
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())