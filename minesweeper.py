import customtkinter
#from https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/simple_example.py
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x480")
app.title("Minesweeper")

frame_1 = customtkinter.CTkFrame(master = app)
frame_1.pack(pady = 20, padx = 60, fill = "both", expand = True)
#End of stolen (for now)
app.resizable(False, False)
frame_2 = customtkinter.CTkFrame(app, width = 400, height = 400)
frame_2.place(x = 100, y = 80)



class Cell():
    def __init__(self, mine = False):
        self.mine = mine
        self.button_object = None
    
    def create_button(self, location = frame_2):
        #button stolen from https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton
        button = customtkinter.CTkButton(location, width = 10, height = 32, border_width = 2, corner_radius = 1, text = "hej")
        self.button_object = button


for x in range(8):
    for y in range(10):
        c = Cell()
        c.create_button()
        c.button_object.grid(column = x, row = y)

app.mainloop()