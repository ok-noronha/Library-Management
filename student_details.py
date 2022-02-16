from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import os


class studentDeailsWindow:

    isselected = False

    def create_window(self, mainloop):
        self.width = 600
        self.height = 400

        _win = Toplevel()
        self._win = _win
        self.main_win_loop = mainloop
        self.screen_width = int((self._win.winfo_screenwidth()) / 4)
        self.screen_height = int((self._win.winfo_screenheight()) / 6)

        self._win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self._win.title("Student Details")
        self._win.resizable(FALSE, FALSE)
        self._win.configure(bg="#CCCCFF")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/christlabel.png"))
        self.top_label = Label(self._win, image=self.photo0, bg="white")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.del_button = Button(
            self._win,
            text="Delete",
            font=("Nirmala UI", 15, "bold"),
            bg="gold",
            command=self.delete_student,
        )
        self.del_button.place(x=470, y=300)

        self.showtree()
        self.show_details()

        self.treev.bind("<ButtonRelease-1>", self.get_image)
        self._win.protocol("WM_DELETE_WINDOW", self.on_closing__win)
        self._win.mainloop()

    def on_closing__win(self):
        self._win.destroy()
        self.main_win_loop.deiconify()

    def showtree(self):

        self.frame = Frame(self._win, bg="#CCCCFF", relief="flat")
        self.frame.place(x=1, y=66, width=450, height=330)

        # constructing vertical scroll bar with tree view
        self.verscr = ttk.Scrollbar(self.frame, orient=VERTICAL)
        self.horscr = ttk.Scrollbar(self.frame, orient=HORIZONTAL)

        # using tree view widget

        self.treev = ttk.Treeview(
            self.frame,
            selectmode="browse",
            xscrollcommand=self.horscr.set,
            yscrollcommand=self.verscr.set,
        )

        self.verscr.pack(side=RIGHT, fill=Y)
        self.horscr.pack(side=BOTTOM, fill=X)

        self.verscr.config(command=self.treev.yview)
        self.horscr.config(command=self.treev.xview)

        # Style

        self.style = ttk.Style()
        self.style.configure(
            "Treeview", background="lightgray", foreground="black", rowheight=20
        )
        self.style.map("Treeview", background=[("selected", "green")])

        # Defining columns
        self.treev["columns"] = (1, 2, 3, 4, 5, 6)
        self.treev.column(1, width=90, anchor="c")
        self.treev.column(2, width=90, anchor="c")
        self.treev.column(3, width=90, anchor="c")
        self.treev.column(4, width=90, anchor="c")
        self.treev.column(5, width=90, anchor="c")
        # Defining headings
        self.treev["show"] = "headings"
        self.treev.heading(1, text="Email Id")
        self.treev.heading(2, text="Name")
        self.treev.heading(3, text="Contact")
        self.treev.heading(4, text="Date of Joining")
        self.treev.heading(5, text="Department")
        self.treev.place(x=0, y=0, width=383, height=313)

    def show_details(self):
        # connecting to postgres database
        connection = psycopg2.connect(
            user="kevin",
            password="2048",
            host="localhost",
            port="5432",
            database="libdb",
        )
        cursor = connection.cursor()

        cursor.execute("select id, name, mobilenumber, doj, dept_id from readers")
        self.row = cursor.fetchall()
        self.treev.delete(*self.treev.get_children())
        if len(self.row) != 0:

            for i in self.row:
                self.treev.insert("", "end", values=i)

        connection.close()

    def get_image(self, ev):

        try:
            self.isselected = True
            # self.curr_row = self.treev.focus()
            # self.contents = self.treev.item(self.curr_row)
            # self.info = self.contents['values']
            #
            #
            # self.label_image = Label(self._win, bg="#CCCCFF", bd=2)
            # self.label_image.place(x=440, y=130, width=100, height=100)
            #
            #
            # # connecting to postgres database
            # connection = psycopg2.connect(user="kevin",
            #                           password="2048",
            #                           host="localhost",
            #                           port="5432",
            #                           database="libdb")
            # cursor = connection.cursor()
            #
            # cursor.execute(f"select image from readers where id = '{self.info[0]}'")
            # self.row_img = cursor.fetchone()
            # connection.close()
            #
            # #writing binary data to file
            #
            # self.picimg = open("Test.png", 'wb')
            # self.picimg.write((self.row_img[0]))
            # self.picimg.close()
            # self.img_picimg = Image.open("Test.png")
            #
            # self.resize_image = self.img_picimg.resize((100,100), Image.ANTIALIAS)
            # self.pic = ImageTk.PhotoImage(self.resize_image)
            #
            # self.label_image.config(image=self.pic)
            # os.remove("Test.png")
            #
            # self.label_1 = Label(self._win, bg="#CCCCFF", bd=2, text="Image", font=("Nirmala UI", 15, 'bold'))
            # self.label_1.place(x=480, y=80)

        except:
            self.isselected = False

    def delete_student(self):

        if self.isselected == True:
            self.curr_row = self.treev.focus()
            self.contents = self.treev.item(self.curr_row)
            self.info = self.contents["values"]

            # connecting to postgres database
            connection = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )
            cursor = connection.cursor()
            print("conn")

            cursor.execute(f"delete from readers where id = '{self.info[0]}'")
            connection.commit()
            connection.close()
            print("exe")
            self.isselected = False
            self.show_details()
            messagebox.showinfo(
                "Library Management System", "Student Deleted Successfully"
            )
            self.label_12 = Label(self._win, bg="#CCCCFF", bd=2)
            self.label_12.place(x=460, y=80, width=70, height=50)
            self.label_image1 = Label(self._win, bg="#CCCCFF", bd=2)
            self.label_image1.place(x=440, y=130, width=100, height=100)

            self.show_details()
