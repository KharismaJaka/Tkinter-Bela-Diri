import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

def interpolate_color(c1, c2, t):
    """Interpolate between two hex colors c1 and c2 by fraction t (0 to 1)."""
    c1 = c1.lstrip("#")
    c2 = c2.lstrip("#")
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"

class WelcomePage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.width, self.height = 1280, 720

        self.themes = {
            "dark": {
                "bg": "#0f1626",
                "fg": "#00ffcc",
                "btn_bg": "#00ffcc",
                "btn_fg": "#0f1626",
                "canvas_bg": "#0f1626",
                "desc_fg": "#00ffcc",
                "credit_fg": "#00ffcc",
                "member_bg": "#004f4f",
                "member_fg": "#40e0d0",
                "member_desc_fg": "#a0f0f0",
                "scrollbar_trough": "#00ffcc",
                "scrollbar_active_bg": "#00cca3",
            },
            "light": {
                "bg": "#ffffff",
                "fg": "#2563eb",
                "btn_bg": "#2563eb",
                "btn_fg": "#ffffff",
                "canvas_bg": "#ffffff",
                "desc_fg": "#6b7280",
                "credit_fg": "#2563eb",
                "member_bg": "#e0e7ff",
                "member_fg": "#1e3a8a",
                "member_desc_fg": "#4b5563",
                "scrollbar_trough": "#2563eb",
                "scrollbar_active_bg": "#1e40af",
            },
        }
        self.current_theme = "dark"

        self.config(bg=self.themes[self.current_theme]["bg"])

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            highlightthickness=0,
            bg=self.themes[self.current_theme]["canvas_bg"],
        )
        self.canvas.pack(fill="both", expand=True)

        self.draw_background()
        self.create_title()
        self.create_description()
        self.create_start_button()
        self.create_feedback_label()
        self.create_image_label()
        self.create_credit_info()
        self.create_settings_button()
        self.create_theme_toggle_button()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.config(bg=theme["bg"])
        self.canvas.config(bg=theme["canvas_bg"])
        self.canvas.delete("all")
        self.draw_background()
        self.create_title()
        self.create_description()

        self.start_button.config(
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            activeforeground="white",
        )
        self.feedback_label.config(fg=theme["fg"], bg=theme["bg"])
        self.label_credit.config(fg=theme["credit_fg"], bg=theme["bg"])

        self.info_button.config(
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
        )
        self.settings_button.config(
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
        )
        self.theme_toggle_button.config(
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
        )
        self.label_desc.config(fg=theme["desc_fg"], bg=theme["bg"])
        self.label_image.config(bg=theme["bg"])

    def fade_colors(self, start_colors, end_colors, steps=10, delay=50, step=0):
        """Animate color transitions for bg and fg of various widgets."""
        if step > steps:
            return

        t = step / steps
        new_bg = interpolate_color(start_colors["bg"], end_colors["bg"], t)
        new_fg = interpolate_color(start_colors["fg"], end_colors["fg"], t)
        new_btn_bg = interpolate_color(start_colors["btn_bg"], end_colors["btn_bg"], t)
        new_btn_fg = interpolate_color(start_colors["btn_fg"], end_colors["btn_fg"], t)

        self.config(bg=new_bg)
        self.canvas.config(bg=new_btn_bg)
        self.start_button.config(bg=new_btn_bg, fg=new_btn_fg)
        self.feedback_label.config(bg=new_bg, fg=new_fg)
        self.label_credit.config(bg=new_bg, fg=new_fg)
        self.info_button.config(bg=new_btn_bg, fg=new_btn_fg)
        self.settings_button.config(bg=new_btn_bg, fg=new_btn_fg)
        self.theme_toggle_button.config(bg=new_btn_bg, fg=new_btn_fg)
        self.label_desc.config(bg=new_bg, fg=new_fg)
        self.label_image.config(bg=new_bg)

        self.after(delay, lambda: self.fade_colors(start_colors, end_colors, steps, delay, step + 1))

    def toggle_theme(self):
        start_colors = self.themes[self.current_theme]
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        end_colors = self.themes[self.current_theme]
        self.fade_colors(start_colors, end_colors)

    def draw_background(self):
        if self.current_theme == "light":
            self.canvas.create_rectangle(
                0, 0, self.width, self.height, fill=self.themes["light"]["canvas_bg"], outline=""
            )
        else:
            self.draw_sky_gradient()
            self.draw_sun(1150, 120, 70)
            self.draw_clouds()
            self.draw_grass(0, self.height - 60, self.width, 60)
            self.draw_trees()

    def draw_sky_gradient(self):
        if self.current_theme == "light":
            return

        from_colors = [(10, 25, 70), (25, 76, 146), (82, 137, 217), (176, 214, 235)]
        steps = 150

        for i in range(steps):
            section_index = int(i / (steps / (len(from_colors) - 1)))
            if section_index >= len(from_colors) - 1:
                section_index = len(from_colors) - 2
            color1 = from_colors[section_index]
            color2 = from_colors[section_index + 1]
            ratio = (i % (steps / (len(from_colors) - 1))) / (steps / (len(from_colors) - 1))
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = int(i * self.height / steps)
            y2 = int((i + 1) * self.height / steps)
            self.canvas.create_rectangle(0, y1, self.width, y2, fill=color, outline="")

    def draw_sun(self, x, y, radius):
        if self.current_theme == "light":
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#FFEA00", outline="")
            return

        colors = ["#FFFACD", "#FFF68F", "#FFEF6E", "#FFD700"]
        for i, color in enumerate(colors[::-1]):
            r = radius + i * 12
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#FFEA00", outline="")

    def draw_clouds(self):
        if self.current_theme == "light":
            return

        cloud_positions = [(200, 120, 120), (600, 90, 150), (900, 150, 100), (1100, 130, 130)]
        for x, y, size in cloud_positions:
            self.draw_cloud(x, y, size)

    def draw_cloud(self, x, y, size):
        if self.current_theme == "light":
            return

        radius = size // 4
        circles = [
            (x, y),
            (x + radius * 1.2, y - radius // 2),
            (x + radius * 2.5, y - radius // 4),
            (x + radius * 3.7, y),
            (x + radius * 4.5, y - radius // 3),
        ]
        for cx, cy in circles:
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="white", outline="")

    def draw_grass(self, x_start, y_start, width_area, height_area):
        if self.current_theme == "light":
            return

        for i in range(0, width_area, 15):
            x = x_start + i
            points = [x, y_start, x + 7, y_start - 30, x + 14, y_start]
            self.canvas.create_polygon(points, fill="#228B22", outline="#176917")

    def draw_trees(self):
        if self.current_theme == "light":
            return
        self.draw_tree(80, self.height - 180)
        self.draw_tree_right(self.width - 200, self.height - 180)

    def draw_tree(self, x, y):
        if self.current_theme == "light":
            return

        self.canvas.create_rectangle(x + 10, y, x + 30, y + 100, fill="#5D3A00", outline="#3E2700")
        self.canvas.create_oval(x - 50, y - 120, x + 70, y + 20, fill="#065214", outline="#033d0a")
        self.canvas.create_oval(x - 40, y - 150, x + 60, y - 40, fill="#0A7B1E", outline="#05460d")
        self.canvas.create_oval(x - 20, y - 180, x + 40, y - 80, fill="#0B9D2D", outline="#057318")

    def draw_tree_right(self, x, y):
        if self.current_theme == "light":
            return

        self.canvas.create_rectangle(x + 10, y, x + 30, y + 100, fill="#5D3A00", outline="#3E2700")
        self.canvas.create_oval(x - 30, y - 120, x + 90, y + 20, fill="#065214", outline="#033d0a")
        self.canvas.create_oval(x - 20, y - 150, x + 80, y - 40, fill="#0A7B1E", outline="#05460d")
        self.canvas.create_oval(x, y - 180, x + 60, y - 80, fill="#0B9D2D", outline="#057318")

    def create_title(self):
        self.canvas.delete("title_texts")
        x = self.width // 2
        y = 180
        text = "WELCOME TO THE TRAINING GROUNDS"
        size = 48
        if self.current_theme == "light":
            fg_color = "#2563eb"
            outline_color = "#a3bffa"
        else:
            fg_color = "#00ffcc"
            outline_color = "#003333"

        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for ox, oy in offsets:
            self.canvas.create_text(
                x + ox, y + oy, text=text, font=("Poppins", size, "bold"), fill=outline_color, tags="title_texts"
            )
        self.canvas.create_text(x, y, text=text, font=("Poppins", size, "bold"), fill=fg_color, tags="title_texts")

    def create_description(self):
        desc_text = "Get ready to embark on an epic journey!\nPress START to begin your adventure."
        if hasattr(self, "label_desc"):
            self.label_desc.destroy()
        theme = self.themes[self.current_theme]
        self.label_desc = tk.Label(
            self,
            text=desc_text,
            font=("Segoe UI", 24, "bold italic"),
            fg=theme["desc_fg"],
            bg=theme["bg"],
            justify="center",
            wraplength=700,
        )
        self.label_desc.place(relx=0.5, rely=0.37, anchor="center")

    def create_start_button(self):
        theme = self.themes[self.current_theme]
        self.start_button = tk.Button(
            self,
            text="START YOUR JOURNEY",
            font=("Poppins", 24, "bold"),
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            activeforeground="white",
            bd=0,
            padx=70,
            pady=18,
            cursor="hand2",
            command=self.bangkit_with_animation,
            relief="ridge",
            borderwidth=2,
        )
        self.start_button.place(relx=0.5, rely=0.5, anchor="center")
        self._add_button_hover(self.start_button)

    def create_feedback_label(self):
        theme = self.themes[self.current_theme]
        self.feedback_label = tk.Label(
            self, text="", font=("Poppins", 18, "italic"), fg=theme["fg"], bg=theme["bg"]
        )
        self.feedback_label.place(relx=0.5, rely=0.60, anchor="center")

    def create_image_label(self):
        self.image1 = ImageTk.PhotoImage(Image.open("pendekar_diam.png").resize((320, 320)))
        self.image2 = ImageTk.PhotoImage(Image.open("pendekar_bangkit.png").resize((320, 320)))
        theme = self.themes[self.current_theme]
        self.label_image = tk.Label(self, image=self.image1, bg=theme["bg"], bd=0)
        self.label_image.place(relx=0.5, rely=0.77, anchor="center")

    def create_credit_info(self):
        theme = self.themes[self.current_theme]
        self.label_credit = tk.Label(
            self,
            text="© 2025 SDA Project - Universitas Lampung",
            font=("Poppins", 12, "bold"),
            fg=theme["credit_fg"],
            bg=theme["bg"],
        )
        self.label_credit.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)

        self.info_button = tk.Button(
            self,
            text="Info",
            font=("Poppins", 12, "bold"),
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            bd=0,
            padx=25,
            pady=6,
            cursor="hand2",
            command=self.show_info,
            relief="ridge",
            borderwidth=1,
        )
        self.info_button.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=40)
        self._add_button_hover(self.info_button)

    def create_settings_button(self):
        theme = self.themes[self.current_theme]
        self.settings_button = tk.Button(
            self,
            text="Settings",
            font=("Poppins", 12, "bold"),
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            bd=0,
            padx=25,
            pady=6,
            cursor="hand2",
            command=self.open_settings,
            relief="ridge",
            borderwidth=1,
        )
        self.settings_button.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=75)
        self._add_button_hover(self.settings_button)

    def create_theme_toggle_button(self):
        theme = self.themes[self.current_theme]
        self.theme_toggle_button = tk.Button(
            self,
            text="Toggle Theme",
            font=("Poppins", 12, "bold"),
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            bd=0,
            padx=25,
            pady=6,
            cursor="hand2",
            command=self.toggle_theme,
            relief="ridge",
            borderwidth=1,
        )
        self.theme_toggle_button.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=110)
        self._add_button_hover(self.theme_toggle_button)

    def _add_button_hover(self, button):
        def on_enter(e):
            button.config(bg=button.cget("activebackground"))

        def on_leave(e):
            button.config(bg=self.themes[self.current_theme]["btn_bg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def open_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)

        theme = self.themes[self.current_theme]
        settings_window.configure(bg=theme["bg"])

        label = tk.Label(settings_window, text="Settings", font=("Poppins", 24, "bold"), fg=theme["fg"], bg=theme["bg"])
        label.pack(pady=20)

        self.data_privacy_var = tk.BooleanVar()
        privacy_checkbox = tk.Checkbutton(
            settings_window,
            text="I agree to the data privacy policy",
            variable=self.data_privacy_var,
            font=("Poppins", 12),
            fg=theme["fg"],
            bg=theme["bg"],
            selectcolor=theme["bg"],
            activebackground=theme["bg"],
            activeforeground=theme["fg"],
        )
        privacy_checkbox.pack(pady=15)

        save_button = tk.Button(
            settings_window,
            text="Save Settings",
            font=("Poppins", 14, "bold"),
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=lambda: self.save_settings(settings_window),
            relief="ridge",
            borderwidth=2,
        )
        save_button.pack(pady=20)
        self._add_button_hover(save_button)

        close_button = tk.Button(
            settings_window,
            text="Close",
            font=("Poppins", 12),
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["scrollbar_active_bg"],
            bd=0,
            padx=20,
            pady=6,
            cursor="hand2",
            command=settings_window.destroy,
            relief="ridge",
            borderwidth=1,
        )
        close_button.pack(pady=10)
        self._add_button_hover(close_button)

    def save_settings(self, window):
        if self.data_privacy_var.get():
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Data Privacy Required", "You must agree to the data privacy policy before proceeding.")

    def show_info(self):
        messagebox.showinfo(
            "Application Information",
            "Welcome to Training Grounds!\n\n"
            "This application is a final project for Data Structures and Algorithms.\n\n"
            "- Built with Tkinter\n"
            "- Uses PIL module for images\n"
            "- Features visual animations\n\n"
            "Click START to begin your journey!",
        )

    def bangkit_with_animation(self):
        def bounce(count=0):
            size = 26 if count % 2 == 0 else 24
            self.start_button.config(font=("Poppins", size, "bold"))
            if count < 4:
                self.after(120, lambda: bounce(count + 1))
            else:
                self.show_feedback()

        bounce()

    def show_feedback(self):
        self.feedback_label.config(text="Starting...")
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


class TeamIntroductionPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.themes = {
            "dark": {
                "bg": "#0f1626",
                "fg": "#00ffcc",
                "member_bg": "#004f4f",
                "member_fg": "#40e0d0",
                "member_desc_fg": "#a0f0f0",
                "btn_fg": "#00ffcc", # Add this line
                "btn_bg": "#004f4f", # Add this line
                "scrollbar_active_bg": "#00cca3", # Add this line
            },
            "light": {
                "bg": "#ffffff",
                "fg": "#2563eb",
                "member_bg": "#e0e7ff",
                "member_fg": "#1e3a8a",
                "member_desc_fg": "#4b5563",
                "btn_fg": "#2563eb", # Add this line
                "btn_bg": "#e0e7ff", # Add this line
                "scrollbar_active_bg": "#1e40af", # Add this line
            },
        }
        self.current_theme = "dark"
        theme = self.themes[self.current_theme]
        self.config(bg=theme["bg"])

        self.label_title = tk.Label(
            self,
            text="Meet Our Team",
            font=("Poppins", 38, "bold underline"),
            fg=theme["fg"],
            bg=theme["bg"],
            pady=20,
        )
        self.label_title.pack(pady=30)

        team_members = [
            ("Elsy Aliffia Sirony Putri", "2417051025"),
            ("Kharisma Jaka Harum", "2417051068"),
            ("Rheal Iftiqar Rozak", "2417051029"),
            ("Yulia Nuritnasari", "2457051008"),
        ]

        # Scroll container frame with horizontal scrollbar
        self.scroll_canvas = tk.Canvas(self, bg=theme["bg"], highlightthickness=0, height=310)
        self.scroll_frame = tk.Frame(self.scroll_canvas, bg=theme["bg"])
        self.h_scrollbar = tk.Scrollbar(
            self, orient="horizontal", command=self.scroll_canvas.xview, troughcolor=theme["member_fg"],
            bd=0, highlightthickness=0, activebackground=theme["member_fg"],
        )

        self.scroll_canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.scroll_canvas.pack(fill="x", padx=60)
        self.h_scrollbar.pack(fill="x", padx=60, pady=(0,20))
        self.scroll_window = self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.member_frames = [] # Keep references to member frames

        for name, description in team_members:
            member_frame = tk.Frame(self.scroll_frame, bg=theme["member_bg"], bd=4, relief="ridge", padx=25, pady=18)
            member_frame.pack(side="left", padx=25, pady=0)
            self.member_frames.append(member_frame)

            member_label = tk.Label(
                member_frame,
                text=name,
                font=("Poppins", 16, "bold"),
                fg=theme["member_fg"],
                bg=theme["member_bg"],
                wraplength=260,
                justify="center",
            )
            member_label.pack(pady=(0, 10))

            desc_label = tk.Label(
                member_frame,
                text=description,
                font=("Poppins", 13, "italic"),
                fg=theme["member_desc_fg"],
                bg=theme["member_bg"],
                wraplength=260,
                justify="center",
            )
            desc_label.pack()

        self.scroll_frame.update_idletasks()
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
        self.scroll_canvas.bind("<Configure>", self._on_canvas_configure)

        self.back_button = tk.Button(
            self,
            text="Back to Welcome",
            font=("Poppins", 22, "bold"),
            fg=theme["bg"],
            bg=theme["member_fg"],
            activebackground=theme["member_fg"],
            activeforeground=theme["bg"],
            bd=0,
            padx=40,
            pady=14,
            cursor="hand2",
            command=lambda: controller.show_frame("WelcomePage"),
            relief="ridge",
            borderwidth=3,
        )
        self.back_button.pack(pady=25)
        self._add_button_hover(self.back_button)

        # Add the scoreboard button
        self.create_scoreboard_button()

    def create_scoreboard_button(self):
        theme = self.themes[self.current_theme]
        self.scoreboard_button = tk.Button(
            self,
            text="Go to Scoreboard",
            font=("Poppins", 12, "bold"),
            fg=theme["btn_fg"], # This should now work
            bg=theme["btn_bg"], # This should now work
            activebackground=theme["scrollbar_active_bg"], # This should now work
            bd=0,
            padx=25,
            pady=6,
            cursor="hand2",
            command=lambda: self.controller.show_frame("ScoreboardApp"),
            relief="ridge",
            borderwidth=1,
        )
        self.scoreboard_button.pack(pady=10)
        self._add_button_hover(self.scoreboard_button)

    def _on_canvas_configure(self, event):
        # Adjust scroll region on resize
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))

    def _add_button_hover(self, button):
        def on_enter(e):
            button.config(bg=button.cget("activebackground"))

        def on_leave(e):
            button.config(bg=self.themes[self.current_theme]["member_fg"])

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

class ScoreboardApp(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.time_left = 10
        self.timer_running = False
        self.ao_score = 0
        self.aka_score = 0

        self.themes = {
            "dark": {
                "bg": "#121212",
                "fg": "#00ffcc",
                "ao_bg": "#004080",
                "aka_bg": "#800000",
                "timer_bg": "#000000",
                "timer_fg": "#32cd32",
                "btn_bg": "#00ffcc",
                "btn_fg": "#121212",
                "btn_active_bg": "#00cca3",
                "font": ("Poppins", 14, "bold"),
            },
            "light": {
                "bg": "#f9f9f9",
                "fg": "#2563eb",
                "ao_bg": "#93c5fd",
                "aka_bg": "#fecaca",
                "timer_bg": "#ffffff",
                "timer_fg": "#166534",
                "btn_bg": "#2563eb",
                "btn_fg": "#ffffff",
                "btn_active_bg": "#1e40af",
                "font": ("Poppins", 14, "bold"),
            },
        }
        self.current_theme = "dark"
        theme = self.themes[self.current_theme]

        self.config(bg=theme["bg"])

        # Outer frame to center content
        self.outer_frame = tk.Frame(self, bg=theme["bg"], padx=20, pady=20)
        self.outer_frame.pack(expand=True, fill="both")

        # Title label
        self.title_label = tk.Label(
            self.outer_frame, text="Scoreboard", font=("Poppins", 28, "bold"), fg=theme["fg"], bg=theme["bg"]
        )
        self.title_label.grid(row=0, column=0, columnspan=5, pady=(0, 20))

        # Team names entries with labels
        tk.Label(
            self.outer_frame, text="Team AO:", font=("Poppins", 16, "bold"), fg=theme["fg"], bg=theme["bg"]
        ).grid(row=1, column=0, sticky="e", padx=10)
        self.ao_name = ttk.Entry(self.outer_frame, font=("Poppins", 14))
        self.ao_name.grid(row=1, column=1, padx=10, sticky="ew")

        tk.Label(
            self.outer_frame, text="Team AKA:", font=("Poppins", 16, "bold"), fg=theme["fg"], bg=theme["bg"]
        ).grid(row=1, column=3, sticky="e", padx=10)
        self.aka_name = ttk.Entry(self.outer_frame, font=("Poppins", 14))
        self.aka_name.grid(row=1, column=4, padx=10, sticky="ew")

        self.ao_name.insert(0, "Naruto")
        self.aka_name.insert(0, "Sasuke")

        # Scores frames
        self.ao_frame = tk.Frame(self.outer_frame, bg=theme["ao_bg"], padx=20, pady=15, bd=2, relief="ridge")
        self.ao_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        self.aka_frame = tk.Frame(self.outer_frame, bg=theme["aka_bg"], padx=20, pady=15, bd=2, relief="ridge")
        self.aka_frame.grid(row=2, column=3, columnspan=2, pady=10, sticky="nsew")

        # Configure grid weights
        self.outer_frame.grid_columnconfigure(1, weight=1)
        self.outer_frame.grid_columnconfigure(4, weight=1)
        self.outer_frame.grid_rowconfigure(2, weight=1)

        # AO Score label and buttons
        self.ao_score_label = tk.Label(
            self.ao_frame, text="0", font=("Poppins", 48, "bold"), fg="white", bg=theme["ao_bg"]
        )
        self.ao_score_label.pack(pady=(0, 15), fill="x")

        btn_ao_frame = tk.Frame(self.ao_frame, bg=theme["ao_bg"])
        btn_ao_frame.pack()

        self._create_score_button(btn_ao_frame, "+1", self.add_ao, theme).pack(side="left", padx=8)
        self._create_score_button(btn_ao_frame, "-1", self.sub_ao, theme).pack(side="left", padx=8)

        # AKA Score label and buttons
        self.aka_score_label = tk.Label(
            self.aka_frame, text="0", font=("Poppins", 48, "bold"), fg="white", bg=theme["aka_bg"]
        )
        self.aka_score_label.pack(pady=(0, 15), fill="x")

        btn_aka_frame = tk.Frame(self.aka_frame, bg=theme["aka_bg"])
        btn_aka_frame.pack()

        self._create_score_button(btn_aka_frame, "+1", self.add_aka, theme).pack(side="left", padx=8)
        self._create_score_button(btn_aka_frame, "-1", self.sub_aka, theme).pack(side="left", padx=8)

        # Timer Label
        self.timer_label = tk.Label(
            self.outer_frame,
            text="0:10",
            font=("Poppins", 36, "bold"),
            bg=theme["timer_bg"],
            fg=theme["timer_fg"],
            relief="sunken",
            bd=4,
            padx=20,
            pady=10,
        )
        self.timer_label.grid(row=3, column=0, columnspan=5, pady=20, sticky="ew")

        # Timer buttons
        btn_frame = tk.Frame(self.outer_frame, bg=theme["bg"])
        btn_frame.grid(row=4, column=0, columnspan=5, pady=(0, 10))

        self._create_action_button(btn_frame, "Start", self.start_timer, theme).pack(side="left", padx=10)
        self._create_action_button(btn_frame, "Stop", self.stop_timer, theme).pack(side="left", padx=10)
        self._create_action_button(btn_frame, "Reset", self.reset_timer, theme).pack(side="left", padx=10)
        self._create_action_button(btn_frame, "Save Score", self.save_score_to_csv, theme).pack(side="left", padx=10)


        # Navigation and quit buttons
        nav_frame = tk.Frame(self.outer_frame, bg=theme["bg"])
        nav_frame.grid(row=5, column=0, columnspan=5, pady=10)

        self._create_action_button(nav_frame, "Back", lambda: self.controller.show_frame("WelcomePage"), theme).pack(
            side="left", padx=10
        )
        self._create_action_button(nav_frame, "Quit", self.controller.quit, theme).pack(side="left", padx=10)

    def _create_score_button(self, parent, text, command, theme):
        btn = tk.Button(
            parent,
            text=text,
            font=theme["font"],
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["btn_active_bg"],
            activeforeground=theme["btn_fg"],
            padx=30,
            pady=10,
            bd=0,
            cursor="hand2",
            command=command,
            relief="raised",
            borderwidth=2,
        )
        self._add_button_hover(btn)
        return btn

    def _create_action_button(self, parent, text, command, theme):
        btn = tk.Button(
            parent,
            text=text,
            font=theme["font"],
            fg=theme["btn_fg"],
            bg=theme["btn_bg"],
            activebackground=theme["btn_active_bg"],
            activeforeground=theme["btn_fg"],
            padx=35,
            pady=12,
            bd=0,
            cursor="hand2",
            command=command,
            relief="ridge",
            borderwidth=2,
        )
        self._add_button_hover(btn)
        return btn

    def _add_button_hover(self, button):
        def on_enter(e):
            button.config(bg=button.cget("activebackground"))

        def on_leave(e):
            current_bg = self.themes[self.current_theme]["btn_bg"]
            button.config(bg=current_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f"{minutes}:{seconds:02d}")
            self.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_running = False
            messagebox.showinfo("Timer", "Time's up!")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.time_left = 10
        self.timer_label.config(text="0:10")

    def add_ao(self):
        self.ao_score += 1
        self.ao_score_label.config(text=str(self.ao_score))

    def sub_ao(self):
        self.ao_score = max(0, self.ao_score - 1)
        self.ao_score_label.config(text=str(self.ao_score))

    def add_aka(self):
        self.aka_score += 1
        self.aka_score_label.config(text=str(self.aka_score))

    def sub_aka(self):
        self.aka_score = max(0, self.aka_score - 1)
        self.aka_score_label.config(text=str(self.aka_score))

    def save_score_to_csv(self): # ini akan otomatis aman walau sudah ada di atas
        import csv
        ao_name = self.ao_name.get()
        aka_name = self.aka_name.get()
        ao_score = self.ao_score
        aka_score = self.aka_score

        with open("score.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([ao_name, ao_score, aka_name, aka_score])

        messagebox.showinfo("Score Saved", "Score berhasil disimpan ke score.csv!")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pendekar Training Grounds")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Initialize pages in the desired order
        for Page in (WelcomePage, TeamIntroductionPage, ScoreboardApp):
            frame = Page(container, self)
            self.frames[Page.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("WelcomePage") # Show the WelcomePage first

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()



if __name__ == "__main__":
    app = App()
    app.mainloop()
