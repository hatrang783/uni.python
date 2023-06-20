from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import os

##### Class
class Employee():
    def __init__(self, Id, name, dob, gender, phone, address, email, doj, department, designation, salary):
        self.Id = Id
        self.name = name
        self.dob = dob 
        self.gender = gender
        self.phone = str(phone)
        self.address = address
        self.email = email
        self.doj = doj
        self.department = department
        self.designation = designation
        self.salary = salary
    def update(self, name, dob, gender, phone, address, email, doj, department, designation, salary):
        self.name = name
        self.dob = dob 
        self.gender = gender
        self.phone = phone
        self.address = address
        self.email = email
        self.doj = doj
        self.department = department
        self.designation = designation
        self.salary = salary
        
class Form:
    def __init__(self,parent,typee,label, column,row):
        self.frame = Frame(parent,bg="#a6a6a6")
        self.frame.grid(column=column,row=row)
        self.lb = Label(self.frame,text=label, width=10,bg="#a6a6a6",fg="black",anchor=W, font=('Arial', 10, 'bold'))
        self.lb.grid(column=1,row=1)
        self.var = StringVar()
        if typee == "Entry":
            self.et = Entry(self.frame,textvariable = self.var,width=30,bg="#333333",fg='white')
            self.et.grid(column=2, row=1,padx=(0,10))
        elif typee == "ComboBox":
            self.ccb = ttk.Combobox(self.frame, textvariable = self.var,width=27)
            self.ccb.grid(column=2, row=1,padx=(0,10))
        
    def set_lb_atb(self,**atb):
        self.lb.config(**atb)
        
    def set_et_atb(self, **atb):
        self.et.config(**atb)
        
    def set_ccb_atb(self, **atb):
        self.ccb.config(**atb)

##### Loading data
# x = os.path.dirname(os.path.abspath(__file__))
# file = open(x+"/employee.csv","r",encoding="UTF-8")
file = open("C:/Users/HUONG GIANG/Desktop/UNI/Python/FINAL/final2/employee.csv","r",encoding="UTF-8")
heading = file.readline()
data = file.readlines()
file.close()

total = 0

Data = {}
for i in data:
    i = i.strip().split(",")
    # i[2] = ""
    Data[i[0]] = Employee(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])
    total += 1

##### Functions
def login():
    if sv_login.get() == "1234":
        fr_login.pack_forget()
        fr_main.pack()
    else:
        messagebox.showwarning("Fail", "Wrong password")
        
def save():
    global total
    if check_valid():
        Id = generate_id()
        Data[Id] = Employee(Id,D_form["Name"].var.get(), D_form["Dob"].var.get(),
                            D_form["Gender"].var.get(), D_form["Phone"].var.get(), 
                            D_form["Address"].var.get(), D_form["Email"].var.get(),
                            D_form["Doj"].var.get(), D_form["Department"].var.get(), 
                            D_form["Designation"].var.get(), D_form["Salary"].var.get())
        total += 1
        clear_display()
        tv_display.insert("", 'end', text='L1',
                 values = T_info(Data[Id]))
        count_config(1,total)
    else:
        messagebox.showwarning("Fail", "All value must be fill in")
       
    
def update():
    global selected_id
    if selected_id in Data:
        Data[selected_id].update(D_form["Name"].var.get(), D_form["Dob"].var.get(), 
                                D_form["Gender"].var.get(), D_form["Phone"].var.get(), 
                                D_form["Address"].var.get(), D_form["Email"].var.get(),
                                D_form["Doj"].var.get(), D_form["Department"].var.get(), 
                                D_form["Designation"].var.get(), D_form["Salary"].var.get())
        clear_display()
        reset()
        tv_display.insert("", 'end', text='L1',
                 values = T_info(Data[selected_id]))
        count_config(1,total)
        selected_id = 0
    
def delete():
    global selected, selected_id, total, l
    if selected_id in Data:
        tv_display.delete(selected)
        Data.pop(selected_id)
        reset()
        total -= 1
        l -= 1
        count_config(l, total)
        selected_id = 0

def reset():
    for i in L:
        for j in i:
            D_form[j].var.set("")

def search():
    global l
    clear_display()
    l = 1
    for i in Data:
        if sv_searchby.get() == "ID":
            compare = sv_search.get() in i
        elif sv_searchby.get()  == "Name":
            compare = sv_search.get().lower() in Data[i].name.lower()
        elif sv_searchby.get() == "Department":
            compare = sv_search.get().lower() in Data[i].department.lower()
            
        if compare:
                tv_display.insert("", 'end', text=f'L{l}',
                                  values =T_info(Data[i]))
                compare = False
                l+=1
    l -= 1
    count_config(l, total)
        

def showAll():
    global l
    clear_display()
    l = 1
    for i in Data:
        tv_display.insert("", 'end', text=f'L{l}',
             values =T_info(Data[i]))
        l+=1
    l -= 1
    count_config(l,total)
    
def item_selected(event):
    global selected
    selected = tv_display.focus()
    values = tv_display.item(selected)['values']
    global selected_id 
    selected_id = str(values[0])
    values[4] = "0"+str(values[4])
    for i in range(1,len(values)):
        D_form[L_heading[i]].var.set(values[i])
        
def clear_display():
    for item in tv_display.get_children():
        tv_display.delete(item)
    count_config(0,total)
        
def generate_id():
    now = datetime.datetime.now()
    now = str(now)
    Id = now[2:4]+now[5:7]+now[8:10]+now[11:13]+now[14:16]+now[17:19]
    return Id


def on_closing():
    if messagebox.askokcancel("Save", "Do you want to save?"):
        save_data()
    sc.destroy()
        
def save_data():
    f = open("employee.csv", "w",encoding="UTF-8")
    f.write("id,name,dob,gender,phone,address,email,doj,department,designation,salary\n")
    for i in Data:
        f.write(Data[i].Id+","+Data[i].name+","+Data[i].dob+","+Data[i].gender+","+Data[i].phone+","
                +Data[i].address+","+Data[i].email+","+Data[i].doj+","+Data[i].department+","
                +Data[i].designation+","+Data[i].salary+"\n")
    f.close()

def T_info(i):
    T = (i.Id, i.name, i.dob, i.gender, i.phone, i.address, i.email, i.doj, i.department, i.designation, i.salary)
    return T

def count_config(l,t):
    lb_count.config(text=f"Total: {l}/{t}")
    
def check_valid():
    for i in L:
        for j in i:
            if D_form[j].var.get() == "":
                return False
    return True

##### GUI    
sc = Tk()
sc.title("Employee Management")

style= ttk.Style()
style.theme_use('default')
style.configure("TCombobox", fieldbackground= "#333333", background= "#333333",foreground="white")

sc.config(bg="#595959")

selected_id = selected = l = 0
sv_login = StringVar()
sv_searchby = StringVar()
sv_search = StringVar()

lb_title = Label(sc, text="EMPLOYEE MANAGEMENT SYSTEM", font=('Arial', 20, 'bold'), fg="white", bg="#595959")
lb_title.pack(padx=30,pady=(20,10))
        
##################################################################
# Login Frame
fr_login = Frame(sc,bg="#595959")

et_login = Entry(fr_login,show="*", textvariable=sv_login, font=('Arial', 15),bg="#333333",fg="white")
et_login.pack(pady=(0,10))
et_login.focus()

bt_login = Button(fr_login, text="LOG-IN", command=login, font=("Arial",15,"bold"),bg="#1a1a1a",fg="#4db8ff")
bt_login.pack(ipadx=30)

fr_login.pack(pady=30)

###################################################################
# Main Frame
fr_main = Frame(sc,bg="#595959")

## Insert Frame  
fr_pr_insert = Frame(fr_main, bg="#a6a6a6", relief="groove")

fr_pr_insert.pack()

fr_insert = Frame(fr_pr_insert, bg="#a6a6a6")

fr_insert.pack(pady=20,padx=20)

L = [["Name", "Dob", "Gender", "Phone", "Address",],
     ["Email","Doj", "Department", "Designation", "Salary"],
    ]

D_form = {}

for i in range(len(L)):
    for j in range(len(L[i])):
        if L[i][j] == "Gender":
            D_form[L[i][j]] = Form(fr_insert,"ComboBox", L[i][j],i, j+1)
            D_form[L[i][j]].set_ccb_atb(values=['Male', 'Female'])
            continue
        elif L[i][j] == "Department":
            D_form[L[i][j]] = Form(fr_insert,"ComboBox",L[i][j], i, j+1)
            D_form[L[i][j]].set_ccb_atb(values=['HR', 'IT', 'Marketing'])
            continue
        D_form[L[i][j]] = Form(fr_insert,"Entry", L[i][j],i, j+1)
       
    
### Menu Frame
fr_menu = Frame(fr_insert, bg="#a6a6a6")

bt_save = Button(fr_menu, text="SAVE", font=("Arial",10,"bold"),command=save, width=12,bg="#1a1a1a",fg="#4db8ff")
bt_save.grid(column=1, row=1,pady=5)

bt_update = Button(fr_menu, text="UPDATE", font=("Arial",10,"bold"), command=update, width=12,bg="#1a1a1a",fg="#4db8ff")
bt_update.grid(column=1, row=2,pady=5)

bt_delete = Button(fr_menu, text="DELETE", font=("Arial",10,"bold"), command=delete, width=12,bg="#1a1a1a",fg="#4db8ff")
bt_delete.grid(column=1, row=3,pady=5)

bt_reset = Button(fr_menu, text="RESET", font=("Arial",10,"bold"), command=reset, width=12,bg="#1a1a1a",fg="#4db8ff")
bt_reset.grid(column=1, row=4,pady=5)

fr_menu.grid(column=2, row=0, rowspan=6,padx=(20,0))

## Search Frame
fr_search = Frame(fr_main,bg="#595959")

lb_search = Label(fr_search, text="SEARCH BY:", font=("Arial",12,"bold"),bg="#595959",fg="white")
lb_search.grid(column=0, row=0)

opt = ['ID', 'Name', 'Department']
ccb_search = ttk.Combobox(fr_search, values = opt, textvariable=sv_searchby, font=("Arial",12))
ccb_search.grid(column=1, row=0,padx=10)

et_search = Entry(fr_search, textvariable=sv_search, font=("Arial",12),bg="#333333",fg="white")
et_search.grid(column=2, row=0,padx=10)

bt_search = Button(fr_search, text="SEARCH", command=search, width=10,bg="#4db8ff",fg="#1a1a1a", font=("Arial",12,"bold"))
bt_search.grid(column=3, row=0,padx=10)

bt_showAll = Button(fr_search, text="SHOW ALL", command=showAll, width=10,bg="#4db8ff",fg="#1a1a1a", font=("Arial",12,"bold"))
bt_showAll.grid(column=4, row=0,padx=10)

fr_search.pack(pady=10)

## Display Frame
fr_display = Frame(fr_main,bg="#595959")

lb_count = Label(fr_display, text=f"Count:0/{total}", font=("Arial",12,"bold"), bg="#595959",fg="white")
lb_count.pack()

tv_display = ttk.Treeview(fr_display, selectmode="browse", show='headings')
tv_display.bind('<ButtonRelease-1>', item_selected)
tv_display.pack(padx=20,pady=20)

tv_display['columns'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9','10','11')
L_heading = ["ID", "Name", "Dob", "Gender", "Phone", "Address", "Email","Doj", "Department", "Designation", "Salary"]


for i in range(len(tv_display['columns'])):
    tv_display.column(tv_display['columns'][i], width=100, anchor='center')
    tv_display.heading(tv_display['columns'][i], text =L_heading[i])

fr_display.pack()

## Quit

sc.protocol("WM_DELETE_WINDOW", on_closing)

#########################################################################   
sc.mainloop()