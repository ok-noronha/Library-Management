from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
import psycopg2


class IssueBook:
    def issue_book_window(self, mainloop):
        # width and height of the window
        self.width = 600
        self.height = 400
        self.main_win_loop = mainloop
        issue_win = Toplevel()
        self.issue_win = issue_win

        self.screen_width = int((self.issue_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.issue_win.winfo_screenheight()) / 6)

        self.issue_win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.issue_win.title("Issue Book")
        self.issue_win.resizable(FALSE, FALSE)
        self.issue_win.configure(bg="#E0FFFF")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/christlabel.png"))
        self.top_label = Label(self.issue_win, image=self.photo0, bg="white")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.draw()

        self.treeview()
        self.showdetails()

        self.trrv.bind("<ButtonRelease-1>", self.selected)

        self.issue_win.protocol("WM_DELETE_WINDOW", self.on_closing_issue_win)

        self.issue_win.mainloop()

    def on_closing_issue_win(self):
        self.issue_win.destroy()
        self.main_win_loop.deiconify()

    def draw(self):
        self.lblEmail = Label(
            self.issue_win,
            text="EMAIL-ID ",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#E0FFFF",
        )
        self.lblEmail.place(x=30, y=100)
        self.lblBookId = Label(
            self.issue_win,
            text="BOOK ISBN",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#E0FFFF",
        )
        self.lblBookId.place(x=300, y=100)
        self.lblIssueDate = Label(
            self.issue_win,
            text="ISSUE-DATE",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#E0FFFF",
        )
        self.lblIssueDate.place(x=30, y=140)
        self.lblDueDate = Label(
            self.issue_win,
            text="DUE-DATE",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#E0FFFF",
        )
        self.lblDueDate.place(x=300, y=140)

        self.emailEntry = Entry(
            self.issue_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.emailEntry.place(x=140, y=100)
        self.bookidEntry = Entry(
            self.issue_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.bookidEntry.place(x=410, y=100)
        self.issueEntry = DateEntry(
            self.issue_win,
            font=("times new roman", 15),
            date_pattern="yyyy-mm-dd",
            width=18,
            state="readonly",
            fg="#F5F5F5",
            relief=GROOVE,
        )
        self.issueEntry.place(x=140, y=140, width=145)
        self.returnEntry = DateEntry(
            self.issue_win,
            font=("times new roman", 15),
            date_pattern="yyyy-mm-dd",
            width=18,
            state="readonly",
            fg="#F5F5F5",
            relief=GROOVE,
        )
        self.returnEntry.place(x=410, y=140, width=145)

        self.searchbutton = Button(
            self.issue_win,
            text="Search Book",
            font=("Nirmala UI", 10, "bold"),
            bg="gold",
            command=self.search_book,
        )
        self.searchbutton.place(x=510, y=200)

        self.issuebutton = Button(
            self.issue_win,
            text="Issue Book",
            font=("Nirmala UI", 10, "bold"),
            bg="gold",
            command=self.issue_book,
        )
        self.issuebutton.place(x=510, y=240, width=87)

    def issue_book(self):

        if self.bookidEntry.get() != "" and self.emailEntry.get() != "":
            self.search_book()

            connection = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )
            cursor = connection.cursor()

            cursor.execute(f"select id from readers where id='{self.emailEntry.get()}'")
            self.row = cursor.fetchone()
            if self.row == None:
                messagebox.showerror(
                    "Library Management System", "Invalid Email Address."
                )
                connection.close()
            else:
                cur1 = connection.cursor()
                cur1.execute(
                    f"select isbn from issuebook where rid='{self.emailEntry.get()}' and isbn='{self.bookidEntry.get()}'"
                )
                r = cur1.fetchone()
                if r == None:
                    connection.close()
                    ######
                    conn = psycopg2.connect(
                        user="kevin",
                        password="2048",
                        host="localhost",
                        port="5432",
                        database="libdb",
                    )

                    cur = conn.cursor()
                    cur.execute(
                        f"select number from books where isbn='{self.bookidEntry.get()}'"
                    )
                    row1 = cur.fetchone()
                    if int(row1[0]) > 0:
                        SQL1 = "update books set number=%s where isbn=%s"
                        data1 = (int(row1[0]) - 1, self.bookidEntry.get())
                        cur.execute(SQL1, data1)
                        conn.commit()
                        conn.close()
                        ##########
                        conn1 = psycopg2.connect(
                            user="kevin",
                            password="2048",
                            host="localhost",
                            port="5432",
                            database="libdb",
                        )
                        cur1 = conn1.cursor()
                        SQL = "insert into issuebook (rid, isbn, doi, dor, fine) values(%s, %s, %s, %s, %s)"
                        data = (
                            self.emailEntry.get(),
                            self.bookidEntry.get(),
                            self.issueEntry.get(),
                            self.returnEntry.get(),
                            0,
                        )
                        cur1.execute(SQL, data)
                        conn1.commit()
                        conn1.close()
                        self.showdetails()

                        messagebox.showinfo(
                            "Library Management System", "Book issued successfully."
                        )
                    else:
                        messagebox.showinfo(
                            "Library Management System", "The quantity of book is zero."
                        )
                        conn.commit()
                        conn.close()
                else:
                    messagebox.showerror(
                        "Library Management System",
                        "The book is already issued to this user.",
                    )

        else:
            messagebox.showerror("Library Management System", "Enter details.")

    def search_book(self):
        isFound = False
        query = self.bookidEntry.get()
        if query != "":
            for child in self.trrv.get_children():
                if query in str(self.trrv.item(child)["values"][0]):
                    self.trrv.selection_set(child)
                    self.bookidEntry.delete(0, END)
                    self.bookidEntry.insert(0, self.trrv.item(child)["values"][0])
                    isFound = True
                    break
            if isFound == False:
                self.bookidEntry.delete(0, END)
                messagebox.showerror("Library Management System", "No result found.")

        else:
            messagebox.showerror("Library Management System", "Enter Book Isbn Number.")

    def treeview(self):

        self.frame = Frame(self.issue_win, bg="#CCCCFF", relief="flat")
        self.frame.place(x=5, y=200, width=500, height=190)

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
        self.trrv.place(x=0, y=0, width=483, height=170)

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

    def selected(self, ev):
        self.curr_row = self.trrv.focus()
        self.contents = self.trrv.item(self.curr_row)
        self.info = self.contents["values"]

        self.bookidEntry.delete(0, END)
        self.bookidEntry.insert(0, self.info[0])
