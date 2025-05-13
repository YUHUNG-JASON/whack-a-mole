import random
import time
import tkinter as tk
from PIL import Image, ImageTk

class Whack_a_Mole(tk.Tk):
    def __init__(self):
        # Initialize the main window
        super().__init__()
        
        self.title("Whack-a-Mole")
        self.geometry("400x400")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frame = {}

        # Create frames for different pages

        for Page in (MainMenu, Game_start, Instructions):
            frame = Page(self)
            self.frame[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frame[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.container)

        # Set up the main menu layout
        content = tk.Frame(self)
        content.pack(expand=True, fill=tk.BOTH)

        pil_img = Image.open("background.jpg").resize((600, 400))
        self.bg_image = ImageTk.PhotoImage(pil_img)

        # use a label to display the background image
        bg_label = tk.Label(content, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Place the title and buttons in the center
        tk.Label(content, text="Whack-a-Mole", font=("Helvetica", 24)).pack(pady=30)
        tk.Button(content, text="Start Game", command=lambda: parent.show_frame(Game_start.__name__)).pack(pady=10)
        tk.Button(content, text="Instructions", command=lambda: parent.show_frame(Instructions.__name__)).pack(pady=10)
        tk.Button(content, text="    Exit    ", command=parent.quit).pack(pady=10)


class Game_start(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        self.parent = parent
        self.parent.geometry("600x400")

        # Initialize game variables
        self.score = 0
        self.time_left = 10

        # Initialize the tool
        self.tool = 'HAMMER'
        self.bind("<space>", self.switch_tool)
        self.focus_set()

        # Top labels area
        data_content = tk.Frame(self)
        data_content.pack(fill=tk.X, pady=10)

        # set up the labels for score and time
        data_content.grid_columnconfigure(0, weight=1)
        data_content.grid_columnconfigure(1, weight=1)
        data_content.grid_columnconfigure(2, weight=1)

        self.score_label = tk.Label(data_content, text=f"Score: {self.score}", font=("Helvetica", 16), anchor="w")
        self.score_label.grid(row=0, column=0, sticky="w", padx=10)

        self.time_label = tk.Label(data_content, text=f"Time Left: {self.time_left}", font=("Helvetica", 16), anchor="e")
        self.time_label.grid(row=1, column=0, sticky="w", padx=10)

        # Canvas area for the game grid
        self.rows = 3
        self.columns = 4
        self.cell_size = 100 
        self.holes = []

        self.canvas = tk.Canvas(self, width=self.columns * self.cell_size,
                                      height=self.rows * self.cell_size,
                                      bg="white")
        self.canvas.pack(pady=5)

        self.mole_image =  Image.open("mole.png").resize((50, 50))
        self.mole_image = ImageTk.PhotoImage(self.mole_image)
        self.bomb_image =  Image.open("bomb.png").resize((50, 50))
        self.bomb_image = ImageTk.PhotoImage(self.bomb_image)

        for i in range(self.rows):
            for j in range(self.columns):
                cx = j * self.cell_size + self.cell_size // 2  # center x
                cy = i * self.cell_size + self.cell_size // 2  # center y
                r = 30  # radius
                hole = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="black")
                self.holes.append((hole, i, j))

        self.active_mole = {}
        self.active_bomb = {}

        return_jpg = Image.open("back.jpg").resize((30, 30))
        self.return_image = ImageTk.PhotoImage(return_jpg)
        # Start button
        start_button = tk.Button(data_content, text="Start Game", command=self.start_game)
        start_button.grid(row=0, column=1, pady=10)
        # Back button
        back_button = tk.Button(data_content, image=self.return_image, command=lambda: parent.show_frame(MainMenu.__name__))
        back_button.grid(row=0, column=2, pady=10)
    
    def switch_tool(self, event=None):
        # switch tool between HAMMER and SHOVEL
        if self.tool == 'HAMMER':
            self.tool = 'SHOVEL'
        else:
            self.tool = 'HAMMER'
        print(f"shift {self.tool}")

    def start_game(self):
        self.spawn_mole()
        self.spawn_bomb()
        self.update_time()
        if self.time_left > 0:
            self.after(1000, self.start_game)
        else:
            self.end_game()

    def spawn_mole(self):
        if not self.holes:
            return
        print(self.holes)
        hole = random.choice(self.holes)
        self.holes.remove(hole)

        cx = hole[1] * self.cell_size + self.cell_size // 2  # center x
        cy = hole[2] * self.cell_size + self.cell_size // 2  # center y

        # spawn mole
        mole_id = self.canvas.create_image(cy, cx, image=self.mole_image)
        self.active_mole[mole_id] = hole

        #  the mole will hide in 3 seconds
        self.after(3000, lambda: self.hide_mole(mole_id))

        # mole click eventh
        self.canvas.tag_bind(mole_id, "<Button-1>", lambda e, row=hole[1], col=hole[2]: self.kill_mole(mole_id))


    def kill_mole(self, mole_id: tuple):
        # make sure the tool is hammer
        if self.tool == 'HAMMER':
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.hide_mole(mole_id)
            print("hit mole")


    def hide_mole(self, mole_id):
        # the mole will hide
        if mole_id in self.active_mole:
            print(mole_id)
            self.holes.append(self.active_mole[mole_id])
            self.canvas.delete(mole_id)
            self.active_mole.pop(mole_id)
            print("hide mole")


    def spawn_bomb(self):
        if not self.holes:
            return
        hole = random.choice(self.holes)
        self.holes.remove(hole)

        cx = hole[1] * self.cell_size + self.cell_size // 2  # center x
        cy = hole[2] * self.cell_size + self.cell_size // 2  # center y

        # spawn mole
        bomb_id = self.canvas.create_image(cy, cx, image=self.bomb_image)
        self.active_bomb[bomb_id] = hole

        #  the mole will trigger in 3 seconds
        self.after(3000, lambda: self.trigger_bomb(bomb_id))

        # mole click eventh
        self.canvas.tag_bind(bomb_id, "<Button-1>", lambda e, row=hole[1], col=hole[2]: self.hide_bomb(bomb_id))

    def trigger_bomb(self, bomb_id):
        # Avoid double-clicking to score
        if bomb_id in self.active_bomb:
            self.score -= 1
            self.score_label.config(text=f"Score: {self.score}")
            self.holes.append(self.active_bomb[bomb_id])
            self.canvas.delete(bomb_id)
            self.active_bomb.pop(bomb_id)
            print("bomb triggered")

    def hide_bomb(self, bomb_id):
        # If the bomb has not been triggered
        if bomb_id in self.active_bomb and self.tool == 'SHOVEL':
            self.holes.append(self.active_bomb[bomb_id])
            self.canvas.delete(bomb_id)
            self.active_bomb.pop(bomb_id)
            print("bomb defused")


    def update_time(self):
        self.time_left -= 1
        self.time_label.config(text=f"Time Left: {self.time_left}")

    def end_game(self):
        # game over and show score
        self.canvas.delete("all")
        self.canvas.create_text(self.columns * self.cell_size // 2,
                                 self.rows * self.cell_size // 2,
                                 text=f"Game Over! Your score: {self.score}",
                                 font=("Helvetica", 24),
                                 fill="black")
        self.score_label.config(text="Score: 0")
        self.time_label.config(text="Time Left: 30")
        self.after_cancel(self.spawn_mole)
        self.canvas.bind("<Button-1>", lambda e: None)


class Instructions(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent.container)
        self.parent = parent
        self.parent.geometry("600x400")

        self.label = tk.Label(self, text="Instructions", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.instructions_text = tk.Text(self, wrap=tk.WORD)
        self.instructions_text.insert(tk.END, """
1.Gain 1 point for hitting a mole. Moles escape after 3 seconds.
2.Bombs explode after 3 seconds and deduct 1 point.
3.Use the hammer to hit moles, and use the scissors to defuse bombs.
4.Press the spacebar to switch between the hammer and the scissors.
5.The game lasts for 30 seconds.""")
        self.instructions_text.pack(expand=True, fill=tk.BOTH)



if __name__ == "__main__":
    root = Whack_a_Mole()
    root.show_frame("MainMenu")
    root.mainloop()

