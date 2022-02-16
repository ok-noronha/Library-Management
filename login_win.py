import psycopg2
import smtplib
import re

import main_win as mw

from tkinter import *
from PIL import Image, ImageTk
# from tkinter import messagebox
from datetime import date
from email.message import EmailMessage
from configparser import ConfigParser

import global_data


class LoginWindow:
    show_the_password = False

    def __init__(self):

        gdt = global_data.GDT()

        self.width = gdt.width
        self.height = gdt.height

        login_win = Tk()
        self.login_win = login_win

        self.screen_width = int((self.login_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.login_win.winfo_screenheight()) / 4)

        self.login_win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.login_win.title("Staff Login")
        self.login_win.iconbitmap(gdt.icon)
        self.login_win.resizable(FALSE, FALSE)
        self.login_win.configure(bg="#E2B188")

        self.img = gdt.login_bg
        self.resized_image = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resized_image)

        self.canvas = Canvas(self.login_win)
        self.canvas.pack(fill=BOTH, expand=1)

        self.canvas.create_image(300, 200, image=self.new_image)

        self.photo0 = ImageTk.PhotoImage(gdt.label)
        self.img_label = Label(self.canvas, image=self.photo0, bg="#FFFFFF")
        self.img_label.place(x=0, y=0, width=600, height=65)

        self.frame = Frame(self.login_win, height=200, bg="#008ae6")
        self.frame.place(x=120, y=100, width=320, height=270)

        self.imglock = ImageTk.PhotoImage(gdt.lockicon)
        self.imgforget = ImageTk.PhotoImage(gdt.frgicon)
        self.imgprofile = ImageTk.PhotoImage(gdt.proficon)
        self.imglogin = ImageTk.PhotoImage(gdt.login_bg)
        self.imgpwdhide = ImageTk.PhotoImage(gdt.hid)
        self.imgpwdshow = ImageTk.PhotoImage(Image.open("images/pwd_show.png"))

        self.labeluser = Label(
            self.frame,
            text="Email ID",
            font=("Nirmala UI", 15, "bold"),
            fg="#333333",
            bg="#008ae6",
        )
        self.labeluser.place(x=30, y=12)
        self.labeluser.config(image=self.imgprofile, compound=LEFT)

        self.user_entry = Entry(
            self.frame, font=("times new roman", 15), bg="#a6a6a6", fg="grey"
        )
        self.user_entry.place(x=30, y=50, width=250)
        self.user_entry.insert(0, "ab.cd@christuniversity.in")

        self.labelpwd = Label(
            self.frame,
            text="Password",
            font=("Nirmala UI", 15, "bold"),
            fg="#333333",
            bg="#008ae6",
        )
        self.labelpwd.place(x=30, y=80)
        self.labelpwd.config(image=self.imglock, compound=LEFT)

        self.password_entry = Entry(
            self.frame, font=("times new roman", 15), bg="#a6a6a6", show="*"
        )
        self.password_entry.place(x=30, y=120, width=250)

        self.log_button = Button(
            self.frame,
            text="Login",
            bg="green",
            activeforeground="green",
            fg="white",
            activebackground="light green",
            command=lambda: self.admin_login(),
            padx=30,
            pady=10,
            cursor="hand2",
            bd=0,
        )

        self.log_button.place(x=95, y=170)

        self.forget_button = Button(
            self.frame,
            bg="#008ae6",
            text="Forget Password?",
            command=lambda: self.forget_password(),
            font=("times new roman", 13, "bold"),
            fg="#333333",
            cursor="hand2",
            bd=0,
            activeforeground="white",
            activebackground="#008ae6",
        )
        self.forget_button.place(x=30, y=230)
        self.forget_button.configure(image=self.imgforget, compound=LEFT)

        self.pwd_show = Button(
            self.frame,
            bg="#008ae6",
            command=lambda: self.show_hide_password(),
            cursor="hand2",
            bd=0,
            activebackground="white",
        )
        self.pwd_show.place(x=285, y=120)
        self.pwd_show.config(image=self.imgpwdhide)

        self.add_librarian_btn = Button(
            self.canvas,
            text="+ Staff",
            bg="gold",
            font=("Nirmala UI", 12, "bold"),
            fg="black",
            command=lambda: self.add_librarian(),
            cursor="hand2",
            bd=2,
            activebackground="yellow",
        )
        self.add_librarian_btn.place(x=480, y=120)

        self.login_win.mainloop()

    def admin_login(self):
        if self.user_entry.get() == "" or self.password_entry.get() == "":
            messagebox.showwarning(
                "Library Management System ",
                "Please, enter both Email ID and Password. ",
            )
        elif self.check_email(self.user_entry.get()) == 0:
            messagebox.showwarning(
                "Library Management System ", "Please, enter valid Email Address."
            )
            self.user_entry.delete(0, END)
        else:
            connection = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )
            cursor = connection.cursor()
            cursor.execute(
                "select * from authentication where password = %s and id in (select id from staff where id = %s)",
                (self.password_entry.get(), self.user_entry.get()),
            )
            self.row = cursor.fetchone()
            if self.row == None:
                ans = messagebox.askquestion("User Not Found", "Do you want to retry?")
                if ans == "yes":
                    self.user_entry.delete(0, END)
                    self.password_entry.delete(0, END)
                elif ans == "no":
                    self.login_win.destroy()
            else:
                cursor.execute(
                    f"select name from staff where id = '{self.user_entry.get()}'"
                )
                self.row1 = cursor.fetchone()

                connection.commit()
                connection.close()
                self.login_win.destroy()

                main_obj = mw.MainWindow()
                main_obj.create_main_window(self.row1)

                self.login_win.mainloop()

    def forget_password(self):
        if self.user_entry.get() == "":
            messagebox.showwarning(
                "Library Management System ", "Please, enter the Email ID."
            )
        elif self.check_email(self.user_entry.get()) == 0:
            messagebox.showwarning(
                "Email Not Valid", "Please enter valid email address."
            )
            self.user_entry.delete(0, END)
        else:
            connection = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )
            cursor = connection.cursor()
            cursor.execute(
                "select password from authentication where id = '%s'"
                % (self.user_entry.get())
            )
            self.row = cursor.fetchone()
            if self.row == None:
                messagebox.showerror(
                    "Error", "No staff with this Email ID is registered"
                )
            else:
                self.send_email(self.user_entry.get(), self.row)
            connection.commit()
            connection.close()

    def add_librarian(self):

        self.login_win.withdraw()

        self.width = 600
        self.height = 400

        librarian_win = Toplevel()
        self.librarian_win = librarian_win

        self.screen_width = int((self.librarian_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.librarian_win.winfo_screenheight()) / 6)

        self.librarian_win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.librarian_win.title("Add Librarian")
        self.librarian_win.resizable(FALSE, FALSE)
        self.librarian_win.configure(bg="#ff9900")

        self.photo0 = ImageTk.PhotoImage(Image.open("images/christlabel.png"))
        self.top_label = Label(self.librarian_win, image=self.photo0, bg="white")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.input_details = [
            "Name",
            "Email Id",
            "Password",
            "Contact No.",
            "Age",
            "Dept.",
            "Date",
        ]

        inc = -40
        inc_x = 70
        for i in range(7):
            inc += 40

            self.lblLibrarian = Label(
                self.librarian_win,
                text=self.input_details[i],
                font=("Nirmala UI", 10, "bold"),
                fg="black",
                bg="#ff9900",
            )
            self.lblLibrarian.place(x=30 + inc_x, y=80 + inc)

            self.lbl = Label(
                self.librarian_win,
                text="*",
                font=("Nirmala UI", 10, "bold"),
                fg="red",
                bg="#ff9900",
            )
            self.lbl.place(x=22 + inc_x, y=80 + inc)
        inc = 0

        self.enteryLibrarian1 = Entry(
            self.librarian_win, font=("times new roman", 15), bg="#F0FFFF"
        )
        self.enteryLibrarian1.place(x=170 + inc_x, y=80 + inc)
        inc += 40
        self.enteryLibrarian2 = Entry(
            self.librarian_win, font=("times new roman", 15), bg="#F0FFFF"
        )
        self.enteryLibrarian2.place(x=170 + inc_x, y=80 + inc)
        inc += 40
        self.enteryLibrarian3 = Entry(
            self.librarian_win, font=("times new roman", 15), bg="#F0FFFF"
        )
        self.enteryLibrarian3.place(x=170 + inc_x, y=80 + inc)
        inc += 40
        self.enteryLibrarian4 = Entry(
            self.librarian_win, font=("times new roman", 15), bg="#F0FFFF"
        )
        self.enteryLibrarian4.place(x=170 + inc_x, y=80 + inc)
        inc += 40

        self.enteryLibrarian5 = Entry(
            self.librarian_win, font=("times new roman", 15), bg="#F0FFFF"
        )
        self.enteryLibrarian5.place(x=170 + inc_x, y=80 + inc)
        inc += 40

        self.enteryLibrarian6 = Entry(
            self.librarian_win, font=("times new roman", 15), bg="#F0FFFF"
        )
        self.enteryLibrarian6.place(x=170 + inc_x, y=80 + inc)
        inc += 40

        self.tLibrarian = Text(
            self.librarian_win,
            width=20,
            height=1,
            font=("times new roman", 15),
            bg="cyan",
        )
        self.tLibrarian.place(x=170 + inc_x, y=80 + inc)
        self.tLibrarian.insert(INSERT, date.today().strftime("%Y-%m-%d"))
        self.tLibrarian.configure(state=DISABLED)

        self.submit_btn = Button(
            self.librarian_win,
            text="SUBMIT",
            bg="green",
            font=("Nirmala UI", 12, "bold"),
            fg="black",
            command=lambda: self.add_librarian_query(),
            cursor="hand2",
            bd=2,
            activebackground="white",
        )
        self.submit_btn.place(x=230, y=350)

        self.librarian_win.protocol("WM_DELETE_WINDOW", self.on_closing_lib_win)

    # on closing librarian window
    def on_closing_lib_win(self):
        self.librarian_win.destroy()
        self.login_win.deiconify()

    # add librarian query
    def add_librarian_query(self):

        if (
            self.enteryLibrarian1.get() == ""
            or self.enteryLibrarian2.get() == ""
            or self.enteryLibrarian3.get() == ""
            or self.enteryLibrarian4.get() == ""
            or self.enteryLibrarian4.get() == ""
            or self.tLibrarian.get("1.0", END) == ""
        ):
            messagebox.showwarning(
                "Library Management System ", "Enter the required feilds marked with *"
            )
        elif self.check_email(self.enteryLibrarian2.get()) == 0:
            messagebox.showwarning("Email Not Valid", "Please Enter valid email id.")
        elif (
            self.send_email(self.enteryLibrarian2.get(), self.enteryLibrarian3.get())
            == 0
        ):
            self.enteryLibrarian2.delete(0, END)
        else:
            connection = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )
            cursor = connection.cursor()

            cursor.execute(
                f"select id from staff where id='{self.enteryLibrarian2.get()}'"
            )
            self.email_s = cursor.fetchone()

            if self.email_s == None:
                cursor.execute(
                    "insert into staff values ('%s','%s','%s','%s','%s','%s')"
                    % (
                        self.enteryLibrarian2.get(),
                        self.enteryLibrarian1.get(),
                        self.enteryLibrarian4.get(),
                        self.enteryLibrarian5.get(),
                        self.tLibrarian.get("1.0", END),
                        self.enteryLibrarian6.get(),
                    )
                )
                cursor.execute(
                    "update authentication set password = '%s' where id = '%s'"
                    % (self.enteryLibrarian3.get(), self.enteryLibrarian2.get())
                )

                connection.commit()
                connection.close()

                messagebox.showinfo(
                    "Library Management System", "Librarian Added Successfully"
                )

                self.enteryLibrarian1.delete(0, END)
                self.enteryLibrarian2.delete(0, END)
                self.enteryLibrarian3.delete(0, END)
                self.enteryLibrarian4.delete(0, END)
                self.enteryLibrarian5.delete(0, END)
                self.enteryLibrarian6.delete(0, END)

            else:
                messagebox.showerror("Error", "Email id already exists.")

    def show_hide_password(self):

        if self.show_the_password == False:
            self.show_the_password = True
        else:
            self.show_the_password = False

        if self.show_the_password == False:
            self.pwd_show.config(image=self.imgpwdhide)
            self.password_entry.config(show=".")
        else:
            self.pwd_show.config(image=self.imgpwdshow)
            self.password_entry.config(show="")

    def check_email(self, email_id):

        """is_valid = validate_email(email_id)

        if is_valid == True:

            return 1
        else:

            return 0"""
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.match(regex, email_id):
            return 1
        else:
            return 0

    def send_email(self, email_add, email_pwd):

        gdata = gdt.HostEmailDetails()
        email_address = gdata.host_email_id()
        email_password = gdata.host_email_password()
        send_to_address = email_add

        msg = EmailMessage()
        msg["Subject"] = "Do not reply"
        msg["From"] = email_address
        msg["To"] = send_to_address
        msg.set_content(
            "Dear user your password for library management software is %s" % email_pwd
        )
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
                messagebox.showinfo(
                    "Library Management System",
                    "Your password has been sent to your email id.",
                )
            return 1
        except Exception as e:
            messagebox.showerror(
                "Library Management System",
                """Either your email id is invalid or you are not connected to the internet.""",
            )
            return 0
