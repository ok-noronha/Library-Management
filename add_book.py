from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import *
from tkinter import filedialog
import os
from tkinter import messagebox
import psycopg2
import cv2
from pyzbar.pyzbar import decode
from isbntools.app import *
from datetime import datetime
import urllib.request
import random


class AddBook:

    image_uploaded1 = False

    def add_book_window(self, mainloop):

        self.width = 600
        self.height = 400
        self.main_win_loop = mainloop

        book_win = Toplevel()
        self.book_win = book_win

        self.screen_width = int((self.book_win.winfo_screenwidth()) / 4)
        self.screen_height = int((self.book_win.winfo_screenheight()) / 6)

        self.book_win.geometry(
            f"{self.width}x{self.height}+{self.screen_width}+{self.screen_height}"
        )
        self.book_win.title("Add Book")
        self.book_win.iconbitmap(r'images/LibIcon.ico')
        self.book_win.resizable(FALSE, FALSE)
        self.book_win.configure(bg="#737373")

        # Top Image
        self.photo0 = ImageTk.PhotoImage(Image.open("images/christlabel.png"))
        self.top_label = Label(self.book_win, image=self.photo0, bg="white")
        self.top_label.place(x=0, y=0, width=600, height=65)

        self.input_details = [
            "ISBN Number",
            "Book Title",
            "Category",
            "Author",
            "Publisher",
            "Date of Publiction",
            "Quantity",
        ]

        inc = -40
        inc_x = 10
        for i in range(7):
            inc += 40
            self.lbldetails = Label(
                self.book_win,
                text=self.input_details[i],
                font=("Nirmala UI", 10, "bold"),
                fg="black",
                bg="#737373",
            )
            self.lbldetails.place(x=30 + inc_x, y=80 + inc)
            self.lbl = Label(
                self.book_win,
                text="*",
                font=("Nirmala UI", 10, "bold"),
                fg="red",
                bg="#737373",
            )
            self.lbl.place(x=20 + inc_x, y=80 + inc)

        inc = 0

        self.isbn_entr = Entry(self.book_win, font=("times new roman", 15))
        self.isbn_entr.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.title_entr = Entry(self.book_win, font=("times new roman", 15))
        self.title_entr.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.cvalues = (
            "Arts & Music",
            "Biography",
            "Business",
            "Comic",
            "Computer & Tech",
            "History",
            "Medical",
            "Engeneering",
            "Others",
        )
        self.category_entr = ttk.Combobox(
            self.book_win, values=self.cvalues, font=("times new roman", 15)
        )
        self.category_entr.set("Select Category")
        self.category_entr.config(state="readonly")
        self.category_entr.place(x=150 + inc_x, y=80 + inc, width=205)
        inc += 40
        self.author_entr = Entry(self.book_win, font=("times new roman", 15))
        self.author_entr.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.publisher_entr = Entry(self.book_win, font=("times new roman", 15))
        self.publisher_entr.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.dop_entr = DateEntry(
            self.book_win,
            font=("times new roman", 15),
            date_pattern="yyyy-mm-dd",
            width=18,
            state="readonly",
            fg="#F5F5F5",
            relief=GROOVE,
        )
        self.dop_entr.place(x=150 + inc_x, y=80 + inc)
        inc += 40
        self.quantity_entr = Entry(self.book_win, font=("times new roman", 15))
        self.quantity_entr.place(x=150 + inc_x, y=80 + inc)

        self.submit_btn = Button(
            self.book_win,
            text="SAVE",
            bg="#4da6ff",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            command=lambda: self.add_book_query(),
            cursor="hand2",
            bd=2,
            activebackground="white",
        )
        self.submit_btn.place(x=100, y=355, width=70)

        self.update_btn = Button(
            self.book_win,
            text="UPDATE",
            bg="#4da6ff",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            command=lambda: self.update_book_query(),
            cursor="hand2",
            bd=2,
            activebackground="white",
        )
        self.update_btn.place(x=10, y=355, width=70)  #

        self.search_btn = Button(
            self.book_win,
            text="SEARCH",
            bg="#4da6ff",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            command=lambda: self.search_book_query(),
            cursor="hand2",
            bd=2,
            activebackground="white",
        )
        self.search_btn.place(x=200, y=355, width=70)

        self.delete_btn = Button(
            self.book_win,
            text="DELETE",
            bg="#4da6ff",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            command=lambda: self.delete_book_query(),
            cursor="hand2",
            bd=2,
            activebackground="white",
        )
        self.delete_btn.place(x=290, y=355, width=70)

        self.clear_btn = Button(
            self.book_win,
            text="CLEAR",
            bg="#4da6ff",
            font=("Nirmala UI", 10, "bold"),
            fg="black",
            command=lambda: self.clear(),
            cursor="hand2",
            bd=2,
            activebackground="white",
        )
        self.clear_btn.place(x=380, y=355, width=70)

        self.scan_button = Button(
            self.book_win,
            text="Scan QR Code",
            cursor="hand2",
            command=lambda: self.scan_QR_Code(),
            bg="#bfbfbf",
            fg="black",
            font=("Nirmala UI", 9, "bold"),
            bd=2,
            relief=RIDGE,
        )
        self.scan_button.place(x=420, y=80, width=120)

        self.radio_var = IntVar()

        self.image_radio = Radiobutton(
            self.book_win,
            text="Image",
            variable=self.radio_var,
            value=1,
            font=("Nirmala UI", 9, "bold"),
            bg="#bfbfbf",
            fg="black",
        )
        self.image_radio.place(x=380, y=110)
        self.image_radio.select()

        self.image_label = Label(self.book_win, relief=GROOVE, bg="lightblue", bd=2)
        self.image_label.place(x=470, y=270, width=120, height=120)

        self.scan_label = Label(self.book_win, relief=GROOVE, bg="lightgreen", bd=2)
        self.scan_label.place(x=380, y=135, width=215, height=130)

        self.camera_radio = Radiobutton(
            self.book_win,
            text="Camera",
            variable=self.radio_var,
            value=2,
            font=("Nirmala UI", 9, "bold"),
            bg="#bfbfbf",
            fg="black",
        )
        self.camera_radio.place(x=480, y=110)

        self.upimag_button = Button(
            self.book_win,
            text="Upload Image",
            cursor="hand2",
            command=lambda: self.upload_image(),
            bg="#bfbfbf",
            fg="black",
            font=("Nirmala UI", 9, "bold"),
            bd=2,
            relief=RIDGE,
        )
        self.upimag_button.place(x=380, y=320, width=85)

        self.delete_btn.configure(state="disabled")
        self.update_btn.configure(state="disabled")

        self.book_win.protocol("WM_DELETE_WINDOW", self.on_closing_book_win)

        self.book_win.mainloop()

    def on_closing_book_win(self):
        self.book_win.destroy()
        self.main_win_loop.deiconify()

    def update_book_query(self):
        if (
            self.isbn_entr.get() == ""
            or self.title_entr.get() == ""
            or self.dop_entr.get() == ""
            or self.category_entr.get() == ""
            or self.category_entr.get() == "Select Category"
            or self.author_entr.get() == ""
            or self.quantity_entr.get() == ""
            or self.publisher_entr.get() == ""
        ):
            messagebox.showwarning(
                "Library Management System", "Enter Necessary Feilds"
            )
        elif self.image_uploaded1 == False:
            messagebox.showwarning("Library Management System", "Please upload image.")
        else:

            conn = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )

            cur = conn.cursor()
            cur.execute(f"select isbn from books where isbn='{self.isbn_entr.get()}'")
            self.row1 = cur.fetchone()
            if self.row1 == None:
                messagebox.showerror(
                    "Library Management System", "No such book in the library"
                )
                self.clear()
                conn.close()
            else:
                self.resize_imgbar1.save("Temp2.png")
                self.drawings1 = open("Temp2.png", "rb").read()
                os.remove("Temp2.png")
                SQL = "update books set title=%s, category=%s, author=%s, publisher=%s, dop=%s, number=%s, image=%s where isbn=%s"
                data = (
                    self.title_entr.get(),
                    self.category_entr.get(),
                    self.author_entr.get(),
                    self.publisher_entr.get(),
                    self.dop_entr.get(),
                    self.quantity_entr.get(),
                    psycopg2.Binary(self.drawings1),
                    self.isbn_entr.get(),
                )
                cur.execute(SQL, data)
                conn.commit()
                conn.close()

                messagebox.showinfo(
                    "Library Management System", "Book updated successfully."
                )

                self.clear()

    def delete_book_query(self):
        if self.isbn_entr.get() != "":
            # connecting to postgres database
            connection = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )
            cursor = connection.cursor()

            cursor.execute(f"delete from books where isbn = '{self.isbn_entr.get()}'")
            connection.commit()
            connection.close()
            messagebox.showinfo(
                "Library Management System", "Book removed successfully."
            )
            self.clear()
        else:
            messagebox.showerror("Book not Found", "Please enter isbn number.")

    def search_book_query(self):

        if self.isbn_entr.get() == "":
            messagebox.showerror("Error", "Please input isbn number.")

        else:

            conn = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )

            cur = conn.cursor()
            cur.execute(f"select * from books where isbn='{self.isbn_entr.get()}'")
            self.row1 = cur.fetchone()

            if self.row1:
                self.clear()
                self.isbn_entr.insert(0, self.row1[0])
                self.title_entr.insert(0, self.row1[1])
                self.category_entr.set(self.row1[4])
                self.author_entr.insert(0, self.row1[2])
                self.publisher_entr.insert(0, self.row1[3])
                self.dop_entr.set_date(self.row1[6])
                self.quantity_entr.insert(0, self.row1[5])
                self.delete_btn.configure(state="normal")
                self.update_btn.configure(state="normal")
                # writing binary data to file

                self.picimg = open("Test.png", "wb")
                self.picimg.write((self.row1[7]))
                self.picimg.close()
                self.img_picimg = Image.open("Test.png")

                self.resize_image = self.img_picimg.resize((120, 120), Image.ANTIALIAS)
                self.pic = ImageTk.PhotoImage(self.resize_image)

                self.image_label.config(image=self.pic)
                self.image_uploaded1 = True
                self.resize_imgbar1 = self.resize_image
                os.remove("Test.png")
                self.delete_btn.configure(state="normal")
                self.update_btn.configure(state="normal")

                conn.commit()
                conn.close()
            else:
                messagebox.showerror("Library management system", "No record found.")

    def upload_image(self):
        self.file_add = self.show_image()
        if self.file_add:
            self.imgbar1 = Image.open(self.file_add)
            self.resize_imgbar1 = self.imgbar1.resize((120, 120), Image.ANTIALIAS)
            self.new_img1 = ImageTk.PhotoImage(self.resize_imgbar1)
            self.image_label.configure(image=self.new_img1)
            self.image_uploaded1 = True
        else:
            messagebox.showerror("Error", "Please select image.")

    def scan_QR_Code(self):
        if self.radio_var.get() == 1:
            # image
            self.file_loc = self.show_image()
            if self.file_loc:
                self.imgbar = Image.open(self.file_loc)
                self.testimg = self.imgbar
                self.resize_imgbar = self.imgbar.resize((215, 130), Image.ANTIALIAS)
                self.new_img = ImageTk.PhotoImage(self.resize_imgbar)

                # read barcode or QR code
                barcode = decode(self.testimg)
                if not barcode:
                    messagebox.showwarning(
                        "Error", "This is not a valid barcode/QR code image."
                    )
                else:
                    self.scan_label.configure(image=self.new_img)
                    for code in barcode:
                        self.isbn_entr.delete(0, END)
                        self.isbn_entr.insert(0, code.data.decode("utf-8"))

        else:
            # Camera

            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 215)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 130)
            if self.capture.isOpened():
                self.show_frames()
            else:
                messagebox.showerror(
                    "Library Management System", "Unable to open camera."
                )

    def show_frames(self):

        if self.radio_var.get() == 1:
            self.capture.release()
            cv2.destroyAllWindows()

        else:
            success, frame = self.capture.read()
            # frame = cv2.flip(frame,0)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgresize = img.resize((215, 130), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=imgresize)
            self.scan_label.imgtk = imgtk
            self.scan_label.configure(image=imgtk)
            # read barcode or QR code
            bar_code = decode(frame)
            if not bar_code:
                pass
            else:
                for c in bar_code:
                    self.isbn_entr.delete(0, END)
                    self.isbn_entr.insert(0, c.data.decode("utf-8"))

            self.scan_label.after(1, self.show_frames)

    def clear(self):
        self.isbn_entr.delete(0, END)
        self.title_entr.delete(0, END)
        self.category_entr.delete(0, END)
        self.author_entr.delete(0, END)
        self.dop_entr.delete(0, END)
        self.publisher_entr.delete(0, END)
        self.quantity_entr.delete(0, END)
        self.file_add = ""
        self.image_uploaded1 = False
        self.category_entr.set("Select Category")
        self.scan_label.configure(image="")
        self.image_label.configure(image="")
        self.delete_btn.configure(state="disabled")
        self.update_btn.configure(state="disabled")

    def add_book_query(self):

        if (
            self.isbn_entr.get() == ""
            or self.title_entr.get() == ""
            or self.dop_entr.get() == ""
            or self.category_entr.get() == ""
            or self.category_entr.get() == "Select Category"
            or self.author_entr.get() == ""
            or self.quantity_entr.get() == ""
            or self.publisher_entr.get() == ""
        ):
            messagebox.showwarning(
                "Library Management System", "All fields are necessary."
            )
        elif self.image_uploaded1 == False:
            messagebox.showwarning("Library Management System", "Please upload image.")
        else:

            conn = psycopg2.connect(
                user="kevin",
                password="2048",
                host="localhost",
                port="5432",
                database="libdb",
            )

            cur = conn.cursor()
            cur.execute(f"select isbn from books where isbn='{self.isbn_entr.get()}'")
            self.row1 = cur.fetchone()
            if self.row1 == None:

                self.resize_imgbar1.save("Temp1.png")
                self.drawings1 = open("Temp1.png", "rb").read()
                os.remove("Temp1.png")
                SQL = "insert into books (isbn, title, category, author, publisher, dop, number, image) values(%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (
                    self.isbn_entr.get(),
                    self.title_entr.get(),
                    self.category_entr.get(),
                    self.author_entr.get(),
                    self.publisher_entr.get(),
                    self.dop_entr.get(),
                    self.quantity_entr.get(),
                    psycopg2.Binary(self.drawings1),
                )
                cur.execute(SQL, data)
                conn.commit()
                conn.close()

                messagebox.showinfo(
                    "Library Management System", "Book added successfully."
                )

                self.clear()

            else:
                self.update_book_query()
                conn.commit()
                conn.close()
                # messagebox.showerror("Library Management System", "Book already exists in the inventory.")
                self.clear()

    def show_image(self):

        img_address = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select image",
            filetype=(("jpg file", "*.jpg"), ("png file", "*.png")),
        )

        return img_address
