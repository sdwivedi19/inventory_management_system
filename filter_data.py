from tkinter import *
import sqlite3
from tkinter import ttk,messagebox

class FilterData:
    def __init__(self,root):
        self.root=root
        self.root.title("Filter Data Automatically")
        self.root.geometry("800x500+100+100")
        self.root.config(bg="white")

        title=Label(self.root,text="Filter Data Automatically While Typing in Python",bg="white")
        footer=Label(self.root,text="Developed by Sudhansu")

        #=====search panel=====
        self.var_search=StringVar()
        lbl_search_roll=Label(self.root,text="Search by Name",font=("goudy old style",20,"bold"),bg="white").place(x=50,y=50)
        txt_search_roll=Entry(self.root,textvariable=self.var_search,font=("goudy old style",20,"bold"),bg="lightyellow")
        txt_search_roll.place(x=250,y=55,width=200,height=30)
        txt_search_roll.bind("<Key>",self.search)
        btn_search=Button(self.root,text="Search",font=("goudy old style",15,"bold"),bg="#03a9f4",fg="white",cursor="hand2").place(x=500,y=55,width=100,height=30)



        #======content=======
        self.C_Frame=Frame(self.root,bd=5,relief=RIDGE)
        self.C_Frame.place(x=100,y=100,width=600,height=350)

        scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
        scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
        self.studentTable=ttk.Treeview(self.C_Frame,columns=("roll","name","email","gender"))

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.studentTable.xview)
        scrolly.config(command=self.studentTable.yview)

        self.studentTable.heading("roll",text="ROLL NO.")
        self.studentTable.heading("name", text="NAME")
        self.studentTable.heading("email", text="E-MAIL")
        self.studentTable.heading("gender", text="GENDER")

        self.studentTable["show"]="headings"

        self.studentTable.column("roll", width=100)
        self.studentTable.column("name", width=100)
        self.studentTable.column("email", width=100)
        self.studentTable.column("gender", width=100)

        self.studentTable.pack(fill=BOTH,expand=1)
        #self.studentTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

#==========================================
    #dummy entries into database
    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        cur.execute("Select * from student where roll=1002")
        row=cur.fetchone()
        count=110
        for i in range(20):
            cur.execute("insert into student(roll,name,email,gender)" Values count, row[1]+ " "+str(count),row[2],row[3],row[4]))
            con.commit()
            count+=1

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from student")
            rows=cur.fetchall()
            self.studentTable.delete(*self.studentTable.get_children())
            for row in rows:
                self.studentTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def search(self,ev):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student where name LIKE '%"+self.var_search.get()+"%'")
            row=cur.fetchall()
            #print(row)
            if len(row)>0:
                self.studentTable.delete(*self.studentTable.get_children())
                for i in row:
                    self.studentTable.insert("",END,values=i)
            else:
                self.studentTable.delete(*self.studentTable.get_children())
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


root=Tk()
obj=FilterData(root)
root.mainloop()




