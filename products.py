from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox #messagebox for pop up
import sqlite3

class productClass:
    def __init__(self, root):  # default constructor
        self.root = root
        self.root.geometry("1000x450+220+120")
        self.root.title("Product")
        self.root.config(bg="white")
        self.root.focus_force() # to highlight the new window

##============== Product Frame=======

        prod_Frame=Frame(self.root,bd=2,bg="white",relief=RIDGE)
        prod_Frame.place(x=10,y=10,width=450,height=430)
    #==============Product Frame title====
        title = Label(prod_Frame, text="Manage Product details", font=("goudy old style", 18), bg="#0f4d7d", fg="white", bd=3,relief=RIDGE)
        title.pack(side=TOP,fill=X)
    #==============Product Frame contents=============
        #=========labels=======
        lbl_category = Label(prod_Frame, text="Category", font=("goudy old style", 18), bg="white")
        lbl_category.place(x=30,y=60)
        lbl_supplier = Label(prod_Frame, text="Supplier", font=("goudy old style", 18), bg="white")
        lbl_supplier.place(x=30, y=110)
        lbl_prod_name = Label(prod_Frame, text="Product", font=("goudy old style", 18), bg="white")
        lbl_prod_name.place(x=30, y=160)
        lbl_price = Label(prod_Frame, text="Price", font=("goudy old style", 18), bg="white")
        lbl_price.place(x=30, y=210)
        lbl_quantity = Label(prod_Frame, text="Quantity", font=("goudy old style", 18), bg="white")
        lbl_quantity.place(x=30, y=260)
        lbl_status = Label(prod_Frame, text="Status", font=("goudy old style", 18), bg="white")
        lbl_status.place(x=30, y=310)
        #==========user input=======
            #=======variables========
        self.var_pid=StringVar()
        self.var_category=StringVar()
        self.var_supplier = StringVar()
        self.var_prod_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()

        self.cat_list=[]                    #for fetched data
        self.sup_list=[]                    #for fetched data
        self.fetch_sup_cat()
        # print(self.cat_list)
        # print(self.sup_list)
            #=======entry fields=========
        cmb_category =ttk.Combobox(prod_Frame,textvariable=self.var_category,values=self.cat_list,state="readonly",justify=CENTER,font=("goudy old style",15)) #state is used so that the user can not write in the search bar
        cmb_category.place(x=160,y=60,width=250,height=30)
        cmb_category.current(0) #default value to show

        cmb_supplier = ttk.Combobox(prod_Frame, textvariable=self.var_supplier, values=self.sup_list, state="readonly",justify=CENTER, font=("goudy old style", 15))
        cmb_supplier.place(x=160, y=110, width=250, height=30)
        cmb_supplier.current(0) #default value to show

        txt_prod_name=Entry(prod_Frame, textvariable=self.var_prod_name, font=("goudy old style", 15), bg="lightyellow")
        txt_prod_name.place(x=160, y=160,width=250,height=30)
        txt_price=Entry(prod_Frame, textvariable=self.var_price, font=("goudy old style", 18), bg="lightyellow")
        txt_price.place(x=160, y=210,width=250,height=30)
        txt_quantity=Entry(prod_Frame, textvariable=self.var_quantity, font=("goudy old style", 18), bg="lightyellow")
        txt_quantity.place(x=160, y=260,width=250,height=30)

        cmb_status = ttk.Combobox(prod_Frame, textvariable=self.var_status, values=("Active","Inactive"), state="readonly",justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=160, y=310, width=250, height=30)
        cmb_status.current(0) #default value to show
        #=====buttons======
        btn_save = Button(prod_Frame, text="Save",command=self.save, font=("goudy old style", 15), bg="#4caf50",fg="white", cursor="hand2")
        btn_save.place(x=20, y=370, width=80, height=25)
        btn_update = Button(prod_Frame, text="Update",command=self.update, font=("goudy old style", 15), bg="#2196f3",fg="white", cursor="hand2")
        btn_update.place(x=120, y=370, width=80, height=25)
        btn_delete = Button(prod_Frame, text="Delete",command=self.delete, font=("goudy old style", 15), bg="#f44336",fg="white", cursor="hand2")
        btn_delete.place(x=220, y=370, width=80, height=25)
        btn_clear = Button(prod_Frame, text="Clear",command=self.clear, font=("goudy old style", 15), bg="#607d8b",fg="white", cursor="hand2")
        btn_clear.place(x=320, y=370, width=80, height=25)

#===========Search frame==========
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 15, "bold"), bd=2,relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=500, height=70)
    #===========Search frame contents======
        #=====Search frame variables=======
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        #=====Search frame entry fields=======
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,values=("Select", "Category", "Supplier", "Product"), state="readonly", justify=CENTER,font=("goudy old style",15))  # state is used so that the user can not write in the search bar
        cmb_search.place(x=10, y=4, width=150, height=30)
        cmb_search.current(0)  # to set select as default value in search bar

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),bg="lightyellow")
        txt_search.place(x=170, y=4, width=200, height=30)
        self.btn_search = Button(SearchFrame, text="Search",command=self.search, font=("goudy old style", 15), bg="#4caf50",fg="white", cursor="hand2")
        self.btn_search.place(x=380, y=3, width=110, height=30)


#============Tree view===================
    #======Tree Frame position=======
        prod_tree = Frame(self.root, bd=3, relief=RIDGE)
        prod_tree.place(x=480, y=90, width=500, height=350)
    #======Scroll Bar function=======
        scrolly = Scrollbar(prod_tree, orient=VERTICAL)     #defining vertical scrollbar
        scrolly.pack(side=RIGHT, fill=Y)                    #positioning vertical scrollbar
        scrollx = Scrollbar(prod_tree, orient=HORIZONTAL)   #defining horizontal scrollbar
        scrollx.pack(side=BOTTOM, fill=X)                   #positioning horizontal scrollbar
    #=======Configuring Tree View======
        self.ProductTable = ttk.Treeview(prod_tree, columns=(
            "pid", "product", "category", "supplier", "price",
            "quantity", "status"),yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set)
        scrolly.config(command=self.ProductTable.yview)    #defining function of vertical scrollbar
        scrollx.config(command=self.ProductTable.xview)    #defining function of horizontal scrollbar
    #========Contents of Tree View=========
        self.ProductTable.heading("pid", text="Product Id")
        self.ProductTable.heading("product", text="Product")
        self.ProductTable.heading("category", text="Category")
        self.ProductTable.heading("supplier", text="Supplier")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("quantity", text="Quantity")
        self.ProductTable.heading("status", text="Status")

        self.ProductTable["show"] = "headings"    #to hide the default heading that was blank

        self.ProductTable.column("pid", width=70)
        self.ProductTable.column("product", width=120)
        self.ProductTable.column("category", width=100)
        self.ProductTable.column("supplier", width=100)
        self.ProductTable.column("price", width=70)
        self.ProductTable.column("quantity", width=70)
        self.ProductTable.column("status", width=70)

        self.ProductTable.pack(fill=BOTH, expand=1)

        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)  # event
        self.show()

#=============fetching data from other tables===========
    def fetch_sup_cat(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")  # comma is required at last since we are passing tuple
            cat=cur.fetchall()
            #print(cat) #to check the output
            ##===to get the desired result
            #cat_list=[]
            self.cat_list.append("Empty")
            if len(cat)>0:
                del self.cat_list[:]            #to clear the list
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            #print(self.cat_list)  # to check the output
            cur.execute("SELECT name FROM supplier")  # comma is required at last since we are passing tuple
            sup = cur.fetchall()
            #print(sup) #to check the output
            ##===to get the desired result
            #sup_list = []
            self.sup_list.append("Empty")
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            #print(self.sup_list) #to check the output

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    #=============buttons functionality======
    #===save button=====
        ##====to save data in database=====
    def save(self):  # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_category.get() == "Select" or self.var_category.get() == "Empty"\
                    or self.var_supplier.get() == "Select" or self.var_supplier.get() == "Empty" or self.var_prod_name.get()=="":
                messagebox.showerror("Error", "All fields are required",parent=self.root)  # parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM products WHERE product=?",(self.var_prod_name.get(),))  # comma is required at last since we are passing tuple
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Product already assigned, try different",parent=self.root)
                else:
                    cur.execute("INSERT INTO products(product,category,supplier,price,quantity,status) VALUES(?,?,?,?,?,?)",(
                            self.var_prod_name.get(),
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_price.get(),
                            self.var_quantity.get(),
                            self.var_status.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        ##self.fetch_sup_cat()  # to update the list

        ##===to show data in tree view===
    def show(self):  # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        ##=====to reflect data in the fields===
    def get_data(self, ev):
        f = self.ProductTable.focus()  # to focus on the selected item
        content = (self.ProductTable.item(f))  # making the content tuple
        row = content['values']  # filtering the values and ssigning to row
        # print(row)
        self.var_pid.set(row[0])
        self.var_prod_name.set(row[1])
        self.var_category.set(row[2])
        self.var_supplier.set(row[3])
        self.var_price.set(row[4])
        self.var_quantity.set(row[5])
        self.var_status.set(row[6])


    #====update button======
    def update(self):  # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list!",parent=self.root)  # parent defines whose messagebox it is
            else:
                ask = messagebox.askyesno("Confirm", "Do you really want to update?", parent=self.root)
                if ask == True:
                    cur.execute("SELECT * FROM products WHERE pid=?",(self.var_pid.get(),))  # comma is required at last since we are passing tuple
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "Invalid Product", parent=self.root)
                    else:
                        cur.execute("UPDATE products SET product=?, category=?,"
                                    "supplier=?,price=?,quantity=?,status=? WHERE pid=?",(
                                self.var_prod_name.get(),
                                self.var_category.get(),
                                self.var_supplier.get(),
                                self.var_price.get(),
                                self.var_quantity.get(),
                                self.var_status.get(),
                                self.var_pid.get(),
                            ))
                        con.commit()
                        self.show()
                        messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        ##self.fetch_sup_cat()  # to update the list

    #====delete button=====
    def delete(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product from list!",parent=self.root)  # parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM products WHERE pid=?",(self.var_pid.get(),))  # comma is required at last since we are passing tuple
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product Name", parent=self.root)
                else:
                    ask = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if ask == True:
                        cur.execute('DELETE FROM products WHERE pid=?', (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        # self.show() #this is already called in the clear function
                        self.clear()  # so that the entries are blank after deleting
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        ##self.fetch_sup_cat()          #to update the list

    # =====clear button======
    def clear(self):
        self.var_prod_name.set("")
        self.var_category.set(self.cat_list[0])
        self.var_supplier.set(self.sup_list[0])
        self.var_price.set("")
        self.var_quantity.set("")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
        ##self.fetch_sup_cat()

    # ====search button=====
    def search(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search Input is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM products WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")  # mind spaces, or else it wll throw exception
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        ##self.fetch_sup_cat()  # to update the list




if __name__=="__main__": #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= productClass(root) #creating object of Billing Class
    root.mainloop()