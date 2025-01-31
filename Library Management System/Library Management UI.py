import tkinter as tk 
import random
import re 
from tkinter import messagebox # type: ignore 
import mysql.connector as c
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
con = c.connect(host='localhost',password="your password",user="root",database="library")
cur = con.cursor()

def sort(input): #used to sort values coming from the database (removing (),'' etc.)
        l = []
        v = 1
        for i in range(len(input)):
            a = str(input[i])
            words = re.findall("[^,^(^)]+",a)           
            for i in range(len(words)):                      
                b = words[i]
                words_final = re.findall(r"""[^'^"]+'s [^'^"]+|[^'^"]+'t [^'^"]+|[^'^"]+""",b)
                for i in range(len(words_final)):
                    
                    if words_final[i] == "None":
                        pass
                    else:
                        l.append(words_final[i]) 
            v = v+1
        return l

class ToolTip(): #used to create tooltip (floating text when hover) of count of books available.

        def __init__(self,widget,text) -> None:
                self.widget = widget
                self.text = text
                self.tool_tip_window = None
                self.widget.bind("<Enter>",self.show_tip)
                self.widget.bind("<Leave>",self.hide_tip)
        def show_tip(self,event=None):
                if self.tool_tip_window or not self.text:
                        return 
                x,y,_cx,_cy = self.widget.bbox("insert")
                x += self.widget.winfo_rootx()-100      
                y += self.widget.winfo_rooty()+55
                self.tool_tip_window = tk.Toplevel(self.widget)
                self.tool_tip_window.wm_overrideredirect(True)
                self.tool_tip_window.wm_geometry(f"+{x}+{y}")
                l = tk.Label(self.tool_tip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1)
                l.pack()
        def hide_tip(self,event=None):
                if self.tool_tip_window :
                        self.tool_tip_window.destroy()
                self.tool_tip_window = None

class GUI: 
        #UTILITY FUNCTIONSP:--> functions which does something to help other functions.
        def gmail_send(self,to_gmail): #This enables to send mail from given 
                from_gmail = "your gmail id" #enter your gmail
                ap = "your app password" #create an app password of your gmail account
                subject = "Welcome to Nexus of Knowledge! 🚀📚"
                body = f"""
Dear {self.name.get()},

We’re beyond excited to welcome you to Nexus of Knowledge – your gateway to a world of 🌍 discovery and 📚 learning!

Your sign-up is complete ✅, and you’re now part of a thriving community dedicated to exploring ideas, gaining insights, and growing together.

What’s Next?
1️⃣ Explore Resources: Access our carefully curated tools and knowledge base.
2️⃣ Engage with the Community: Share your voice and connect with like-minded thinkers.
3️⃣ Stay Updated: Look out for exclusive updates, events, and tips in your inbox!

Your Details:
Customer ID: {self.c_id}
Password: {self.Password}
Welcome aboard! Let’s shape the future of learning together. 🌟

Warm regards,
💼 The NEXUS OF KNOWLEDGE Team
"""
                msg = MIMEMultipart()
                msg['From']= from_gmail
                msg['To']= to_gmail
                msg['Subject']=subject
                msg.attach(MIMEText(body,'plain'))

                try:
                        server = smtplib.SMTP('smtp.gmail.com',587)
                        server.starttls()
                        server.login(from_gmail,ap)
                        server.sendmail(from_gmail,to_gmail,msg.as_string())
                except Exception as e:
                        messagebox.showerror("Error Occured",f"{e}\nPlease Retry")
                        self.sign_up()
                finally:
                        server.quit()
                
        def sign_in_submit_function(self): #submits sign in function 
                self.w =1 #JUGAAD
                cur.execute("select customer_id from customer_details;")
                c_ids = cur.fetchall()
                g = sort(c_ids)
                if self.custID.get() in g:
                        cur.execute(f"insert into daily_log values('{self.custID.get()}',(select NOW()),NULL);")
                        cur.execute(f"select name from customer_details where customer_id = '{self.custID.get()}';")
                        self.NAME = sort([cur.fetchone()])
                        cur.execute(f"select gmail_id from customer_details where customer_id = '{self.custID.get()}';")
                        self.GMAIL = sort([cur.fetchone()])
                        self.c_id = self.custID.get()
                        #CHECK PASSWORD
                        cur.execute(f"select user_password from password_table where customer_id = '{self.custID.get()}';")
                        _d = cur.fetchall()
                        d = sort(_d)
                        if d[0] == self.password.get():
                                self.option_page()
                        else:
                                messagebox.showerror("Incorect password","Incorrect password. Please try again")
                else:
                        self.error = messagebox.showerror("Invalid Customer ID","The entered customer Id is not found please try again or\n sign up to create an account.")
                        self.home_page()

        def show_pass(self,event): #function to support toggle button of show password.
                self.user_pass1.config(text=self.pa[0])
                self.pass_toggle.config(image=self.closed_eye)

        def hide_pass(self,event): #function to support toggle button of show password.
                self.user_pass1.config(text=self.z)
                self.pass_toggle.config(image=self.open_eye)
                
        def sign_up_submit_function(self): #submits sign up function
                #CUSTOMER ID GENERATOR
                a = list(self.name.get())
                f = "_"
                for i in a:
                        if i !=" ":
                                f += i            
                self.c_id = f"{f}"+f"{self.AGE.get()}"+f"_{self.phn.get()}" 
                #PASSWORD GENERATOR
                sp = random.choice(['!','@','#','$','%','^','&','*'])
                self.Password = (self.name.get()[0:3])+str(self.phn.get())[-4:]+sp+self.gmail.get()[0:3]+str(self.AGE.get())
                messagebox.showinfo("Sign-Up Successfull","Your Customer ID and Password has been mailed to you kindly check.\nThank You for Signing Up.")
                cur.execute(f"insert into daily_log values('{self.c_id}',(select NOW()),NULL);")
                cur.execute(f"insert into customer_details values('{self.c_id}','{self.name.get()}','{self.AGE.get()}','{self.phn.get()}','{self.ADD.get()}','{self.gmail.get()}','No');")
                cur.execute(f"insert into password_table values('{self.c_id}','{self.Password}');")
                con.commit()
                self.x = 1 #JUGAAD
                self.gmail_send(self.gmail.get()) #SENDING MAIL TO NEW CUSTOMER
                self.option_page()

        def SQL(self): #function to fetch all required data in advance
                cur.execute('select book_name from books where book_niche = "classic literature";')
                self.cl = cur.fetchall()
                self.classic_literature = sort(self.cl)
                cur.execute('select book_name from books where book_niche = "Science Fiction and Fantasy";')
                self.sff = cur.fetchall() 
                self.Science_Fiction_Fantasy = sort(self.sff)
                cur.execute('select book_name from books where book_niche = "Mystery and Thriller";')
                self.mt = cur.fetchall() 
                self.Mystery_and_Thriller = sort(self.mt)
                cur.execute('select book_name from books where book_niche = "Historical Fiction";')
                self.hf = cur.fetchall() 
                self.Historical_Fiction = sort(self.hf)
                cur.execute('select book_name from books where book_niche = "Non-Fiction";')
                self.nf = cur.fetchall() 
                self.Non_Fiction = sort(self.nf)
                cur.execute('select book_name from books where book_niche = "Philosophy and Self Help";')
                self.psh = cur.fetchall() 
                self.Philosophy_and_Self_Help = sort(self.psh)
                cur.execute('select book_name from books where book_niche = "Poetry";')
                self.p = cur.fetchall() 
                self.Poetry = sort(self.p)
                cur.execute("select table_no from TABLE_OCCUPANCY where table_occupancy = 'un-occupied';")
                self.table = cur.fetchall()
                f = sort(self.table)
                self.table_no = random.choice(f) #GETTING A RANDOM TABLE NUMBER
                
        def add_donated_books(self): #adding donated books to the database when + clicked
                #MESSAGE
                messagebox.showinfo("Books Donated Successfully",f"""Thank You for donating {self.num_donated_books} books. You can ask for
recepit from the main counter.
Have a nice day. 
                """)
                #JUGAAD
                if self.b==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b==-1:
                        self.c1=self.new_user_id.get()
                #FETCHING NAME
                cur.execute(f"select name from customer_details where customer_id = '{self.c1}';")
                name  = cur.fetchone()
                n = sort(name)
                #FETCHING BOOK ID
                cur.execute("select book_id from books;")
                f = sort(cur.fetchall())
                #CHECKING BOOK ID
                bid = random.randint(100,999)
                while(bid in f):
                        bid = random.randint(100,999)
                books = cur.fetchall()
                self.books = sort(books)
                #ADDING BOOKS
                if self.book_name1.get() not in self.books:
                        cur.execute("insert into donate_books values(%s,%s,%s,%s,NULL,curdate());",(self.book_name1.get(),self.author1.get(),self.year1.get(),n[0],)) 
                        cur.execute("insert into books values(%s,%s,%s,%s,NULL,NULL);",(bid,self.book_name1.get(),self.author1.get(),self.year1.get()))
                        con.commit()
                self.option_page()

        def cash_page(self):#adding payments data to database
                #MESSAGE
                messagebox.showinfo("Cash Payment","Pay cash at the reception with your Recepit No.\nThank You.")
                #ADDING TO THE DATABASE
                self.mode = "Cash"
                self.payments_database()

        def return_issue_msg(self):#updating database on returning of books
                #MESSAGE
                messagebox.showinfo("Thank You",f"Thank you for returing book(s).\nHave a nice day.")
                cur.fetchall()
                #UPDATING DATABASE
                cur.execute("delete from book_issued where issue_id = %s;",(self.cissueID.get(),))
                con.commit()
                self.option_page()

        def UPI_page(self):#adding payments data to database
                self.mode = "UPI"
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=lambda: self.payments_page(self.money))
                #GETTING SCREEN INFO
                screen_width = self.win.winfo_width()
                screen_height = self.win.winfo_height()
                #MAKING LABEL ATTRIBUTES
                back_label_width = 500
                back_label_height = 300
                back_label_x = (screen_width - back_label_width) // 2
                back_label_y = (screen_height - back_label_height) // 2
                self.back_label1 = tk.Label(self.win, bg="#f3e5ab", relief="ridge", borderwidth=8, anchor="n")
                self.back_label1.place(x=back_label_x, y=back_label_y, width=back_label_width, height=back_label_height)
                #PLACING OR CODE
                self.qr_image = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\13.png")
                qr_label_x = back_label_x + (back_label_width - self.qr_image.width()) // 2
                qr_label_y = back_label_y + (back_label_height - self.qr_image.height()) // 2
                self.qr_label = tk.Label(self.win, image=self.qr_image)
                self.qr_label.place(x=qr_label_x, y=qr_label_y-20)
                self.scan = tk.Label(self.win, text=f"Scan this QR code and pay ₹{self.money}", bg="#f3e5ab", font=("Baskerville Old Face", 14), fg="#592b0a")
                self.scan.place(x=(screen_width - 400) // 2, y=back_label_y + back_label_height + 10-20-20-20, width=400)
                #OKAY BUTTON
                self.okay = tk.Button(self.win,bg="#d41311",text="Okay",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command= self.payments_database)
                self.okay.place(x=(screen_width - 400) // 2+155,y=back_label_y + back_label_height + 10,width=95,height=40)
                
        def library_card_database(self):#adding library card details to database
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                #LIBRARY CARD ID GENERATOR
                cur.fetchall()
                cur.execute("select name from customer_details where customer_id = %s;",(self.c1,))
                n = (sort(cur.fetchone()))
                _n = str(n[0])
                #GENERATING LIBRARY CARD ID
                self.libray_card_id = f"LIB-{datetime.datetime.now().strftime("%Y")}-{_n[0:2]}-{random.randint(1000,9999)}"
                cur.execute("insert into library_card_details values(%s,%s,%s,curdate(),curdate() + interval 1 year);",(self.c1,self.libray_card_id,n[0]))
                
        def payments_database(self):#adding payments details to database
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                #MESSAGE
                messagebox.showinfo("Payment Successful","Thank You for your payment you are being directed to home page.\nHave a nice day.")
                cur.execute("select name from customer_details where customer_id = %s",(self.c1,))
                _n = sort(cur.fetchone())
                cur.execute("insert into payments values(%s,%s,%s,%s,%s,curdate());",(self.c1,_n[0],self.money,self.mode,self.payment_type))
                con.commit()
                #UPDATING HAS CARD
                if self.pay1 == 1:
                        cur.execute("update customer_details set has_card = 'Yes' where customer_id = %s;",(self.c1,))
                        con.commit()
                        self.library_card_database()
                #UPDATING VALIDITY OF CARD
                if self.card ==1:
                        cur.execute("select valid_till from library_card_details where customer_id = %s;",(self.c1,))
                        valid_till = sort(cur.fetchone())
                        cur.fetchall()
                        cur.execute('update library_card_details set valid_till = DATE_ADD(%s, INTERVAL 1 YEAR) where library_card_id = %s;',(valid_till[0],self.lib_id[0]))
                        con.commit()
                self.option_page()

        def add_donate_options(self):#adding donate options
                self.num_donated_books +=1
                #JUGAAD
                if self.b==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b==-1:
                        self.c1=self.new_user_id.get()
                #FETCHING NAME
                cur.execute(f"select name from customer_details where customer_id = '{self.c1}';")
                name  = cur.fetchone()
                n = sort(name)
                #FETCHING BOOK ID
                cur.execute("select book_id from books;")
                f = sort(cur.fetchall())
                #CHECKING BOOK ID
                bid = random.randint(100,999)
                while(bid in f):
                        bid = random.randint(100,999)
                books = cur.fetchall()
                self.books = sort(books)
                #CHECKING DONATED BOOKS DO NOT EXISTED ALREADY
                if self.book_name1.get() not in self.books:
                        cur.execute("insert into donate_books values(%s,%s,%s,%s,NULL,curdate());",(self.book_name1.get(),self.author1.get(),self.year1.get(),n[0],)) 
                        cur.execute("insert into books values(%s,%s,%s,%s,NULL,NULL);",(bid,self.book_name1.get(),self.author1.get(),self.year1.get()))
                        con.commit()
                self.donate_books_page()

        def add_return_options(self):#updating books occupied table when + clicked
                cur.execute("delete from book_occupied where book_id = %s;",(self.book_id.get(),))
                con.commit()
                self.return_book_page()
                self.num_return_books +=1
        
        def remove_occupied_books(self):#updating books occupied table
                #MESSAGE
                messagebox.showinfo("Books Returned Successfully",f"""Thank You for returning {self.num_return_books} books.
Have a nice day. 
                """)
                cur.execute("delete from book_occupied where book_id = %s;",(self.book_id.get(),))
                con.commit()
                self.option_page()

        def add_entry_info_page(self):#adding entry widget in info page
                self.e = tk.Entry(self.win,width=30,insertbackground="#592b0a",insertwidth=3,borderwidth=5,bg="#f3e5ab",fg="#592b0a",relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.e.place(x=self.x,y=self.y+5)
                self.v += 1

        def edit_entry(self,widget):#editing info from info page
                #GETTING INFO OF WIDGET
                self.x = widget.winfo_x()
                self.y = widget.winfo_y()
                #DESTROYING WIDGET
                widget.destroy()
                self.go_back_button.destroy()
                #PLACING SAVE BUTTON
                self.save_button = tk.Button(self.win,text="Save",bg="#d41311",activebackground="#d41311",font=("Baskerville Old Face",14),fg="#f5f5dc",relief="raised",border=6,command=self.save_changes)
                self.save_button.place(x=590+10+5+45,y=555,width=90,height=40)
                #EDTING INFO
                if (self.y==self.user_name.winfo_y()):
                        self.new_name = tk.StringVar()
                        self.add_entry_info_page()
                        self.e.config(textvariable=self.new_name)
                        self._name = 1 #JUGAAD
                if (self.y==self.user_id.winfo_y()):
                        self.new_user_id = tk.StringVar()
                        self.add_entry_info_page()
                        self.e.config(textvariable=self.new_user_id)
                        self._id = 1 #JUGAAD
                if (self.y==self.user_pass.winfo_y()):
                        self.new_pass = tk.StringVar()
                        self.add_entry_info_page()
                        self.e.config(textvariable=self.new_pass)
                        self._pass = 1 #JUGAAD
                if (self.y==self.user_age.winfo_y()):
                        self.new_age = tk.IntVar()
                        self.add_entry_info_page()
                        self.e.config(textvariable=self.new_age)
                        self._age = 1 #JUGAAD
                if (self.y==self.user_address.winfo_y()):
                        self.new_address = tk.StringVar()
                        self.add_entry_info_page()
                        self.e.config(textvariable=self.new_address)
                        self._add = 1 #JUGAAD
                        
        def logout(self):#loging out 
                self.home_page()
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()          
                cur.fetchall()
                #UPDATING EXIT TIME
                cur.execute("update daily_log set exit_time = NOW() where customer_id = %s;",(self.c1,))
                con.commit()
                
        def save_changes(self):#saving changes
                if self._name == 1:
                        if self.new_name.get() !="":
                                cur.execute("update customer_details set name = %s  where name = %s;",(self.new_name.get(),self.n1[0]))
                                con.commit()

                if self._id == 1:
                        if self.new_user_id.get() !="":
                                cur.execute("update customer_details set customer_id = %s where customer_id = %s;",(self.new_user_id.get(),self.c1))
                                cur.execute("update password_table set customer_id = %s where customer_id = %s;",(self.new_user_id.get(),self.c1))
                                self.b = -1 #JUGAAD
                                con.commit()
                if self._pass == 1:
                        if self.new_pass.get() !="":
                                cur.execute("update password_table set user_password = %s where user_password = %s;",(self.new_pass.get(),self.pa[0]))
                                con.commit()
                if self._age == 1:
                        if self.a==[]:
                                a = ''
                        else:
                                a = self.a[0]
                        if self.new_age.get() != "":
                                cur.execute("update customer_details set age = %s where age = %s;",(str(self.new_age.get()),a))
                                con.commit()                                
                if self._add == 1:
                        if self.ad==[]:
                                ad = ''
                        else:
                                ad = self.ad[0]
                        if self.new_address.get() != "":
                                cur.execute("update customer_details set address = %s where address = %s;",(self.new_address.get(),ad))
                                con.commit()
                self.info_page() 
                
        def buy_card(self):#buying library card
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                #JUGAAD
                self.pay1 =1 
                self.payment_type = "Buy Card"
                self.back.config(command=self.option_page)
                #PLACING BACK LABEL
                self.back_label1 = tk.Label(self.win,bg="#f3e5ab",relief="ridge",borderwidth=8)
                self.back_label1.place(x=300-20,y=150,width=820,height=500)
                #PLACING CARD INFO
                self.card_info1 = tk.Label(self.win,text = "Introducing the Library Card",bg="#4f7942",font=("Baskerville Old Face",18,"bold"),fg="#f3e5ab",justify="center",wraplength=780,relief="raised",bd=8)
                self.card_info1.place(x=525,y=175,width=350,height=50)
                info = """Your gateway to a world of knowledge, adventure, and endless learning!
Imagine a year full of endless discoveries, where you can borrow as many books as you desire, explore different genres, and enrich your mind without any restrictions.
For just ₹1100 per year, the Library Card offers unlimited access to our vast collection of books, borrow as many books as you like for a full year! Additionally, get to read  research materials, and exclusive resources."""
                self.card_info = tk.Label(self.win,text = info,bg="#f3e5ab",font=("Baskerville Old Face",15,"bold"),fg="#592b0a",justify="center",wraplength=780)
                self.card_info.place(x=290,y=230,width=800,height=150)
                self.card_features1 = tk.Label(self.win,text = "Key Features:",bg="#4f7942",font=("Baskerville Old Face",18,"bold"),fg="#f3e5ab",justify="center",wraplength=780,relief="raised",bd=8)
                self.card_features1.place(x=590,y=390,width=200,height=50)
                features = """1. Unlimited Borrowing: Borrow as many times and, as many books as you wish to! 
        2. Priority Access: Get early access to newly added books.
        3. Online Portal: Reserve, renew, and manage your books anytime.
        4. Exclusive Discounts: Enjoy special discounts on events and workshops."""
                self.card_features = tk.Label(self.win,text = features,bg="#f3e5ab",font=("Baskerville Old Face",15,"bold"),fg="#592b0a",justify="center",wraplength=780)
                self.card_features.place(x=290,y=445,width=800)
                #BUY BUTTON
                self.buy_now_button = tk.Button(self.win,text="Buy Now",bg="#d41311",activebackground="#d41311",font=("Baskerville Old Face",14),fg="#f5f5dc",command=lambda: self.payments_page(1100),activeforeground="#f5f5dc",relief="raised")
                self.buy_now_button.place(x=640,y=570,height=40,width=100)

        def card_renewal(self):#card renewal
                #JUGAAD
                self.card = 1
                self.pay1 = -1
                self.payment_type = "Card Renewal"
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                if self.b == 1:
                        self.c1 = self.custID.get()
                if self.b == 0:
                        self.c1=self.c_id
                if self.b == -1: 
                        self.c1=self.new_user_id.get()
                #PLACING BACK LABEL
                self.back_label2 = tk.Label(self.win,bg="#f3e5ab",relief="ridge",borderwidth=8,anchor="n")
                self.back_label2.place(x=300-20+50+10,y=150+20,width=700,height=400)
                #LIBRARY CARD PLACE
                self.card_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\14.png")
                self.library_card = tk.Label(self.win,image=self.card_icon,bg="#f3e5ab")
                self.library_card.place(x=540,y=180+10)
                cur.fetchall()
                #FETCHING CARD DETAILS
                cur.execute("select library_card_id from library_card_details where customer_id = %s;",(self.c1,))
                self.lib_id = sort(cur.fetchone())
                self.libray_card_id_label = tk.Label(self.win,text=f"Library Card ID: {self.lib_id[0]}",bg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),fg="#592b0a")
                self.libray_card_id_label.place(x=490+5,y=400-5+10,width=400)
                cur.execute("select issue_date from library_card_details where customer_id = %s;",(self.c1,))
                issue_date = sort(cur.fetchone())
                self.issue_date = tk.Label(self.win,text=f"Issue Date: {issue_date[0]}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a")
                self.issue_date.place(x=400+80,y=435+10,width=200)
                cur.execute("select valid_till from library_card_details where customer_id = %s;",(self.c1,))
                valid_till = sort(cur.fetchone())
                self.issue_date = tk.Label(self.win,text=f"Valid Till: {valid_till[0]}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a")
                self.issue_date.place(x=600+20+100,y=435+10,width=200)
                #CARD RENEWAL BUTTON
                self.card_renewal_button = tk.Button(text="Renew Now",font=("Baskerville Old Face",16),bg="#d41311",fg="white",activebackground="#f3e5ab",relief="raised",bd=5,command=lambda: self.payments_page(1100))
                self.card_renewal_button.place(x=615,y=490+10,width=150,height=30)
                
        def due_days(self):#fetching due date of library card
                cur.fetchall()
                cur.execute("select book_id from book_issued;")
                _k = sort(cur.fetchall())
                for i in _k:
                        curdate = datetime.datetime.now().strftime("%Y-%m-%d")
                        cur.fetchall()
                        cur.execute("select return_date from book_issued where book_id = %s;",(i,))
                        _return_date = sort(cur.fetchone())
                        if curdate<_return_date[0]:
                                pass
                        elif curdate>_return_date[0]:
                                cur.fetchall()
                                cur.execute("update book_issued set due_days = DATEDIFF(%s,%s) where book_id = %s;",(curdate,_return_date[0],i))      
                                cur.execute("update book_issued set penalty = due_days*20 where book_id = %s;",(i,))      
                                con.commit()

        #MAIN FUNCTIONS:--> functions which acts as pages
        def __init__(self):
                #CREATING WINDOW
                self.win = tk.Tk()
                self.win.config(bg="#592b0a",cursor="hand2")
                self.win.title("NEXUS OF KNOWLEDGE")
                self.win.attributes('-fullscreen',True)
                #JUGAAD
                self.l = 0
                self.v = 0
                self._name = 0
                self._id = 0
                self._pass = 0
                self._age = 0
                self._add = 0
                self.num_donated_books = 1
                self.card = 0
                
        def show_msg_request(self):#shows message when book is requested
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                #FETCHING BOOK NAMES
                cur.execute("select book_name from books;")
                kitab = cur.fetchall()
                kitabe = sort(kitab)
                #CHECKING IF EXIST
                if self.book_name.get() not in kitabe:
                        messagebox.showinfo("Book Request Succesfull","""Your request has been submitted and 
desired book will be avaialable in a week
Thank You For Your Paitence.""")
                        #ADDING INFO TO DATABASE
                        cur.execute(f"select name from customer_details where customer_id = '{self.c1}'")
                        self.g = sort(cur.fetchone())
                        cur.execute(f"select gmail_id from customer_details where customer_id = '{self.c1}'")
                        self.h = sort(cur.fetchone())
                        cur.execute("insert into requested_books values (%s,%s,%s,%s,%s,NOW());",(self.book_name.get(),self.author.get(),self.year.get(),self.g[0],self.h[0]))
                        con.commit()
                        self.book_page()
                else:
                       messagebox.showwarning("Book Already Exist","The requested book already exist in our library kindly check again.")
                        
        def show_msg_table(self):#shows message when table is allocated
                #MESSAGE
                messagebox.showinfo("Table Alloted",f"""
Kindly proceed to table no. {self.table_no} your requested books will be brought to you shortly.
Thank You.""")
                cur.execute(f"update TABLE_OCCUPANCY set table_occupancy = 'occupied' where table_no = {self.table_no};")
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                #ADDING BOOKS TO DATABASE
                for i in self.books_chosen:
                        cur.execute("select book_id from books where book_name = %s;",(i,))
                        bid = sort(cur.fetchone())
                        cur.execute("insert into book_occupied values(%s,%s,%s,NOW(),NULL);",(bid[0],i,self.c1))
                        con.commit()
                self.option_page()

        def show_msg_cross(self):#shows message when cross button is pressed
                self.message = messagebox.askyesno("NEXUS OF KNOWLEGDE","""Do you want to exit?""")
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()          
                if self.message:
                        cur.fetchall()
                        #UPDATING EXIT TIME
                        cur.execute("update daily_log set exit_time = NOW() where customer_id = %s;",(self.c1,))
                        con.commit()
                        self.win.destroy()
                
        def basic_functions(self):#basic functions common to all pages
                #CROSS BUTTON 
                self.cross_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\5.png")
                self.cross = tk.Button(image=self.cross_icon,bg="#d41311",command=self.show_msg_cross,activebackground="#d41311")
                self.cross.place(x=1325,y=10,width=30,height=30)
                #BACK BUTTON
                self.back_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\3.png")
                self.back = tk.Button(self.win,bg="#f3e5ab",image=self.back_icon,command=self.home_page,activebackground="#f3e5ab")
                self.back.place(x=10,y=10,width=30,height=30)
                #HOME BUTTON
                self.home_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\2.png")
                self.home = tk.Button(self.win,bg="#f3e5ab",image=self.home_icon,command=self.option_page,activebackground="#f3e5ab")
                self.home.place(x=50,y=10,width=30,height=30)
                self.home.config(state="normal")

        def home_page(self):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.j = self.win.winfo_screenheight()
                self.k = self.win.winfo_screenwidth()
                self.win1 = self.win.winfo_height()
                self.win2 = self.win.winfo_width()
                #LABELS
                self.label = tk.Label(self.win,text='''WELCOME TO THE NEXUS OF KNOWLEDGE''',bg="#4F7942",font=("Baskerville Old Face",16,"bold"),fg="#f3e5ab",relief="raised",borderwidth=12,padx=20,pady=20)
                self.label.place(x=425,y=65)
                self.label_1= tk.Label(self.win,text='''Welcome to the Nexus of Knowledge, a cutting-edge sanctuary for the curious mind. 
Our futuristic library is designed to inspire and elevate your intellectual pursuits. 
As you enter, you'll discover a world where advanced technology seamlessly integrates with a serene and inviting atmosphere.
Explore our extensive collection of books spanning all genres, from timeless classics to the latest scientific breakthroughs. 
Our shelves are stocked with everything from gripping novels and historical accounts to comprehensive encyclopedias and innovative research.
Here, your curiosity is our priority, and every corner is crafted to ignite your passion for learning. 
Welcome to the future of libraries.'''
,bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",relief="raised",borderwidth=8,padx=10,pady=10,justify="center")
                self.label_1.place(x=80,y=250,width=1200)
                #SIGN UP BUTTON
                self.sign_up_button = tk.Button(self.win,text="Sign Up",bg="#4F7942",font=("Baskerville Old Face",14),height=2,width=20,fg="#f3e5ab",relief="raised",borderwidth=8,command=self.sign_up)
                self.sign_up_button.place(x=300-2,y=550,anchor="w",width = 202, height=64)
                #SIGN IN BUTTON
                self.sign_in_button = tk.Button(self.win,bg="#4F7942",font=("Baskerville Old Face",14),text="Sign In",height=2,width=20,fg="#f3e5ab",relief="raised",borderwidth=8,command=self.sign_in)
                self.sign_in_button.place(x=900-12,y=550,anchor="w",width = 202, height=64)      
                #CROSS BUTTON
                self.cross_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\5.png")  
                self.cross = tk.Button(image=self.cross_icon,bg="#d41311",command=self.show_msg_cross)
                self.cross.place(x=1325,y=10,width=30,height=30)
                self.win.mainloop()
                
        def sign_up(self):#just as the name suggest
                #JUGAAD
                self.w=0
                self.b=0
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                #LABEL
                self.info = tk.Label(self.win,text="Sign-Up Information",bg="#f3e5ab",font=("Baskerville Old Face",18),relief="ridge",borderwidth=8,fg="#592b0a",anchor="n")
                self.info.place(x=290,y=225+20,width=800,height=300)
                #LABLES
                self.label_name = tk.Label(self.info,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Name:",fg="#592b0a")
                self.label_name.place(x=0,y=40)
                self.label_age = tk.Label(self.info,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Age:",fg="#592b0a")
                self.label_age.place(x=0,y=80,width=70)
                self.phone_no = tk.Label(self.info,bg="#f3e5ab",font=("Baskerville Old Face",16),width=13,height=1,relief="flat",text="Phone Number:",fg="#592b0a")
                self.phone_no.place(x=0,y=120) 
                self.address = tk.Label(self.info,bg="#f3e5ab",font=("Baskerville Old Face",16),width=8,height=1,relief="flat",text="Address:",fg="#592b0a")
                self.address.place(x=0,y=160) 
                self.gmail_id = tk.Label(self.info,bg="#f3e5ab",font=("Baskerville Old Face",16),width=8,height=1,relief="flat",text="Email Id:",fg="#592b0a")
                self.gmail_id.place(x=0,y=200)
                #VARIABLES
                self.name = tk.StringVar()
                self.AGE = tk.IntVar()
                self.phn = tk.IntVar()
                self.ADD = tk.StringVar()
                self.gmail = tk.StringVar()
                #ENTRY
                self.n = tk.Entry(self.info,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.name,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.n.place(x=189,y=44)
                self.age = tk.Spinbox(self.info,width=59,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.AGE,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"),from_=0,to=120,wrap=True)
                self.age.place(x=189,y=83)
                self.phone = tk.Entry(self.info,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.phn,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.phone.delete(0)
                self.phone.place(x=189,y=123)
                self.add = tk.Entry(self.info,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.ADD,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.add.place(x=189,y=165)
                self.gmailID = tk.Entry(self.info,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.gmail,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.gmailID.place(x=189,y=203)
                #SUBMIT BUTTON
                self.submit1 = tk.Button(self.info,bg="#d41311",text="Submit",font=("Baskerville Old Face",16),fg="white",command=self.sign_up_submit_function,relief="raised",bd=5)
                self.submit1.place(x=685,y=245,width=90,height=30)
                
        def sign_in(self):#just as the name suggest
                #JUGAAD
                self.b=1
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.j = self.win.winfo_screenheight()
                self.k = self.win.winfo_screenwidth()
                self.win1 = self.win.winfo_height()
                self.win2 = self.win.winfo_width()
                #LABLES
                self.info = tk.Label(self.win,text="Sign-In Information",bg="#f3e5ab",font=("Baskerville Old Face",18),relief="ridge",borderwidth=8,fg="#592b0a",anchor="n")
                self.info.place(x=270,y=300,width=800,height=170)
                self.cid = tk.Label(self.info,bg="#f3e5ab",width=10,height=1,font=("Baskerville Old Face",16),relief="flat",text="Customer ID:",fg="#592b0a")
                self.cid.place(x=0,y=40)
                self.passw = tk.Label(self.info,bg="#f3e5ab",width=7,height=1,font=("Baskerville Old Face",16),relief="flat",text="Password:",fg="#592b0a")
                self.passw.place(x=0,y=80)
                #VARIABLES
                self.custID = tk.StringVar()
                self.password = tk.StringVar()
                #ENTRY
                self.CUSTOMER_ID = tk.Entry(self.info,width=70,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.custID,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.CUSTOMER_ID.place(x=135,y=44)
                self.PASSWORD = tk.Entry(self.info,width=70,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.password,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"),)
                self.PASSWORD.place(x=135,y=84)
                #BUTTONS
                self.s = False
                self.submit2 = tk.Button(self.info,bg="#d41311",text="Submit",font=("Baskerville Old Face",16),fg="white",command=self.sign_in_submit_function,relief="raised",bd=5)
                self.submit2.place(x=685,y=120,width=90,height=30)
                   
        def option_page(self):#just as the name suggest '
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                #JUGAAD 
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                #ALL OPTIONS
                self.option_msg = tk.Label(self.win,bg="#4F7942",text="Select what do you want to do:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                self.option_msg.place(x=505,y=80,width=350,height=60)
                self.read_book = tk.Button(self.win,text="Read Book",bg="#f3e5ab",font=("Baskerville Old Face",19,"bold"),fg="#592b0a",relief="raised",bd=8,anchor="n",command=self.book_page)
                self.read_book.place(x=550,y=200,width=270,height=50)
                self.return_book = tk.Button(self.win,text="Return Book",bg="#f3e5ab",font=("Baskerville Old Face",19,"bold"),fg="#592b0a",relief="raised",bd=8,anchor="n",command=self.return_book_page)
                self.return_book.place(x=550,y=300,width=270,height=50)
                self.issue_book = tk.Button(self.win,text="Issue Book",bg="#f3e5ab",font=("Baskerville Old Face",19,"bold"),fg="#592b0a",relief="raised",bd=8,anchor="n",command=self.issue_book_page)
                self.issue_book.place(x=550,y=400,width=270,height=50)
                self.return_issued_book = tk.Button(self.win,text="Return Issued Book",bg="#f3e5ab",font=("Baskerville Old Face",19,"bold"),fg="#592b0a",relief="raised",bd=8,anchor="n",command=self.return_issued_book_page)
                self.return_issued_book.place(x=550,y=500,width=270,height=50)
                self.donate_books = tk.Button(self.win,text="Donate Books",bg="#f3e5ab",font=("Baskerville Old Face",19,"bold"),fg="#592b0a",relief="raised",bd=8,anchor="n",command=self.donate_books_page)
                self.donate_books.place(x=550,y=600,width=270,height=50)
                #USER INFO
                self.f8 = tk.Frame(bg="#f3e5ab",relief="raised",bd=10)
                self.f8.place(x=1050-20,y=680-20+5+5,height=63+15,width=300-10+20+10)
                self.login_name = tk.Label(self.f8,text=f"",bg="#f3e5ab",font=("Baskerville Old Face",12,"bold"),fg="#592b0a",anchor="nw")
                self.login_name.place(x=5,y=0+5+2-5,height=30,width=300-10)
                self.login_id = tk.Label(self.f8,text="",bg="#f3e5ab",font=("Baskerville Old Face",12,"bold"),fg="#592b0a",anchor="nw")
                self.login_id.place(x=5,y=25+5+2-5,height=30,width=300-10)
                #INFO BUTTON
                self.info_icon = tk.PhotoImage(file="C:\\Users\\Dutta Family\\Desktop\\Aakar\\New folder\\9.png")
                self.info_button = tk.Button(self.win,image=self.info_icon,bg="#f3e5ab",activebackground="#f3e5ab",command=self.info_page)
                self.info_button.place(x=90,y=10,width=30,height=30)
                #LOGOUT BUTTON
                self.logout_button = tk.Button(self.win,text="Logout",bg="#d41311",activebackground="#d41311",command=self.logout,font=("Baskerville Old Face",14),fg="#f5f5dc",relief="raised",border=6,activeforeground="#f5f5dc")
                self.logout_button.place(x=25,y=680-20+5+5+40,height=40,width=150)
                #CARD RENEWAL
                cur.fetchall()
                cur.execute("select has_card from customer_details where customer_id = %s;",(self.c1,))
                self._has_card = sort(cur.fetchone())
                if self._has_card[0] == "No":
                        self.card_renewal_button = tk.Button(self.win,text="Buy Card",bg="#f3e5ab",activebackground="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a",command=self.buy_card,relief="raised",border=6)
                        self.card_renewal_button.place(x=25,y=680-20,height=40,width=150)
                if self._has_card[0] == "Yes":
                        self.card_renewal_button = tk.Button(self.win,text="Card Renewal",bg="#f3e5ab",activebackground="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a",command=self.card_renewal,relief="raised",border=6)
                        self.card_renewal_button.place(x=25,y=680-20,height=40,width=150)
                #GETTING INFO
                cur.execute(f"select gmail_id from customer_details where customer_id = '{self.c1}'")
                self.gmail1 = sort(cur.fetchone())
                gmail1 = self.gmail1[0]
                self.login_name.config(text=f"User's Name: {self.c1}")
                self.login_id.config(text=f"Login ID: {gmail1}")

        def book_page(self):#just as the name suggest
                #JUGAAD
                self._w=0
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                #LABEL
                self.head = tk.Label(bg="#4F7942",text="""Here are the list of various niches of books present here:""",fg="#f3e5ab",font=("Baskerville Old Face",18),relief="raised",borderwidth=12,anchor="center")
                self.head.place(x=300-20,y=100,width=820,height=70)
                #VARIABLES FOR CHECKBUTTON
                self.rb1 = tk.StringVar()
                self.rb2 = tk.StringVar()
                self.rb3 = tk.StringVar()
                self.rb4 = tk.StringVar()
                self.rb5 = tk.StringVar()
                self.rb6 = tk.StringVar()
                self.rb7 = tk.StringVar()
                #CHECKBUTTONS FOR BOOKS  
                self.r1 = tk.Checkbutton(self.win,text="Classic Literature",variable=self.rb1,bg="#f3e5ab",fg="#592b0a",onvalue="Classic Literature",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Classic Literature';")
                num_cl = sort(cur.fetchone())
                t1 = ToolTip(self.r1,f"No. Of Books Available: {num_cl[0]}")
                self.r1.deselect()
                self.r1.place(x=300-20,y=200+25,width=220,height=50)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Science Fiction and Fantasy';")
                num_sct = sort(cur.fetchone())
                self.r2 = tk.Checkbutton(self.win,text="Science Fiction & Fantasy",bg="#f3e5ab",fg="#592b0a",variable=self.rb2,onvalue="Science Fiction & Fantasy",offvalue="nothing",font=("Baskerville Old Face",11,"bold"),relief="raised",borderwidth=7)
                t2 = ToolTip(self.r2,f"No. Of Books Available: {num_sct[0]}")
                self.r2.deselect()
                self.r2.place(x=300-20,y=300+25,width=220,height=50)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Mystery and Thriller';")
                num_mt = sort(cur.fetchone())
                self.r3 = tk.Checkbutton(self.win,text="Mystery & Thriller",bg="#f3e5ab",fg="#592b0a",variable=self.rb3,onvalue="Mystery & Thriller",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                t3 = ToolTip(self.r3,f"No. Of Books Available: {num_mt[0]}")
                self.r3.deselect()
                self.r3.place(x=300-20,y=400+25,width=220,height=50)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Historical Fiction';")
                num_h = sort(cur.fetchone())
                self.r4 = tk.Checkbutton(self.win,text="Historical Fiction",bg="#f3e5ab",fg="#592b0a",variable=self.rb4,onvalue="Historical Fiction",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                t4 = ToolTip(self.r4,f"No. Of Books Available: {num_h[0]}")
                self.r4.deselect()
                self.r4.place(x=900-20,y=200+25,width=220,height=50)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Non-Fiction';")
                num_nf = sort(cur.fetchone())
                self.r5 = tk.Checkbutton(self.win,text="Non-Fiction",bg="#f3e5ab",fg="#592b0a",variable=self.rb5,onvalue="Non-Fiction",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                t5 = ToolTip(self.r5,f"No. Of Books Available: {num_nf[0]}")
                self.r5.deselect()
                self.r5.place(x=900-20,y=300+25,width=220,height=50)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Philosophy and Self Help';")
                num_phs = sort(cur.fetchone())
                self.r6 = tk.Checkbutton(self.win,text="Philosophy & Self Help",bg="#f3e5ab",fg="#592b0a",variable=self.rb6,onvalue="Philosophy & Self Help",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                t6 = ToolTip(self.r6,f"No. Of Books Available: {num_phs[0]}")
                self.r6.deselect()
                self.r6.place(x=900-20,y=400+25,width=220,height=50)
                cur.fetchall()
                cur.execute("select count(book_id) from books where book_niche = 'Poetry';")
                num_p = sort(cur.fetchone())
                self.r7 = tk.Checkbutton(self.win,text="Poetry",bg="#f3e5ab",fg="#592b0a",variable=self.rb7,onvalue="Poetry",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                t7 = ToolTip(self.r7,f"No. Of Books Available: {num_p[0]}")
                self.r7.deselect()
                self.r7.place(x=600-20,y=500+25,width=220,height=50)
                # NEXT BUTTON
                self.forward_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\6.png")
                self.forward = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.select_book)
                self.forward.place(x=1020,y=600,width=80,height=40)
                
        def request_book_page(self):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.book_page)
                #SORRY LABEL
                self.sorry = tk.Label(bg="#4F7942",text="Sorry for your in-convience please enter the details of your desired book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                self.sorry.place(x=340,y=180,width=700,height=70)
                #REQUESTED BOOK DETAILS
                self.bd = tk.Label(self.win,text="Book Details",bg="#f3e5ab",font=("Baskerville Old Face",18),relief="ridge",borderwidth=8,fg="#592b0a",anchor="n")
                self.bd.place(x=300-20,y=280,width=820,height=205)
                #LABLES
                self.label_book_name = tk.Label(self.bd,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Tilte Of The Book:",fg="#592b0a")
                self.label_book_name.place(x=0,y=40,width=180)
                self.label_author = tk.Label(self.bd,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Author Name:",fg="#592b0a")
                self.label_author.place(x=0,y=80,width=140)
                self.label_year = tk.Label(self.bd,bg="#f3e5ab",font=("Baskerville Old Face",16),width=13,height=1,relief="flat",text="Year of Publication:",fg="#592b0a")
                self.label_year.place(x=0,y=120,width=190) 
                #VARIABLES
                self.book_name = tk.StringVar()
                self.author = tk.StringVar()
                self.year = tk.StringVar()
                #ENTRY
                self.bn = tk.Entry(self.bd,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.book_name,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.bn.place(x=189,y=44)
                self.an = tk.Entry(self.bd,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.author,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.an.place(x=189,y=83)
                self.yop = tk.Entry(self.bd,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.year,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.yop.place(x=189,y=123)
                self.submit3 = tk.Button(self.bd,bg="#d41311",text="Request Book",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command=self.show_msg_request)
                self.submit3.place(x=640,y=155,width=150,height=30)

        def select_book(self):#just as the name suggest
                #TO GET USER CHOSEN NICHES
                self.choices = [self.rb1.get(),self.rb2.get(),self.rb3.get(),self.rb4.get(),self.rb5.get(),self.rb6.get(),self.rb7.get()]
                self.select_values_lb1 = []
                self.select_values_lb2 = []
                self.select_values_lb3 = []
                self.select_values_lb4 = []
                self.select_values_lb5 = []
                self.select_values_lb6 = []
                self.select_values_lb7 = []
                #CHOOSING
                for i in self.choices:
                        if i == "Classic Literature" :
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Classic Literature Section \nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 1
                                self.f1 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f1.place(x=380, y=210)
                                #LISTBOX 1
                                self.lb1 = tk.Listbox(self.f1, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.classic_literature:
                                        self.lb1.insert(tk.END, _i)
                                self.lb1.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f1, orient="vertical", command=self.lb1.yview,bg="#f3e5ab")
                                self.lb1.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXt BUTTON
                                self.next1 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb1)
                                self.next1.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)
                                
                        if i == "Science Fiction & Fantasy" :
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Science Fiction & Fantasy Section \nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 2
                                self.f2 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f2.place(x=380, y=210)
                                #LISTBOX 2
                                self.lb2 = tk.Listbox(self.f2, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.Science_Fiction_Fantasy:
                                        self.lb2.insert(tk.END, _i)
                                self.lb2.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f2, orient="vertical", command=self.lb2.yview,bg="#f3e5ab")
                                self.lb2.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXT BUTTON
                                self.next2 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb2)
                                self.next2.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)

                        if i =="Mystery & Thriller":
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Mystery & Thriller Section \nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 3
                                self.f3 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f3.place(x=380, y=210)
                                #LISTBOX 3
                                self.lb3 = tk.Listbox(self.f3, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.Mystery_and_Thriller:
                                        self.lb3.insert(tk.END, _i)
                                self.lb3.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f3, orient="vertical", command=self.lb3.yview,bg="#f3e5ab")
                                self.lb3.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXT BUTTON
                                self.next3 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb3)
                                self.next3.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)

                        if i == "Historical Fiction":
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Historical Fiction Section\nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 4
                                self.f4 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f4.place(x=380, y=210)
                                #LISTBOX 4
                                self.lb4 = tk.Listbox(self.f4, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.Historical_Fiction:
                                        self.lb4.insert(tk.END, _i)
                                self.lb4.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f4, orient="vertical", command=self.lb4.yview,bg="#f3e5ab")
                                self.lb4.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXT BUTTON
                                self.next4 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb4)
                                self.next4.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)

                        if i == "Non-Fiction":
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Non-Fiction Section\nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 5
                                self.f5 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f5.place(x=380, y=210)
                                #LISTBOX 5
                                self.lb5 = tk.Listbox(self.f5, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.Non_Fiction:
                                        self.lb5.insert(tk.END, _i)
                                self.lb5.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f5, orient="vertical", command=self.lb5.yview,bg="#f3e5ab")
                                self.lb5.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXT BUTTON
                                self.next5 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb5)
                                self.next5.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)

                        if i == "Philosophy & Self Help":
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Philosophy & Self Help Section\nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 6
                                self.f6 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f6.place(x=380, y=210)
                                #LISTBOX 6
                                self.lb6 = tk.Listbox(self.f6, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.Philosophy_and_Self_Help:
                                        self.lb6.insert(tk.END, _i)
                                self.lb6.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f6, orient="vertical", command=self.lb6.yview,bg="#f3e5ab")
                                self.lb6.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXT BUTTON
                                self.next6 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb6)
                                self.next6.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)

                        if i == "Poetry":
                                for i in self.win.winfo_children():
                                        i.destroy()
                                self.basic_functions()
                                self.back.config(command=self.book_page)
                                #TOP LABLE
                                self.book_niche = tk.Label(bg="#4F7942",text="Poetry Section \nNow Select Your Desired Book:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                                self.book_niche.place(x=480,y=80,width=400,height=75)
                                #FRAME 7
                                self.f7 = tk.Frame(self.win, height=500, width=600,bg="#592b0a")
                                self.f7.place(x=380, y=210)
                                #LISTBOX 7
                                self.lb7 = tk.Listbox(self.f7, selectmode="multiple", activestyle="dotbox",fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#592b0a",selectforeground="#f3e5ab")
                                for _i in self.Poetry:
                                        self.lb7.insert(tk.END, _i)
                                self.lb7.place(x=0, y=0, height=500, width=580)
                                #SCROLLBAR
                                self.sc = tk.Scrollbar(self.f7, orient="vertical", command=self.lb7.yview,bg="#f3e5ab")
                                self.lb7.config(yscrollcommand=self.sc.set)
                                self.sc.place(x=579,y=0,height=500,width=20)
                                #NEXT BUTTON
                                self.next7 = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.selected_book_confirmation_lb7)
                                self.next7.place(x=1020,y=670,width=80,height=40)
                                # DIDN'T FIND YOUR DESIRED BOOK? BUTTON 
                                self.dfydb_l = tk.Button(self.win,text="Didn't Find Your Desired Book?",font=("Baskerville Old Face",14,"bold"),bg="#4F7942",fg="#f3e5ab",command=self.request_book_page)
                                self.dfydb_l.place(x=40,y=690)

        def selected_book_confirmation_lb1(self):#GETTING BOOK SELECTIONS
                if self.lb1.winfo_exists():
                        self.select_indices_lb1 = self.lb1.curselection()
                        self.select_values_lb1 = [self.lb1.get(i) for i in self.select_indices_lb1]
                        self.book_confirmation_page()

        def selected_book_confirmation_lb2(self):#GETTING BOOK SELECTIONS
                if self.lb2.winfo_exists():
                        self.select_indices_lb2 = self.lb2.curselection()
                        self.select_values_lb2 = [self.lb2.get(i) for i in self.select_indices_lb2]
                        self.book_confirmation_page()

        def selected_book_confirmation_lb3(self):#GETTING BOOK SELECTIONS
                if self.lb3.winfo_exists():
                        self.select_indices_lb3 = self.lb3.curselection()
                        self.select_values_lb3 = [self.lb3.get(i) for i in self.select_indices_lb3]
                        self.book_confirmation_page()

        def selected_book_confirmation_lb4(self):#GETTING BOOK SELECTIONS
                if self.lb4.winfo_exists():
                        self.select_indices_lb4 = self.lb4.curselection()
                        self.select_values_lb4 = [self.lb4.get(i) for i in self.select_indices_lb4]
                        self.book_confirmation_page()

        def selected_book_confirmation_lb5(self):#GETTING BOOK SELECTIONS
                if self.lb5.winfo_exists():
                        self.select_indices_lb5 = self.lb5.curselection()
                        self.select_values_lb5 = [self.lb5.get(i) for i in self.select_indices_lb5]
                        self.book_confirmation_page()

        def selected_book_confirmation_lb6(self):#GETTING BOOK SELECTIONS
                if self.lb6.winfo_exists():
                        self.select_indices_lb6 = self.lb6.curselection()
                        self.select_values_lb6 = [self.lb6.get(i) for i in self.select_indices_lb6]
                        self.book_confirmation_page()

        def selected_book_confirmation_lb7(self):#GETTING BOOK SELECTIONS
                if self.lb7.winfo_exists():
                        self.select_indices_lb7 = self.lb7.curselection()
                        self.select_values_lb7 = [self.lb7.get(i) for i in self.select_indices_lb7]
                        self.book_confirmation_page()

        def recepit_page_issue_book(self):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1: 
                        self.c1=self.new_user_id.get()
                #LABEL
                self.back_label1 = tk.Label(self.win,bg="#f3e5ab",relief="ridge",borderwidth=8,anchor="n")
                self.back_label1.place(x=300-20,y=150+30,width=820,height=500-100)
                self.title = tk.Label(self.win,text="Libary Receipt",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.title.place(x=590,y=160+35,width=200)
                #GENERATING RECEIPT ID
                receipt_id = f"REC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.receipt_no = tk.Label(self.win,text=f"Receipt No: {receipt_id}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_no.place(x=440,y=200+35,width=500)
                cur.fetchall()
                cur.execute(f"select name from customer_details where customer_id = '{self.c1}'")
                n = sort(cur.fetchone())
                #GETTING INFO
                self.receipt_name = tk.Label(self.win,text=f"Customer Name: {n[0]}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_name.place(x=440,y=225+35,width=500)
                self.receipt_custid = tk.Label(self.win,text=f"Customer ID: {self.c1}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_custid.place(x=440,y=250+35,width=500)
                self.back.config(command=self.issue_book_page)
                self.receipt_DOI = tk.Label(self.win,text=f"Date Of Issue: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_DOI.place(x=440,y=275+35,width=500)
                self.books_chosen_label = tk.Label(self.win,text="Books Chosen:",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.books_chosen_label.place(x=590,y=300+35,width=200)
                self.books_chosen_listbox = tk.Listbox(self.win,fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),selectbackground="#f3e5ab",selectforeground="#592b0a",activestyle="none")
                self.books_chosen_listbox.place(x=440,y=325+35,width=500,height=100)
                s_no = 0
                for i in self.books_chosen:
                        s_no+=1
                        j = f"{str(s_no)}. {i}"
                        self.books_chosen_listbox.insert(tk.END, j)
                self.sc = tk.Scrollbar(self.win, orient="vertical", command=self.books_chosen_listbox.yview,bg="#f3e5ab")
                self.books_chosen_listbox.config(yscrollcommand=self.sc.set)
                self.sc.place(x=940+10,y=325+35,height=100)
                self.total_books = tk.Label(self.win,text=f"Total Books Issued: {s_no}",bg="#f3e5ab",font=("Baskerville Old Face",14,"bold"),fg="#592b0a")
                self.total_books.place(x=590,y=425+35,width=200)
                #NOTES
                self.note = tk.Label(self.win,text="Note: Return books on time (within 10 days) to avoid late fees.\nLate fee: ₹20/day/book. Lost Book: ₹100/book",bg="#f3e5ab",font=("Baskerville Old Face",12),fg="#d41311")
                self.note.place(x=490,y=450+35,width=400)
                self.thank_you = tk.Label(self.win,text="Thank you for using our library!",bg="#f3e5ab",font=("Baskerville Old Face",12),fg="#4F7942")
                self.thank_you.place(x=490,y=500+35,width=400)
                #BUTTON
                self.okay_button = tk.Button(self.win,bg="#d41311",text="Okay",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command=self.option_page)
                self.okay_button.place(x=650,y=500+35+40+20,width=80,height=40)

        def book_confirmation_page(self):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions() 
                self.back.config(command=self.book_page)     
                self.books_chosen = []
                #CONFIRM MSESSAGE  
                self.confirm_msg = tk.Label(bg="#4F7942",text="You have Chosen These Books:",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                self.confirm_msg.place(x=492,y=80,width=400,height=75)
                #CONFIRM CHOICES
                self.final_choices = self.select_values_lb1 + self.select_values_lb2 + self.select_values_lb3 + self.select_values_lb4 + self.select_values_lb5 + self.select_values_lb6 + self.select_values_lb7
                self.final_choices_listbox = tk.Listbox(self.win,fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),relief="flat",bd=10,selectbackground="#f3e5ab",selectforeground="#592b0a",activestyle="none")
                for i in self.final_choices:
                        if i in self.classic_literature:
                                j = i + " (Classic literature)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                        if i in self.Mystery_and_Thriller:
                                j = i + " (Mystery & Thriller)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                        if i in self.Science_Fiction_Fantasy:
                                j = i + " (Science Fiction & Fantasy)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                        if i in self.Historical_Fiction:
                                j = i + " (Historical Fiction)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                        if i in self.Non_Fiction:
                                j = i + " (Non Fiction)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                        if i in self.Philosophy_and_Self_Help:
                                j = i + " (Philosophy and Self Help)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                        if i in self.Poetry:
                                j = i + " (Poetry)\n"
                                self.final_choices_listbox.insert(tk.END, j)
                                self.books_chosen.append(i)
                self.final_choices_listbox.place(x=330, y=200, height=500, width=700)
                #SCROLLBAR
                self.sc = tk.Scrollbar(self.win, orient="vertical", command=self.final_choices_listbox.yview,bg="#f3e5ab")
                self.final_choices_listbox.config(yscrollcommand=self.sc.set)
                self.sc.place(x=955+10+40+10,y=200,height=501)
                #CONFIRM BUTTON
                self.confirm1 = tk.Button(self.win,bg="#d41311",text="Confirm",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command=self.show_msg_table)
                self.confirm1.place(x=1020+40,y=660,width=95,height=40)
                #JUGAAD
                if self._w==1:
                        self.confirm1 = tk.Button(self.win,bg="#d41311",text="Confirm",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command=self.issue_book_confirm_page)
                        self.confirm1.place(x=1020+40,y=660,width=95,height=40)
                elif self._w==0:
                        self.confirm1 = tk.Button(self.win,bg="#d41311",text="Confirm",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command=self.show_msg_table)
                        self.confirm1.place(x=1020+40,y=660,width=95,height=40)
        
        def return_book_page(self):#just as the name suggest
                self.num_return_books = 1
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                #ENTER MESSAGE
                self.enter_msg = tk.Label(self.win,bg="#4F7942",text="""Enter the name of the books you want to return:""",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                self.enter_msg.place(x=450,y=180,width=480,height=65)
                self.bd2 = tk.Label(self.win,text="Book Details",bg="#f3e5ab",font=("Baskerville Old Face",18),relief="ridge",borderwidth=8,fg="#592b0a",anchor="n")
                self.bd2.place(x=300-20,y=280+40,width=820,height=205-50)
                #LABLES
                self.label_book_name2 = tk.Label(self.bd2,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Tilte Of The Book:",fg="#592b0a")
                self.label_book_name2.place(x=0,y=40,width=180)
                self.label_book_id = tk.Label(self.bd2,bg="#f3e5ab",font=("Baskerville Old Face",16),width=13,height=1,relief="flat",text="Book ID:",fg="#592b0a")
                self.label_book_id.place(x=0,y=80,width=100) 
                #VARIABLES
                self.book_name2 = tk.StringVar()
                self.book_id = tk.IntVar()
                #ENTRY
                self.bn2 = tk.Entry(self.bd2,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.book_name2,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.bn2.place(x=189,y=44)
                self.bid2 = tk.Entry(self.bd2,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.book_id,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.bid2.place(x=189,y=83)
                self.bid2.delete(0)
                #CONFIRM BUTTON
                self.CONFIRM2 = tk.Button(text="Continue",font=("Baskerville Old Face",16),bg="#d41311",fg="white",command=self.remove_occupied_books,activebackground="#f3e5ab",relief="raised",bd=5)
                self.CONFIRM2.place(x=620,y=490,width=150,height=30)
                #ADD BUTTON
                self.add_icon2 = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\7.png")
                self.add2 = tk.Button(self.win,image=self.add_icon2,bg="#f3e5ab",command=self.add_return_options,activebackground="#f3e5ab")
                self.add2.place(x=1045,y=425,width=32,height=32)

        def issue_book_page(self):#just as the name suggest
                #JUGAAD
                self._w=1
                self.pay1= 0
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                cur.fetchall()
                cur.execute("select has_card from customer_details where customer_id = %s;",(self.c1,))
                self._has_card1 = sort(cur.fetchone())
                #CHECKING IF HAS CARD OR NOT
                if self._has_card1[0] == "Yes":
                        for i in self.win.winfo_children():
                                i.destroy()
                        self.basic_functions()
                        self.back.config(command=self.option_page)
                        self.head = tk.Label(bg="#4F7942",text="""Here are the list of various niches of books present here: (You can choose one or more than one)""",fg="#f3e5ab",font=("Baskerville Old Face",15),relief="raised",borderwidth=12,anchor="center")
                        self.head.place(x=300-20,y=100,width=820,height=70)
                        #VARIABLES FOR CHECKBUTTON
                        self.rb1 = tk.StringVar()
                        self.rb2 = tk.StringVar()
                        self.rb3 = tk.StringVar()
                        self.rb4 = tk.StringVar()
                        self.rb5 = tk.StringVar()
                        self.rb6 = tk.StringVar()
                        self.rb7 = tk.StringVar()
                        #CHECKBUTTONS FOR BOOKS  
                        self.r1 = tk.Checkbutton(self.win,text="Classic Literature",variable=self.rb1,bg="#f3e5ab",fg="#592b0a",onvalue="Classic Literature",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                        t1 = ToolTip(self.r1,"No. Of Books Available: 9328")
                        self.r1.deselect()
                        self.r1.place(x=300-20,y=200+25,width=220,height=50)
                        self.r2 = tk.Checkbutton(self.win,text="Science Fiction & Fantasy",bg="#f3e5ab",fg="#592b0a",variable=self.rb2,onvalue="Science Fiction & Fantasy",offvalue="nothing",font=("Baskerville Old Face",11,"bold"),relief="raised",borderwidth=7)
                        t2 = ToolTip(self.r2,"No. Of Books Available: 3455")
                        self.r2.deselect()
                        self.r2.place(x=300-20,y=300+25,width=220,height=50)
                        self.r3 = tk.Checkbutton(self.win,text="Mystery & Thriller",bg="#f3e5ab",fg="#592b0a",variable=self.rb3,onvalue="Mystery & Thriller",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                        t3 = ToolTip(self.r3,"No. Of Books Available: 9873")
                        self.r3.deselect()
                        self.r3.place(x=300-20,y=400+25,width=220,height=50)
                        self.r4 = tk.Checkbutton(self.win,text="Historical Fiction",bg="#f3e5ab",fg="#592b0a",variable=self.rb4,onvalue="Historical Fiction",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                        t4 = ToolTip(self.r4,"No. Of Books Available: 1334")
                        self.r4.deselect()
                        self.r4.place(x=900-20,y=200+25,width=220,height=50)
                        self.r5 = tk.Checkbutton(self.win,text="Non-Fiction",bg="#f3e5ab",fg="#592b0a",variable=self.rb5,onvalue="Non-Fiction",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                        t5 = ToolTip(self.r5,"No. Of Books Available: 6435")
                        self.r5.deselect()
                        self.r5.place(x=900-20,y=300+25,width=220,height=50)
                        self.r6 = tk.Checkbutton(self.win,text="Philosophy & Self Help",bg="#f3e5ab",fg="#592b0a",variable=self.rb6,onvalue="Philosophy & Self Help",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                        t6 = ToolTip(self.r6,"No. Of Books Available: 7654")
                        self.r6.deselect()
                        self.r6.place(x=900-20,y=400+25,width=220,height=50)
                        self.r7 = tk.Checkbutton(self.win,text="Poetry",bg="#f3e5ab",fg="#592b0a",variable=self.rb7,onvalue="Poetry",offvalue="nothing",font=("Baskerville Old Face",12,"bold"),relief="raised",borderwidth=7)
                        t7 = ToolTip(self.r7,"No. Of Books Available: 6534")
                        self.r7.deselect()
                        self.r7.place(x=600-20,y=500+25,width=220,height=50)
                        # NEXT BUTTON
                        self.forward_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\6.png")
                        self.forward = tk.Button(self.win,bg="#d41311",image=self.forward_icon,activebackground="Red",relief="raised",bd=5,command=self.select_book)
                        self.forward.place(x=1020,y=600,width=80,height=40)
                #IF NO CARD
                else: 
                        messagebox.showerror("Library Card Required","In order to issue you book you must have a library card\nor your card need to be renewed")
                        s = messagebox.askyesno("","Would you like to buy a card")
                        if s:
                                self.buy_card()
                        else:
                                self.option_page()
                
        def issue_book_confirm_page(self):
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                cur.execute("select upper(name) from customer_details where customer_id = %s",(self.c1,))
                j = sort(cur.fetchone())
                #ISSUE ID GENERATOR
                self.issue_id = f"ISSUE-{date}-{j[0]}"
                messagebox.showinfo("Books Issued",f"""Your Issue ID : {self.issue_id}
Kindly proceed to proceed to our waiting lounge your requested book(s) will be brought to you shortly.
Thank You.""")  
                k = 0
                #ADDING ISSUED BOOKS TO DATABASE
                for i in self.books_chosen:
                        cur.execute("select book_id from books where book_name = %s;",(i,))
                        bid = sort(cur.fetchone())
                        cur.execute("insert into book_issued values(%s,%s,%s,%s,curdate(),curdate() + interval 10 day,NULL,NULL);",(self.c1,self.issue_id,bid[0],i))
                        con.commit()
                        k+=1
                self.recepit_page_issue_book()

        def payments_page(self,money):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1: 
                        self.c1=self.new_user_id.get()
                #LABELS
                self.back_label1 = tk.Label(self.win,bg="#f3e5ab",relief="ridge",borderwidth=8,anchor="n")
                self.back_label1.place(x=300-20,y=150,width=820,height=500)
                self.title = tk.Label(self.win,text="Libary Receipt",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.title.place(x=590,y=160,width=200)
                #RECEIPT ID GENERATOR
                receipt_id = f"REC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.receipt_no = tk.Label(self.win,text=f"Receipt No: {receipt_id}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_no.place(x=440,y=200,width=500)
                cur.fetchall()
                #GETTING INFO
                cur.execute(f"select name from customer_details where customer_id = '{self.c1}'")
                n = sort(cur.fetchone())
                self.receipt_name = tk.Label(self.win,text=f"Customer Name: {n[0]}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_name.place(x=440,y=225,width=500)
                self.receipt_custid = tk.Label(self.win,text=f"Customer ID: {self.c1}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.receipt_custid.place(x=440,y=250,width=500)
                self.back.config(command=self.option_page)
                self.card_icon = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\14.png")
                self.library_card = tk.Label(self.win,image=self.card_icon,bg="#f3e5ab")
                self.library_card.place(x=540,y=280)
                self.thank_you = tk.Label(self.win,text="Thank you for using our library!",bg="#f3e5ab",font=("Baskerville Old Face",12),fg="#4F7942")
                self.thank_you.place(x=490,y=500,width=400)
                self.total = tk.Label(self.win,text=f"Total Money: ₹{money}",bg="#f3e5ab",font=("Baskerville Old Face",14,"bold"),fg="#592b0a")
                self.total.place(x=590,y=525,width=200)
                self.question = tk.Label(self.win,text="How would you like to pay?",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                self.question.place(x=540,y=550,width=300)
                #BUTTONS
                self.cash = tk.Button(self.win,text="Cash",bg="#4F7942",font=("Baskerville Old Face",14),fg="#f3e5ab",command=self.cash_page)
                self.cash.place(x=540+20,y=575+10)
                self.QR = tk.Button(self.win,text="UPI",bg="#4F7942",font=("Baskerville Old Face",14),fg="#f3e5ab",command=self.UPI_page)
                self.QR.place(x=740+20,y=575+10)
                self.money = money

        def return_issued_book_page(self):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                #PARENT LABEL
                self.parent_label = tk.Label(self.win,bg="#f3e5ab",relief="ridge",bd=8,fg="#592b0a",font=("Baskerville Old Face",18),text="Issue Book Details",anchor="n")
                self.parent_label.place(x=290,y=275,height=180,width=800)
                #LABEL
                self.isid = tk.Label(self.parent_label,bg="#f3e5ab",width=7,height=1,font=("Baskerville Old Face",16),text="Issue ID:",fg="#592b0a")
                self.isid.place(x=4,y=7+47)
                self.cisid = tk.Label(self.parent_label,bg="#f3e5ab",width=13,height=1,font=("Baskerville Old Face",16),text="Confirm Issue ID:",fg="#592b0a")
                self.cisid.place(x=4,y=45+47)
                #VARIABLES
                self.issueID = tk.StringVar()
                self.cissueID = tk.StringVar()
                #ENTRY
                self.ISSUE_ID = tk.Entry(self.parent_label,width=65,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.issueID,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.ISSUE_ID.place(x=175,y=6+47+2,height=23)
                self.CISSUE_ID = tk.Entry(self.parent_label,width=65,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.cissueID,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.CISSUE_ID.place(x=175,y=45+47+2,height=23)
                #SUBMIT BUTTON
                self.submit4 = tk.Button(self.parent_label,bg="#d41311",text="Submit",font=("Baskerville Old Face",16),fg="white",relief="raised",bd=5,command=self.get_issued_books)
                self.submit4.place(x=684,y=128,width=90,height=30)
                
        def get_issued_books(self):#just as the name suggest
                self.money = 100
                if self.issueID.get() == self.cissueID.get():
                        cur.execute("select book_name from BOOK_ISSUED where issue_id = %s;",(self.cissueID.get(),))
                        self.books_fetched = sort(cur.fetchall())
                        for i in self.win.winfo_children():
                                i.destroy()
                        self.basic_functions()
                        #JUGAAD
                        if self.b ==1:
                                self.c1 = self.custID.get()
                        if self.b==0:
                                self.c1=self.c_id
                        if self.b == -1: 
                                self.c1=self.new_user_id.get()
                        #LABEL
                        self.back_label1 = tk.Label(self.win,bg="#f3e5ab",relief="ridge",borderwidth=8,anchor="n")
                        self.back_label1.place(x=300-20+100+10,y=150+100-30,width=600,height=350)
                        self.issue_id_label = tk.Label(self.win,text=f"Issued ID: {self.cissueID.get()}",bg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),fg="#592b0a")
                        self.issue_id_label.place(x=490,y=300-40-5-20,width=400)
                        self.books_chosen_label = tk.Label(self.win,text="Here are the books issued:",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                        self.books_chosen_label.place(x=490,y=335-40-5-20,width=400)
                        self.books_chosen_listbox = tk.Listbox(self.win,fg="#592b0a", height=28, width=80,bg="#f3e5ab",font=("Baskerville Old Face",15),selectbackground="#f3e5ab",selectforeground="#592b0a",activestyle="none")
                        self.books_chosen_listbox.place(x=440,y=370-40-5-20,width=500,height=100)
                        s_no = 0
                        #BOOKS FETCHED
                        for i in self.books_fetched:
                                s_no+=1
                                j = f"{str(s_no)}. {i}"
                                self.books_chosen_listbox.insert(tk.END, j)
                        #SCROLLBAR
                        self.sc = tk.Scrollbar(self.win, orient="vertical", command=self.books_chosen_listbox.yview,bg="#f3e5ab")
                        self.books_chosen_listbox.config(yscrollcommand=self.sc.set)
                        self.sc.place(x=940+10,y=370-40-5-20,height=100)
                        #LABEL
                        self.total_books = tk.Label(self.win,text=f"Total Books Issued: {s_no}",bg="#f3e5ab",font=("Baskerville Old Face",14,"bold"),fg="#592b0a")
                        self.total_books.place(x=590,y=505-40-5-50,width=200)
                        cur.execute("select date_issued from book_issued where issue_id = %s;",(self.cissueID.get(),))
                        _date_issued = sort(cur.fetchone())
                        self.issue_date_label =  tk.Label(self.win,text=f"Issue Date: {_date_issued[0]}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#4F7942")
                        self.issue_date_label.place(x=450+20,y=540-40-5-50,width=200)
                        cur.fetchall()
                        #GETTING RETURN DATES
                        cur.execute("select return_date from book_issued where issue_id = %s;",(self.cissueID.get(),))
                        _return_date = sort(cur.fetchone())
                        self.return_date_label =  tk.Label(self.win,text=f"Return Date: {_return_date[0]}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#d41311")
                        self.return_date_label.place(x=700+20,y=540-40-5-50,width=200)
                        date_issued = datetime.datetime.strptime(_date_issued[0], "%Y-%m-%d").date()
                        return_date = datetime.datetime.strptime(_return_date[0], "%Y-%m-%d").date()
                        days_left = (return_date - date_issued).days
                        self.days_left_label =  tk.Label(self.win,text=f"Days Left: {days_left}",bg="#f3e5ab",font=("Baskerville Old Face",14),fg="#592b0a")
                        self.days_left_label.place(x=590,y=575-40-5-50,width=200)
                        #CONTINUE
                        self.continue2 = tk.Button(text="Continue",font=("Baskerville Old Face",16),bg="#d41311",fg="white",command=self.return_issue_msg,activebackground="#f3e5ab",relief="raised",bd=5)
                        self.continue2.place(x=615,y=605-40-5-50+5,width=150,height=35)
                        #JUGAAD
                        self.books_chosen = self.books_fetched

                elif self.issueID.get() != self.cissueID.get():
                        messagebox.showerror("Unmatched Issue ID","The entered Issue ID do not match please try again.")
                        self.return_issued_book_page()
                        return
                cur.execute("select issue_id from book_issue;")
                _issue_ids = sort(cur.fetchall())
                if self.cissueID.get() not in _issue_ids:
                        messagebox.showerror("Incorrect Issue ID","The entered Issue ID is not correct or unavailable please try again.")
                        self.return_issued_book_page()
                        return
                
        def donate_books_page(self):#just as the name suggest
                for i in self.win.winfo_children():
                        i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                #ENTER MESSAGE
                self.enter_msg = tk.Label(self.win,bg="#4F7942",text="""Enter the name of the books you want to donate:""",fg="#f3e5ab",font=("Baskerville Old Face",16,"bold"),relief="raised",borderwidth=12,anchor="center")
                self.enter_msg.place(x=450,y=150,width=480,height=65)
                self.bd1 = tk.Label(self.win,text="Book Details",bg="#f3e5ab",font=("Baskerville Old Face",18),relief="ridge",borderwidth=8,fg="#592b0a",anchor="n")
                self.bd1.place(x=300-20,y=280,width=820,height=205)
                #LABLES
                self.label_book_name1 = tk.Label(self.bd1,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Tilte Of The Book:",fg="#592b0a")
                self.label_book_name1.place(x=0,y=40,width=180)
                self.label_author1 = tk.Label(self.bd1,bg="#f3e5ab",font=("Baskerville Old Face",16),width=7,height=1,relief="flat",text="Author Name:",fg="#592b0a")
                self.label_author1.place(x=0,y=80,width=140)
                self.label_year1 = tk.Label(self.bd1,bg="#f3e5ab",font=("Baskerville Old Face",16),width=13,height=1,relief="flat",text="Year of Publication:",fg="#592b0a")
                self.label_year1.place(x=0,y=120,width=190) 
                #VARIABLES
                self.book_name1 = tk.StringVar()
                self.author1 = tk.StringVar()
                self.year1 = tk.StringVar()
                #ENTRY
                self.bn1 = tk.Entry(self.bd1,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.book_name1,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.bn1.place(x=189,y=44)
                self.an1 = tk.Entry(self.bd1,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.author1,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.an1.place(x=189,y=83)
                self.yop1 = tk.Entry(self.bd1,width=60,insertbackground="#592b0a",insertwidth=3,bg="#f3e5ab",fg="#592b0a",textvariable=self.year1,relief="solid",bd=2,font=("Baskerville Old Face",12,"bold"))
                self.yop1.place(x=189,y=123)
                #CONFIRM BUTTON
                self.CONFIRM1 = tk.Button(text="Continue",font=("Baskerville Old Face",16),bg="#d41311",fg="white",command=self.add_donated_books,activebackground="#f3e5ab",relief="raised",bd=5)
                self.CONFIRM1.place(x=620,y=500,width=150,height=40)
                #ADD BUTTON
                self.add_icon1 = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\7.png")
                self.add1 = tk.Button(self.win,image=self.add_icon1,bg="#f3e5ab",command=self.add_donate_options,activebackground="#f3e5ab")
                self.add1.place(x=1045,y=430,width=32,height=32)

        def info_page(self):#just as the name suggest
                for _i in self.win.winfo_children():
                        _i.destroy()
                self.basic_functions()
                self.back.config(command=self.option_page)
                #JUGAAD
                if self.b ==1:
                        self.c1 = self.custID.get()
                if self.b==0:
                        self.c1=self.c_id
                if self.b == -1:
                        self.c1=self.new_user_id.get()
                #GETTING INFO
                cur.execute(f"select name from customer_details where customer_id = '{self.c1}'")
                self.n1 = sort(cur.fetchone())
                n = self.n1[0]
                cur.execute(f"select age from customer_details where customer_id = '{self.c1}'")
                self.a = sort(cur.fetchone())
                if self.a==[]:
                        a = ''
                else:
                        a = self.a[0]
                cur.execute(f"select phone from customer_details where customer_id = '{self.c1}'")
                self.p = sort(cur.fetchone())   
                if self.p==[]:
                        p = ''
                else:
                        p = self.p[0]
                cur.execute(f"select address from customer_details where customer_id = '{self.c1}'")
                self.ad = sort(cur.fetchone())
                if self.ad==[]:
                        ad = ''
                else:
                        ad = self.ad[0]
                cur.execute(f"select has_card from customer_details where customer_id = '{self.c1}'")
                self.card = sort(cur.fetchone())
                if self.card==[]:
                        card = ''
                else:
                        card = self.card[0]
                cur.execute(f"select gmail_id from customer_details where customer_id = '{self.c1}'")
                self.gmail1 = sort(cur.fetchone())
                gmail1 = self.gmail1[0]
                #PASSWORD HIDE
                self.z = ""
                cur.execute(f"select user_password from password_table where customer_id = '{self.c1}';")
                w = cur.fetchall()
                self.pa = sort(w)
                for i in range(0,len(self.pa[0])):
                        self.z+="*"
                #BACKGROUND LABEL
                self.back_label = tk.Label(self.win,text="Account Details",bg="#f3e5ab",font=("Baskerville Old Face",20,"bold"),relief="ridge",borderwidth=8,fg="#592b0a",anchor='n')
                self.back_label.place(x=380+10,y=200,width=600,height=325)
                #USER NAME 
                self.user_name = tk.Label(self.win,text="Name:",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_name.place(x=5+395,y=30+20+200)
                self.user_name1 = tk.Label(self.win,text=f"{n}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_name1.place(x=90+395,y=30+20+200,width=200,height=34)
                #USER ID 
                self.user_id = tk.Label(self.win,text="Customer ID:",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_id.place(x=5+395,y=30+30+20+200)
                self.user_id1 = tk.Label(self.win,text=f"{self.c1}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_id1.place(x=165+395,y=30+30+20+200,width=400,height=34)
                #USER PASSWORD
                self.user_pass = tk.Label(self.win,text="Password:",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_pass.place(x=5+395,y=30+60+20+200)
                self.user_pass1 = tk.Label(self.win,text=f"{self.z}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_pass1.place(x=120+395,y=30+60+20+200,width=200,height=34)
                #USER AGE 
                self.user_age = tk.Label(self.win,text="Age:",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_age.place(x=5+395,y=60+60+20+200)
                self.user_age1 = tk.Label(self.win,text=f"{a}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_age1.place(x=65+395,y=60+60+20+200,width=200,height=34)
                #USER PHONE
                self.user_phone = tk.Label(self.win,text="Mobile Number:",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_phone.place(x=5+395,y=90+60+20+200)
                self.user_phone1 = tk.Label(self.win,text=f"{p}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_phone1.place(x=195+395,y=90+60+20+200,width=200,height=34)
                #USER ADDRESS
                self.user_address = tk.Label(self.win,text="Address:",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_address.place(x=5+395,y=120+60+20+200)
                self.user_address1 = tk.Label(self.win,text=f"{ad}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_address1.place(x=110+395,y=120+60+20+200,width=200,height=34)
                #USER HAS CARD
                self.user_has_card = tk.Label(self.win,text="Card Issued: ",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_has_card.place(x=5+395,y=150+60+20+200)
                self.user_has_card1 = tk.Label(self.win,text=f"{card}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_has_card1.place(x=150+395,y=150+60+20+200,width=200,height=34)
                #USER GMAIL
                self.user_gmail = tk.Label(self.win,text="Gmail ID: ",bg="#f3e5ab",font=("Baskerville Old Face",18,"bold"),fg="#592b0a")
                self.user_gmail.place(x=5+395,y=180+60+20+200)
                self.user_gmail1 = tk.Label(self.win,text=f"{gmail1}",bg="#f3e5ab",font=("Baskerville Old Face",16),fg="#592b0a",anchor="w")
                self.user_gmail1.place(x=130+395,y=180+60+20+200,width=200,height=34)
                #PASSWORD CLOSING FEATURE
                self.closed_eye = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\10.png")
                self.open_eye = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\11.png")
                self.pass_toggle = tk.Button(self.back_label,bg="#f3e5ab",activebackground="#f3e5ab",image=self.open_eye)
                self.pass_toggle.place(x=550,y=30+60+20,width=34,height=34)
                self.pass_toggle.bind("<Button-1>",self.show_pass)
                self.pass_toggle.bind("<Leave>",self.hide_pass)
                #EDIT BUTTON
                self.edit = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\12.png")
                self.edit_button = tk.Button(self.win,image=self.edit,text="  Edit",bg="#4F7942",activebackground="#4F7942",anchor="w",compound="left",font=("Baskerville Old Face",14),fg="#f3e5ab",relief="raised",border=6,command=self.edit_info)
                self.edit_button.place(x=590+10+5-20,y=555,width=90,height=40)
                #GO BACK BUTTON
                self.go_back_button = tk.Button(self.win,text="Go Back",bg="#d41311",activebackground="#d41311",anchor="w",compound="left",font=("Baskerville Old Face",14),fg="#f5f5dc",relief="raised",border=6,command=self.option_page)
                self.go_back_button.place(x=680+10+5+20,y=555,width=90,height=40)
        
        def edit_info(self):#just as the name suggest
                self.edit_button.destroy()
                #EDIT BUTTON
                self.edit = tk.PhotoImage(file=r"C:\Users\Dutta Family\Desktop\Aakar\New folder\12.png")
                #NAME
                self.edit_button_1 = tk.Button(self.win,image=self.edit,bg="#4F7942",activebackground="#4F7942",anchor="w",font=("Baskerville Old Face",14),fg="#f3e5ab",relief="raised",border=5,command=lambda: self.edit_entry(self.user_name1))
                self.edit_button_1.place(x=550+200+195+3,y=30+20+220-12,width=34,height=34)
                #USER ID
                self.edit_button_2 = tk.Button(self.win,image=self.edit,bg="#4F7942",activebackground="#4F7942",anchor="w",font=("Baskerville Old Face",14),fg="#f3e5ab",relief="raised",border=5,command=lambda: self.edit_entry(self.user_id1))
                self.edit_button_2.place(x=550+200+195+3,y=30+30+20+220-12,width=34,height=34)
                #USER PASSWORD
                self.edit_button_3 = tk.Button(self.win,image=self.edit,bg="#4F7942",activebackground="#4F7942",anchor="w",font=("Baskerville Old Face",14),fg="#f3e5ab",relief="raised",border=5,command=lambda: self.edit_entry(self.user_pass1))
                self.edit_button_3.place(x=550+200+195+3,y=30+60+20+220-12,width=34,height=34)
                #USER AGE 
                self.edit_button_4 = tk.Button(self.win,image=self.edit,bg="#4F7942",activebackground="#4F7942",anchor="w",font=("Baskerville Old Face",14),fg="#f3e5ab",relief="raised",border=5,command=lambda: self.edit_entry(self.user_age1))
                self.edit_button_4.place(x=550+200+195+3,y=60+60+20+220-12,width=34,height=34)
                #USER ADDRESS
                self.edit_button_5 = tk.Button(self.win,image=self.edit,bg="#4F7942",activebackground="#4F7942",anchor="w",font=("Baskerville Old Face",14),fg="#f3e5ab",relief="raised",border=5,command=lambda: self.edit_entry(self.user_address1))
                self.edit_button_5.place(x=550+200+195+3,y=120+60+20+220-12,width=34,height=34)
                #GO BACK
                self.go_back_button.place(x=650,y=555)
                
a = GUI()       
a.SQL()
a.home_page()
a.due_days()