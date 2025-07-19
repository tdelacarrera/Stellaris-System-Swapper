# Stellaris System Swapper

A simple Python GUI tool that lets you swap two systems in a Stellaris save game, built with **Tkinter**.

## Features

- Swap coordinates, arm, index, precursors and hyperlanes of two systems.
- Automatically update connected hyperlanes across the two systems.

## Run the application

Clone the repository:

    git clone https://github.com/tdelacarrera/stellaris-system-swapper.git
    
To run this application

    cd stellaris-system-swapper
    python app.py
    
## Usage

1. Extract your `.sav` save file using a file extractor
   
   You will get two files: 
   - `gamestate`  
   - `meta`

3. Launch the application and open the extracted `gamestate` file. 

4. Enter the IDs of the two star systems you want to swap.

5. Click Swap.

6. The tool will generate a new file named `gamestate_new` by default, with the modified systems.

7. Rename `gamestate_new` to `gamestate`

8. Repack the modified `gamestate` and original `meta` into a new `.zip` archive with a .sav extension.

9. Place the modified `.sav` file back into your Stellaris save folder and load it in-game.

## ⚠️ Disclaimer

This tool is an unofficial utility designed to work with Stellaris save files.  
It is not affiliated with, endorsed by, or associated with Paradox Interactive or Stellaris in any way.
