from tkinter import *
from tkinter import ttk, messagebox
import sqlite3



class ForgotPasswordClass:
    def __init__(self, root, email, otp):
        self.otp = otp
        self.email = email
        self.root = root          # self is used so that root becomes an object of the class & a part of the class only
        self.root.title("Login System | Developed by Sudhansu")
        self.root.geometry("500x400+400+80")
        self.root.focus_force()


        title = Label(self.root, text="Reset Password", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        title.pack(side=TOP, fill=X)

        lbl_reset =Label(self.root, text=f"Enter OTP sent on your registered email id:\n\t\t{self.email}", font=("goudy old style", 15))
        lbl_reset.place(x=10, y=30)
        self.txt_otp = Entry(self.root,font=("goudy old style", 15), bg="lightyellow")
        self.txt_otp.place(x=250, y=90, width=200, height=30)

        self.btn_submit_otp = Button(self.root, text="Submit", command=self.submit_otp, font=("Arial", 15), bg="lightblue",fg="white", cursor="hand2")
        self.btn_submit_otp.place(x=250, y=140, width=100, height=30)

        lbl_new_pass = Label(self.root, text="New Password :",font=("goudy old style", 15))
        lbl_new_pass.place(x=10, y=200)
        self.txt_new_pass = Entry(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_new_pass.place(x=30, y=240, width=200, height=30)


        lbl_confirm_new_pass = Label(self.root, text="Confirm New Password :",font=("goudy old style", 15))
        lbl_confirm_new_pass.place(x=10, y=280)
        self.txt_confirm_new_pass = Entry(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_confirm_new_pass.place(x=30, y=320, width=200, height=30)

        self.btn_change_pass = Button(self.root, text="Update", state=DISABLED, command=self.change_pass, font=("Arial", 15), bg="lightblue",fg="white", cursor="hand2")
        self.btn_change_pass.place(x=200, y=360, width=100, height=30)


    def change_pass(self):
        if self.txt_new_pass.get() == "" or self.txt_confirm_new_pass.get() == "":
            messagebox.showerror("Error","Password is required!", parent=self.root)
        elif self.txt_new_pass.get() != self.txt_confirm_new_pass.get():
            messagebox.showerror("Error", "New Password and Confirm New Password must be same!", parent=self.root)
        else:
            con = sqlite3.connect(database=r'pntb.db')
            cur = con.cursor()
            try:
                cur.execute("UPDATE employee SET pass=? WHERE email=?",
                    (self.txt_new_pass.get(), self.email))
                con.commit()
                messagebox.showinfo("Success", "Password Updated successfully!", parent=self.root)
                self.root.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def submit_otp(self):
        if int(self.txt_otp.get()) == self.otp:
            self.btn_submit_otp.config(state=DISABLED)
            self.btn_change_pass.config(state=NORMAL)
        else:
            messagebox.showerror("Error","Invalid OTP! Try Again.",parent=self.root)




if __name__ == "__main__":
    root = Tk()
    obj = ForgotPasswordClass(root)
    root.mainloop()             # Without mainloop, the code gets executed but the window doesn't open
