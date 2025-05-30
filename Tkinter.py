import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

class WelcomePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#0f1626")
        self.controller = controller
        self.width, self.height = 1280, 720

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, highlightthickness=0, bg="#0f1626")
        self.canvas.pack(fill="both", expand=True)

        self.draw_background()
        self.create_title()
        self.create_description()
        self.create_start_button()
        self.create_feedback_label()
        self.create_image_label()
        self.create_credit_info()

    def draw_background(self):
        self.draw_sky_gradient()
        self.draw_sun(1150, 120, 70)
        self.draw_clouds()
        self.draw_grass(0, self.height - 60, self.width, 60)
        self.draw_trees()
        
    def draw_sky_gradient(self):
        from_colors = [(10, 25, 70), (25, 76, 146), (82, 137, 217), (176, 214, 235)]
        steps = 150
        section_height = self.height / (len(from_colors) - 1)
        for i in range(steps):
            section_index = int(i / (steps / (len(from_colors) -1)))
            if section_index >= len(from_colors) -1 :
                section_index = len(from_colors) - 2
            color1 = from_colors[section_index]
            color2 = from_colors[section_index + 1]
            ratio = (i % (steps / (len(from_colors) - 1))) / (steps / (len(from_colors) -1))
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = int(i * self.height / steps)
            y2 = int((i+1)* self.height / steps)
            self.canvas.create_rectangle(0,y1,self.width,y2, fill=color, outline="")

    def draw_sun(self, x, y, radius):
        colors = ["#FFFACD", "#FFF68F", "#FFEF6E", "#FFD700"]
        for i, color in enumerate(colors[::-1]):
            r = radius + i * 12
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#FFEA00", outline="")

    def draw_clouds(self):
        cloud_positions = [(200, 120, 120), (600, 90, 150), (900, 150, 100), (1100, 130, 130)]
        for x, y, size in cloud_positions:
            self.draw_cloud(x, y, size)
