from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile

class BillingClass:
    def __init__(self, root):  # default constructor
        self.root = root
        self.root.geometry("1250x630+0+0")
        self.root.title("PnT Billing | Developed by Sudhansu Dwivedi")
        self.root.config(bg="lightgrey")

##============Main title=============
        self.icon_title = Image.open("images/im3.jpg")
        self.icon_title = self.icon_title.resize((70,50),Image.ANTIALIAS)
        self.icon_title = ImageTk.PhotoImage(self.icon_title)  # logo #for jpg or other file format PIL is to be used
        title = Label(self.root, text="Pipes N Tiles Billing", image=self.icon_title, compound=LEFT,font=("times new roman", 30, "bold"), bg="darkblue", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0,relwidth=1,height=50)
        # label is static #Anchor is used to position the title #Padx is used to distant the title from the border
        # compound is to position the image w.r.t. text in title
        #===logout button==
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"), bg="red",cursor="hand2")
        btn_logout.place(x=1100, y=10, height=30, width=100)

##=============clock label==========
        self.lbl_clock = Label(self.root, text="Welcome to Billing system\t\t  Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman", 10), bg="yellow", fg="black")
        self.lbl_clock.pack(side=TOP,fill=X,pady=50)

##============variables=============
        self.var_prod_search = StringVar()      #used in search product frame

        self.cur_cart_del = StringVar()         #used as flag for deleting selected item from the cart using delete button

        self.var_cust_name=StringVar()          #used in customer details frame
        self.var_cust_contact=StringVar()       #used in customer details frame

        self.var_product_id=StringVar()         #used in add cart widgets frame
        self.var_product_name=StringVar()       #used in add cart widgets frame
        self.var_product_price=StringVar()      #used in add cart widgets frame
        self.var_product_quantity=StringVar()   #used in add cart widgets frame
        self.var_product_stock=StringVar()      #used in add cart widgets frame
        self.var_item_discount=StringVar()      #used in add cart widgets frame

        self.var_calculator_entry=StringVar()   #used in calculator frame

        self.cart_list=[]                       #to show the list in cart frame
        self.chk_print=0

##=============Products Frame========
    #========main product frame==========
        product_Frame = Frame(self.root, bd=4, relief=RIDGE)
        product_Frame.place(x=5, y=80, width=410, height=545)
        prod_frame_title = Label(product_Frame, text="All Products", font=("goudy old style", 20, "bold"), bg="brown",fg="white")
        prod_frame_title.pack(side=TOP, fill=X)

    #======search product frame========
        product_Frame1 = Frame(product_Frame, bd=2, relief=RIDGE,bg="white")
        product_Frame1.place(x=2, y=42, width=398, height=90)
        lbl_search_prod=Label(product_Frame1,text="Search product by name:",font=("goudy old style",15,"bold"),bg="white",fg="green")
        lbl_search_prod.place(x=2,y=5)
        lbl_prod_name=Label(product_Frame1,text="Product Name",font=("goudy old style",15,"bold"),bg="white")
        lbl_prod_name.place(x=5,y=40)
        txt_prod_search=Entry(product_Frame1,textvariable=self.var_prod_search,font=("goudy old style",15),bg="lightyellow")
        txt_prod_search.place(x=135,y=45,width=160,height=30)
        btn_prod_search = Button(product_Frame1, text="Search",command=self.search, font=("goudy old style", 15),bg="lightgrey",fg="black",cursor="hand2")
        btn_prod_search.place(x=310, y=45, width=80, height=28)
        btn_show_all = Button(product_Frame1, text="Show All",command=self.show, font=("goudy old style", 15), bg="#083531",fg="white", cursor="hand2")
        btn_show_all.place(x=310, y=10, width=80, height=28)

    #====Tree view to show results=====
        product_Frame2 = Frame(product_Frame, bd=3, relief=RIDGE)
        product_Frame2.place(x=2, y=140, width=398, height=375)
        lbl_cart = Label(product_Frame2, text="Cart", font=("goudy old style", 15, "bold"), bg="lightyellow",fg="blue")
        lbl_cart.pack(side=TOP,fill=X)

        scrolly = Scrollbar(product_Frame2, orient=VERTICAL)
        scrollx = Scrollbar(product_Frame2, orient=HORIZONTAL)

        self.CartProductTable = ttk.Treeview(product_Frame2, columns=("pid", "pname", "price", "quantity", "status","stock"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartProductTable.xview)  # to make the scroll bar work
        scrolly.config(command=self.CartProductTable.yview)

        self.CartProductTable.heading("pid", text="P Id")
        self.CartProductTable.heading("pname", text="Product Name")
        self.CartProductTable.heading("price", text="Price")
        self.CartProductTable.heading("quantity", text="Quantity")
        self.CartProductTable.heading("status", text="Status")
        self.CartProductTable.heading("stock", text="Stock")

        self.CartProductTable["show"] = "headings"  # to hide the default heading that was blank

        self.CartProductTable.column("pid", width=30)
        self.CartProductTable.column("pname", width=150)
        self.CartProductTable.column("price", width=50)
        self.CartProductTable.column("quantity", width=50)
        self.CartProductTable.column("status", width=50)
        self.CartProductTable.column("stock", width=50)

        self.CartProductTable.pack(fill=BOTH, expand=1)
        self.CartProductTable.bind("<ButtonRelease-1>", self.get_data)  # event
        #self.show()

        lbl_note=Label(product_Frame,text="NOTE: Enter 0 in Quantity to remove the product from the Cart!", font=("goudy old style",10),fg="Red",bg="white",anchor="w")
        lbl_note.pack(side=BOTTOM,fill=X)

##============Second Column===========
    #========customer details frame==========
        customer_Frame = Frame(self.root, bd=4, relief=RIDGE,bg="white")
        customer_Frame.place(x=420, y=80, width=530, height=70)
        customer_title = Label(customer_Frame, text="Customer details", font=("goudy old style", 15,"bold"), bg="lightgrey")
        customer_title.pack(side=TOP,fill=X)

        #====contents=====
        lbl_cust_name = Label(customer_Frame, text="Name", font=("goudy old style", 12, "bold"),bg="white")
        lbl_cust_name.place(x=2, y=30)
        txt_cust_name = Entry(customer_Frame, textvariable=self.var_cust_name, font=("goudy old style", 12),bg="lightyellow")
        txt_cust_name.place(x=48, y=30, width=200, height=25)
        lbl_cust_contact = Label(customer_Frame, text="Contact No.", font=("goudy old style", 12, "bold"), bg="white")
        lbl_cust_contact.place(x=250, y=30)
        txt_cust_contact = Entry(customer_Frame, textvariable=self.var_cust_contact, font=("goudy old style", 12),bg="lightyellow")
        txt_cust_contact.place(x=338, y=30, width=180, height=25)

    #========Calculator and cart frame==========
        cal_cart_Frame = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        cal_cart_Frame.place(x=420, y=155, width=530, height=380)
        #====contents====
            #======calculator frame==========
        cal_Frame = Frame(cal_cart_Frame, bd=4, relief=RIDGE, bg="white")
        cal_Frame.place(x=5, y=10, width=172, height=360)
        # cal_title = Label(cal_Frame, text="Calculator", font=("goudy old style", 15, "bold"),bg="lightgrey")
        # cal_title.pack(side=TOP, fill=X)
        #cannot use pack simultaneously with grid

            #======Calculator frame content=========
        self.txt_calculator_input=Entry(cal_Frame,textvariable=self.var_calculator_entry,font=("arial",15,"bold"),width=12,bg="lightyellow",bd=15,relief=GROOVE,justify=RIGHT)
        self.txt_calculator_input.grid(row=0,columnspan=4)
        #grid gives us a layout of rows and columns where we can insert values

        btn_7=Button(cal_Frame,text="7",command=lambda:self.get_input(7),font=("arial",15,"bold"),bd=5,width=2,pady=8,cursor="hand2")
        btn_7.grid(row=1,column=0)
        btn_8 = Button(cal_Frame, text="8", command=lambda:self.get_input(8),font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_8.grid(row=1, column=1)
        btn_9 = Button(cal_Frame, text="9",command=lambda:self.get_input(9), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_9.grid(row=1, column=2)
        btn_sum = Button(cal_Frame, text="+",command=lambda:self.get_input("+"), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_sum.grid(row=1, column=3)

        btn_4 = Button(cal_Frame, text="4", command=lambda:self.get_input(4),font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_4.grid(row=2, column=0)
        btn_5 = Button(cal_Frame, text="5", command=lambda:self.get_input(5),font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_5.grid(row=2, column=1)
        btn_6 = Button(cal_Frame, text="6", command=lambda:self.get_input(6),font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_6.grid(row=2, column=2)
        btn_diff = Button(cal_Frame, text="-",command=lambda:self.get_input("-"), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_diff.grid(row=2, column=3)

        btn_1 = Button(cal_Frame, text="1",command=lambda:self.get_input(1), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_1.grid(row=3, column=0)
        btn_2 = Button(cal_Frame, text="2",command=lambda:self.get_input(2), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_2.grid(row=3, column=1)
        btn_3 = Button(cal_Frame, text="3",command=lambda:self.get_input(3), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_3.grid(row=3, column=2)
        btn_prod = Button(cal_Frame, text="*",command=lambda:self.get_input("*"), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_prod.grid(row=3, column=3)

        btn_0 = Button(cal_Frame, text="0", command=lambda:self.get_input(0),font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_0.grid(row=4, column=0)
        btn_decimal = Button(cal_Frame, text=".",command=lambda:self.get_input("."), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_decimal.grid(row=4, column=1)
        btn_equal = Button(cal_Frame, text="=",command=self.perform_cal,font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_equal.grid(row=4, column=2)
        btn_division = Button(cal_Frame, text="/",command=lambda:self.get_input("/"), font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_division.grid(row=4, column=3)

        btn_clear = Button(cal_Frame, text="AC", command=self.clear_cal,font=("arial", 15, "bold"), bd=5, width=2, pady=8, cursor="hand2")
        btn_clear.grid(row=5, column=0)
        btn_backspace = Button(cal_Frame, text="C", command=self.backspace, font=("arial", 15, "bold"), bd=5, width=2,pady=8, cursor="hand2")
        btn_backspace.grid(row=5, column=1)

        #====Tree view to show results=====
            #=======cart frame=========
        cart_Frame = Frame(cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=180, y=10, width=335, height=360)
        self.cart_title = Label(cart_Frame, text="Cart\t  Total Product(s): [0]", font=("goudy old style", 15, "bold"), bg="lightgrey",anchor="w")
        self.cart_title.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("pid", "pname", "rate", "quantity","discount","amount","savings"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)  # to make the scroll bar work
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="P Id")
        self.CartTable.heading("pname", text="Product Name")
        self.CartTable.heading("rate", text="Rate")
        self.CartTable.heading("quantity", text="Qty")
        self.CartTable.heading("discount", text="Dis(%)")
        self.CartTable.heading("amount", text="Amount")
        self.CartTable.heading("savings", text="Your Savings")


        self.CartTable["show"] = "headings"  # to hide the default heading that was blank

        self.CartTable.column("pid", width=30)
        self.CartTable.column("pname", width=150)
        self.CartTable.column("rate", width=50)
        self.CartTable.column("quantity", width=50)
        self.CartTable.column("discount", width=50)
        self.CartTable.column("amount", width=50)
        self.CartTable.column("savings", width=80)


        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.cur_cart_item)  # event
        # self.show()

##=========Add cart Widgets Frame============
        add_cart_widget_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        add_cart_widget_Frame.place(x=420, y=540, width=530, height=85)

        lbl_product_name=Label(add_cart_widget_Frame,text="Name",font=("goudy old style",15),bg="white")
        lbl_product_name.place(x=5,y=2)
        txt_product_name=Entry(add_cart_widget_Frame,textvariable=self.var_product_name, font=("goudy old style", 15),state="readonly")
        txt_product_name.place(x=5, y=30,width=200,height=22)

        lbl_product_price=Label(add_cart_widget_Frame, text="Rate", font=("goudy old style", 15), bg="white")
        lbl_product_price.place(x=220, y=2)
        txt_product_price=Entry(add_cart_widget_Frame, textvariable=self.var_product_price,font=("goudy old style", 15),bg="lightyellow")
        txt_product_price.place(x=220, y=30, width=100, height=22)

        lbl_item_discount = Label(add_cart_widget_Frame, text="Discount(%)", font=("goudy old style", 14), bg="white")
        lbl_item_discount.place(x=325, y=2)
        txt_item_discount = Entry(add_cart_widget_Frame, textvariable=self.var_item_discount,font=("goudy old style", 15), bg="lightyellow")
        txt_item_discount.place(x=330, y=30, width=80, height=22)


        lbl_product_quantity=Label(add_cart_widget_Frame, text="Quantity", font=("goudy old style", 15), bg="white")
        lbl_product_quantity.place(x=430, y=2)
        txt_product_quantity= Entry(add_cart_widget_Frame, textvariable=self.var_product_quantity,font=("goudy old style", 15),bg="lightyellow")
        txt_product_quantity.place(x=430, y=30, width=90, height=22)

        self.lbl_product_stock=Label(add_cart_widget_Frame, text="In Stock: ", font=("goudy old style", 15), bg="white")
        self.lbl_product_stock.place(x=5, y=50)     #here we have used self because we will use this in function and that's why double line is necessary

        btn_clear_cart = Button(add_cart_widget_Frame, text="Clear",command=self.clear_product_details, font=("goudy old style", 13), bg="lightgray",cursor="hand2")
        btn_clear_cart.place(x=170, y=55, width=110, height=22)

        btn_add_cart = Button(add_cart_widget_Frame, text="Add|Update", command=self.add_update_cart,font=("goudy old style", 13), bg="orange",cursor="hand2")
        btn_add_cart.place(x=290, y=55, width=110, height=22)

        btn_delete_cart = Button(add_cart_widget_Frame, text="Delete", command=self.delete_cart,font=("goudy old style", 13), bg="orange", cursor="hand2")
        btn_delete_cart.place(x=410, y=55, width=110, height=22)

        ##===========Column3-Billing Area==========
    #=======text======
        bill_Frame=Frame(self.root,bd=2,relief=RIDGE)
        bill_Frame.place(x=955,y=80,width=290,height=410)
        bill_title = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#262626",fg="white")
        bill_title.pack(side=TOP, fill=X)
        scrolly = Scrollbar(bill_Frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx = Scrollbar(bill_Frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM,fill=X)

        self.txt_bill_area=Text(bill_Frame,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        scrollx.config(command=self.txt_bill_area.xview)
    #=======buttons======
        bill_button_Frame = Frame(self.root, bd=2, relief=RIDGE)
        bill_button_Frame.place(x=955, y=500, width=290, height=125)

        self.lbl_amount = Label(bill_button_Frame, text="Bill Amount \nRs \n[0]", font=("arial", 11, "bold"), bg="#3f51b5",fg="white")
        self.lbl_amount.place(x=5,y=5,width=90,height=70)
        self.lbl_discount = Label(bill_button_Frame, text="Tot. Dis.\nRs \n[0]", font=("arial", 11, "bold"),bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=98, y=5, width=90, height=70)
        self.lbl_netpay = Label(bill_button_Frame, text="Net Pay\nRs \n[0]", font=("arial", 11, "bold"),bg="#607d8b", fg="white")
        self.lbl_netpay.place(x=191, y=5, width=90, height=70)

        btn_print = Button(bill_button_Frame, text="Print",command=self.print_bill, font=("arial", 10, "bold"),bg="#3f51b5", fg="white",cursor="hand2")
        btn_print.place(x=5, y=85, width=90, height=30)
        btn_clear_all =Button(bill_button_Frame, text="Clear All", command=self.clear_all,font=("arial", 10, "bold"),bg="#8bc34a", fg="white",cursor="hand2")
        btn_clear_all.place(x=98, y=85, width=70, height=30)
        btn_generate =Button(bill_button_Frame, text="Generate/Save Bill",command=self.generate_bill,font=("arial", 9, "bold"),bg="#607d8b", fg="white",cursor="hand2")
        btn_generate.place(x=171, y=85, width=110, height=30)

    #=====to show the details=========
        self.show()
        self.update_date_time()
        #self.bill_top()
##===============All functionalities=========
    #=======Calculator functions===========
        #=======function for all input keys in calculator=====
    def get_input(self,num):
        xnum=self.var_calculator_entry.get()+str(num)
        self.var_calculator_entry.set(xnum)
        #=======function for "AC" button=====
    def clear_cal(self):
        self.var_calculator_entry.set("")
        #======function for "C" button=====
    def backspace(self):
        back_result=self.var_calculator_entry.get()
        self.var_calculator_entry.set(back_result[:-1])
        #=====function for "=" button====
    def perform_cal(self):
        result=self.var_calculator_entry.get()
        self.var_calculator_entry.set(eval(result))     #inbuilt function to evaluate expression
    #====================================================

    #==========to show data in tree view=========
    def show(self):  # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            self.var_prod_search.set("")
            #self.CartProductTable = ttk.Treeview(product_Frame2,columns=("pid", "pname", "price", "quantity", "status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
            cur.execute("SELECT pid, product, price, quantity, status FROM products where status='Active'")
            rows = cur.fetchall()
            self.CartProductTable.delete(*self.CartProductTable.get_children())
            for row in rows:
                self.CartProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    #=======================================

    #====product search button==============
    def search(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_prod_search.get() == "":
                messagebox.showerror("Error", "Search Input is required", parent=self.root)
            else:
                cur.execute(
                    "SELECT pid, product, price, quantity, status FROM products WHERE product LIKE '%"+self.var_prod_search.get()+"%' and status='Active'")  # mind spaces, or else it wll throw exception
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.CartProductTable.delete(*self.CartProductTable.get_children())
                    for row in rows:
                        self.CartProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    #=============================================

    #=====to reflect data in the fields===
    def get_data(self, ev):
        f = self.CartProductTable.focus()          #to focus on the selected item
        content = (self.CartProductTable.item(f))  #making the content tuple
        row = content['values']                    #filtering the values and ssigning to row
        #print(row)
        self.var_product_id.set(row[0])                                   #used in add cart widgets frame
        self.var_product_name.set(row[1])                                 #used in add cart widgets frame
        self.var_product_price.set(row[2])                                #used in add cart widgets frame
        self.lbl_product_stock.config(text=f"In Stock: [{str(row[3])}]")  #used in add cart widgets frame

        self.var_item_discount.set("")
        self.var_product_quantity.set("1")
        self.var_product_stock.set(row[3])
    #============================================

    #===============add or update items in the cart=======
    def entry_validation(self,field_entry):
        try:
            float(field_entry)
            return True
        except:
            return False
    def add_update_cart(self):
        #=========validations========
        if self.var_item_discount.get()=="":
            self.var_item_discount.set("0")
        if self.var_product_id.get() == "" or self.var_product_name.get()=="":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.entry_validation(self.var_product_price.get()) is False:  #or self.var_product_price.get() is not int:
            messagebox.showerror("Error", "Rate must be a real number!",parent=self.root)
        elif self.entry_validation(self.var_item_discount.get()) is False:  # or self.var_item_discount.get() is not int:
            messagebox.showerror("Error", "Discount must be a real number!",parent=self.root)
        elif self.entry_validation(self.var_product_quantity.get()) is False:
            messagebox.showerror("Error", "Quantity must be a real number!",parent=self.root)

        item_index = 0     #will be used for updating the list
        cart_data=[]
        #========functions=============
        if self.var_product_quantity.get()=="0":
            up="no"
            cart_data.extend(self.var_product_id.get())
            for item in self.cart_list:
                if item[0]==cart_data[0]:
                    up="yes"
                    item_index = self.cart_list.index(item)
            print(item_index,up)
            if up=="yes":
                ask=messagebox.askyesno("Confirm", "Product is in the cart.\nDo you really want to DELETE?",parent=self.root)
                if ask == True:
                    del self.cart_list[item_index]
            else:
                messagebox.showerror("Error","Quantity is Zero, please select quantity!",parent=self.root)
            #self.clear_product_details()
        elif float(self.var_product_stock.get())<float(self.var_product_quantity.get()):
            messagebox.showerror("Error","Not enough stock!",parent=self.root)
        else:
            item_amount1=float(self.var_product_price.get())*float(self.var_product_quantity.get())
            discount=round(float(self.var_item_discount.get()),2)
            discount=float("{:.2f}".format(discount))
            item_amount2=round((item_amount1*(100-discount)/100),2)
            item_amount2=float("{:.2f}".format(item_amount2))
            item_savings=round((item_amount1-item_amount2),2)
            item_savings=float("{:.2f}".format(item_savings))

            #print(item_amount)
            #self.clear_product_details()
            cart_data.extend([self.var_product_id.get(),self.var_product_name.get(),self.var_product_price.get(),self.var_product_quantity.get(),self.var_item_discount.get(),item_amount2,item_savings,self.var_product_stock.get()])
            #print(cart_data)
        #=========update cart==========
            up="no"
            for item in self.cart_list:
                if item[0]==cart_data[0]:
                    up = "yes"
                    item_index = self.cart_list.index(item)
            if up=="yes":
                ask = messagebox.askyesno("Confirm","Product already added to cart.\nDo you really want to UPDATE?",parent=self.root)
                if ask == True:
                    del self.cart_list[item_index]
                    self.cart_list.insert(item_index,cart_data)
            else:
                self.cart_list.append(cart_data)
                # cart_data[3]=float(item[3])+float(cart_data[3])
                # cart_data[5]=float(item[5])+float(cart_data[5])
        self.show_cart()
        self.bill_updates()
    #=============================================



    #===to show data in cart area====================
    def show_cart(self):        #we are passing self because we have defined all our variables with self and used self in all our widgets
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    #===================================================

    #===========clear the product details frame============
    def clear_product_details(self):
        self.var_product_quantity.set("")
        self.var_product_price.set("")
        self.var_product_name.set("")
        self.var_item_discount.set("")
        self.lbl_product_stock.config(text="In Stock: ")
    #============================================

    #====to store the index of the current selected item in the cart list so that it can be deleted using delete button====
    def cur_cart_item(self,ev):
        f = self.CartTable.focus()          #to focus on the selected item
        self.delete_index = (self.CartTable.index(f))  #making the content tuple
        content=(self.CartTable.item(f))    #making the content tuple
        row=content['values']               #filtering the values and ssigning to row
        self.var_product_id.set(row[0])  # used in add cart widgets frame
        self.var_product_name.set(row[1])  # used in add cart widgets frame
        self.var_product_price.set(row[2])  # used in add cart widgets frame
        self.var_product_quantity.set(row[3])
        self.var_item_discount.set(row[4])
        self.lbl_product_stock.config(text=f"In Stock: [{str(row[7])}]")  #used in add cart widgets frame
        self.cur_cart_del.set("yes")
        #print(row,self.delete_index,type(self.delete_index))
        #print(content)
        #row = content['values']  # filtering the values and ssigning to row
    def delete_cart(self):
        if len(self.cart_list)==0:
            messagebox.showerror("Error","The cart is empty!",parent=self.root)
        elif self.cur_cart_del.get()!="yes":
            messagebox.showerror("Error", "No item selected.", parent=self.root)
        else:
            ask = messagebox.askyesno("Confirm", "Do you really want to DELETE the product?",parent=self.root)
            if ask == True:
                del self.cart_list[self.delete_index]
                self.show_cart()
                self.bill_updates()
    #===============================================

    #==================bill updates===============
    def bill_updates(self):
        self.bill_amount=0
        self.total_savings=0
        self.prod=0
        for item in self.cart_list:
            self.prod=self.prod+1
            self.bill_amount=self.bill_amount+item[5]+item[6]
            self.total_savings=self.total_savings+item[6]
        self.net_pay=self.bill_amount-self.total_savings
        self.lbl_amount.config(text=f"Bill Amount \nRs \n[{str(self.bill_amount)}]")
        self.lbl_discount.config(text=f"Tot. Dis. \nRs \n[{str(self.total_savings)}]")
        self.lbl_netpay.config(text=f"Net Pay \nRs \n[{str(self.net_pay)}]")
        self.cart_title.config(text=f"Cart\t  Total Product(s): [{str(self.prod)}]")
    #==================================================

    #==========generate bill==========================
    def generate_bill(self):
        if self.var_cust_name.get()=="" or self.var_cust_contact.get()=="":
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please ADD products to the cart", parent=self.root)
        else:
            ask=messagebox.askyesno("Confirm","Are you sure?",parent=self.root)
            if ask==True:
                #=======bill top==========
                self.bill_top()
                #=======bill middle==========
                self.bill_middle()
                #=======bill bottom==========
                self.bill_bottom()

                #=======to save bill in backend=====
                cust_first_name = str(self.var_cust_name.get().split(" ")[0])
                file_name=str(self.invoice_no) + '_' + cust_first_name+".txt"
                file_path="bills/"+file_name
                self.create_bill_content(file_path)

                # fp=open(f"bills/{file_name}.txt",'w')
                # fp.write(self.txt_bill_area.get('1.0',END))
                # fp.close()
                    #========backup file========
                backup_path="D:/DwivediPipesNTilesBackup/bills_backup/"
                backup_file=os.path.join(backup_path,file_name)
                self.create_bill_content(backup_file)
                # fp1 = open(f"bills/{file_name}.txt", 'w')
                # fp1.write(self.txt_bill_area.get('1.0', END))
                # fp1.close()
                self.chk_print=1
                messagebox.showinfo("Saved","Bill has been generated/Saved",parent=self.root)

    def create_bill_content(self,fpath_name):
        fp=open(fpath_name,'w')
        fp.write(self.txt_bill_area.get('1.0',END))
        fp.close()


    def bill_top(self):
        self.invoice_no=str(time.strftime("%d_%m_%y_"))+str(time.strftime("%H%M%S"))
        # print(self.invoice_no)
        #===in triple quote f string type in the exact layout that you want
        bill_top_temp=f'''          
\tDWIVEDI PIPES N TILES
\tPhone No. 9437120730
At-BTM Colony, Infront of HP Petrol Pump
{str("="*55)}
Customer Name: {self.var_cust_name.get()}
Cutomer Contact: {self.var_cust_contact.get()}
Bill No.:{self.invoice_no}\t\t\tDate:{str(time.strftime("%d/%m/%y"))}
{str("="*55)}
Product\t\tQty\tPrice\tDiscount\tAmount\tSavings
{str("="*55)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                #print(row)
                pname=row[1]
                rate=str(float(row[2]))
                quantity=str(float(row[3]))
                discount=str(float(row[4]))
                amount=str(float(row[5]))
                savings=str(float(row[6]))
                self.txt_bill_area.insert(END,"\n"+pname+"\t\t"+quantity+"\t"+rate+"\t"+discount+"\t\t"+amount+"\t"+savings)
                #====updating the quantity of products=====
                p_id=row[0]
                st=cur.execute("SELECT quantity FROM products WHERE pid=?",p_id).fetchone()
                #print(st[0]) #st will be a tuple of strings in the form ('34',)
                stock=int(st[0])
                status="Active"
                if stock==int(row[3]):
                    status="Inactive"
                qty=stock-int(row[3])
                cur.execute("UPDATE products SET quantity=?,status=? WHERE pid=?",(qty,status,p_id))
                con.commit()
            con.close()
            self.show()
            self.clear_product_details()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*55)}
Total Number of Products:\t\t{self.prod}
Bill Amount:\t\t\tRs.{self.bill_amount}
Total Savings:\t\t\tRs.{self.total_savings}
Net Pay:\t\t\tRs.{self.net_pay}
{str("="*55)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_all(self):
        ask=messagebox.askyesno("Confirm","Do you really want to clear all?",parent=self.root)
        if ask==True:
            del self.cart_list[:]
            self.var_cust_contact.set("")
            self.var_cust_name.set("")
            self.var_calculator_entry.set("")
            self.txt_bill_area.delete('1.0',END)
            self.clear_product_details()
            self.cart_title.config(text="Cart\t  Total Product(s): [0]")
            self.show()
            self.show_cart()
            self.chk_print=0

    def update_date_time(self):
        tm=time.strftime("%I:%M:%S")    #%I is for indian format of time %H is for 24 hour format
        dt=time.strftime("%d-%m-%Y")    #%D will fetch the whole date as DD/MM/YY so we use %d
        self.lbl_clock.config(text=f"Welcome to Billing system\t\t  Date: {str(dt)}\t\t Time: {str(tm)}")
        #to call the function repeatedly to show date and time in realtime
        self.lbl_clock.after(200,self.update_date_time)

##############################
    #==========printing bill=============
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing!",parent=self.root)
            new_print_file = tempfile.mktemp('.txt')  # to make temporary file
            open(new_print_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_print_file, 'print')   #printing
            self.chk_print=2
        elif self.chk_print==0:
            messagebox.showinfo("Print", "Please generate bill to print the receipt!", parent=self.root)
        else:
            ask=messagebox.askyesno("Print", "Receipt already printed.\nDo want to print again?", parent=self.root)
            if ask==True:
                self.chk_print=1
                self.print_bill()

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":        #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= BillingClass(root)     #creating object of Billing Class
    root.mainloop()             #so that the window stays until we manually exit