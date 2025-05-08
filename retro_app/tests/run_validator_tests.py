#!/usr/bin/env python
"""
Run validation tests on example dialogue files to demonstrate the validator's capabilities.
"""
import os
import sys
import subprocess
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Get the root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

VALIDATOR_PATH = os.path.join(ROOT_DIR, "dialogue_validator.py")
SCHEMA_PATH = os.path.join(ROOT_DIR, "dialogue_schema.json")
TEST_FILES_DIR = SCRIPT_DIR

def print_header(text):
    """Print a header with color and formatting"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
    print(f"{text.center(80)}")
    print(f"{'=' * 80}{Style.RESET_ALL}\n")

def run_validator(file_path, verbose=False):
    """Run the validator on a file and return the process"""
    args = [sys.executable, VALIDATOR_PATH, "--file", file_path, "--schema", SCHEMA_PATH]
    if verbose:
        args.append("--verbose")
    
    process = subprocess.run(args, capture_output=True, text=True)
    return process

def run_fix_test(file_path, output_dir):
    """Run the validator with the fix option"""
    os.makedirs(output_dir, exist_ok=True)
    
    args = [
        sys.executable,
        VALIDATOR_PATH,
        "--file", file_path,
        "--schema", SCHEMA_PATH,
        "--fix",
        "--output-dir", output_dir,
        "--verbose"
    ]
    
    process = subprocess.run(args, capture_output=True, text=True)
    return process

def run_directory_test():
    """Run the validator on the entire directory"""
    args = [
        sys.executable,
        VALIDATOR_PATH,
        "--dir", TEST_FILES_DIR,
        "--schema", SCHEMA_PATH,
        "--pattern", "test_*.json",
        "--verbose"
    ]
    
    process = subprocess.run(args, capture_output=True, text=True)
    return process

def main():
    """Run the validation tests"""
    # Check if validator and schema exist
    if not os.path.exists(VALIDATOR_PATH):
        print(f"{Fore.RED}Error: Validator not found at {VALIDATOR_PATH}{Style.RESET_ALL}")
        sys.exit(1)
    
    if not os.path.exists(SCHEMA_PATH):
        print(f"{Fore.RED}Error: Schema not found at {SCHEMA_PATH}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Print introduction
    print_header("Dialogue Validator Test Suite")
    print(f"Testing validator: {VALIDATOR_PATH}")
    print(f"Using schema: {SCHEMA_PATH}")
    print(f"Test files directory: {TEST_FILES_DIR}\n")
    
    # Test 1: Valid file
    print_header("Test 1: Valid Dialogue File")
    valid_file = os.path.join(TEST_FILES_DIR, "test_valid.json")
    process = run_validator(valid_file)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 2: Invalid references
    print_header("Test 2: Invalid References")
    invalid_ref_file = os.path.join(TEST_FILES_DIR, "test_invalid_references.json")
    process = run_validator(invalid_ref_file, verbose=True)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 3: Missing fields
    print_header("Test 3: Missing Fields")
    missing_fields_file = os.path.join(TEST_FILES_DIR, "test_missing_fields.json")
    process = run_validator(missing_fields_file, verbose=True)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 4: Circular references
    print_header("Test 4: Circular References")
    circular_ref_file = os.path.join(TEST_FILES_DIR, "test_circular_reference.json")
    process = run_validator(circular_ref_file, verbose=True)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 5: Naming conventions
    print_header("Test 5: Naming Conventions")
    naming_file = os.path.join(TEST_FILES_DIR, "test_naming_conventions.json")
    process = run_validator(naming_file, verbose=True)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 6: Quest issues
    print_header("Test 6: Quest Issues")
    quest_file = os.path.join(TEST_FILES_DIR, "test_quest_issues.json")
    process = run_validator(quest_file, verbose=True)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 7: Auto-fixing
    print_header("Test 7: Auto-fixing Missing Fields")
    output_dir = os.path.join(TEST_FILES_DIR, "fixed")
    process = run_fix_test(missing_fields_file, output_dir)
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    # Test 8: Directory validation
    print_header("Test 8: Directory Validation")
    process = run_directory_test()
    print(process.stdout)
    if process.stderr:
        print(f"{Fore.RED}{process.stderr}{Style.RESET_ALL}")
    
    print_header("All Tests Completed")

if __name__ == "__main__":
    main()