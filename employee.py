from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox #messagebox for pop up
import sqlite3

class employeeClass:
    def __init__(self, root):  # default constructor
        self.root = root
        self.root.geometry("1000x450+220+120")
        self.root.title("Employee")
        self.root.config(bg="white")
        self.root.focus_force() # to highlight the new window
        #=============
        #All Variables====
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()


        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()

        self.var_salary=StringVar()

        #=====search frame======
        SearchFrame=LabelFrame(self.root, text="Search Employee",font=("goudy old style",15,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=220,y=5,width=625,height=70)

        #===options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Contact"),state="readonly",justify=CENTER,font=("goudy old style",15)) #state is used so that the user can not write in the search bar
        cmb_search.place(x=10,y=4,width=180,height=30)
        cmb_search.current(0) #to set select as default value in search bar

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=220,y=4,width=180,height=30)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=430,y=3,width=180,height=30)

        #==title====
        title=Label(self.root,text="Employee details",font=("goudy old style",15),bg="#0f4d7d",fg="white",bd=3,relief=RIDGE).place(x=50,y=80,width=900) #without anchor, the text will be automatically at center

    #====content====
        #===row1=======
        lbl_empid=Label(self.root,text="Emp ID",font=("goudy old style",15),bg="white").place(x=50,y=110)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15),bg="white").place(x=350,y=110)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=675,y=110)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=110, width=150)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,values=("Select", "Male", "Female", "Other"), state="readonly", justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=450, y=110,width=150)
        cmb_gender.current(0)
        txt_contact = Entry(self.root,textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=775, y=110,width=150) #Entry for single line input

        #===row2====
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_dob = Label(self.root, text="D.O.B.", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        lbl_doj = Label(self.root, text="D.O.J.", font=("goudy old style", 15), bg="white").place(x=675, y=150)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15),bg="lightyellow").place(x=150, y=150, width=150)
        txt_dob = Entry(self.root,textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=450, y=150, width=150)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15),bg="lightyellow").place(x=775, y=150, width=150)

        # ===row3====
        lbl_email = Label(self.root, text="E-mail", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=675, y=190)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190, width=150)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow").place(x=450, y=190, width=150)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"),state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=775, y=190, width=150)
        cmb_utype.current(0)

        # ===row4====
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place(x=500, y=230)

        self.txt_address=Text(self.root, font=("goudy old style", 15), bg="lightyellow") #Text for multiple line input
        self.txt_address.place(x=150, y=230, width=300, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow").place(x=600, y=230, width=150)

        #===row5 buttons====
        btn_save=Button(self.root,text="Save",command=self.save,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=500,y=270,width=80,height=25)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=600,y=270,width=80,height=25)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=700,y=270,width=80,height=25)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=800,y=270,width=80,height=25)

        #====Tree view to show results=====

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=310,relwidth=1,height=140)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview) # to make the scroll bar work
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name", text="NAME")
        self.EmployeeTable.heading("email", text="E-MAIL")
        self.EmployeeTable.heading("gender", text="GENDER")
        self.EmployeeTable.heading("contact", text="CONTACT")
        self.EmployeeTable.heading("dob",text="D.O.B.")
        self.EmployeeTable.heading("doj", text="D.O.J.")
        self.EmployeeTable.heading("pass", text="PASSWORD")
        self.EmployeeTable.heading("utype", text="USER TYPE")
        self.EmployeeTable.heading("address", text="ADDRESS")
        self.EmployeeTable.heading("salary",text="SALARY")

        self.EmployeeTable["show"]="headings" #to hide the default heading that was blank

        self.EmployeeTable.column("eid",width=70)
        self.EmployeeTable.column("name",width=120)
        self.EmployeeTable.column("email",width=120)
        self.EmployeeTable.column("gender",width=70)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=70)
        self.EmployeeTable.column("address",width=150)
        self.EmployeeTable.column("salary",width=70)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data) #event

        self.show()
#=====database functionality==========================================
    #======save button======
        #====to save data in database=====
    def save(self): # we are passing self because we have defined all our variables with self and used self in all our widgets
        con=sqlite3.connect(database=r'pntb.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required", parent=self.root)#parent defines whose messagebox it is
            elif self.var_name.get()=="":
                messagebox.showerror("Error","Employee Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?",(self.var_emp_id.get(),)) #comma is required at last since we are passing tuple
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(
                                self.var_emp_id.get(),
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_doj.get(),
                                self.var_pass.get(),
                                self.var_utype.get(),
                                self.txt_address.get('1.0',END),
                                self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

        #===to show data in tree view===
    def show(self): # we are passing self because we have defined all our variables with self and used self in all our widgets
        con=sqlite3.connect(database=r'pntb.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
        #=====to reflect data in the fields===
    def get_data(self,ev):
        f=self.EmployeeTable.focus() #to focus on the selected item
        content=(self.EmployeeTable.item(f)) #making the content tuple
        row=content['values'] #filtering the values and ssigning to row
        #print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    #======updat button======
    def update(self):  # we are passing self because we have defined all our variables with self and used self in all our widgets
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required",parent=self.root)  # parent defines whose messagebox it is
            else:
                ask = messagebox.askyesno("Confirm", "Do you really want to update?", parent=self.root)
                if ask == True:
                    cur.execute("SELECT * FROM employee WHERE eid=?",(self.var_emp_id.get(),))  # comma is required at last since we are passing tuple
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                    else:
                        cur.execute(
                            "UPDATE employee SET name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? WHERE eid=?",
                            (

                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_doj.get(),
                                self.var_pass.get(),
                                self.var_utype.get(),
                                self.txt_address.get('1.0', END),
                                self.var_salary.get(),
                                self.var_emp_id.get(),
                            ))
                        con.commit()
                        self.show()
                        messagebox.showinfo("Success", "Employee updated successfully", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    #======delete button=====
    def delete(self):
        con = sqlite3.connect(database=r'pntb.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required",parent=self.root)  # parent defines whose messagebox it is
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?",(self.var_emp_id.get(),))  # comma is required at last since we are passing tuple
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    ask=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if ask==True:
                        cur.execute('DELETE FROM employee WHERE eid=?',(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        #self.show() #this is already called in the clear function
                        self.clear() # so that the entries are blank after deleting
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    #=====clear button======
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
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
                cur.execute("SELECT * FROM employee WHERE "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'") #mind spaces, or else it wll throw exception
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__=="__main__": #while dealing with multiple files "main" means this is the main file
    root=Tk()
    obj= employeeClass(root) #creating object of Billing Class
    root.mainloop()