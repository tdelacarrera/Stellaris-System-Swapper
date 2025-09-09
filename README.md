# Stellaris System Swapper

A simple Python GUI tool that lets you swap two systems in a Stellaris save game.

## Features

- Swap coordinates, arm, index, precursors and hyperlanes of two systems.
- Automatically update connected hyperlanes across the two systems.
- Remove exploration data for all empires in the galaxy.

## Run the application

Clone the repository:

    git clone https://github.com/tdelacarrera/stellaris-system-swapper.git
    
To run this application

    cd stellaris-system-swapper
    python app.py
    
## Usage

1. Open your save game.

2. Enter the IDs of the two systems you want to swap.

3. Click **Swap**.
   
4. (Optional) Click **Remove Exploration Data** to remove all exploration data.  
This will restore Terra incognita across the entire galaxy, affecting all players.

5. The tool will generate a new save game, with the modified systems.

## ⚠️ Disclaimer

This tool is an unofficial utility designed to work with Stellaris save files.  
It is not affiliated with, endorsed by, or associated with Paradox Interactive or Stellaris in any way.
