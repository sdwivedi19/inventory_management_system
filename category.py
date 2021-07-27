from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox  # messagebox for pop up
import sqlite3


class categoryClass:
    def __init__(self, root):  # default constructor
        self.root = root
        self.root.geometry("1000x450+220+120")
        self.root.title("Category")
        self.root.config(bg="white")
        self.root.focus_force()  # to highlight the new window

        #====variables=====
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #===title===
        lbl_title=Label(self.root,text="Product Categories",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=20,pady=5)

        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",20),bg="white").place(x=25,y=80)
        txt_name=Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="lightyellow").place(x=25,y=150,width=300)

        btn_add=Button(self.root, text="Add", command=self.save,font=("goudy old style", 12), bg="#4caf50",fg="white",cursor="hand2").place(x=345,y=145,width=100)
        btn_delete=Button(self.root, text="Delete",command=self.delete,font=("goudy old style", 12), bg="#4caf50", fg="white",cursor="hand2").place(x=465,y=145,width=100)


        #====TreeView - Category Details=====
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=575, y=60, relwidth=0.4, height=150)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CategoryTable.xview)  # to make the scroll bar work
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid", text="C ID")
        self.CategoryTable.heading("name", text="NAME")
        self.CategoryTable["show"] = "headings"  # to hide the default heading that was blank

        self.CategoryTable.column("cid", width=70)
        self.CategoryTable.column("name", width=120)
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)  # event to show the selected row in corresponding fields

        self.show()
        #====images====
            #===image1=====
        self.im1=Image.open("images/im1.jpg")
        self.im1=self.im1.resize((450,200),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)
            #===image2====
        self.im2 = Image.open("images/im2.png")
        self.im2 = self.im2.resize((450, 200), Image.ANTIALIAS)
        self.im2 = ImageTk.PhotoImage(self.im2)

        self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lbl_im2.place(x=500, y=220)

#================Functions===========
        # ======save button======
        # ====to save data in database=====
    def save(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required",parent=self.root)  # parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM category WHERE name=?",(self.var_name.get(),))  # comma is required at last since we are passing tuple
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Category Name already present, try different",parent=self.root)
                else:
                    cur.execute("INSERT INTO category(name) VALUES(?)", (
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        # ===to show data in tree view===

    def show(self):                                                 # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        # =====to reflect data in the fields===

    def get_data(self, ev):
        f = self.CategoryTable.focus()  # to focus on the selected item
        content = (self.CategoryTable.item(f))  # making the content tuple
        row = content['values']  # filtering the values and assigning to row
        # print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    # ======delete button=====
    def delete(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category must be required",parent=self.root)  # parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM category WHERE name=?",(self.var_name.get(),))  # comma is required at last since we are passing tuple
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Category", parent=self.root)
                else:
                    ask = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if ask == True:
                        cur.execute('DELETE FROM category WHERE name=?', (self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        # self.show() #this is already called in the clear function
                        self.clear()  # so that the entries are blank after deleting
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_name.set("")
        self.show()


if __name__=="__main__": #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= categoryClass(root) #creating object of Billing Class
    root.mainloop()