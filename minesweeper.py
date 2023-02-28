import customtkinter
import random
#from https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/simple_example.py
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x480")
app.title("Minesweeper")

frame_1 = customtkinter.CTkFrame(master = app)
frame_1.pack(pady = 20, padx = 60, fill = "both", expand = True)
#End of stolen (for now)
app.resizable(False, False)
frame_2 = customtkinter.CTkFrame(app, width = 600, height = 600)
frame_2.place(x = 100, y = 80)


def grid_size():
    size2 = customtkinter.CTkInputDialog(text = "type in small, medium or large: ")
    print(size2)
    size = input("type in small, medium or large: ")
    if size.lower() == "small":
        x = 5
        y = 8
        n = 10
        app.geometry("350x400")
    elif size.lower() == "medium":
        x = 10
        y = 12
        n = 15
        app.geometry("480x580")
    elif size.lower() == "large":
        x = 15
        y = 16
        n = 20
        app.geometry("590x630")
    return x, y, n, size2

size = grid_size()
x = size[0]
y = size[1]
n = size[2]

class Cell():
    all = []
    def __init__(self, w, t, mine = False):
        self.mine = mine
        self.button_object = None
        self.w = w
        self.t = t
        self.all.append(self)
    
    def create_button(self, location = frame_2):
        #button stolen from https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton
        button = customtkinter.CTkButton(location, width = 10, height = 32, border_width = 2, corner_radius = 1, text = "{w},{t}".format(w = self.w, t = self.t))
        button.bind('<Button-1>', self.left_click_button)
        button.bind('<Button-3>', self.right_click_button)
        self.button_object = button
    
    def create_mines():
        mines = random.sample(Cell.all, n)
        for mine in mines:
            mine.mine = True

    def left_click_button(self, event):
        print(event)
        print("Vänster")
        if self.mine:
            self.show_mine()
        else:
            self.show_cell()
    
    def show_cell(self):
        num = self.count_mines()
        print(num)

    @property
    def get_surronded_cells(self):
        surronded_cells = [
            self.get_cell(self.t - 1, self.w - 1),
            self.get_cell(self.t - 1, self.w ),
            self.get_cell(self.t - 1, self.w + 1),
            self.get_cell(self.t, self.w - 1),
            self.get_cell(self.t, self.w + 1),
            self.get_cell(self.t + 1, self.w - 1),
            self.get_cell(self.t + 1, self.w ),
            self.get_cell(self.t + 1, self.w + 1)        
                           ]
        surronded_cells = [cell for cell in surronded_cells if cell is not None]
        return surronded_cells
    
    def count_mines(self):
        counter = 0
        for cell in self.get_surronded_cells:
            if cell.mine:
                counter += 1
        return counter
    
    def get_cell(self, t, w):
        for cell in Cell.all:
            if cell.t == t and cell.w == w:
                return cell


    def show_mine(self):
        self.button_object.configure(fg_color = "red")
    
    def right_click_button(self, event):
        print("Höger")
    

    def __repr__(self):
        return "cell({w}, {t})".format(w = self.w, t = self.t )


    # stolen from https://www.youtube.com/watch?v=OqbGRZx4xUc
for w in range(x):
    for t in range(y):
        c = Cell(w, t)
        c.create_button()
        c.button_object.grid(column = w, row = t)

Cell.create_mines()
app.mainloop()