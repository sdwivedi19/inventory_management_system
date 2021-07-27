from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk                         # "pip install pillow" - command to install pillow
import pymysql                                         # "pip install pymysql"
import sqlite3

# Classes are very useful. We can define all the widgets in top and then we can define their functionality
# This gives us a structure and avoids confusion
# Whenever we call any attribute of this class, we will use self
# There are two ways to fetch the data from the entryfields -
#   1. defining a variable in the beginning and using it
#   2. using self with the name of entry fields so that they can be used directly
#       In this code, we have used second way only for last name, for rest we have used first way
class User_Registration:

    def __init__(self, root):
        self.root = root          # self is used so that root becomes an object of the class & a part of the class only
        self.root.title("Login System | Developed by Sudhansu")
        self.root.geometry("1250x620+0+10")
        self.root.config(bg="white") # To change the background color of window
        self.root.focus_force()

        # ====Variables===============
            #for last name we have used the second method to fetch the data of entry field
        self.var_first_name = StringVar()
        #self.var_last_name = StringVar()
        self.var_contact_no = IntVar()
        self.var_email = StringVar()
        self.var_security_que = StringVar()
        self.var_security_ans = StringVar()
        self.var_user_name = StringVar()
        self.var_confirm_user_name = StringVar()
        self.var_password = StringVar()
        self.var_confirm_password = StringVar()

        #=====background image=======
        self.bg_im = Image.open("images/im_bg1.jpeg")
        self.bg_im = self.bg_im.resize((950,620), Image.ANTIALIAS)
        self.bg_im = ImageTk.PhotoImage(self.bg_im)

        self.lbl_bg_im = Label(self.root, image=self.bg_im, bd=0)
        self.lbl_bg_im.place(relx=0.24, y=0, relwidth=0.76, relheight=1)

        #=====Label Frame============
        self.info_bg_im = Image.open("images/im_background.jpg")
        self.info_bg_im = self.info_bg_im.resize((400,450), Image.ANTIALIAS)
        self.info_bg_im = ImageTk.PhotoImage(self.info_bg_im)

        self.lbl_info_bg_im = Label(self.root, image=self.info_bg_im, bd=0)
        self.lbl_info_bg_im.place(x=100, y=100)

        lbl_info_text1 = Label(self.lbl_info_bg_im, text="Billing Software", font=("elephant", 25, "bold"), bg="black", fg="white")
        lbl_info_text1.place(x=70, y=50)
        lbl_info_text2 = Label(self.lbl_info_bg_im, text="Developed by Sudhansu", font=("elephant", 12, "bold"), bg="black", fg="white")
        lbl_info_text2.place(x=150, y=100)
        lbl_info_text3 = Label(self.lbl_info_bg_im, text="Log In here", font=("elephant", 15, "bold"), bg="black", fg="white")
        lbl_info_text3.place(x=100, y=360)

        btn_login = Button(self.lbl_info_bg_im, text="Log In", command=self.login, font=("times new roman", 15, "bold"), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2")
        btn_login.place(x=175, y=400, width=100, height=30)

        #====register frame============
        register_Frame = Frame(self.root, bd=2, relief=RIDGE)
        register_Frame.place(x=500, y=100, width=600, height=450)

        title_register_Frame = Label(register_Frame, text="Sign Up", font=("elephant", 30, "bold"), fg="green")
        title_register_Frame.place(x=0, y=10, relwidth=1)

        #===row1===
        lbl_first_name = Label(register_Frame, text="First Name*", font=("Andalus", 15))
        lbl_first_name.place(x=20, y=60)
        txt_first_name = Entry(register_Frame, textvariable=self.var_first_name, font=("times new roman", 15), fg="#767171", bg="#ECECEC")
        txt_first_name.place(x=20, y=90, width=220)

        lbl_last_name = Label(register_Frame, text="Last Name", font=("Andalus", 15))
        lbl_last_name.place(x=320, y=60)
            # we are using the second method to fetch data, so used self
        self.txt_last_name = Entry(register_Frame, font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        self.txt_last_name.place(x=320, y=90, width=220)

        #===row2===
        lbl_contact_no = Label(register_Frame, text="Contact No.*", font=("Andalus", 15))
        lbl_contact_no.place(x=20, y=120)
        txt_contact_no = Entry(register_Frame, textvariable=self.var_contact_no, font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        txt_contact_no.place(x=20, y=150, width=220)

        lbl_email = Label(register_Frame, text="Email*", font=("Andalus", 15))
        lbl_email.place(x=320, y=120)
        txt_email = Entry(register_Frame, textvariable=self.var_email, font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        txt_email.place(x=320, y=150, width=220)

        #===row3===
        lbl_security_que = Label(register_Frame, text="Select Security Question*", font=("Andalus", 15))
        lbl_security_que.place(x=20, y=180)
        cmb_content = (
            "Select",
            "What is your nickname?",
            "What was the name of your high school?",
            "What is your favourite colour?",
            "What is your favourite game?",
            "What is your birthplace?"
            )
        cmb_security_que = ttk.Combobox(register_Frame, textvariable=self.var_security_que, values=cmb_content, state="readonly", justify=CENTER, font=("goudy old style", 15))  # state is used so that the user can not write in the search bar
        cmb_security_que.place(x=20, y=210, width=220, height=30)
        cmb_security_que.current(0)  # to set select as default value in search bar

        lbl_security_ans = Label(register_Frame, text="Security Answer*", font=("Andalus", 15))
        lbl_security_ans.place(x=320, y=180)
        txt_security_ans = Entry(register_Frame, textvariable=self.var_security_ans, font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        txt_security_ans.place(x=320, y=210, width=220)

        #===row4===
        lbl_user_name = Label(register_Frame, text="Username*", font=("Andalus", 15))
        lbl_user_name.place(x=20, y=240)
        txt_user_name = Entry(register_Frame, textvariable=self.var_user_name, font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        txt_user_name.place(x=20, y=270, width=220)

        lbl_confirm_user_name = Label(register_Frame, text="Confirm Username*", font=("Andalus", 15))
        lbl_confirm_user_name.place(x=320, y=240)
        txt_confirm_user_name = Entry(register_Frame, textvariable=self.var_confirm_user_name, font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        txt_confirm_user_name.place(x=320, y=270, width=220)


        lbl_password = Label(register_Frame, text="Password*", font=("Andalus", 15))
        lbl_password.place(x=20, y=300)
        txt_password = Entry(register_Frame, textvariable=self.var_password, show="*", font=("times new roman", 15),fg="#767171", bg="#ECECEC")
        txt_password.place(x=20, y=330, width=220)

        lbl_confirm_password = Label(register_Frame, text="Confirm Password*", font=("Andalus", 15))
        lbl_confirm_password.place(x=320, y=300)
        txt_confirm_password = Entry(register_Frame, textvariable=self.var_confirm_password, show="*", font=("times new roman", 15), fg="#767171", bg="#ECECEC")
        txt_confirm_password.place(x=320, y=330, width=220)

        #===row5-terms&conditions===
        self.var_chk = IntVar()
        self.chk = Checkbutton(register_Frame, text="I Agree the Terms and Conditions*", variable=self.var_chk, font=("times new roman",12), onvalue=1, offvalue=0)
        self.chk.place(x=20, y=370)

        #===row6-register button===
        self.register_im = Image.open("images/im_register.jpg")
        self.register_im = self.register_im.resize((200, 30), Image.ANTIALIAS)
        self.register_im = ImageTk.PhotoImage(self.register_im)

        #btn_register = Button(register_Frame, text="REGISTER NOW", font=("times new roman", 13), bg="green", activebackground="darkgreen", fg="white", activeforeground="white", cursor="hand2")
        btn_register = Button(register_Frame, image=self.register_im, command=self.register_data, cursor="hand2", bd=0)
        btn_register.place(x=20, y=400)

#==========Functions======
    def register_data(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            #print is to show the demo of thw two methods of getting the data from entry field
            #print(self.var_first_name.get(),
            #      self.txt_last_name.get(),self.var_contact_no.get(),self.var_email.get(),self.var_security_que.get(),self.var_security_ans.get(),self.var_user_name.get(),self.var_confirm_user_name.get(),self.var_password.get(),self.var_confirm_password.get())
            if self.var_first_name.get() == "" or\
                self.var_contact_no.get() == "" or\
                self.var_email.get() == "" or\
                self.var_security_que.get() == "" or\
                self.var_security_ans.get() == "" or\
                self.var_user_name.get() == "" or\
                self.var_confirm_user_name.get() == "" or\
                self.var_password.get() == "" or\
                self.var_confirm_password.get() == "":
                messagebox.showerror("Error","All the fields marked * are required!", parent=self.root)
            elif self.var_user_name.get() != self.var_confirm_user_name.get():
                messagebox.showerror("Error", "Username and Confirm Username must be same.", parent=self.root)
            elif self.var_password.get() != self.var_confirm_password.get():
                messagebox.showerror("Error", "Password and Confirm Password must be same.", parent=self.root)
            elif self.var_chk.get() == 0:
                messagebox.showerror("Error", "Please agree to our Terms and Conditions.", parent=self.root)
            else:

                #===to check for used contact======
                cur.execute("SELECT * FROM users WHERE contact=?", (self.var_contact_no.get(),))  # comma is required at last since we are passing tuple
                row1 = cur.fetchone()
                # ===to check for used email======
                cur.execute("SELECT * FROM users WHERE email=?",(self.var_email.get(),))  # comma is required at last since we are passing tuple
                row2 = cur.fetchone()
                # ===to check for used username======
                cur.execute("SELECT * FROM users WHERE username=?",(self.var_user_name.get(),))  # comma is required at last since we are passing tuple
                row3 = cur.fetchone()

                if row1 != None:
                    messagebox.showerror("Error", "This contact already registered, try different!", parent=self.root)
                elif row2 != None:
                    messagebox.showerror("Error", "This email already registered, try different!", parent=self.root)
                elif row3 != None:
                    messagebox.showerror("Error", "This username already registered, try different!", parent=self.root)
                else:
                    cur.execute("INSERT INTO users(fname,lname,contact,email,securityque,securityans,username,password) VALUES(?,?,?,?,?,?,?,?)",
                        (
                                self.var_first_name.get(),
                                self.txt_last_name.get(),
                                self.var_contact_no.get(),
                                self.var_email.get(),
                                self.var_security_que.get(),
                                self.var_security_ans.get(),
                                self.var_user_name.get(),
                                self.var_password.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Registered successfully!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



    def login(self): #self pass so that the root class can be used
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = User_Registration(root)
    root.mainloop()             # Without mainloop, the code gets executed but the window doesn't open
