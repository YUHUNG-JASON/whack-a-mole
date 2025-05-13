🎯 Whack-a-Mole
A fun, fast-paced reaction game built with Python and Tkinter. Smash moles, defuse bombs, and beat the clock! Perfect for practicing GUI development and event handling in Python.

🕹️ Gameplay
🐹 Hit moles with a hammer to earn +1 point.

💣 Defuse bombs using a shovel (referred to as “scissors” in instructions) to avoid losing -1 point.

⏱️ Moles and bombs disappear or explode after 3 seconds.

🎮 Press Spacebar to switch tools between hammer and shovel.

🧠 The game runs for 30 seconds. Score as high as you can!


📦 Install Dependencies
Open a terminal and run:

python your_script_name.py
Make sure your project folder contains the following image files:

background.jpg — main menu background

back.jpg — back button image

mole.png — mole sprite

bomb.png — bomb sprite

⚠️ File names and image sizes are important – images are resized to fit 50x50 or 30x30 pixels in the code.

🧠 Project Structure
📁 your-project/
├── background.jpg
├── back.jpg
├── mole.png
├── bomb.png
└── whack_a_mole.py  # main game script
💡 Features
Full GUI interface using tkinter

Game loop and timing with after()

Score and timer display

Image-based sprites with click interaction

Tool switching (hammer/shovel) via keyboard

Instructions page and menu navigation

⚙️ Known Issues
Tool switching uses spacebar but instructions mention “scissors” – may confuse users (suggest changing to "shovel" for consistency).

Time resets to 30 on game end, but initial self.time_left is set to 10 in code. Consider changing to 30 for consistency.

Mole and bomb can occasionally overlap if not properly managed.

📜 License
This project is for educational and non-commercial use. Feel free to modify and experiment!
