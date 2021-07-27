from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from employee import *
from supplier import *
from category import *
from products import *
from sales import *
import time

class Dashboard:
    def __init__(self,root): #default constructor
        self.root=root
        self.root.geometry("1250x630+0+0")
        self.root.title("PnT Billing | Developed by Sudhansu Dwivedi")
        self.root.config(bg="white")
        #===title==
        self.icon_title = Image.open("images/im3.jpg")
        self.icon_title = self.icon_title.resize((70, 50), Image.ANTIALIAS)  # ANTIALIAS doesn't change picture quality
        self.icon_title=ImageTk.PhotoImage(self.icon_title) #logo #for jpg or other file format PIL is to be used

        title=Label(self.root,text="Pipes N Tiles Billing",image=self.icon_title,compound=LEFT,font=("times new roman",30,"bold"),bg="blue",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=50)
        #label is static #Anchor is used to position the title #Padx is used to distant the title from the border
        #compound is to position the image w.r.t. text in title

        #===logout button==
        btn_logout=Button(self.root,text="Logout", command=self.logout, font=("times new roman",15,"bold"),bg="red",cursor="hand2").place(x=1100,y=10,height=30,width=100)

        #===clock===
        self.lbl_clock=Label(self.root,text="Welcome to Billing system\t\t  Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",10),bg="yellow",fg="black")
        self.lbl_clock.place(x=0,y=50,relwidth=1,height=30)

        #==LeftMenu===
        self.MenuLogo=Image.open("images/im1.jpg")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS) #ANTIALIAS doesn't change picture quality
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo) #Image is dynamically placed

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=82,width=200,height=550)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman", 18), bg="#009688").pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,font=("times new roman", 16, "bold"),anchor="w",padx=10, bg="green", bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,font=("times new roman", 16, "bold"),anchor="w",padx=10, bg="green", bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,font=("times new roman", 16, "bold"),anchor="w",padx=10, bg="green", bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_products=Button(LeftMenu,text="Products",command=self.product,font=("times new roman", 16, "bold"),anchor="w",padx=10, bg="green", bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,font=("times new roman", 16, "bold"), anchor="w",padx=10,bg="green", bd=3, cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",font=("times new roman", 16, "bold"), anchor="w",padx=10,bg="green", bd=3, cursor="hand2").pack(side=TOP,fill=X)

        #====Content===
        self.lbl_employee=Label(self.root,text="Total Employee\n[ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=225,y=120,height=125,width=250)
        self.lbl_supplier=Label(self.root, text="Total Supplier\n[ 0 ]", bd=5, relief=RIDGE, bg="#ff5722", fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=550, y=120, height=125, width=250)
        self.lbl_category=Label(self.root, text="Total Category\n[ 0 ]", bd=5, relief=RIDGE, bg="#009688", fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=875, y=120, height=125, width=250)
        self.lbl_products=Label(self.root, text="Total Product\n[ 0 ]", bd=5, relief=RIDGE, bg="#607d8b", fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_products.place(x=225, y=300, height=125, width=250)
        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", bd=5, relief=RIDGE, bg="#ffc107", fg="white",font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=550, y=300, height=125, width=250)

        # ===footer===
        lbl_footer = Label(self.root, text="Billing system | Developed by Sudhansu Dwivedi \nFor any Technical Issue contact: 7008853498", font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        #===call the function for realtime time and date
        self.update_contents()
#=================================================================================
    def employee(self): #self pass so that the root class can be used
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self): #self pass so that the root class can be used
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self): #self pass so that the root class can be used
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self): #self pass so that the root class can be used
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self): #self pass so that the root class can be used
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_contents(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM products")
            product=cur.fetchall()
            self.lbl_products.config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute("SELECT * FROM products")
            product = cur.fetchall()
            self.lbl_products.config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[ {str(len(supplier))} ]")

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total category\n[ {str(len(category))} ]")

            cur.execute("SELECT * FROM employee")
            tot_employees = cur.fetchall()
            self.lbl_employee.config(text=f"Total employee\n[ {str(len(tot_employees))} ]")

            tot_sales=len(os.listdir("bills/"))
            self.lbl_sales.config(text=f"Total sales\n[ {str(tot_sales)} ]")
        #=============to update the time=========================
            tm = time.strftime("%I:%M:%S")  # %I is for indian format of time %H is for 24 hour format
            dt = time.strftime("%d-%m-%Y")  # %D will fetch the whole date as DD/MM/YY so we use %d
            self.lbl_clock.config(text=f"Welcome to Billing system\t\t  Date: {str(dt)}\t\t Time: {str(tm)}")
            # to call the function repeatedly to show date and time in realtime
            self.lbl_clock.after(200, self.update_contents)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__": #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= Dashboard(root) #creating object of Billing Class
    root.mainloop() # so that the window stays until we manually exit
