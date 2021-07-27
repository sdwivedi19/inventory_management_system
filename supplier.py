from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox #messagebox for pop up
import sqlite3

class supplierClass:
    def __init__(self, root):  # default constructor
        self.root = root
        self.root.geometry("1000x450+220+120")
        self.root.title("Supplier")
        self.root.config(bg="white")
        self.root.focus_force() # to highlight the new window
        #=============
        #All Variables====
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()


        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()

        #=====search frame======
        SearchFrame=LabelFrame(self.root, text="Search Supplier",font=("goudy old style",15,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=410,y=60,relwidth=0.58,height=70)

        #===options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Invoice","Name","Contact","Description"),state="readonly",justify=CENTER,font=("goudy old style",15)) #state is used so that the user can not write in the search bar
        cmb_search.place(x=10,y=4,width=150,height=30)
        cmb_search.current(0) #to set select as default value in search bar

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=190,y=4,width=250,height=30)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=470,y=3,width=100,height=30)

        #==title====
        title=Label(self.root,text="Supplier details",font=("goudy old style",30),bg="#0f4d7d",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=20,pady=5) #without anchor, the text will be automatically at center

    #====content====
        #===row1=======
        lbl_sup_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=20,y=60)
        txt_sup_invoice=Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=130, y=60, width=200)
        #===row2====
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=20, y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15),bg="lightyellow").place(x=130, y=100, width=200)
        # ===row3====
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=20, y=140)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=130, y=140, width=200)
        # ===row4====
        lbl_address = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=20, y=180)
        self.txt_desc=Text(self.root, font=("goudy old style", 15), bg="lightyellow") #Text for multiple line input
        self.txt_desc.place(x=130, y=180, width=270, height=130)
        #===row5 buttons====
        btn_save=Button(self.root,text="Save",command=self.save,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=20,y=320,width=80,height=25)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=120,y=320,width=80,height=25)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=220,y=320,width=80,height=25)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=320,y=320,width=80,height=25)

        #====Tree view to show results=====

        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=410,y=150,relwidth=0.58,height=290)

        scrolly = Scrollbar(sup_frame, orient=VERTICAL)
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(sup_frame, columns=("invoice", "name", "contact", "description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview) # to make the scroll bar work
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text="INVOICE NO.")
        self.SupplierTable.heading("name", text="NAME")
        self.SupplierTable.heading("contact", text="CONTACT")
        self.SupplierTable.heading("description", text="DESCRIPTION")
        self.SupplierTable["show"]= "headings" #to hide the default heading that was blank

        self.SupplierTable.column("invoice", width=70)
        self.SupplierTable.column("name", width=120)
        self.SupplierTable.column("contact", width=100)
        self.SupplierTable.column("description", width=100)
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data) #event

        self.show()
#=====database functionality==========================================
    #======save button======
        #====to save data in database=====
    def save(self): # we are passing self because we have defined all our variables with self and used self in all our widgets
        con=sqlite3.connect(database=r'pntb.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()== "":
                messagebox.showerror("Error","Invoice no. must be required", parent=self.root)#parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),)) #comma is required at last since we are passing tuple
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice no. already assigned, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier(invoice,name,contact,description) VALUES(?,?,?,?)",(
                                self.var_sup_invoice.get(),
                                self.var_name.get(),
                                self.var_contact.get(),
                                self.txt_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

        #===to show data in tree view===
    def show(self): # we are passing self because we have defined all our variables with self and used self in all our widgets
        con=sqlite3.connect(database=r'pntb.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
        #=====to reflect data in the fields===
    def get_data(self,ev):
        f=self.SupplierTable.focus() #to focus on the selected item
        content=(self.SupplierTable.item(f)) #making the content tuple
        row=content['values'] #filtering the values and assigning to row
        #print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

    #======update button======
    def update(self):  # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice no. is required",parent=self.root)  # parent defines whose messagebox it is
            else:
                ask = messagebox.askyesno("Confirm", "Do you really want to update?", parent=self.root)
                if ask == True:
                    cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))  # comma is required at last since we are passing tuple
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "Invalid Invoice no.!", parent=self.root)
                    else:
                        cur.execute(
                            "UPDATE supplier SET name=?,contact=?,description=? WHERE invoice=?",(
                                self.var_name.get(),
                                self.var_contact.get(),
                                self.txt_desc.get('1.0', END),
                                self.var_sup_invoice.get(),
                            ))
                        con.commit()
                        messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    #======delete button=====
    def delete(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required",parent=self.root)  # parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))  # comma is required at last since we are passing tuple
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    ask=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if ask==True:
                        cur.execute('DELETE FROM supplier WHERE invoice=?', (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        #self.show() #this is already called in the clear function
                        self.clear() # so that the entries are blank after deleting
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    #=====clear button======
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    #====search button=====
    def search(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error", "Search Input is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'") #mind spaces, or else it wll throw exception
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    for row in rows:
                        self.SupplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__=="__main__": #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= supplierClass(root) #creating object of Billing Class
    root.mainloop()