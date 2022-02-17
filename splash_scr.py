import time
from tkinter import *
from tkinter.ttk import Progressbar, Style
from PIL import Image, ImageTk

import global_data


class SplashScreen:
    def __init__(self):

        gdt = global_data.GDT()

        self.width = gdt.width
        self.height = gdt.height

        splash_win = Tk()
        self.splash_win = splash_win

        self.screen_width = int((self.splash_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.splash_win.winfo_screenheight()) / 6)

        self.splash_win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.splash_win.overrideredirect(1)

        self.img = gdt.sp_sc
        self.resized_image = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resized_image)

        self.canvas = Canvas(self.splash_win)
        self.canvas.pack(fill=BOTH, expand=1)

        self.style = Style(self.canvas)
        self.style.layout(
            "LabeledProgressbar",
            [
                (
                    "LabeledProgressbar.trough",
                    {
                        "children": [
                            (
                                "LabeledProgressbar.pbar",
                                {"side": "left", "sticky": "ns"},
                            ),
                            ("LabeledProgressbar.label", {"sticky": ""}),
                        ],
                        "sticky": "nswe",
                    },
                )
            ],
        )

        info = gdt.coder
        self.canvas.create_image(0, 0, anchor="nw", image=self.new_image)
        self.canvas.create_text(
            100,
            self.height - 30,
            text=info,
            font=("Nirmala UI", "8"),
            fill=gdt.coder_color,
        )

        # creating progress bar
        self.progress = Progressbar(
            self.canvas,
            style="LabeledProgressbar",
            orient=HORIZONTAL,
            length=400,
            mode="determinate",
        )
        self.progress.pack(side=BOTTOM, padx=30, pady=100)

        self.style.configure("LabeledProgressbar", text="0 %")
        self.style.configure(
            "LabeledProgressbar", background=gdt.prog_bar_bg, foreground=gdt.prog_bar_fg
        )

        def update():
            for i in range(self.progress["maximum"] + 1):
                self.style.configure("LabeledProgressbar", text="{0} %".format(i))
                time.sleep(0.03)
                self.progress["value"] = i
                self.canvas.update()
            time.sleep(1)
            self.splash_win.destroy()

        self.progress.after(1, update)

        self.splash_win.mainloop()
