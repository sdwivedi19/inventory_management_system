from tkinter import *
from tkinter import ttk, messagebox
import PIL.Image, PIL.ImageTk       # we are using PIL. because of some error otherwise we can directly use from PIL import Image and ImageTk
from registration import *
import sqlite3
from forgotpass import *
import os                           # to run the dashboard file directly
from email_pass import *
import time



# Classes are very useful. We can define all the widgets in top and then we can define their functionality
# This gives us a structure and avoids confusion
# Whenever we call any attribute of this class, we will use self
class Login_System:

    def __init__(self, root):
        self.root = root          # self is used so that root becomes an object of the class & a part of the class only
        self.root.title("Login System | Developed by Sudhansu")
        self.root.geometry("1250x620+0+10")
        #self.root.config(bg="#fafafa") # To change the background color of window

        self.root.wm_iconbitmap('billing.ico')

        #====image==============
            ## INFO- PhotoImage is inbuilt in tkinter and can be used only for png images
        #self.main_image=PhotoImage(file="images/im.png")
            ## INFO- Our file is other than png so we will have to use ImageTk method
        # self.main_image = ImageTk.PhotoImage(file="images/im2.jpg")
        self.main_image = PIL.Image.open("images/im4.jpg")
        self.main_image = self.main_image.resize((600, 500), PIL.Image.ANTIALIAS)
        self.main_image = PIL.ImageTk.PhotoImage(self.main_image)

        self.lbl_main_image = Label(self.root, image=self.main_image, bd=0)
        self.lbl_main_image.place(x=90, y=50)

        #====Variables===============
        self.var_user_name = StringVar()
        self.var_password = StringVar()


        #====login frame============
        login_Frame = Frame(self.root, bd=2, relief=RIDGE)
        login_Frame.place(x=750, y=60, width=350, height=450)

        title_login_Frame = Label(login_Frame, text="Login System", font=("elephant", 30, "bold"))
        title_login_Frame.place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_Frame, text="Username or Employee Id", font=("Andalus", 15), fg="#767171")
        lbl_user.place(x=50, y=100)
        txt_user = Entry(login_Frame, textvariable=self.var_user_name, font=("times new roman", 15), fg="#767171", bg="#ECECEC")
        txt_user.place(x=50, y=140, width=250)

        lbl_password = Label(login_Frame, text="Password", font=("Andalus", 15), fg="#767171")
        lbl_password.place(x=50, y=180)
        txt_password = Entry(login_Frame, textvariable=self.var_password, show="*", font=("times new roman", 15), fg="#767171", bg="#ECECEC")
        txt_password.place(x=50, y=220, width=250)      #show is used to hide the password from user when typed

        btn_login = Button(login_Frame, text="Log In", command=self.login, font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2")
        btn_login.place(x=50, y=260, width=250, height=30)

        horizontal_row = Label(login_Frame, bg="lightgray")
        horizontal_row.place(x=50, y=305, width=250, height=2)

        or_row = Label(login_Frame, text="OR", font=("times new roman", 15, "bold"))
        or_row.place(x=150, y=290)

        btn_forgot_password = Button(login_Frame, text="Forgot Password?", command=self.forgot_password, font=("times new roman", 13),  fg="#00B0F0", activeforeground="#00B0F0", bd=0, cursor="hand2")
        btn_forgot_password.place(x=50, y=320, width=250, height=30)

        #====register frame============
        register_Frame = Frame(self.root, bd=2, relief=RIDGE)
        register_Frame.place(x=750, y=520, width=350, height=70)

        lbl_register = Label(register_Frame, text="SUBSCRIBE | LIKE | SHARE", font=("times new roman", 13))
        lbl_register.place(x=0, y=15, relwidth=1)
        btn_register = Button(register_Frame, text="Register Here", command=self.register_user, font=("times new roman", 13), fg="#00B0F0", activeforeground="#00B0F0", bd=0, cursor="hand2")
        btn_register.place(x=20, y=30, width=250, height=30)

        #=====animation images======
        self.im1 = PIL.Image.open("images/im1.jpg")
        self.im1 = self.im1.resize((600, 500), PIL.Image.ANTIALIAS)
        self.im1 = PIL.ImageTk.PhotoImage(self.im1)

        self.im2 = PIL.Image.open("images/im2.jpg")
        self.im2 = self.im2.resize((600, 500), PIL.Image.ANTIALIAS)
        self.im2 = PIL.ImageTk.PhotoImage(self.im2)

        self.im3 = PIL.Image.open("images/im3.jpg")
        self.im3 = self.im3.resize((600, 500), PIL.Image.ANTIALIAS)
        self.im3 = PIL.ImageTk.PhotoImage(self.im3)

        self.lbl_image_change = Label(self.root)     # you can use bg color to check the position of the label
        self.lbl_image_change.place(x=90, y=50, width=600, height=500)

        self.animate()

    def animate(self):
        # concept of swapping to change the image constantly
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im

        self.lbl_image_change.config(image=self.im)
        self.lbl_image_change.after(2000, self.animate) # 2000 is in milliseconds which means 2 seconds

    def login(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_user_name.get() == "" or self.var_password.get() == "":
                messagebox.showerror("Error", "All fields are required!", parent=self.root)
            else:
                cur.execute("SELECT utype,pass FROM employee WHERE eid=?", (self.var_user_name.get(),))
                check = cur.fetchone()
                #print(check)
                if len(check) == 0:
                    messagebox.showerror("Error", "Invalid username!", parent=self.root)
                elif self.var_password.get() != check[1]:
                    messagebox.showerror("Error", "Wrong password!", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome : {str(self.var_user_name.get())}", parent=self.root)
                    if check[0] == "Admin":
                        # ====to close the current window====
                        self.root.destroy()
                        # =========command to run the dashboard file directly============
                        os.system("python dwivedipntbilling.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def register_user(self): #self pass so that the root class can be used
        self.new_win=Toplevel(self.root)
        self.new_obj=User_Registration(self.new_win)


    def forgot_password(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_user_name.get() == "":
                messagebox.showerror("Error", "Employee Id is required!", parent=self.root)
            else:
                cur.execute("SELECT email FROM employee WHERE eid=?", (self.var_user_name.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee Id!\nTry Again", parent=self.root)
                else:
                    email=row[0]
                    messagebox.showinfo("Info","Please wait while the OTP to reset your password is sent to your registerd email and the new window opens...",parent=self.root)
                    otp = int(time.strftime("%H%M%S")) + int(time.strftime("%S"))
                    chk = Email_Otp(email, otp)
                    if chk == 'f':
                        messagebox.showerror("Error","Connection Error, Try Again!", parent=self.root)
                    else:
                        #=====open forgot password window=====
                        self.forgot_win = Toplevel(self.root)
                        self.new_obj = ForgotPasswordClass(self.forgot_win, email,otp)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()             # Without mainloop, the code gets executed but the window doesn't open


