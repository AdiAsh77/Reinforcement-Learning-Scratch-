import customtkinter as ctk # type: ignore
from main import rl, maze_path, block_tuple, evaluation, eval_plot, row_mat, column_mat, q_table
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GridApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("REINFORCEMENT LEARNING")
        self.geometry("1000x700")
        dist = 100
        self.evaluation_list = [[],[]]
        self.rows = row_mat
        self.columns = column_mat
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 15, 30, 25]



        # Main container — everything aligned to the left
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
            anchor="nw"
        )

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="UI visualizer for REINFORCEMENT LEARNING",
            font=("Arial", 26, "bold")
        )
        self.title_label.pack(anchor="w", pady=(0, 20))

        # Controls
        self.controls_frame = ctk.CTkFrame(
            self.main_frame,
            border_width=2,
            border_color="blue"
        )
        self.controls_frame.pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(
            self.controls_frame,
            text="Rows:"
        ).grid(row=0, column=0, padx=(15, 5), pady=15)

        self.rows_entry = ctk.CTkEntry(
            self.controls_frame,
            width=80,
            placeholder_text="Rows",
        )
        self.rows_entry.grid(row=0, column=1, padx=5, pady=15)
        self.rows_entry.insert(0, f"{self.rows}")

        ctk.CTkLabel(
            self.controls_frame,
            text="Columns:"
        ).grid(row=0, column=2, padx=5, pady=15)

        self.columns_entry = ctk.CTkEntry(
            self.controls_frame,
            width=80,
            placeholder_text="Columns"
        )
        self.columns_entry.grid(row=0, column=3, padx=5, pady=15)
        self.columns_entry.insert(0, f"{self.columns}")

        self.generate_button = ctk.CTkButton(
            self.controls_frame,
            text="-:START ALGO:-",
            command=self.path
        )
        self.generate_button.grid(
            row=0, column=4, padx=15, pady=15
        )


        self.container = ctk.CTkFrame(
            self.main_frame
        )
        self.container.pack(anchor='w', padx=(120,0))


        # Grid workspace — positioned on the left
        self.grid_frame1 = ctk.CTkFrame(
            self.container,
            border_width=2,
            border_color="grey",
            width=400,
            height=360,
        )
        self.grid_frame1.pack(side='left', padx = (10, dist), pady=10)
        self.grid_frame1.pack_propagate(False)

        self.canvas1 = ctk.CTkCanvas(
            self.grid_frame1,
            width=450,
            height=400,
            bg="#202020",
            highlightthickness=0
        )
        self.canvas1.pack(padx=10, pady=20, expand="true")

        self.episode_label = ctk.CTkLabel(
            self.container,
            text="Episode Count: ",
            font=("Arial", 26, "bold")
        )
        self.episode_label.pack(side='left', anchor="w")
        
        # Grid workspace — positioned on the left
        self.grid_frame2 = ctk.CTkFrame(
            self.container,
            border_width=2,
            border_color="grey",
            width=400,
            height=360,
        )
        self.grid_frame2.pack(side='left', padx = (dist, 10), pady=10)
        self.grid_frame2.pack_propagate(False)

        self.canvas2 = ctk.CTkCanvas(
            self.grid_frame2,
            width=450,
            height=400,
            bg="#202020",
            highlightthickness=0
        )
        self.canvas2.pack(padx=10, pady=20, expand="true")
        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.pack(fill="x", anchor="w")

        self.draw_grid(self.canvas1)
        self.draw_grid(self.canvas2)

        # data = [
        #         [[0, 0, 0, 0] for _ in range(self.rows)]
        #         for _ in range(self.columns)
        #     ]
        
        self.create_table(q_table)
        self.create_graph()
        for i in block_tuple:
            self.draw_block(self.canvas1, i[0], i[1])
        # self.path()

    def generate_grid(self):
        try:
            rows = int(self.rows_entry.get())
            columns = int(self.columns_entry.get())

            if not (1 <= rows <= 50 and 1 <= columns <= 50):
                raise ValueError

            self.rows = rows
            self.columns = columns
            self.draw_grid()

        except ValueError:
            print("Enter valid row and column values between 1 and 50.")

    def draw_grid(self, canvas):
        canvas.delete("all")

        canvas_width = 450
        canvas_height = 400

        cell_width = canvas_width / self.columns
        cell_height = canvas_height / self.rows

        self.cell_rects1 = []
        cell_rects = self.cell_rects1

        # Draw grid cells and labels
        for row in range(self.rows):
            rect_row = []
            for col in range(self.columns):
                x1 = col * cell_width
                y1 = row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                rect_id = canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="#777777",
                    width=2
                )
                rect_row.append(rect_id)



                canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=f"{row}, {col}",
                    # text=f"{col}, {(self.rows -1)-row}",
                    fill="white",
                    font=("Arial", 10)
                )
            cell_rects.append(rect_row)

        # Draw a line from the first cell to the last cell
        # self.draw_arrow(canvas, 2,3,4)
        

    def draw_line(self, canvas, row1, col1, row2, col2):
        canvas_width = 450
        canvas_height = 400

        cell_width = canvas_width / self.columns
        cell_height = canvas_height / self.rows
       
        x1 = (col1+1 - 0.5) * cell_width
        y1 = (row1+1 - 0.5) * cell_height

        x2 = (col2+1 - 0.5) * cell_width
        y2 = (row2+1 - 0.5) * cell_height

        canvas.create_line(
            x1, y1, x2, y2,
            fill="red",
            tags="line",
            width=3
        )
    
    def draw_arrow(self, canvas, row1, col1, action):
        canvas_width = 450
        canvas_height = 400

        cell_width = canvas_width / self.columns
        cell_height = canvas_height / self.rows

        if action == 1:
            x1 = (col1+1 - 0.5) * cell_width
            y1 = (row1+1 - 0.1) * cell_height

            x2 = (col1+1 - 0.5) * cell_width
            y2 = (row1+1 - 0.9) * cell_height

        elif action == 2:
            x1 = (col1+1 - 0.5) * cell_width
            y1 = (row1+1 - 0.9) * cell_height

            x2 = (col1+1 - 0.5) * cell_width
            y2 = (row1+1 - 0.1) * cell_height
        
        elif action == 3:
            x1 = (col1+1 - 0.1) * cell_width
            y1 = (row1+1 - 0.5) * cell_height

            x2 = (col1+1 - 0.9) * cell_width
            y2 = (row1+1 - 0.5) * cell_height

        elif action == 4:
            x1 = (col1+1 - 0.9) * cell_width
            y1 = (row1+1 - 0.5) * cell_height

            x2 = (col1+1 - 0.1) * cell_width
            y2 = (row1+1 - 0.5) * cell_height

        canvas.create_line(
            x1, y1, x2, y2,
            arrow=ctk.LAST,
            arrowshape=(14,19,6),
            fill="red",
            tags="line",
            width=4
        )

    def draw_block(self, canvas, row1, col1):
        canvas_width = 450
        canvas_height = 400

        cell_width = canvas_width / self.columns
        cell_height = canvas_height / self.rows
   
        x1 = (col1+1 - 0.9) * cell_width
        y1 = (row1+1 - 0.1) * cell_height

        x2 = (col1+1 - 0.9) * cell_width
        y2 = (row1+1 - 0.9) * cell_height

        x3 = (col1+1 - 0.1) * cell_width
        y3 = (row1+1 - 0.1) * cell_height
        
        x4 = (col1+1 - 0.1) * cell_width
        y4 = (row1+1 - 0.9) * cell_height

        canvas.create_line(
            x1, y1, x4, y4,
            fill="#5B56F6",
            width=5
        )
        
        canvas.create_line(
            x3, y3, x2, y2,
            fill="#5B56F6",
            width=5
        )
        canvas.create_rectangle(
                x1, y1, x4, y4,
                outline="#5B56F6",
                width=5
            )


    def change_cell_color(self, canvas, row, col, color):
        # Convert from 1-based grid coordinates to 0-based list indices
        # row -= 1
        # col -= 1

        if not (0 <= row < self.rows and 0 <= col < self.columns):
            return

        if canvas == self.canvas1:
            rect_id = self.cell_rects1[row][col]
        elif canvas == self.canvas2:
            rect_id = self.cell_rects2[row][col]
        else:
            return

        canvas.itemconfig(rect_id, fill=color)


    def path(self,episodes=0):
        self.change_cell_color(self.canvas1, 2, 4, "#202020")
        if episodes >500:
            print(self.evaluation_list)
            # eval_plot(self.evaluation_list)
            return
        
        if episodes % 5 == 0:
            self.evaluation_list[0].append(episodes)
            self.evaluation_list[1].append(evaluation(episodes))
            self.update_graph(self.evaluation_list)
            # print(episodes)
        self.canvas1.delete("line")
        self.canvas2.delete("line")
        path_list, ac, j = rl(episodes)
        # print(path_list)

        for i in range(1, len(path_list)):
            self.draw_line(self.canvas1, path_list[i-1][0], path_list[i-1][1], path_list[i][0], path_list[i][1])
            self.draw_arrow(self.canvas2, path_list[i-1][0], path_list[i-1][1], ac[i-1])
        if (path_list[-1] == (2,4)):
            self.change_cell_color(self.canvas1, 2, 4, "#5CDA22")
            # print("lesgoo reached")
        self.update_table(j)
        print("current episode: ",episodes)
        self.episode_label.configure( text=f"Episode Count: {episodes}" )
        # n = 1
        # m = 2 - 0
        # self.change_cell_color(self.canvas1, m,n, "green")
        self.after(110, lambda: self.path(episodes + 1))

    def val_string(self, val):
        string = f"1: {val[0]}\n2: {val[1]}\n3: {val[2]}\n4: {val[3]}"
        return string

    def update_graph(self, j):
        self.ax.clear()

        x = j[0]
        y = j[1]
        self.ax.plot(x, y)

        self.fig.tight_layout()
        self.graph_canvas.draw_idle()

    def create_graph(self):
        self.graph_frame = ctk.CTkFrame(self.bottom_frame)
        self.graph_frame.pack(side="left", padx=(200, 0), pady=(10,0))

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.graph_canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.graph_frame
        )
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack()


    def update_table(self, data):
        for row_index, row in enumerate(data):
            for col_index, values in enumerate(row):
                self.table_cells[row_index][col_index].configure(
                    text=self.val_string(values)
                )

    def create_table(self, data):
        table_width = 600
        table_height = 320

        rows = len(data)
        cols = max((len(row) for row in data), default=0)

        if rows == 0 or cols == 0:
            return

        

        self.table_frame = ctk.CTkFrame(
            self.bottom_frame,
            width=table_width,
            height=table_height,
            border_width=3,
            corner_radius=0
        )
        self.table_frame.pack(anchor="w", side="left", pady=(15, 0), padx=(80,0))
        self.table_frame.pack_propagate(False)

        cell_width = table_width / cols
        cell_height = table_height / rows
        font_size = max(6, int(min(cell_width, cell_height) * 0.20))

        # Store references to cell labels
        self.table_cells = []

        for row_index, row in enumerate(data):
            cell_row = []

            for col_index, values in enumerate(row):
                cell_frame = ctk.CTkFrame(
                    self.table_frame,
                    width=cell_width,
                    height=cell_height,
                    corner_radius=0,
                    border_width=1,
                    border_color="white"
                )
                cell_frame.grid(
                    row=row_index,
                    column=col_index,
                    padx=1,
                    pady=1,
                    sticky="nsew"
                )
                cell_frame.grid_propagate(False)

                cell = ctk.CTkLabel(
                    cell_frame,
                    text=self.val_string(values),
                    fg_color="#2b2b2b",
                    text_color="white",
                    corner_radius=0,
                    anchor="center",
                    font=ctk.CTkFont(size=font_size)
                )
                cell.grid(
                    row=0,
                    column=0,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

                cell_frame.grid_rowconfigure(0, weight=1)
                cell_frame.grid_columnconfigure(0, weight=1)

                # Save this label
                cell_row.append(cell)

            self.table_cells.append(cell_row)

        for col_index in range(cols):
            self.table_frame.grid_columnconfigure(
                col_index, weight=1, uniform="columns"
            )

        for row_index in range(rows):
            self.table_frame.grid_rowconfigure(
                row_index, weight=1, uniform="rows"
            )

def maximize():
    app.state('zoomed')

if __name__ == "__main__":
    app = GridApp()
    # app.after(0, maximize)
    
    app.mainloop()
