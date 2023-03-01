import customtkinter #GUI
import random #Creat mines
import os #restart
import sys  #restart
#from https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/simple_example.py
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.title("Minesweeper")
app.resizable(False, False)

#function to get GRID size from user
def grid_size():
    size_question = customtkinter.CTkInputDialog(text = "type in small, medium or large: ")
    size = size_question.get_input()
    if size.lower() == "small":
        r = 5
        c = 8
        n = 9
        geo_x = 470
        geo_y = 500
    elif size.lower() == "medium":
        r = 10
        c = 12
        n = 15
        geo_x = 480
        geo_y = 580
    elif size.lower() == "large":
        r = 15
        c = 16
        n = 20
        geo_x = 700
        geo_y = 650
    return r, c, n, geo_x, geo_y

size = grid_size()
r = size[0]
c = size[1]
n = size[2]
geo_x = size[3]
geo_y = size[4]

app.geometry("{x}x{y}".format(x = geo_x, y = geo_y))

#frame_1 = background / mainwindow, frame_2 = GRID, frame_3 = end of game
frame_1 = customtkinter.CTkFrame(master = app)
frame_1.pack(pady = 20, padx = 60, fill = "both", expand = True)
frame_2 = customtkinter.CTkFrame(app, width = geo_x, height = geo_y)
frame_2.place(x = 100, y = 80)
frame_3 = customtkinter.CTkFrame(app, width = geo_x * 0.7, height = geo_y * 0.8,corner_radius = 0)

class Cell():
    all = []
    cell_count_object = None
    cell_counted = c * r
    mine_count_object = None
    mine_counted = n
    def __init__(self, x, y, mine = False):
        self.mine = mine
        self.button_object = None
        self.x = x
        self.y = y
        self.is_open = False
        self.is_marked = False
        self.all.append(self)

    @staticmethod
    #Used to count and show how many cells that are still unopened
    def cell_count(location = frame_1):
        info_cell = customtkinter.CTkLabel(location, text = "Cells left: {}".format(Cell.cell_counted))
        Cell.cell_count_object = info_cell

    @staticmethod
    #Used to count and show how many mines that are still unmarked
    def mines_left(location = frame_1):
        info_mines = customtkinter.CTkLabel(location, text = "Mines left: {}".format(Cell.mine_counted))
        Cell.mine_count_object = info_mines
    
    #Basic settings for the cell-buttons and binds "clic-events" and cells.
    def create_button(self, location = frame_2):
        #button stolen from https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton
        button = customtkinter.CTkButton(location, width = 30, height = 32, border_width = 2, corner_radius = 1, text = " ")
        button.bind('<Button-1>', self.left_click_button)
        button.bind('<Button-3>', self.right_click_button)
        self.button_object = button
    
    #Creates the mines in random places, "n" is a variable from the grid_size function
    def create_mines():
        mines = random.sample(Cell.all, n)
        for mine in mines:
            mine.mine = True

    #what happens after a button is left click, different outcome if the button is a mine or not
    def left_click_button(self, event):
        if self.mine:
            self.show_mine()
        else:
            self.show_cell()
            if self.count_mines() == 0:
                for cell_obj in self.get_surronded_cells:
                    cell_obj.show_cell()
                    cell_obj.is_open = True

    #if not mine
    def show_cell(self):
        if not self.is_open:
            Cell.cell_counted -= 1
            self.button_object.configure(fg_color = "grey", text = self.count_mines())
            Cell.cell_count_object.configure(text = "Cells left: {}".format(Cell.cell_counted))
        self.is_open = True

    #gathers information about the selected cell's surrounding cells (using get_cell and count_mines)
    @property
    def get_surronded_cells(self):
        surronded_cells = [
            self.get_cell(self.x - 1, self.y - 1),
            self.get_cell(self.x - 1, self.y ),
            self.get_cell(self.x - 1, self.y + 1),
            self.get_cell(self.x, self.y - 1),
            self.get_cell(self.x, self.y + 1),
            self.get_cell(self.x + 1, self.y - 1),
            self.get_cell(self.x + 1, self.y ),
            self.get_cell(self.x + 1, self.y + 1)        
                           ]
        surronded_cells = [cell for cell in surronded_cells if cell is not None]
        return surronded_cells
    
    #The function get_surronded_cells uses it to find surrounding cells
    def get_cell(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
    #the function show cell() uses it to determine how many mines that surrounds the cell (aka. what number to print on button)
    def count_mines(self):
        counter = 0
        for cell in self.get_surronded_cells:
            if cell.mine:
                counter += 1
        return counter
    
    #if chosen cell.mine = True, this happens
    def show_mine(self):
        self.button_object.configure(fg_color = "red", hover_color = 'red')
        frame_3.place(x = 80, y = 80)
        game_lost = customtkinter.CTkLabel(frame_3, text = "BOOOM")
        game_lost.place(x = geo_x * 0.3, y = geo_y * 0.2)
        Cell.show_reset_button()


    @staticmethod
    def show_reset_button():
        button_restart = customtkinter.CTkButton(frame_3, border_width = 2,width = 60, height = 32, corner_radius = 1, text = "Play again", command= restart_program)
        button_restart.place(x = geo_x * 0.3, y = geo_y * 0.3)
    
    #function to "mark" cells as mines.
    def right_click_button(self, event):
        self.button_object.configure(fg_color = "green", hover_color = 'green')
        Cell.mine_counted -= 1
        Cell.mine_count_object.configure(text = "Mines left: {}".format(Cell.mine_counted))
        self.is_marked = True
        count_marked = 0
        if Cell.mine_counted == 0:
            for cell in Cell.all:
                if cell.mine and cell.is_marked:
                    count_marked += 1
        if count_marked == n:
            frame_3.place(x = 80, y = 80)
            game_won = customtkinter.CTkLabel(frame_3, text = "You won!")
            game_won.place(x = geo_x * 0.3, y = geo_y * 0.2)
            Cell.show_reset_button()

    def __repr__(self):
        return "cell({y}, {x}).".format(y = self.y, x = self.x)


    # stolen from https://www.youtube.com/watch?v=OqbGRZx4xUc
#Creates the cells
def create_cells():
    for x in range(r):
        for y in range(c):
            c1 = Cell(x, y)
            c1.create_button()
            c1.button_object.grid(column = x, row = y)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


create_cells()
Cell.cell_count()
Cell.cell_count_object.place(x = 40, y = 0)
Cell.mines_left()
Cell.mine_count_object.place(x = 40, y = 20)
Cell.create_mines()


app.mainloop()