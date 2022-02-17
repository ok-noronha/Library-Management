from PIL import Image


class GDT:
    def host_email_id(self):
        return "yourCUlibrarian"

    def host_email_password(self):
        return "KevinN9ro%google"

    def __init__(self):

        self.font_family = "times new roman"

        self.coder = "Kevin Noronha"
        self.coder_color = "#800080"

        self.params = """user=kevin
        password=2048
        host=localhost
        port=5432
        dbname=libdb"""

        # width and height of the window
        self.width = 600
        self.height = 400
        self.label_height = 75

        # paths to images and icons
        self.icon = r"images/LibIcon.ico"
        self.sp_sc = Image.open("images/splash_screen.jpg")

        self.login_bg = Image.open("images/login_bg.png")
        self.label = Image.open("images/christlabel.png")
        self.lockicon = Image.open("images/lock.png")
        self.frgicon = Image.open("images/forget.png")
        self.proficon = Image.open("images/profile.png")
        self.hid = Image.open("images/pwd_hide.png")
        self.shw = Image.open("images/pwd_show.png")

        # colors used in the application
        self.prog_bar_bg = "#550A35"
        self.prog_bar_fg = "#c55f52"
        self.login_bg_col = "#E2B188"
        self.label_bg_col = "#FFFFFF"
        self.frame_bg = "#008ae6"
        self.text_col = "#333333"
        self.log_in_col = "#504D50"
        self.log_in_bg = "#A296A1"
        self.addlib_col = "#ff9900"
