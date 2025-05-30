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

    def draw_cloud(self, x, y, size):
        radius = size // 4
        circles = [
            (x, y),
            (x + radius * 1.2, y - radius // 2),
            (x + radius * 2.5, y - radius // 4),
            (x + radius * 3.7, y),
            (x + radius * 4.5, y - radius // 3)
        ]
        for cx, cy in circles:
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                    fill="white", outline="")

    def draw_grass(self, x_start, y_start, width_area, height_area):
        for i in range(0, width_area, 15):
            x = x_start + i
            points = [x, y_start, x + 7, y_start - 30, x + 14, y_start]
            self.canvas.create_polygon(points, fill="#228B22", outline="#176917")

    def draw_trees(self):
        self.draw_tree(80, self.height - 180)
         self.draw_tree_right(self.width - 200, self.height - 180)

    def draw_tree(self, x, y):
        self.canvas.create_rectangle(x + 10, y, x + 30, y + 100, fill="#5D3A00", outline="#3E2700")
        self.canvas.create_oval(x - 50, y - 120, x + 70, y + 20, fill="#065214", outline="#033d0a")
        self.canvas.create_oval(x - 40, y - 150, x + 60, y - 40, fill="#0A7B1E", outline="#05460d")
        self.canvas.create_oval(x - 20, y - 180, x + 40, y - 80, fill="#0B9D2D", outline="#057318")

    def draw_tree_right(self, x, y):
        self.canvas.create_rectangle(x + 10, y, x + 30, y + 100, fill="#5D3A00", outline="#3E2700")
        self.canvas.create_oval(x - 30, y - 120, x + 90, y + 20, fill="#065214", outline="#033d0a")
        self.canvas.create_oval(x - 20, y - 150, x + 80, y - 40, fill="#0A7B1E", outline="#05460d")
        self.canvas.create_oval(x, y - 180, x + 60, y - 80, fill="#0B9D2D", outline="#057318")

    def create_title(self):
        self.create_gaming_text(self.width // 2, 180, "WELCOME TO THE TRAINING GROUNDS", 48, "#00ffcc", "#003333")

    def create_gaming_text(self, x, y, text, size, fg_color, outline_color):
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for ox, oy in offsets:
            self.canvas.create_text(x + ox, y + oy, text=text, font=("Poppins", size, "bold"), fill=outline_color)
        self.canvas.create_text(x, y, text=text, font=("Poppins", size, "bold"), fill=fg_color)

    def create_description(self):
        desc_text = "Get ready to embark on an epic journey!\nPress START to begin your adventure."
        if hasattr(self, 'label_desc'):
            self.label_desc.destroy()
        self.label_desc = tk.Label(
            self,
            text=desc_text,
            font=("Segoe UI", 24, "bold italic"),
            fg="#00ffcc",
            bg="#0f1626",
            justify="center",
            wraplength=700
        )
        self.label_desc.place(relx=0.5, rely=0.37, anchor="center")

    def create_start_button(self):
        self.start_button = tk.Button(
            self,
            text="START YOUR JOURNEY",
            font=("Poppins", 22, "bold"),
            fg="#0f1626", bg="#00ffcc", activebackground="#00cca3",
            activeforeground="white", bd=0, padx=60, pady=18,
            cursor="hand2", command=self.bangkit_with_animation
        )
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")

    def create_feedback_label(self):
        self.feedback_label = tk.Label(self, text="", font=("Poppins", 16, "bold italic"), fg="#00ffcc", bg="#0f1626")
        self.feedback_label.place(relx=0.5, rely=0.58, anchor="center")

    def create_image_label(self):
        self.image1 = ImageTk.PhotoImage(Image.open("pendekar_diam.png").resize((320, 320)))
        self.image2 = ImageTk.PhotoImage(Image.open("pendekar_bangkit.png").resize((320, 320)))
        self.label_image = tk.Label(self, image=self.image1, bg="#0f1626", bd=0)
        self.label_image.place(relx=0.5, rely=0.77, anchor="center")

    def create_credit_info(self):
        self.label_credit = tk.Label(
            self,
            text="© 2025 SDA Project - Universitas Lampung",
            font=("Poppins", 12, "bold"),
            fg="#00ffcc",
            bg="#0f1626"
        )
        self.label_credit.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)

        self.info_button = tk.Button(
            self,
            text="❓ Info",
            font=("Poppins", 12),
            fg="#0f1626", bg="#00ffcc", activebackground="#00cca3",
            bd=0, padx=20, pady=5, cursor="hand2", command=self.show_info
        )
        self.info_button.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=40)

    def show_info(self):
        messagebox.showinfo("Informasi Aplikasi",
                            "👋 Selamat datang di Training Grounds!\n\n"
                            "Aplikasi ini adalah bagian dari proyek akhir Struktur Data dan Algoritma.\n\n"
                            "- Dibuat dengan Tkinter\n"
                            "- Menggunakan modul PIL untuk gambar\n"
                            "- Berbasis antarmuka visual dan animasi\n\n"
                            "Klik START untuk memulai perjalananmu!")

    def bangkit_with_animation(self):
        def bounce(count=0):
            self.start_button.config(font=("Poppins", 24 if count % 2 == 0 else 22, "bold"))
            if count < 3:
                self.after(100, lambda: bounce(count + 1))
            else:
                self.show_feedback()
        bounce()

    def show_feedback(self):
        self.feedback_label.config(text="Memulai...")
        alpha = 1.0

        def fade_out():
            nonlocal alpha
            alpha -= 0.1
            if alpha <= 0:
                self.feedback_label.config(text="")
                self.bangkit()
            else:
                fg_color = f"#{int(0 * alpha):02x}{int(255 * alpha):02x}{int(204 * alpha):02x}"
                self.feedback_label.config(fg=fg_color)
                self.after(100, fade_out)
        fade_out()

    def bangkit(self):
        self.label_image.config(image=self.image2)
        self.after(1500, lambda: self.controller.show_frame("TeamIntroductionPage"))
