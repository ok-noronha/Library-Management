from PIL import Image


class GDT:
    def __init__(self):

        self.coder = {"name":"Kevin Noronha", "color": "#800080"}
        # width and height of the window
        self.res = {"width": 600,"height": 400}

        # paths to images and icons
        self.icon = r"images/LibIcon.ico"
        self.sp_sc = Image.open("images/splash_screen.jpg")

        self.login_bg = Image.open("images/login_bg.png")
        self.label = Image.open("images/christlabel.png")
        self.lockicon = Image.open("images/lock.png")
        self.frgicon = Image.open("images/forget.png")
        self.proficon = Image.open("images/profile.png")
        Image.open("images/login_bg.png")
        self.hid = Image.open("images/pwd_hide.png")

        # colors used in the application
        self.prog_bar = {bg = "#550A35",fg = "#c55f52"}


class HostEmailDetails:
    def host_email_id(self):
        return "yourCUlibrarian"

    def host_email_password(self):
        return "KevinN9ro%google"
