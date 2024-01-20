# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:02:49 2023

@author: Sendil
"""

from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk as ttk1
import mysql.connector as db
from datetime import datetime 
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
global check, name
check=0
check1=0
root=Tk()
root.title('Grocery Shop')
root.geometry('900x700')

def start_page():
    root.title('Grocery Shop')
    frame1=Frame(root,bg="#6F1AB6")
    frame1.place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Welcome to Grocery Shop!")
    label1.place(relx=0.25,rely=0.1,relheight=0.12,relwidth=0.5)
    frame2=Frame(frame1,bg="#9EA1D4")
    frame2.place(relheight=0.5,relwidth=0.8,relx=0.1,rely=0.3)
    button1=Button(frame2,bg="#E5E0FF",text="Sign Up",command=sign_up)
    button1.place(relx=0.3,rely=0.2,relwidth=0.4,relheight=0.2)
    button2=Button(frame2,bg="#E5E0FF",text="Login",command=login_page)
    button2.place(relx=0.3,rely=0.6,relwidth=0.4,relheight=0.2)
    root.mainloop()

def sign_up():
    global entry2,entry3,entry4,entry5,un,name,contact,pd
    root.title('Registration')
    name=StringVar()
    username=StringVar()
    password=StringVar()
    contact=IntVar()
    frame1=Frame(root,bg="#6F1AB6").place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Sign-Up").place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
    low_frame=Frame(frame1,bg="#9EA1D4").place(relwidth=0.8,relheight=0.5,relx=0.1,rely=0.3)
    label2=Label(low_frame,bg="#9EA1D4",text="Name:").place(relx=0.2,rely=0.35,relheight=0.08,relwidth=0.2)
    entry2=Entry(low_frame,textvariable=name)
    entry2.place(relx=0.45,rely=0.35,relheight=0.06,relwidth=0.3)
    label3=Label(low_frame,bg="#9EA1D4",text="Contact:").place(relx=0.2,rely=0.45,relheight=0.08,relwidth=0.2)
    entry3=Entry(low_frame,textvariable=contact)
    entry3.place(relx=0.45,rely=0.45,relheight=0.06,relwidth=0.3)
    label4=Label(low_frame,bg="#9EA1D4",text="Username:").place(relx=0.2,rely=0.55,relheight=0.08,relwidth=0.2)
    entry4=Entry(low_frame,textvariable=username)
    entry4.place(relx=0.45,rely=0.55,relheight=0.06,relwidth=0.3)
    label5=Label(low_frame,bg="#9EA1D4",text="Password:").place(relx=0.2,rely=0.65,relheight=0.08,relwidth=0.2)
    entry5=Entry(low_frame,textvariable=password)
    entry5.place(relx=0.45,rely=0.65,relheight=0.06,relwidth=0.3)
    button1=Button(frame1,text='Submit',bg="#E5E0FF",command=sign_up_main).place(rely=0.85,relx=0.6,relheight=0.1,relwidth=0.2)
    button1=Button(frame1,text='Back',bg="#E5E0FF",command=start_page).place(rely=0.85,relx=0.2,relheight=0.1,relwidth=0.2)
    root.mainloop()
    
    
def sign_up_main():
    name = entry2.get()
    contact = entry3.get()
    un = entry4.get()
    pd = entry5.get()
    t=datetime.now() 
    current_time=t.strftime("%Y/%m/%d %H:%M:%S")
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur=db1.cursor()
    cur.execute(''' CREATE TABLE IF NOT EXISTS USER_TABLE
          (user_id smallint(5) Primary Key Not Null Unique Auto_Increment,
           user_name varchar(25) Not Null Unique,
           password varchar(25) Not Null,
           name varchar(25) Not Null,
           phone_no bigint Not Null Unique,
           created_at datetime,
           modified_at datetime)''')
    cur.execute("insert into user_table(user_name,password,name,phone_no,created_at,modified_at) values('{}','{}','{}','{}','{}','{}')".format(
        un, pd, name, contact, current_time, current_time))
    db1.commit()
    db1.close()
    mb.showinfo("Registration", "You have registered successfully!!")
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    start_page()
    
def login_page():
    root.title('Log in')
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='Log in as:', bg='#C3ACD0')
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    lower_frame2 = Frame(frame, bg='#9EA1D4')
    lower_frame2.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    button1 = Button(lower_frame2, text='User', bg='#E5E0FF',command=User_login)
    button1.place(relwidth=0.4, relheight=0.2, relx=0.5, rely=0.2, anchor='n')
    button2 = Button(lower_frame2, text='Admin', bg='#E5E0FF',command=admin_login)
    button2.place(relwidth=0.4, relheight=0.2, relx=0.5, rely=0.75, anchor='s')
    button = Button(frame, text='Back', bg='#E5E0FF',command=start_page)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='s')
    root.mainloop()

def User_login():
    global entry1,entry2,un,pd
    root.title('User login')
    un=StringVar()
    pd=StringVar()
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='User Login', bg='#C3ACD0',font=('calibre',15,'normal'))
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    lower_frame3 = Frame(root, bg='#9EA1D4')
    lower_frame3.place(relheight=0.6, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    label1 = Label(lower_frame3, text='Username:', bg='#9EA1D4',font=('calibre',15,'normal'))
    label1.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.2)
    entry1 = Entry(lower_frame3, bd=3, font=('calibre', 20, 'normal'),textvariable=un)
    entry1.place(relheight=0.1,relwidth=0.3,relx=0.5,rely=0.2)
    label2 = Label(lower_frame3, text='Password:', bg='#9EA1D4',font=('calibre',15,'normal'))
    label2.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.45)
    entry2 = Entry(lower_frame3, bd=3, font=('calibre', 20, 'normal'), show='*',textvariable=pd)
    entry2.place(relheight=0.1,relwidth=0.3,relx=0.5,rely=0.45)
    button = Button(lower_frame3, text='Enter', bg='#E5E0FF',command=user_login_main)
    button.place(relwidth=0.3, relheight=0.15, relx=0.55, rely=0.75)
    button0 = Button(lower_frame3, text='Back', bg='#E5E0FF',command=login_page)
    button0.place(relwidth=0.3, relheight=0.15, relx=0.15, rely=0.75)
    root.mainloop()
    
def user_login_main():
    global name,user_name
    name=entry1.get()
    pwd=entry2.get()
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur=db1.cursor()
    cur.execute('''SELECT user_name, password FROM user_table''')
    lst=cur.fetchall()
    db1.close()
    count=0
    for i in lst:
        if i[0]==name and i[1]==pwd:
            count+=1
    if count>0:
        check=0
        user_name=name
        user_menu()
    else:
        mb.showerror("Error", "Username and Password entered incorrectly!")
        entry1.delete(0, END)
        entry2.delete(0, END)
            
def profile():
    root.title('Profile')
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur=db1.cursor()
    if check==0:
        cur.execute('''select user_name, name, phone_no, created_at from user_table where user_table.user_name='{}' '''.format(name))
        lst=cur.fetchall()
        un1=lst[0][0]
        name1=lst[0][1]
        phno1=lst[0][2]
        time1=lst[0][3]
        frame = Frame(root, bg='#6F1AB6')
        frame.place(relwidth=1, relheight=1)
        label = Label(frame, text='Profile', bg='#C3ACD0')
        label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
        lower_frame2 = Frame(root, bg='#9EA1D4')
        lower_frame2.place(relheight=0.6, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
        label1=Label(lower_frame2,text='Name:',bg='#9EA1D4')
        label1.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.2)
        label2=Label(lower_frame2,text=name1,bg='#9EA1D4')
        label2.place(relheight=0.1,relwidth=0.2,relx=0.5,rely=0.2)
        label3=Label(lower_frame2,text='User Name:',bg='#9EA1D4')
        label3.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.3)
        label4=Label(lower_frame2,text=un1,bg='#9EA1D4')
        label4.place(relheight=0.1,relwidth=0.2,relx=0.5,rely=0.3)
        label7=Label(lower_frame2,text='Phone Number:',bg='#9EA1D4')
        label7.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.4)
        label8=Label(lower_frame2,text=phno1,bg='#9EA1D4')
        label8.place(relheight=0.1,relwidth=0.2,relx=0.5,rely=0.4)
        label9=Label(lower_frame2,text='Created at:',bg='#9EA1D4')
        label9.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.5)
        label10=Label(lower_frame2,text=time1,bg='#9EA1D4')
        label10.place(relheight=0.1,relwidth=0.2,relx=0.5,rely=0.5)
        button0 = Button(lower_frame2, text='Back', bg='#E5E0FF',command=user_menu)
        button0.place(relwidth=0.3, relheight=0.15, relx=0.35, rely=0.8)
    else:
        cur.execute('''select user_name, password from admin_table where admin_table.user_name='{}' '''.format(name))
        lst=cur.fetchall()
        un1=lst[0][0]
        pd1=lst[0][1]
        frame = Frame(root, bg='#6F1AB6')
        frame.place(relwidth=1, relheight=1)
        label = Label(frame, text='Profile', bg='#C3ACD0')
        label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
        lower_frame2 = Frame(root, bg='#9EA1D4')
        lower_frame2.place(relheight=0.6, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
        label1=Label(lower_frame2,text='User Name:',bg='#9EA1D4')
        label1.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.3)
        label2=Label(lower_frame2,text=un1,bg='#9EA1D4')
        label2.place(relheight=0.1,relwidth=0.2,relx=0.5,rely=0.3)
        label3=Label(lower_frame2,text='Password:',bg='#9EA1D4')
        label3.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.4)
        label4=Label(lower_frame2,text=pd1,bg='#9EA1D4')
        label4.place(relheight=0.1,relwidth=0.2,relx=0.5,rely=0.4)
        button0 = Button(lower_frame2, text='Back', bg='#E5E0FF',command=admin_menu)
        button0.place(relwidth=0.3, relheight=0.15, relx=0.35, rely=0.80)
    db1.close()
    root.mainloop()

    

def view_prod():
    root.title('Grocery Shop')
    frame1=Frame(root,bg="#6F1AB6").place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Products").place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
    low_frame=Frame(frame1,bg="#9EA1D4").place(relwidth=0.8,relheight=0.6,relx=0.1,rely=0.3)
    button1=Button(low_frame,bg="#E5E0FF",text='Vegetables',command=vegetables).place(relx=0.21,rely=0.4,relheight=0.1,relwidth=0.25)
    button2=Button(low_frame,bg="#E5E0FF",text='Fruits',command=fruits).place(relx=0.51,rely=0.4,relheight=0.1,relwidth=0.25)
    button1=Button(low_frame,bg="#E5E0FF",text='Snacks',command=snacks).place(relx=0.21,rely=0.55,relheight=0.1,relwidth=0.25)
    button2=Button(low_frame,bg="#E5E0FF",text='Beverages',command=beverages).place(relx=0.51,rely=0.55,relheight=0.1,relwidth=0.25)
    button1=Button(low_frame,bg="#E5E0FF",text='Dairy',command=dairy).place(relx=0.21,rely=0.7,relheight=0.1,relwidth=0.25)
    button2=Button(low_frame,bg="#E5E0FF",text='Stationary',command=stationary).place(relx=0.51,rely=0.7,relheight=0.1,relwidth=0.25)
    if ch1==1:
        button1=Button(low_frame,bg="#E5E0FF",text='Back',command=user_menu)
        button1.place(relx=0.36,rely=0.82,relheight=0.05,relwidth=0.25)
    else: 
        button1=Button(low_frame,bg="#E5E0FF",text='Back',command=admin_menu)
        button1.place(relx=0.36,rely=0.82,relheight=0.05,relwidth=0.25)
    root.mainloop()


def vegetables():
    global pro_name
    pro_name = 'vegetables'
    if ch1==1:
        productlist()
    elif ch1==2:
        up_del_()
    else:
        salebar()
       

def fruits():
    global pro_name
    pro_name = 'fruits'
    if ch1==1:
        productlist()
    elif ch1==2:
        up_del_()
    else:
        salebar()    

def snacks():
    global pro_name
    pro_name = 'snacks'
    if ch1==1:
        productlist()
    elif ch1==2:
        up_del_()
    else:
        salebar()  

def beverages():
    global pro_name
    pro_name = 'beverages'
    if ch1==1:
        productlist()
    elif ch1==2:
        up_del_()
    else:
        salebar()    

def dairy():
    global pro_name
    pro_name = 'dairy'
    if ch1==1:
        productlist()
    elif ch1==2:
        up_del_()
    else:
        salebar()  

def stationary():
    global pro_name
    pro_name = 'stationary'
    if ch1==1:
        productlist()
    elif ch1==2:
        up_del_()
    else:
        salebar()

def productlist():
    root.geometry('900x700')
    root.title('Grocery Shop')
    global p,d,listbox
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='Product List', bg='#C3ACD0')
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur = db1.cursor()
    cur.execute("select product_name from product_table where category_name='{}'".format(pro_name))
    d = cur.fetchall()
    p_name = StringVar(value=d)
    listbox = Listbox(frame, listvariable=p_name,selectmode='browse') 
    listbox.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    listbox.configure(background="#9EA1D4")
    scrollbar = Scrollbar(listbox, orient='vertical')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    button = Button(frame, text='Select', bg='#E5E0FF', command=display_prod_details)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='sw')
    button = Button(frame, text='Back', bg='#E5E0FF', command=user_menu)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='se')

    root.mainloop()
    

def display_prod_details():
    global p,d,listbox,q
    try:
        p = d[listbox.curselection()[0]][0]
    except IndexError:
        productlist()
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur = db1.cursor()
    cur.execute("select product_name,price,disc_percentage,category_name from product_table where product_name='{}'".format(p))
    d = cur.fetchall()
    db1.close()
    root.title('{}'.format(p.title()))
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    
    label = Label(frame, text='{}'.format(p), bg='#C3ACD0')
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    
    canvas = Canvas(root, bg='#9EA1D4')
    canvas.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    
    label1 = Label(canvas, text='Name:', bg='#9EA1D4', font=('calibre', 12))
    label1.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.05)
    label6 = Label(canvas, text=d[0][0], bg='#9EA1D4',font=('calibre', 12 ))
    label6.place(relheight=0.15,relwidth=0.2,relx=0.5,rely=0.05)
    label2 = Label(canvas, text='Price:', bg='#9EA1D4', font=('calibre', 12))
    label2.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.3)
    label7 = Label(canvas, text=str(d[0][1]), bg='#9EA1D4',font=('calibre', 12))
    label7.place(relheight=0.15,relwidth=0.2,relx=0.5,rely=0.3)
    label4 = Label(canvas, text='Discount %:', bg='#9EA1D4', font=('calibre', 12))
    label4.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.55)
    label9 = Label(canvas, text=str(d[0][2]), bg='#9EA1D4',font=('calibre', 12))
    label9.place(relheight=0.15,relwidth=0.2,relx=0.5,rely=0.55)
    if d[0][3] in ('vegetables','fruits'):
        label10=Label(canvas, text='Quantity (kg):', bg='#9EA1D4', font=('calibre', 12))
        label10.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.8)
    elif d[0][3]==('beverages','dairy'):
        label10=Label(canvas, text='Quantity (L):', bg='#9EA1D4', font=('calibre', 12))
        label10.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.8)
    else:
        label10=Label(canvas, text='Quantity:', bg='#9EA1D4', font=('calibre', 12))
        label10.place(relheight=0.1,relwidth=0.2,relx=0.2,rely=0.8)
    q=StringVar()
    qty_box=ttk1.Combobox(canvas,width=20,height=10,textvariable=q)
    qty_box['values']=(1,2,3,4,5,6,7,8,9,10)
    qty_box.current(0)
    qty_box.place(relheight=0.15,relwidth=0.2,relx=0.5,rely=0.8)
    def add_to_cart():
        global q,d,d1
        db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
        cur=db1.cursor()
        cur.execute(''' create table if not exists cart_table
              (cart_id smallint PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT,
               user_id smallint NOT NULL,
               product_id smallint NOT NULL,
               product_name varchar(25) NOT NULL,
               price decimal(10,2) NOT NULL,
               qty smallint NOT NULL,
               disc_perc decimal(10,2),
               final_price decimal(10,2) NOT NULL,
               FOREIGN KEY (user_id) REFERENCES user_table (user_id),
               FOREIGN KEY (product_id) REFERENCES product_table(product_id));''')
        cur.execute("select product_id,product_name,price,disc_percentage from product_table where product_name='{}'".format(p))
        d1= cur.fetchall()
        qty=q.get()
        final_price = int(qty)*(float(d1[0][2])-(float(d1[0][2])*float(d1[0][3])/100))
        cur.execute("select user_id from user_table where user_name='{}'".format(name))
        d2 = cur.fetchall()
        user_id = d2[0][0]
        sql = '''insert into cart_table (user_id, product_id, product_name, price,qty,disc_perc, final_price)
         values('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(user_id, d1[0][0], d1[0][1], d1[0][2],qty,d1[0][3],final_price)
        cur.execute(sql)
        db1.commit()
        db1.close()
        mb.showinfo("Item Added", "Item added to shopping cart!")
    button = Button(frame, text='Add to Cart', bg='#E5E0FF', command=add_to_cart)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='sw')
    button = Button(frame, text='Back', bg='#E5E0FF', command=productlist)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='se')
    root.mainloop()
    
                    
        

def shopping_cart():
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur=db1.cursor()
    cur.execute(''' create table if not exists cart_table
          (cart_id smallint PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT,
           user_id smallint NOT NULL,
           product_id smallint NOT NULL,
           product_name varchar(25) NOT NULL,
           price decimal(10,2) NOT NULL,
           qty smallint NOT NULL,
           disc_perc decimal(10,2),
           final_price decimal(10,2) NOT NULL,
           FOREIGN KEY (user_id) REFERENCES user_table (user_id),
           FOREIGN KEY (product_id) REFERENCES product(product_id));''')
    db1.commit()
    db1.close()
    display_cart()
          
def display_cart():
    global p,d
    root.title('Shopping Cart')
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='Shopping Cart', bg='#C3ACD0')
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur = db1.cursor()
    cur.execute("select product_name from cart_table")
    d = cur.fetchall()
    p_name = StringVar(value=d)
    lbox =Listbox(frame, listvariable=p_name, bg='#9EA1D4',selectmode='browse')  # specified selectmode so only one item is selected
    lbox.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    scrollbar = Scrollbar(lbox, orient='vertical')
    scrollbar.config(command=lbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    def display_cart_prod():
        global d,p
        try:
            p = d[lbox.curselection()[0]][0]
        except IndexError:
            display_cart()
        db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
        cur=db1.cursor()
        root.title('Shopping Cart')
        frame = Frame(root, bg='#6F1AB6')
        frame.place(relwidth=1, relheight=1)
        label = Label(frame, text='Shopping Cart', bg='#C3ACD0')
        label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
        lower_frame=Frame(frame,bg="#9EA1D4")
        lower_frame.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
        cur.execute('''select product_name,price,disc_perc,final_price from cart_table where product_name="{}"'''.format(p))
        lst=cur.fetchall()
        cur.execute('''select * from cart_table where cart_table.product_name="{}"'''.format(p))
        d=cur.fetchall()
        db1.commit()
        db1.close()  
        name1=lst[0][0]
        price1=lst[0][1]
        disc_perc1=lst[0][2]
        final_price1=lst[0][3]
        label1 =Label(lower_frame, text='Product Name:', bg='#9EA1D4')
        label1.place(relheight=0.1, relwidth=0.3, relx=0.2, rely=0.1, anchor='n')
        label2 =Label(lower_frame, text='Price:', bg='#9EA1D4')
        label2.place(relheight=0.1, relwidth=0.2, relx=0.2, rely=0.3, anchor='n')
        label3 =Label(lower_frame, text='Disc_Percentage:', bg='#9EA1D4')
        label3.place(relheight=0.1, relwidth=0.2, relx=0.2, rely=0.5, anchor='n')
        label4 =Label(lower_frame, text='Final Price:', bg='#9EA1D4')
        label4.place(relheight=0.1, relwidth=0.2, relx=0.2, rely=0.7, anchor='n')
        label11 =Label(lower_frame, text=name1, bg='#9EA1D4', font=('calibre', 10, 'bold'))
        label11.place(relheight=0.1, relwidth=0.3, relx=0.6, rely=0.1, anchor='n')
        label22 =Label(lower_frame, text=price1, bg='#9EA1D4', font=('calibre', 10, 'bold'))
        label22.place(relheight=0.1, relwidth=0.2, relx=0.6, rely=0.3, anchor='n')
        label33 =Label(lower_frame, text=disc_perc1, bg='#9EA1D4', font=('calibre', 10, 'bold'))
        label33.place(relheight=0.1, relwidth=0.2, relx=0.6, rely=0.5, anchor='n')
        label44 =Label(lower_frame, text=final_price1, bg='#9EA1D4', font=('calibre', 10, 'bold'))
        label44.place(relheight=0.1, relwidth=0.2, relx=0.6, rely=0.7, anchor='n')
        def display_cart_prod_remove():
            db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
            cur=db1.cursor()
            cur.execute('''delete from cart_table where product_name="{}"'''.format(name1))
            mb.showinfo('Item Removed',"Product has been removed from cart!")
            db1.commit()
            db1.close()  
            display_cart()
        
        button1=Button(frame,text='Back',bg="#E5E0FF",command=display_cart)
        button1.place(rely=0.85,relx=0.2,relheight=0.1,relwidth=0.2)
        button2=Button(frame,text='Delete',bg="#E5E0FF",command=display_cart_prod_remove)
        button2.place(rely=0.85,relx=0.5,relheight=0.1,relwidth=0.2)
        root.mainloop()
    button1=Button(frame,text='View',bg="#E5E0FF",command=display_cart_prod)
    button1.place(rely=0.85,relx=0.4,relheight=0.1,relwidth=0.2)
    button2=Button(frame,text='Back',bg="#E5E0FF",command=user_menu)
    button2.place(rely=0.85,relx=0.1,relheight=0.1,relwidth=0.2)
    button3=Button(frame,text='View Bill',bg="#E5E0FF",command=view_bill)
    button3.place(rely=0.85,relx=0.7,relheight=0.1,relwidth=0.2)
    root.mainloop()
    
def view_bill():
    global bill_amt
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur=db1.cursor()
    root.title('Bill')
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='Bill', bg='#C3ACD0')
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    canvas=Canvas(frame,bg="#9EA1D4")
    scrollbar = Scrollbar(canvas, orient='vertical')
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    
    cur.execute('''select product_name,qty, final_price from cart_table''')
    d=cur.fetchall()
    db1.close()
    
    label1 = Label(canvas, text='Product Name:', bg='#9EA1D4')
    label1.place(relx=0.1,rely=0.1,relwidth=0.2,relheight=0.1)
    label2 = Label(canvas, text='Quantity:', bg='#9EA1D4')
    label2.place(relx=0.4,rely=0.1,relwidth=0.2,relheight=0.1)
    label3 = Label(canvas, text='Price:', bg='#9EA1D4')
    label3.place(relx=0.7,rely=0.1,relwidth=0.2,relheight=0.1)
    c=len(d)
    y_space=0.3
    bill_amt=0
    while True:
        if c>0:
            for i in range(len(d)):
                label3 = Label(canvas, text=d[i][0], bg='#9EA1D4')
                label3.place(relx=0.1,rely=y_space,relwidth=0.2,relheight=0.1)
                label4 = Label(canvas, text=d[i][1], bg='#9EA1D4')
                label4.place(relx=0.4,rely=y_space,relwidth=0.2,relheight=0.1)
                label5 = Label(canvas, text=d[i][2], bg='#9EA1D4')
                label5.place(relx=0.7,rely=y_space,relwidth=0.2,relheight=0.1)
                y_space+=0.2
                bill_amt+=float(d[i][2])
                c-=1
            else:
                label4 = Label(canvas, text='Total Amount:', bg='#9EA1D4')
                label4.place(relx=0.3,rely=y_space,relwidth=0.2,relheight=0.1)
                label4 = Label(canvas, text='Rs. '+str(bill_amt), bg='#9EA1D4')
                label4.place(relx=0.7,rely=y_space,relwidth=0.2,relheight=0.1)
                break
    button5=Button(frame,text='Back',bg="#E5E0FF",command=display_cart)
    button5.place(rely=0.8,relx=0.2,relheight=0.1,relwidth=0.2)
    def checkout():
        global d
        t=datetime.now() 
        t_chout=t.strftime("%Y/%m/%d %H:%M:%S")
        db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
        cur=db1.cursor()
        cur.execute('''select product_name from cart_table''')
        lst=cur.fetchall()
        for i in range(len(lst)):
            cur.execute('select stock_qty from product_table where product_name="{}"'.format(lst[i][0]))
            d=cur.fetchall()
            cur.execute('select qty from cart_table where product_name="{}"'.format(lst[i][0]))
            d1=cur.fetchall()
            new_qty=d[0][0]-d1[0][0]
            cur.execute('''update product_table set stock_qty={} where product_name="{}" '''.format(new_qty,lst[i][0]))
        cur.execute("""select product_name,qty,final_price from cart_table""")
        lst=cur.fetchall()
        fob=open('{}.txt'.format(user_name),'a')
        fob.write("""**********************************BILL**********************************""")
        fob.write('\n')
        fob.write("""Check out at: {}""".format(t_chout)) 
        fob.write('\n')
        fob.write("""             Product Name    |    Qty    |    Price""")
        fob.write('\n')
        for i in lst:
            fob.write('                 '+i[0]+'        '+str(i[1])+'        '+str(i[2]))
            fob.write('\n')
        fob.write("""                                       Total Price={}""".format(bill_amt))
        fob.write('\n')
        fob.write("""************************************************************************""")
        fob.write('\n')
        fob.close()
        for i in lst:
            cur.execute('''delete from cart_table where product_name='{}' '''.format(i[0]))
        db1.commit()
        db1.close()
        root.title('Shopping System')
        frame = Frame(root, bg='#6F1AB6')
        frame.place(relwidth=1, relheight=1)
        label = Label(frame, text='THANK YOU FOR SHOPPING WITH US!', bg='#C3ACD0')
        label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
        def exit_main():
            root.destroy()
        button6=Button(frame,text='Exit',bg="#E5E0FF",command=exit_main)
        button6.place(rely=0.6,relx=0.35,relheight=0.1,relwidth=0.2)
        button6=Button(frame,text='Shop Again',bg="#E5E0FF",command=start_page)
        button6.place(rely=0.6,relx=0.75,relheight=0.1,relwidth=0.2)
        root.mainloop() 
    button6=Button(frame,text='Checkout',bg="#E5E0FF",command=checkout)
    button6.place(rely=0.8,relx=0.5,relheight=0.1,relwidth=0.2)
    root.mainloop()

def admin_login():
    global entry1,entry2
    root.title('ADMIN LOGIN')
    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='Admin Login', bg='#C3ACD0',font=('calibre',15,'normal')).place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    lower_frame3 = Frame(root, bg='#9EA1D4')
    lower_frame3.place(relheight=0.6, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    label1 = Label(lower_frame3, text='Username:', bg='#9EA1D4',font=('calibre',15,'normal'))
    label1.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.2)
    entry1 = Entry(lower_frame3, bd=3, font=('calibre', 20, 'normal'))
    entry1.place(relheight=0.1,relwidth=0.3,relx=0.5,rely=0.2)
    label2 = Label(lower_frame3, text='Password:', bg='#9EA1D4',font=('calibre',15,'normal'))
    label2.place(relheight=0.15,relwidth=0.2,relx=0.2,rely=0.45)
    entry2 = Entry(lower_frame3, bd=3, font=('calibre', 20, 'normal'), show='*')
    entry2.place(relheight=0.1,relwidth=0.3,relx=0.5,rely=0.45)
    button = Button(lower_frame3, text='Back', bg='#E5E0FF',command=login_page)
    button.place(relwidth=0.3, relheight=0.15, relx=0.15, rely=0.75)
    button0 = Button(lower_frame3, text='Enter', bg='#E5E0FF',command=admin_login_main)
    button0.place(relwidth=0.3, relheight=0.15, relx=0.55, rely=0.75)
    root.mainloop()
    
def admin_login_main():
    global name,check
    name=entry1.get()
    pwd=entry2.get()
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur=db1.cursor()
    cur.execute('''SELECT user_name, password FROM admin_table''')
    lst=cur.fetchall()
    db1.close()
    count=0
    for i in lst:
        if i[0]==name and i[1]==pwd:
            count+=1
    if count>0:
        check=1
        admin_menu()
    else:
        mb.showerror("Error", "Username and Password entered incorrectly!")
        entry1.delete(0, END)
        entry2.delete(0, END)
    
    
def user_menu():
    global ch1
    ch1=1
    root.title('E-Shop')
    frame1=Frame(root,bg="#6F1AB6")
    frame1.place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Menu")
    label1.place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
    low_frame=Frame(frame1,bg="#9EA1D4")
    low_frame.place(relwidth=0.8,relheight=0.6,relx=0.1,rely=0.3)
    button1=Button(low_frame,bg="#E5E0FF",text='View Products',command=view_prod)
    button1.place(relx=0.32,rely=0.25,relheight=0.2,relwidth=0.35)
    button2=Button(low_frame,bg="#E5E0FF",text='View Cart',command=shopping_cart)
    button2.place(relx=0.32,rely=0.65,relheight=0.2,relwidth=0.35)
    menubar=Menu(root)
    file=Menu(menubar,tearoff=0)
    file.add_command(label='Profile',command=profile)
    def view_hist():
        f=open('{}.txt'.format(user_name),'r')
        lst=f.readlines()
        root.title('History')
        frame1=Frame(root,bg="#6F1AB6")
        frame1.place(relwidth=1,relheight=1)
        label1=Label(frame1,bg="#C3ACD0",text="History").place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
        low_frame=Frame(frame1,bg="#9EA1D4")
        low_frame.place(relwidth=0.8,relheight=0.5,relx=0.1,rely=0.3)
        y_space=0.1
        for i in lst:
            txt=i.strip('\n')
            label1=Label(low_frame,bg="#9EA1D4",text=txt)
            label1.place(relx=0,rely=y_space,relheight=0.1,relwidth=1)
            y_space+=0.1
        button1=Button(frame1,bg="#E5E0FF",text='Back',command=user_menu)
        button1.place(relx=0.31,rely=0.85,relheight=0.1,relwidth=0.35)
        f.close()
        root.mainloop()
        
    file.add_command(label='History',command=view_hist)
    file.add_command(label='Logout',command=start_page)
    menubar.add_cascade(label="Menu",menu=file)
    root.config(menu=menubar)
    root.mainloop()
    
def admin_menu():
    global ch1
    ch1=2
    def product_list_main():
        db1 = db.connect(host='localhost', user='root', passwd='mydat1974SQL',database='online_shop')
        cur = db1.cursor()
        cur.execute (''' CREATE TABLE IF NOT EXISTS PRODUCT_TABLE
                    (product_id smallint(5) Primary Key Not Null Unique Auto_Increment,
                    product_name varchar(25) Not Null Unique,
                    category_name varchar(25) NOT NULL,
                    stock_qty smallint(4) ,
                    price decimal(8),
                    disc_percentage decimal(4),
                    disc_amt decimal(7));''')
        db1.commit()
        db1.close()
    product_list_main()
    root.title('E-Shop')
    frame1=Frame(root,bg="#6F1AB6").place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Menu").place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
    low_frame=Frame(frame1,bg="#9EA1D4").place(relwidth=0.8,relheight=0.6,relx=0.1,rely=0.3)
    button1=Button(low_frame,bg="#E5E0FF",text='Add Products',command=add_product).place(relx=0.32,rely=0.4,relheight=0.1,relwidth=0.35)
    button1=Button(low_frame,bg="#E5E0FF",text='Update Product Information',command=update).place(relx=0.32,rely=0.55,relheight=0.1,relwidth=0.35)
    button1=Button(low_frame,bg="#E5E0FF",text='Delete Products',command=delete).place(relx=0.32,rely=0.7,relheight=0.1,relwidth=0.35)    
    menubar=Menu(root)
    file=Menu(menubar,tearoff=0)
    file.add_command(label='Profile',command=profile)
    file.add_command(label='Sales',command=sales)
    file.add_command(label='Logout',command=start_page)
    file.add_command(label='Menu',command=admin_menu)
    menubar.add_cascade(label="Menu",menu=file)
    root.config(menu=menubar)
    root.mainloop()

def sales():
    global ch1
    ch1=3
    root.title('E-Shop')
    frame1=Frame(root,bg="#6F1AB6").place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Products").place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
    low_frame=Frame(frame1,bg="#9EA1D4").place(relwidth=0.8,relheight=0.6,relx=0.1,rely=0.3)
    button1=Button(low_frame,bg="#E5E0FF",text='Vegetables',command=vegetables).place(relx=0.21,rely=0.4,relheight=0.1,relwidth=0.25)
    button2=Button(low_frame,bg="#E5E0FF",text='Fruits',command=fruits).place(relx=0.51,rely=0.4,relheight=0.1,relwidth=0.25)
    button1=Button(low_frame,bg="#E5E0FF",text='Snacks',command=snacks).place(relx=0.21,rely=0.55,relheight=0.1,relwidth=0.25)
    button2=Button(low_frame,bg="#E5E0FF",text='Beverages',command=beverages).place(relx=0.51,rely=0.55,relheight=0.1,relwidth=0.25)
    button1=Button(low_frame,bg="#E5E0FF",text='Dairy',command=dairy).place(relx=0.21,rely=0.7,relheight=0.1,relwidth=0.25)
    button2=Button(low_frame,bg="#E5E0FF",text='Stationery',command=stationary).place(relx=0.51,rely=0.7,relheight=0.1,relwidth=0.25)
    button1=Button(low_frame,bg="#E5E0FF",text='Back',command=admin_menu).place(relx=0.36,rely=0.85,relheight=0.05,relwidth=0.25)

def salebar():
    root.title('E-Shop')
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur = db1.cursor()
    cur.execute("select product_name from product_table where category_name='{}'".format(pro_name))
    d = cur.fetchall()
    cur.execute("select stock_qty from product_table where category_name='{}'".format(pro_name))
    d1 = cur.fetchall()
    db1.commit()
    db1.close()
    ld=[item for t in d for item in t]
    ld1=[item for t in d1 for item in t]
    ld2=list(map(lambda x: 100-x,ld1))
    figure = Figure(figsize=(6, 4), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure,root)
    axes = figure.add_subplot()
    axes.bar(ld,ld2,color ='#A75D5D',width = 0.4)
    axes.set_title("Product name")
    axes.set_ylabel("No. of products sold per month")
    figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    root.mainloop()

    
def update():
    global ch
    ch=1
    view_prod()


def delete():
    global ch
    ch=2
    view_prod()

def up_del_():
    root.geometry('900x700')
    global p,d,listbox
    def logic():
        if ch==2:
            try:
                p = d[listbox.curselection()[0]][0]
            except IndexError:
                up_del_()
            db1 = db.connect(host='localhost', user='root', passwd='mydat1974SQL', 
            database='online_shop')
            c = db1.cursor()
            c.execute('''delete from product_table where product_name='{}' ;'''.format(p))
            db1.commit()
            db1.close()
            mb.showinfo("Deleted Product", "Product has been successfully deleted!!")
            up_del_()
        elif ch==1:
            root.geometry('900x700')
            frame = Frame(root, bg='#6F1AB6')
            frame.place(relwidth=1, relheight=1)
            label = Label(frame, text='UPDATE PRODUCT DETAILS:', bg='#C3ACD0')
            label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
            lower_frame =Frame(root, bg='#9EA1D4')
            lower_frame.place(relheight=0.6, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
            quantity = IntVar()
            price = DoubleVar()
            discperc = DoubleVar()
            global e3, e4, e5
            name3 = Label(lower_frame, text='Stock Quantity:', bg='#9EA1D4')
            name3.grid(row=0, column=0, pady=3)
            e3 = Entry(lower_frame, textvariable=quantity, font=('calibre', 12, 'normal'))
            e3.grid(row=0, column=1)
            name4 = Label(lower_frame, text='Price:', bg='#9EA1D4')
            name4.grid(row=1, column=0, pady=3)
            e4 = Entry(lower_frame, textvariable=price, font=('calibre', 12, 'normal'))
            e4.grid(row=1, column=1)
            name5 = Label(lower_frame, text='Discount Percentage:', bg='#9EA1D4')
            name5.grid(row=2, column=0, pady=35)
            e5 = Entry(lower_frame, textvariable=discperc, font=('calibre', 12, 'normal'))
            e5.grid(row=2, column=1)
            button1 = Button(lower_frame, text='Submit', bg='#E5E0FF',command=update_new1)
            button1.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='sw')
            button = Button(lower_frame, text='Back', bg='#E5E0FF', command=admin_menu)
            button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='se')
            root.mainloop()
    def update_new1():
        try:
            p = d[listbox.curselection()[0]][0]
        except IndexError:
            up_del_()
        db1 = db.connect(host='localhost', user='root', passwd='mydat1974SQL',database='online_shop')
        c = db1.cursor()
        disc_amt = float(e4.get()) - (float(e4.get()) * float(e5.get()) / 100)
        sql = "update product_table set stock_qty={},price={},disc_percentage={},disc_amt={} where product_name='{}' ".format(e3.get(), e4.get(), e5.get(), disc_amt, p)
        c.execute(sql)
        db1.commit()
        db1.close()
        mb.showinfo("Updated Product Information", "Product details has been successfully updated!!")
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)

    frame = Frame(root, bg='#6F1AB6')
    frame.place(relwidth=1, relheight=1)
    label = Label(frame, text='Product List', bg='#C3ACD0')
    label.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor='n')
    db1=db.connect(host='localhost',user='root',passwd='mydat1974SQL',database='online_shop')
    cur = db1.cursor()
    cur.execute("select product_name from product_table where category_name='{}'".format(pro_name))
    d = cur.fetchall()
    db1.close()
    p_name = StringVar(value=d)
    listbox = Listbox(frame, listvariable=p_name,selectmode='browse') 
    listbox.place(relheight=0.5, relwidth=0.75, relx=0.5, rely=0.25, anchor='n')
    listbox.configure(background="#9EA1D4")
    scrollbar = Scrollbar(listbox, orient='vertical')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    button = Button(frame, text='Select', bg='#E5E0FF', command=logic)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='sw')
    button = Button(frame, text='Back', bg='#E5E0FF', command=admin_menu)
    button.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.9, anchor='se')
    root.mainloop() 

def add_product():
    root.title('E-Shop')
    name=StringVar()
    discount=IntVar()
    category=StringVar()
    stock=IntVar()
    price=IntVar()
    frame1=Frame(root,bg="#6F1AB6").place(relwidth=1,relheight=1)
    label1=Label(frame1,bg="#C3ACD0",text="Add Products").place(relx=0.31,rely=0.1,relheight=0.12,relwidth=0.35)
    low_frame=Frame(frame1,bg="#9EA1D4").place(relwidth=0.8,relheight=0.5,relx=0.1,rely=0.3)
    def store():
        db1 = db.connect(host='localhost', user='root', passwd='mydat1974SQL', database='online_shop')
        cur = db1.cursor()
        disc_amt = float(entry5.get()) - (float(entry5.get()) * float(entry6.get()) / 100)
        cur.execute('''insert into product_table(product_name,category_name,stock_qty, price,disc_percentage, disc_amt)
         values('{}','{}','{}','{}','{}','{}')'''.format(entry2.get(), entry3.get(), entry4.get(), entry5.get(),entry6.get(), disc_amt))
        db1.commit()
        db1.close()
        mb.showinfo("Added Product", "Product has been successfully added!!")
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        entry6.delete(0, END)
    label2=Label(low_frame,bg="#9EA1D4",text="Name:").place(relx=0.22,rely=0.33,relheight=0.07,relwidth=0.2)
    entry2=Entry(low_frame,textvariable=name)
    entry2.place(relx=0.45,rely=0.33,relheight=0.05,relwidth=0.3)
    label3=Label(low_frame,bg="#9EA1D4",text="Category:").place(relx=0.22,rely=0.43,relheight=0.07,relwidth=0.2)
    entry3=Entry(low_frame,textvariable=category)
    entry3.place(relx=0.45,rely=0.43,relheight=0.05,relwidth=0.3)
    label4=Label(low_frame,bg="#9EA1D4",text="Stock:").place(relx=0.22,rely=0.53,relheight=0.07,relwidth=0.2)
    entry4=Entry(low_frame,textvariable=stock)
    entry4.place(relx=0.45,rely=0.53,relheight=0.05,relwidth=0.3)
    label5=Label(low_frame,bg="#9EA1D4",text="Price:").place(relx=0.22,rely=0.63,relheight=0.07,relwidth=0.2)
    entry5=Entry(low_frame,textvariable=price)
    entry5.place(relx=0.45,rely=0.63,relheight=0.05,relwidth=0.3)
    label6=Label(low_frame,bg="#9EA1D4",text="Discount:").place(relx=0.22,rely=0.73,relheight=0.07,relwidth=0.2)
    entry6=Entry(low_frame,textvariable=discount)
    entry6.place(relx=0.45,rely=0.73,relheight=0.05,relwidth=0.3)
    button1=Button(frame1,text='Submit',bg="#E5E0FF",command=store).place(rely=0.85,relx=0.6,relheight=0.1,relwidth=0.2)
    button1=Button(frame1,text='Back',bg="#E5E0FF",command=admin_menu).place(rely=0.85,relx=0.2,relheight=0.1,relwidth=0.2)    
    root.mainloop()
        
    
    
start_page()
"""CREATE TABLE IF NOT EXISTS ADMIN_TABLE
    -> (admin_id smallint(5) Primary Key Not Null Unique Auto_Increment,
    -> user_name varchar(25) Not Null Unique,
    -> password varchar(25) Not Null);
    insert into admin_table(user_name,password) values('admin1','ADMIN1');"""