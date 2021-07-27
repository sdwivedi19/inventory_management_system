from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox #messagebox for pop up
import sqlite3
import os                          #for working with files and directories

class salesClass:
    def __init__(self, root):  # default constructor
        self.root = root
        self.root.geometry("1000x450+220+120")
        self.root.title("Sales")
        self.root.config(bg="white")
        self.root.focus_force() # to highlight the new window

##=============title===========
        lbl_title = Label(self.root, text="View Customer Bills", font=("goudy old style", 30), bg="#0f4d7d", fg="white", bd=3,relief=RIDGE)
        lbl_title.pack(side=TOP,fill=X,padx=20,pady=5)

##=============contents=====================
    #======content variables================
        self.var_invoice=StringVar()
        self.bill_list=[]

    #======content labels and entries=======
        #===row1===
        lbl_invoice=Label(self.root, text="Invoice No.", font=("goudy old style", 15), bg="white")
        lbl_invoice.place(x=20,y=70)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice,font=("goudy old style", 15), bg="lightyellow")
        txt_invoice.place(x=150, y=70,width=180,height=30)
        btn_search = Button(self.root, text="Search", command=self.search,font=("goudy old style", 15,"bold"), bg="#2196f3",fg="white",cursor="hand2")
        btn_search.place(x=350, y=70, width=150, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear,font=("goudy old style", 15,"bold"), bg="lightgrey",cursor="hand2")
        btn_clear.place(x=520, y=70, width=150, height=30)
        #===sales bill frame===
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=20,y=120,width=220,relheight=0.7)
            #===Listbox to show files===
                #===scrollbar in listbox===
        scrolly1 = Scrollbar(sales_Frame, orient=VERTICAL)
        scrolly1.pack(side=RIGHT, fill=Y)
        scrollx1 = Scrollbar(sales_Frame, orient=HORIZONTAL)
        scrollx1.pack(side=BOTTOM, fill=X)
                #===Listbox===
        self.sales_list=Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly1.set, xscrollcommand=scrollx1.set)
        self.sales_list.pack(fill=BOTH,expand=1)       #fill=BOTH to fill the whole frame, expand=1 means expand property is True
        scrolly1.config(command=self.sales_list.yview)
        scrollx1.config(command=self.sales_list.xview)  # to make the scroll bar work

        #to show the content of bill file in the "Bill Area Frame"
        self.sales_list.bind("<ButtonRelease-1>",self.get_bill_data)        #This is an event

        #to show the list of bills in the "Sales bill frame"
        self.show_bill()

        #===bill area frame===
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=120, width=410, relheight=0.7)
            #===Text area to show files===
                # ===Bill Area title===
        lbl_billarea_title = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 15), bg="orange")
        lbl_billarea_title.pack(side=TOP, fill=X)
                #===scrollbar in bill area===
        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrollx2 = Scrollbar(bill_Frame, orient=HORIZONTAL)
        scrollx2.pack(side=BOTTOM, fill=X)
                #===Bill Area text===
        self.bill_area = Text(bill_Frame, font=("goudy old style", 15), bg="lightyellow", yscrollcommand=scrolly2.set,xscrollcommand=scrollx2.set)
        self.bill_area.pack(fill=BOTH,expand=1)         #fill=BOTH to fill the whole frame, expand=1 means expand property is True
        scrolly2.config(command=self.bill_area.yview)
        scrollx2.config(command=self.bill_area.xview)  #to make the scroll bar work

        #=====Image====
            #===accessing the image and resizing===
        self.bill_Photo = Image.open("images/im2.png")
        self.bill_Photo = self.bill_Photo.resize((250, 300), Image.ANTIALIAS)  #ANTIALIAS doesn't change picture quality
        self.bill_Photo = ImageTk.PhotoImage(self.bill_Photo)                  #Image is dynamically placed
            #===placing the image===
        lbl_bill_Photo = Label(self.root, image=self.bill_Photo,bd=0)
        lbl_bill_Photo.place(x=730,y=130)

##============ Functionality =============
    #to show the list of bills in the bills directory
    def show_bill(self):
        del self.bill_list[:]                             #to clear the list
        self.sales_list.delete(0,END)
        #print(os.listdir("../dwivediPnTbilling/bills"))  #the path can also be given as "../dwivediPnTbilling/"
        for i in os.listdir("bills"):
            if i.split(".")[-1]=="txt": #to get and compare the file extension
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    #to show the contents of the bill file in the bill area
    def get_bill_data(self,ev):                      #For event we have to pass a parameter
        file_index=self.sales_list.curselection() #curselection helps to show the index of the selected item from the list
        bill_file_name=self.sales_list.get(file_index)
        #print(bill_file_name)
        self.bill_area.delete('1.0',END)        #string indexing starts from 1.0 because it is text entry field
        fp=open(f"bills/{bill_file_name}",'r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    #to show the search results
    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
            #print(self.bill_list,self.var_invoice.get()) #debugging
            if self.var_invoice.get() in self.bill_list:
                #print("Yes find the invoice")            #debugging
                fp = open(f"bills/{self.var_invoice.get()}.txt", 'r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error", "Invalid Invoice no.", parent=self.root)

    #to clear the list
    def clear(self):
        self.show_bill()                     #so that the list of bills doesn't vanish
        self.bill_area.delete("1.0",END)
        self.var_invoice.set("")


if __name__=="__main__": #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= salesClass(root) #creating object of Billing Class
    root.mainloop()