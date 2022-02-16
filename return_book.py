from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
import psycopg2
import datetime as dt


class ReturnBook:
    def return_book_window(self, mainloop):
        # width and height of the window
        self.width = 600
        self.height = 400
        self.main_win_loop = mainloop
        return_win = Toplevel()
        self.return_win = return_win

        self.screen_width = int((self.return_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.return_win.winfo_screenheight()) / 6)

        self.return_win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.return_win.title("Return Book")
        self.return_win.resizable(FALSE, FALSE)
        self.return_win.configure(bg="#cdffcd")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/christlabel.png"))
        self.top_label = Label(self.return_win, image=self.photo0, bg="white")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.draw()
        self.update_fine()
        self.treeview()
        self.showdetails()

        self.trrv.bind("<ButtonRelease-1>", self.selected)
        self.return_win.protocol("WM_DELETE_WINDOW", self.on_closing_return_win)
        self.return_win.mainloop()

    def on_closing_return_win(self):
        self.return_win.destroy()
        self.main_win_loop.deiconify()

    def draw(self):
        self.lblEmail = Label(
            self.return_win,
            text="EMAIL-ID ",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#cdffcd",
        )
        self.lblEmail.place(x=30, y=80)
        self.lblBookId = Label(
            self.return_win,
            text="BOOK ISBN",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#cdffcd",
        )
        self.lblBookId.place(x=300, y=80)
        self.lblIssueDate = Label(
            self.return_win,
            text="ISSUE-DATE",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#cdffcd",
        )
        self.lblIssueDate.place(x=30, y=120)
        self.lblDueDate = Label(
            self.return_win,
            text="DUE-DATE",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#cdffcd",
        )
        self.lblDueDate.place(x=300, y=120)
        self.lblfine = Label(
            self.return_win,
            text="FINE",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            bg="#cdffcd",
        )
        self.lblfine.place(x=30, y=160)

        self.emailEntry = Entry(
            self.return_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.emailEntry.place(x=140, y=80)
        self.bookidEntry = Entry(
            self.return_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.bookidEntry.place(x=410, y=80)
        self.issueEntry = Entry(
            self.return_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.issueEntry.place(x=140, y=120, width=145)
        self.returnEntry = Entry(
            self.return_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.returnEntry.place(x=410, y=120, width=145)

        self.fineEntry = Entry(
            self.return_win, font=("Nirmala UI", 10, "bold"), fg="black", bg="white"
        )
        self.fineEntry.place(x=140, y=160, width=145)

        self.issueEntry.config(state="disabled")
        self.returnEntry.config(state="disabled")
        self.fineEntry.config(state="disabled")

        self.searchbutton = Button(
            self.return_win,
            text="Search Book",
            font=("Nirmala UI", 10, "bold"),
            bg="gold",
            command=self.search_book,
        )
        self.searchbutton.place(x=510, y=200)

        self.returnbutton = Button(
            self.return_win,
            text="Return Book",
            font=("Nirmala UI", 10, "bold"),
            bg="gold",
            command=self.returns_book,
        )
        self.returnbutton.place(x=510, y=240, width=87)

    def returns_book(self):

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

            cursor.execute(
                f"select rid from issuebook where rid='{self.emailEntry.get()}' and isbn='{self.bookidEntry.get()}'"
            )
            self.row = cursor.fetchone()
            if self.row != None:
                cursor.execute(
                    f"delete from issuebook where rid='{self.emailEntry.get()}' and isbn='{self.bookidEntry.get()}'"
                )
                connection.commit()
                connection.close()
                self.showdetails()

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

                SQL1 = "update books set number=%s where isbn=%s"
                data1 = (int(row1[0]) + 1, self.bookidEntry.get())
                cur.execute(SQL1, data1)
                conn.commit()
                conn.close()
                self.update_fine()
                messagebox.showinfo(
                    "Library Management System", "Book returned successfully."
                )
                self.clear()

        else:
            messagebox.showerror("Library Management System", "Enter details.")

    def search_book(self):
        isFound = False
        query2 = self.bookidEntry.get()
        query1 = self.emailEntry.get()
        if query1 != "" or query2 != "":

            if query1 != "" and query2 == "":
                for child in self.trrv.get_children():
                    if query1 in str(self.trrv.item(child)["values"][0]):
                        self.trrv.selection_set(child)
                        self.issueEntry.config(state="normal")
                        self.returnEntry.config(state="normal")
                        self.fineEntry.config(state="normal")

                        self.bookidEntry.delete(0, END)
                        self.emailEntry.delete(0, END)
                        self.returnEntry.delete(0, END)
                        self.issueEntry.delete(0, END)
                        self.fineEntry.delete(0, END)

                        self.emailEntry.insert(0, self.trrv.item(child)["values"][0])
                        self.bookidEntry.insert(0, self.trrv.item(child)["values"][1])
                        self.issueEntry.insert(0, self.trrv.item(child)["values"][2])
                        self.returnEntry.insert(0, self.trrv.item(child)["values"][3])
                        self.fineEntry.insert(0, self.trrv.item(child)["values"][4])

                        self.issueEntry.config(state="disabled")
                        self.returnEntry.config(state="disabled")
                        self.fineEntry.config(state="disabled")

                        isFound = True
                        break
            elif query1 == "" and query2 != "":
                for child in self.trrv.get_children():
                    if query2 in str(self.trrv.item(child)["values"][1]):
                        self.trrv.selection_set(child)
                        self.issueEntry.config(state="normal")
                        self.returnEntry.config(state="normal")
                        self.fineEntry.config(state="normal")

                        self.bookidEntry.delete(0, END)
                        self.emailEntry.delete(0, END)
                        self.returnEntry.delete(0, END)
                        self.issueEntry.delete(0, END)
                        self.fineEntry.delete(0, END)

                        self.emailEntry.insert(0, self.trrv.item(child)["values"][0])
                        self.bookidEntry.insert(0, self.trrv.item(child)["values"][1])
                        self.issueEntry.insert(0, self.trrv.item(child)["values"][2])
                        self.returnEntry.insert(0, self.trrv.item(child)["values"][3])
                        self.fineEntry.insert(0, self.trrv.item(child)["values"][4])

                        self.issueEntry.config(state="disabled")
                        self.returnEntry.config(state="disabled")
                        self.fineEntry.config(state="disabled")

                        isFound = True
                        break
            elif query1 != "" and query2 != "":
                for child in self.trrv.get_children():
                    if query1 == str(
                        self.trrv.item(child)["values"][0]
                    ) and query2 == str(self.trrv.item(child)["values"][1]):
                        self.trrv.selection_set(child)
                        self.issueEntry.config(state="normal")
                        self.returnEntry.config(state="normal")
                        self.fineEntry.config(state="normal")

                        self.bookidEntry.delete(0, END)
                        self.emailEntry.delete(0, END)
                        self.returnEntry.delete(0, END)
                        self.issueEntry.delete(0, END)
                        self.fineEntry.delete(0, END)

                        self.emailEntry.insert(0, self.trrv.item(child)["values"][0])
                        self.bookidEntry.insert(0, self.trrv.item(child)["values"][1])
                        self.issueEntry.insert(0, self.trrv.item(child)["values"][2])
                        self.returnEntry.insert(0, self.trrv.item(child)["values"][3])
                        self.fineEntry.insert(0, self.trrv.item(child)["values"][4])

                        self.issueEntry.config(state="disabled")
                        self.returnEntry.config(state="disabled")
                        self.fineEntry.config(state="disabled")

                        isFound = True
                        break

            if isFound == False:
                self.clear()
                messagebox.showerror("Library Management System", "No result found.")

        else:
            messagebox.showerror(
                "Library Management System", "Enter Book Isbn Number or User Email Id."
            )

    def treeview(self):

        self.frame = Frame(self.return_win, bg="#CCCCFF", relief="flat")
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
        self.trrv["columns"] = (1, 2, 3, 4, 5)
        self.trrv.column(1, width=110, anchor="c")
        self.trrv.column(2, width=90, anchor="c")
        self.trrv.column(3, width=90, anchor="c")
        self.trrv.column(4, width=90, anchor="c")
        self.trrv.column(5, width=90, anchor="c")

        # Defining headings
        self.trrv["show"] = "headings"
        self.trrv.heading(1, text="Email Id")
        self.trrv.heading(2, text="Book Isbn")
        self.trrv.heading(3, text="Issued Date")
        self.trrv.heading(4, text="Return Date")
        self.trrv.heading(5, text="Fine")

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

        cursor.execute("select * from issuebook")
        self.row = cursor.fetchall()
        self.trrv.delete(*self.trrv.get_children())
        if len(self.row) != 0:
            for i in self.row:
                self.trrv.insert("", "end", values=i)

        connection.close()

    def get_selection(self):
        self.curr_row = self.trrv.focus()
        self.contents = self.trrv.item(self.curr_row)
        self.info = self.contents["values"]
        if self.info != "":
            self.issueEntry.config(state="normal")
            self.returnEntry.config(state="normal")
            self.fineEntry.config(state="normal")

            self.bookidEntry.delete(0, END)
            self.emailEntry.delete(0, END)
            self.returnEntry.delete(0, END)
            self.issueEntry.delete(0, END)
            self.fineEntry.delete(0, END)

            self.emailEntry.insert(0, self.info[0])
            self.bookidEntry.insert(0, self.info[1])
            self.issueEntry.insert(0, self.info[2])
            self.returnEntry.insert(0, self.info[3])
            self.fineEntry.insert(0, self.info[4])

            self.issueEntry.config(state="disabled")
            self.returnEntry.config(state="disabled")
            self.fineEntry.config(state="disabled")

    def selected(self, ev):
        self.get_selection()

    def clear(self):
        self.issueEntry.config(state="normal")
        self.returnEntry.config(state="normal")
        self.fineEntry.config(state="normal")

        self.bookidEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.returnEntry.delete(0, END)
        self.issueEntry.delete(0, END)
        self.fineEntry.delete(0, END)

        self.issueEntry.config(state="disabled")
        self.returnEntry.config(state="disabled")
        self.fineEntry.config(state="disabled")

    def update_fine(self):
        curdate = dt.date.today()
        # curdate = today.strftime("%Y-%m-%d")

        connection = psycopg2.connect(
            user="kevin",
            password="2048",
            host="localhost",
            port="5432",
            database="libdb",
        )
        cursor = connection.cursor()

        cursor.execute("select * from issuebook ")

        result = cursor.fetchall()
        for row in result:

            date_obj = row[3]
            delta = curdate - date_obj

            if delta.days > 0:
                if delta.days <= 10:

                    SQL1 = "update issuebook set fine=%s where rid=%s and isbn=%s"
                    data1 = (10, row[0], row[1])
                    cursor.execute(SQL1, data1)

                elif 10 < delta.days <= 20:
                    SQL2 = "update issuebook set fine=%s where rid=%s and isbn=%s"
                    data2 = (25, row[0], row[1])
                    cursor.execute(SQL2, data2)

                else:
                    SQL3 = "update issuebook set fine=%s where rid=%s and isbn=%s"
                    data3 = (50, row[0], row[1])
                    cursor.execute(SQL3, data3)

        connection.commit()
        connection.close()
