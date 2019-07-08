import tkinter as tk
from tkinter import messagebox
import stockclick as sc
import time
import os
import pyperclip
import subprocess
import datetime
import stockmodule as m
import datetime
import s0056

def check_pw():
    global stop 
    stop = False
    _, msg1, msg2 = s0056.send_info(2)
    listbox.insert(tk.END, str(msg1))
    listbox.insert(tk.END, str(msg2))
    if pwvar.get()  == 'joejoe': 
        stockinfo = sc.sclick()
        for stock_item in stockinfo:
            listbox.insert(tk.END, str(stock_item))

    else:
        messagebox.askyesno("Reminder", "Pleae enter the password")
def athenz():
    os.system('~/mypython/iterm2run.sh ~/Desktop/athenz-user-cert')
def yinit():
    os.system('~/mypython/iterm2run.sh ub')
def kubelogin():
    os.system("~/mypython/iterm2run.sh 'kubectl plugin login'")
def clean():
    listbox.delete(0, 'end')
def okta():
    if pwvar.get()  == 'joejoe':
        status, result = subprocess.getstatusoutput('cat okta.passwd')
        if status == 0:
            pyperclip.copy(result)
        else:
            ssagebox.askyesno("Reminder", "Put your password in file and check it")
    else:
        messagebox.askyesno("Reminder", "Pleae enter the password")
def bouncer():
    if pwvar.get()  == 'joejoe':
        status, result = subprocess.getstatusoutput('cat bouncer.passwd')
        if status == 0:
            pyperclip.copy(result)
        else:
            messagebox.askyesno("Reminder", "Put your password in file and check it")
    else:
        messagebox.askyesno("Reminder", "Pleae enter the password")
def sanitize():
    status, result = subprocess.getstatusoutput('ls -al ~/.athenz/cert |\
            cut -d" " -f9-12 |\
            xargs -I % echo "Athenz started at %"')
    listbox.delete(0, 'end')
    listbox.insert(tk.END, result)
    window.after(300000, sanitize)    

def stock_when_to_buy():
    now = datetime.datetime.now()
    if datetime.date.today().isoweekday() <= 5:
        if now.hour < 14 and now.hour >= 9:
            stock_buy_info = m.check_stock_send()
            _, msg = s0056.send_info(2)
            for item in stock_buy_info:
                listbox.insert(tk.END, str(item))
            listbox.insert(tk.END, str(msg))
    window.after(180000, stock_when_to_buy)

#main window
window = tk.Tk()
window.geometry('480x320')
window.title('Joe Yang')
#upper frame
upper_fm = tk.Frame(window, bg='green', width=480, height=320-100)
upper_fm.pack()
#lower frame
below_fm = tk.Frame(window,bg='red', width=480, height=100)
below_fm.pack()
#label for password
lb= tk.Label(below_fm, text='Enter Your Password', bg='red', fg='white',
        font=('細明體',20)) 
lb.place(rely=0.25, relx=0.5, anchor='center')    
#Entry
pwvar = tk.StringVar()                     
entry = tk.Entry(below_fm, width=15, textvariable=pwvar, show='*')
entry.place(rely=0.5, relx=0.5, anchor='center')    
#Stock button
stock_btn = tk.Button(upper_fm, bg='#FFD700', fg='black', text='click', 
        command=check_pw, font=('細明體',20))
stock_btn.place(rely=0.1, relx=0.2, anchor='center')

#Athenz Button
athenz_btn = tk.Button(upper_fm, bg='#FFD700', fg='black', text='athenz-user-cert', 
        command=athenz, font=('細明體',20))
athenz_btn.place(rely=0.1, relx=0.5, anchor='center')

#yinit Button
yinit_btn = tk.Button(upper_fm, bg='#FFD700', fg='black', text='yinit', 
        command=yinit, font=('細明體',20))
yinit_btn.place(rely=0.1, relx=0.8, anchor='center')

#Kubelogin Button
kubelogin_btn = tk.Button(upper_fm, bg='#FFD700', fg='black', text='kubelogin', 
        command=kubelogin, font=('細明體',20))
kubelogin_btn.place(rely=0.3, relx=0.2, anchor='center')

#clean Button
clean_btn = tk.Button(upper_fm, bg='red', fg='black', text='clean', 
        command=clean, font=('細明體',20))
clean_btn.place(rely=0.3, relx=0.4, anchor='center')

#okta Button
clean_btn = tk.Button(upper_fm, bg='red', fg='black', text='okta', 
        command=okta, font=('細明體',20))
clean_btn.place(rely=0.3, relx=0.6, anchor='center')

#bouncer Button
clean_btn = tk.Button(upper_fm, bg='red', fg='black', text='bouncer', 
        command=bouncer, font=('細明體',20))
clean_btn.place(rely=0.3, relx=0.8, anchor='center')





#listbox for stock information
listbox  = tk.Listbox(upper_fm, width=27, height=5)
listbox.place(rely=0.7, relx=0.5, anchor='center')
#Scrollbar
sbar = tk.Scrollbar(upper_fm)
sbar.place(rely=0.7, relx=0.735, anchor='center' )
#Scrollbar & listbox
sbar.config(command = listbox.yview)
listbox.config(yscrollcommand = sbar.set)

#while loop function
window.after(1000, sanitize)
window.after(1000, stock_when_to_buy)

#main
window.mainloop()
