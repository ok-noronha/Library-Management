from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
import os


class bookDeailsWindow:

    _isselected = False

    def book_details_window(self, mainwin):
        self.width = 600
        self.height = 400

        bookwin = Toplevel()
        self.bookwin = bookwin
        self.main_win_loop = mainwin

        self.screen_width = int((self.bookwin.winfo_screenwidth()) / 4)
        self.screen_height = int((self.bookwin.winfo_screenheight()) / 6)

        self.bookwin.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.bookwin.title("Book Details")
        self.bookwin.resizable(FALSE, FALSE)
        self.bookwin.configure(bg="#CCCCFF")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/christlabel.png"))
        self.top_label = Label(self.bookwin, image=self.photo0, bg="white")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.delbutton = Button(
            self.bookwin,
            text="Delete",
            font=("Nirmala UI", 15, "bold"),
            bg="gold",
            command=self.delete_book,
        )
        self.delbutton.place(x=470, y=300)

        self.treeview()
        self.showdetails()

        self.trrv.bind("<ButtonRelease-1>", self.getimage)

        self.bookwin.protocol("WM_DELETE_WINDOW", self.on_closing_bookwin)
        self.bookwin.mainloop()

    def on_closing_bookwin(self):
        self.bookwin.destroy()
        self.main_win_loop.deiconify()

    def treeview(self):

        self.frame = Frame(self.bookwin, bg="#CCCCFF", relief="flat")
        self.frame.place(x=1, y=66, width=400, height=330)

        # constructing vertical scroll bar with tree view
        self.verscr = ttk.Scrollbar(self.frame, orient=VERTICAL)
        self.horscr = ttk.Scrollbar(self.frame, orient=HORIZONTAL)

        # using tree view widget

        self.trrv = ttk.Treeview(
            self.frame,
            selectmode="browse",
            xscrollcommand=self.horscr.set,
            yscrollcommand=self.verscr.set,
        )

        self.verscr.pack(side=RIGHT, fill=Y)
        self.horscr.pack(side=BOTTOM, fill=X)

        self.verscr.config(command=self.trrv.yview)
        self.horscr.config(command=self.trrv.xview)

        # Style

        self.style = ttk.Style()
        self.style.configure(
            "Treeview", background="lightgray", foreground="black", rowheight=20
        )
        self.style.map("Treeview", background=[("selected", "gold")])

        # Defining columns
        self.trrv["columns"] = (1, 2, 3, 4, 5, 6, 7)
        self.trrv.column(1, width=90, anchor="c")
        self.trrv.column(2, width=90, anchor="c")
        self.trrv.column(3, width=90, anchor="c")
        self.trrv.column(4, width=90, anchor="c")
        self.trrv.column(5, width=90, anchor="c")
        self.trrv.column(6, width=90, anchor="c")
        self.trrv.column(7, width=90, anchor="c")
        # Defining headings
        self.trrv["show"] = "headings"
        self.trrv.heading(1, text="ISBN Number")
        self.trrv.heading(2, text="Book Title")
        self.trrv.heading(3, text="Category")
        self.trrv.heading(4, text="Author")
        self.trrv.heading(5, text="Publisher")
        self.trrv.heading(6, text="Date of publication")
        self.trrv.heading(7, text="Quantity")
        self.trrv.place(x=0, y=0, width=383, height=313)

    def showdetails(self):
        # connecting to postgres database
        connection = psycopg2.connect(
            user="kevin",
            password="2048",
            host="localhost",
            port="5432",
            database="libdb",
        )
        cursor = connection.cursor()

        cursor.execute(
            "select isbn, title, category, author, publisher, dop, number from books"
        )
        self.row = cursor.fetchall()
        self.trrv.delete(*self.trrv.get_children())
        if len(self.row) != 0:
            for i in self.row:
                self.trrv.insert("", "end", values=i)

        connection.close()

    def getimage(self, ev):

        try:
            self._isselected = True
            # self.curr_row = self.trrv.focus()
            # self.contents = self.trrv.item(self.curr_row)
            # self.info = self.contents['values']
            #
            #
            # self.label_image = Label(self.bookwin, bg="#CCCCFF", bd=2)
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
            # cursor.execute(f"select image from books where isbn = '{self.info[0]}'")
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
            # self.label_1 = Label(self.bookwin, bg="#CCCCFF", bd=2, text="Image", font=("Nirmala UI", 15, 'bold'))
            # self.label_1.place(x=460, y=80)

        except:
            self._isselected = False

    def delete_book(self):

        if self._isselected == True:
            self.curr_row = self.trrv.focus()
            self.contents = self.trrv.item(self.curr_row)
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

            cursor.execute(f"delete from books where isbn = '{self.info[0]}'")
            connection.commit()
            connection.close()
            self._isselected = False
            messagebox.showinfo(
                "Library Management System", "Book Removed Successfully"
            )
            self.label_12 = Label(self.bookwin, bg="#CCCCFF", bd=2)
            self.label_12.place(x=460, y=80, width=70, height=50)
            self.label_image1 = Label(self.bookwin, bg="#CCCCFF", bd=2)
            self.label_image1.place(x=440, y=130, width=100, height=100)

            self.showdetails()
