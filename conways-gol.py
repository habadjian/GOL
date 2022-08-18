import tkinter as tk

bob = 0
while bob == 0:
    run = input("What would you like to run\n1. Beehive\n2. Blinker\n3. Block\n4. Glider \n5. Random Pattern\n")

    if run == "QUIT":
        print("Thanks for playing Conway's Game of Life!")
        break


    class Cell:


        ref_dict = {}
        active_cells = set()

        def __init__(
                self, coords, size, grid_size, conditions = {},
                active_color = "black", inactive_color = "white", state = False):

            self.coords = coords
            self.size = size
            self.grid_size = grid_size
            self.conditions = conditions
            self.active_color = active_color
            self.inactive_color = inactive_color
            self.state = state
            self.new_state = False
            self.neighbor_coords = ()
            self.get_neighbor_coords()
            self.alive_neighbors = 0
            Cell.ref_dict[self.coords] = self

        def valid_coord(self, coord):
            (x, y) = coord
            return (0 <= x < self.grid_size) and (0 <= y < self.grid_size)

        def get_neighbor_coords(self):
            (x, y) = self.coords
            self.neighbor_coords = tuple(filter(self.valid_coord,
            [(x + a, y + b)
            for a in range(-1, 2) for b in range(-1, 2) if a != 0 or b != 0]))
            return self

        def get_alive_neighbors(self):
            self.alive_neighbors = 0
            for n in self.neighbor_coords:
                if Cell.ref_dict[n].state:
                    self.alive_neighbors += 1
            return self

        def get_new_state(self):
            if not self.neighbor_coords:
                self.get_neighbor_coords().get_alive_neighbors()
            else:
                self.get_alive_neighbors()
            if self.state:
                if not 2 <= self.alive_neighbors <= 3:
                    self.new_state = False
                else:
                    self.new_state = True
            else:
                if self.alive_neighbors == 3:
                    self.new_state = True
                else:
                    self.new_state = False
            return self

        def update_state(self):
            self.state = self.new_state

            if self.state and self.coords not in Cell.active_cells:
                Cell.active_cells.add(self.coords)
            elif not self.state and self.coords in Cell.active_cells:
                Cell.active_cells.remove(self.coords)

            self.new_state = False
            return self

    class Grid:

        def __init__(
                self, size, cell_size, active_color = "black",
                inactive_color = "white", condition_dict = {},
                initial_active_cells = []):
            self.size = size
            self.cell_size = cell_size
            self.active_color = active_color
            self.inactive_color = inactive_color
            self.condition_dict = condition_dict
            self.initial_active_cells = initial_active_cells
            self.sim_cells = set()
            self.create_cells().set_active_cells(initial_active_cells)

        def create_cells(self):
            if self.condition_dict:
                for x in range(0, self.size):
                    for y in range(0, self.size):
                        Cell(
                            (x, y), self.cell_size, self.size,
                            conditions = self.condition_dict[(x, y)],
                            active_color = self.active_color,
                            inactive_color = self.inactive_color)
            else:
                for x in range(0, self.size):
                    for y in range(0, self.size):
                        Cell(
                            (x, y), self.cell_size, self.size,
                            active_color = self.active_color,
                            inactive_color = self.inactive_color)
            return self

        def set_active_cells(self, initial_active_cells):
            for coord in initial_active_cells:
                Cell.ref_dict[coord].new_state = True
                Cell.ref_dict[coord].update_state()
            return self

        def get_sim_cells(self):
            self.sim_cells = set()
            for coord in Cell.active_cells:
                self.sim_cells.add(coord)
            self.sim_cells.update(
                [(x + a, y + b)
                for a in range(-1,2) for b in range(-1,2)
                for (x,y) in self.sim_cells
                if Cell.valid_coord(Cell.ref_dict[(x,y)], (x + a, y + b))])
            return self

        def update_grid(self):
        
            self.get_sim_cells()
            for coord in self.sim_cells:
                Cell.ref_dict[coord].get_new_state()
            for coord in self.sim_cells:
                Cell.ref_dict[coord].update_state()
            return self

    class App:
        canvas_dict = {}

        def __init__(
                self, grid_size, cell_size,
                active_color = "black", inactive_color = "white",
                condition_dict = {}, initial_active_cells = []):
            self.grid_size = grid_size
            self.cell_size = cell_size
            self.active_color = active_color
            self.inactive_color = inactive_color
            self.condition_dict = condition_dict
            self.initial_active_cells = initial_active_cells

            self.size = grid_size * cell_size
            self.grid = Grid(
                self.grid_size, self.cell_size,
                active_color = self.active_color,
                inactive_color = self.inactive_color,
                condition_dict = self.condition_dict,
                initial_active_cells = self.initial_active_cells)
            self.root = tk.Tk()
            self.canvas = tk.Canvas(
                self.root, bg = "white",
                height = self.size, width = self.size)
            self.canvas.pack()
            self.render_canvas(canvas_created = False)

            self.root.after(1000, self.refresh_display)
            self.root.mainloop()

        def refresh_display(self):
            self.grid.update_grid()
            self.render_canvas(canvas_created = True)
            self.root.after(50, self.refresh_display)

        def render_canvas(self, canvas_created = False):
            if not canvas_created:
                for x in range(0, self.grid_size):
                    for y in range(0, self.grid_size):
                        if (x, y) in self.initial_active_cells:
                            App.canvas_dict[(x, y)] = self.canvas.create_polygon(
                                x * self.cell_size, y * self.cell_size,
                                (x+1) * self.cell_size, y * self.cell_size,
                                (x+1) * self.cell_size, (y+1) * self.cell_size,
                                x * self.cell_size, (y+1) * self.cell_size,
                                fill = self.active_color, outline = "black")
                        else:
                            App.canvas_dict[(x, y)] = self.canvas.create_polygon(
                                x * self.cell_size, y * self.cell_size,
                                (x+1) * self.cell_size, y * self.cell_size,
                                (x+1) * self.cell_size, (y+1) * self.cell_size,
                                x * self.cell_size, (y+1) * self.cell_size,
                                fill = self.inactive_color, outline = "black")
            else:
                for coord in self.grid.sim_cells:
                    if Cell.ref_dict[coord].state:
                        self.canvas.itemconfig(
                            App.canvas_dict[coord], fill = self.active_color)
                    else:
                        self.canvas.itemconfig(
                            App.canvas_dict[coord], fill = self.inactive_color)

    if __name__ == "__main__":
            """app = App(60, 5, initial_active_cells = [
            (25,5), (23,21), (25,22), (13,3),
            (14,31), (21,23), (22,3), (35,34),
            (36,31), (12,34), (16,4), (21,42),
            (22,14), (35,24), (36,14), (19,35),
            (2,15), (11,5), (17,35), (21,5),
            (22,5), (21,16), (22,26), (19,16),
            (15,6), (17,6), (18,16), (23,6),
            (15,36), (11,7), (17,17), (25,7),
            (2,28), (16,38), (33,20), (14,9)])
            app = App(60, 5, initial_active_cells = [
            (25,1), (23,21), (25,22), (13,3),
            (14,31), (21,23), (22,3), (35,34),
            (36,31), (12,34), (16,4), (21,42),
            (22,14), (35,24), (36,14), (19,35),
            (2,15), (11,5), (17,35), (21,5),
            (22,5), (21,16), (22,26), (19,16),
            (15,6), (17,6), (18,16), (23,6),
            (15,36), (11,7), (17,17), (25,7),
            (2,28), (16,38), (33,20), (14,9)])"""


    if run == "4":
            app = App(60, 5, initial_active_cells = [
            (25,1), (23,2), (25,2), (13,3),
            (14,3), (21,3), (22,3), (35,3),
            (36,3), (12,4), (16,4), (21,4),
            (22,4), (35,4), (36,4), (1,5),
            (2,5), (11,5), (17,5), (21,5),
            (22,5), (1,6), (2,6), (11,6),
            (15,6), (17,6), (18,6), (23,6),
            (25,6), (11,7), (17,7), (25,7),
            (12,8), (16,8), (13,9), (14,9)])


    if run == "5":

            app = App(60, 5, initial_active_cells = [
            (25,1), (23,2), (25,2), (13,3),
            (14,3), (21,3), (22,3), (15,3),
            (36,3), (22,4), (16,4), (1,4),
            (22,4), (35,4), (36,4), (11,5),
            (12,5), (11,5), (27,5), (21,5),
            (22,5), (11,6), (2,6), (19,6),
            (15,6), (17,6), (18,6), (23,6),
            (5,6), (11,7), (17,7), (5,7),
            (16,8), (1,8), (13,9), (4,9)])

    if run == "2":
            app = App(60, 5, initial_active_cells = [
            (5,15), (23,21), (25,22), (13,3),
            (14,31), (21,23), (22,3), (5,34),
            (6,31), (2,4), (6,4), (21,2),
            (22,14), (25,24), (36,14), (19,35),
            (2,15), (11,5), (17,35), (31,5),
            (22,5), (21,16), (22,26), (19,16),
            (11,6), (17,6), (8,16), (13,6),
            (5,3), (11,17), (17,17), (25,7),
            (12,8), (6,8), (3,20), (4,9)])


    if run == "1":
            app = App(80, 5, initial_active_cells = [
            (5,1), (23,22), (25,2), (13,3),
            (14,3), (21,3), (22,3), (5,3),
            (36,3), (32,4), (16,4), (21,4),
            (22,4), (35,4), (36,4), (1,5),
            (2,5), (45,5), (17,5), (21,5),
            (2,5), (1,6), (2,6), (11,6),
            (15,6), (17,6), (18,6), (23,6),
            (45,6), (31,7), (27,17), (25,7),
            (12,8), (6,8), (13,19), (14,9)])





    if run == "3":
            app = App(100, 5, initial_active_cells = [
            (25,1), (23,2), (25,2), (13,3),
            (14,3), (21,3), (22,3), (35,3),
            (36,3), (12,4), (16,4), (21,4),
            (22,4), (35,4), (36,4), (1,5),
            (2,5), (11,5), (17,5), (21,5),
            (22,5), (1,6), (2,6), (11,6),
            (15,6), (17,6), (18,6), (23,6),
            (25,6), (1,7), (17,7), (25,7),
            (12,8), (16,8), (31,9), (14,9)])
    else :
        print("Incorrect Input. Please select a given option above.\n")
