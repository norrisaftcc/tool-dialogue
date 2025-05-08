"""
Terminal Dialogue Simulator with Retro Aesthetic
Main entry point that coordinates the three-layer architecture
"""
import os
import sys
import streamlit as st
from gui_layer import main as gui_main

if __name__ == "__main__":
    # Run the simulator
    gui_main()