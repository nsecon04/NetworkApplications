import logging
import os
import telnetlib
import socket
import threading
import logging
import time
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
import shlex
import re
import subprocess
import os



# Global variables
PORTS = [80, 443]
FAILED_ENDPOINTS = []
CONNECTED_ENDPOINTS = []
DOMAIN_LIST = []
ENDPOINTS = [
        "dromapi.cable.comcast.com",
        "drom-qa1.cable.comcast.com",
        "dromapi-stg.cable.comcast.com",
        "inventory.cable.comcast.com",
        "clips-staging.cable.comcast.com",
        "helix.comcast.com",
        "hlxapppr.sys.comcast.net",
        "helix-stage.comcast.com",
        "hlxapppr-dt-as.ula.comcast.net",
        "hlxdb-dt-01q.ula.comcast.net"
        ]

# INT
INT_SVC_CH2 = [
    "ebzsvc-ch2-03i",
    "ebzsvc-ch2-04i",
    "ebzsvc-ch2-05i",
    "ebzsvc-ch2-07i",
    "ebzsvc-ch2-08i"
    ]
INT_SVC_WC = [
    "ebzsvc-wc-03i",
    "ebzsvc-wc-04i",
    "ebzsvc-wc-05i",
    "ebzsvc-wc-07i",
    "ebzsvc-wc-08i"
    ]
INT_SVC_PDC = [
    "ebzsvc-po-03i",
    "ebzsvc-po-04i",
    "ebzsvc-po-05i",
    "ebzsvc-po-07i",
    "ebzsvc-po-08i"
    ]
INT_WEB_CH2 = [
    "ebzweb-ch2-07i",
    "ebzweb-ch2-08i",
    "ebzweb-ch2-09i",
    "ebzweb-ch2-10i",
    "ebzweb-ch2-11i",
    "ebzweb-ch2-12i"
    ]
INT_WEB_WC = [
    "ebzweb-wc-07i",
    "ebzweb-wc-08i",
    "ebzweb-wc-09i",
    "ebzweb-wc-10i",
    "ebzweb-wc-11i",
    "ebzweb-wc-12i"
    ]
INT_WEB_PDC = [
    "ebzweb-po-07i",
    "ebzweb-po-08i",
    "ebzweb-po-09i",
    "ebzweb-po-10i",
    "ebzweb-po-11i",
    "ebzweb-po-12i"
    ]

#STG
STG_SVC_CH2 = [
    "ebzsvc-ch2-01s",
    "ebzsvc-ch2-02s",
    "ebzsvc-ch2-03s",
    "ebzsvc-ch2-04s",
    "ebzsvc-ch2-05s",
    "ebzsvc-ch2-07s",
    "ebzsvc-ch2-08s"
    ]
STG_SVC_WC = [
    "ebzsvc-wc-01s",
    "ebzsvc-wc-02s",
    "ebzsvc-wc-03s",
    "ebzsvc-wc-04s",
    "ebzsvc-wc-05s",
    "ebzsvc-wc-07s",
    "ebzsvc-wc-08s"
    ]
STG_SVC_PDC = [
    "ebzsvc-po-01s",
    "ebzsvc-po-02s",
    "ebzsvc-po-03s",
    "ebzsvc-po-07s",
    "ebzsvc-po-08s",
    "ebzsvc-po-04s",
    "ebzsvc-po-05s"
    ]
STG_WEB_CH2 = [
    "ebzweb-ch2-07s",
    "ebzweb-ch2-08s",
    "ebzweb-ch2-09s",
    "ebzweb-ch2-10s",
    "ebzweb-ch2-11s",
    "ebzweb-ch2-12s"
    ]
STG_WEB_WC = [
    "ebzweb-wc-07s",
    "ebzweb-wc-08s",
    "ebzweb-wc-09s",
    "ebzweb-wc-10s",
    "ebzweb-wc-11s",
    "ebzweb-wc-12s"
    ]
STG_WEB_PDC = [
    "ebzweb-po-07s",
    "ebzweb-po-08s",
    "ebzweb-po-09s",
    "ebzweb-po-10s",
    "ebzweb-po-11s",
    "ebzweb-po-12s"
    ]

# PROD
PROD_SVC_CH2 = [
    "ebzsvc-ch2-11p",
    "ebzsvc-ch2-12p",
    "ebzsvc-ch2-13p",
    "ebzsvc-ch2-14p",
    "ebzsvc-ch2-15p"
	]
PROD_SVC_WC = [
    "ebzsvc-wc-11p",
    "ebzsvc-wc-12p",
    "ebzsvc-wc-13p",
    "ebzsvc-wc-14p",
    "ebzsvc-wc-15p"
	]
PROD_SVC_PDC = [
    "ebzsvc-po-11p",
    "ebzsvc-po-12p",
    "ebzsvc-po-13p",
    "ebzsvc-po-14p",
    "ebzsvc-po-15p"
	]
PROD_WEB_CH2 = [
    "ebzweb-ch2-76p",
    "ebzweb-ch2-77p",
    "ebzweb-ch2-78p",
    "ebzweb-ch2-79p",
    "ebzweb-ch2-80p",
    "ebzweb-ch2-81p",
    "ebzweb-ch2-82p",
    "ebzweb-ch2-83p",
    "ebzweb-ch2-84p",
    "ebzweb-ch2-85p",
    "ebzweb-ch2-86p",
    "ebzweb-ch2-87p",
    "ebzweb-ch2-88p",
    "ebzweb-ch2-89p",
    "ebzweb-ch2-90p"
	]
PROD_WEB_WC = [
    "ebzweb-wc-76p",
    "ebzweb-wc-77p",
    "ebzweb-wc-78p",
    "ebzweb-wc-79p",
    "ebzweb-wc-80p",
    "ebzweb-wc-81p",
    "ebzweb-wc-82p",
    "ebzweb-wc-83p",
    "ebzweb-wc-84p",
    "ebzweb-wc-85p",
    "ebzweb-wc-86p",
    "ebzweb-wc-87p",
    "ebzweb-wc-88p",
    "ebzweb-wc-89p",
    "ebzweb-wc-90p"
	]
PROD_WEB_PDC = [
    "ebzweb-po-76p",
    "ebzweb-po-77p",
    "ebzweb-po-78p",
    "ebzweb-po-79p",
    "ebzweb-po-80p",
    "ebzweb-po-81p",
    "ebzweb-po-82p",
    "ebzweb-po-83p",
    "ebzweb-po-84p",
    "ebzweb-po-85p",
    "ebzweb-po-86p",
    "ebzweb-po-87p",
    "ebzweb-po-88p",
    "ebzweb-po-89p",
    "ebzweb-po-90p"
	]

ALL_INT_WEB = [INT_WEB_CH2, INT_WEB_PDC, INT_WEB_WC]
ALL_INT_SVC = [INT_SVC_CH2, INT_SVC_PDC, INT_SVC_WC]
ALL_STG_WEB = [STG_WEB_CH2, STG_WEB_PDC, STG_WEB_WC]
ALL_STG_SVC = [STG_SVC_CH2, STG_SVC_PDC, STG_SVC_WC]
ALL_PROD_WEB = [PROD_WEB_CH2, PROD_WEB_PDC, PROD_WEB_WC]
ALL_PROD_SVC = [PROD_SVC_CH2, PROD_SVC_PDC, PROD_SVC_WC]

def print_list(lists,txtbox):
    txtbox.delete(1.0, END)
    for item in lists:
        for list in item:
            txtbox.insert(END,(list + "\n"))
def reachability():
    stext1.delete(1.0, END)
    stext1.insert(INSERT, "....Reachability_Test_Initiated....\n")
    timeout = 3
    for endpoint in ENDPOINTS:
        for port in PORTS:
            try:
                hosts = socket.gethostbyname(str(endpoint))
                tn = telnetlib.Telnet(endpoint, port, timeout)
                passing = {endpoint: port}
                CONNECTED_ENDPOINTS.append(passing)
                tn.close()
            except Exception as e:
                try:
                    hosts = socket.gethostbyname(str(endpoint))
                    failing = {endpoint: port}
                    FAILED_ENDPOINTS.append(failing)
                except:
                    print()
    # Results
    # Passes
    print("Connected Endpoints:")
    stext1.insert(INSERT, "Connected Endpoints:\n")
    for passes in CONNECTED_ENDPOINTS:
        print("Connected: " + str(passes) )
        response=("Connected: " + str(passes) + "\n")
        stext1.insert(INSERT, response)
    # Fails
    stext1.insert(INSERT, "\n")
    print("Failed Endpoints:")
    stext1.insert(INSERT, "Failed Endpoints:\n")
    for item in FAILED_ENDPOINTS:
        print("Failed: " + str(item))
        response = ("Failed: " + str(item) + "\n")
        stext1.insert(INSERT, response)
    print("Reachability_Test_Completed")
    stext1.insert(INSERT, "....Reachability_Test_Completed....\n")
    stext1.insert(END, "\n")
    stext1.insert(END, "\n")
def dns_resolution():
    conn_screen_delete()
    #
    stext1.place(x=5, y=120)
    #
    input_box4.place(x=95, y=53)
    #
    env_label7.place(x=5, y=50)
    #
    btn13.place(x=600, y=50)
    btn14.place(x=275, y=75)
    #
    for host in ENDPOINTS:
        try:
            ip = socket.gethostbyname(str(host))
            lookup = {host: ip}
            DOMAIN_LIST.append(lookup)
        except:
            lookup = {host: "DNS_Failure"}
            DOMAIN_LIST.append(lookup)

        # results
    print("\n Domain_Lookup_Initiated >>>> :")
    for each_item in DOMAIN_LIST:
        print(str(each_item))
    print("Domain_Lookup_Completed \n")
def env_switcher(arg):
    switcher = {
        1: "INT",
        2: "STG",
        3: "PROD"
    }
    #print("arg = "+ str(arg))
    return (switcher.get(arg, "Invalid selection"))
def input_box():
    #input_box1.destroy()
    input_box1 = Entry(window, width=30)
    input_box1.place(x=625, y=102)
    input_box1.focus()  # Place cursor in textbox when launched
def mutable():
    input_box1 = Entry(window, width=30, state='disabled')
    input_box1.place(x=625, y=102)
def master_kill():
    window.destroy()
def file_download():
    #ref https://likegeeks.com/downloading-files-using-python/
    pass
def canvas_window():
    app4 = Tk()
    app4.geometry('1024x900')
    app4.title("OCN_Canvas")
    canvas = Canvas(app4, width=600, height=400)
    canvas.place(x=0, y=0)
    app4.mainloop()
def open_file_demo():
    file = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))     # Single file
    #files = filedialog.askopenfilenames(filetypes = (("Text files","*.txt"),("all files","*.*")))   # multiple files
    #file = filedialog.askopenfilename(initialdir=path.dirname(__file__))        # specify initial dir
    #dir = filedialog.askdirectory()         # ask for directory
    # more code .....
def teardown_window_env():
    pass
def categories():
        app2 = Tk()
        app2.geometry('1024x900')
        app2.title("OCN_Apps")
        tab_control = ttk.Notebook(app2)
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Network')
        tab_control.add(tab2, text='Security')
        tab_control.pack(expand=1, fill='both')

        #####################################################################################################
        # create bottons
        # Network Tab
        conn_test = Button(tab1, text="Connectivity Test", fg="black", bg="lightblue", width=20, height=2)
        dns_test = Button(tab1, text="DNS Resolution", fg="black", bg="lightblue", width=20, height=2)
        host_entry = Button(tab1, text="Host Editor", fg="black", bg="lightblue", width=20, height=2)
        conn_test.grid(column=0, row=0, padx=5, pady=5)
        dns_test.grid(column=1, row=0, padx=5, pady=5)
        host_entry.grid(column=3, row=0, padx=5, pady=5)

        # Specify deminsion of scrolledText
        network_text1 = scrolledtext.ScrolledText(tab1, width=115, height=45, wrap='word')
        network_text1.delete(1.0, END)  # Delete the entire content
        network_text1.insert(INSERT, "")  # Inserting items in box
        network_text1.place(x=5, y=100)


        #####################################################################################################
        # Security Tab
        gen_csr = Button(tab2, text="Generate CSR", fg="black", bg="lightblue", width=20, height=2)
        val_csr = Button(tab2, text="Validate CSR+Cert+Key", fg="black", bg="lightblue", width=20, height=2)
        sec_proto = Button(tab2, text="Crypto Editor", fg="black", bg="lightblue", width=20, height=2)
        gen_csr.grid(column=0, row=0, padx=5, pady=5)
        val_csr.grid(column=1, row=0, padx=5, pady=5)
        sec_proto.grid(column=2, row=0, padx=5, pady=5)

        #####################################################################################################
        # Run the app
        app2.mainloop()
def network_tools():
    conn_screen_delete()
    conn_test.place(x=5,y=50)
    dns_test.place(x=155,y=50)
    host_entry.place(x=305,y=50)
    #
    stext1.place(x=5, y=180)
def security_tools():
    conn_screen_delete()
    gen_csr.place(x=5,y=50)
    val_csr.place(x=155,y=50)
    sec_proto.place(x=305,y=50)
    #
    stext1.place(x=5, y=180)
def server_info():
    conn_screen_delete()
    app3 = Tk()
    app3.geometry('1024x900')
    app3.title("Server_List")
    app3.configure(background='ivory3')
    tab_control = ttk.Notebook(app3)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Web Servers')
    tab_control.add(tab2, text='SVC Servers')
    tab_control.pack(expand=1, fill='both')

    # create inner tabs
    # Web servers
    web_tab_control = ttk.Notebook(tab1)
    web_tab1 = ttk.Frame(web_tab_control)
    web_tab2 = ttk.Frame(web_tab_control)
    web_tab3 = ttk.Frame(web_tab_control)
    web_tab_control.add(web_tab1, text='INT')
    web_tab_control.add(web_tab2, text='STG')
    web_tab_control.add(web_tab3, text='PROD')
    web_tab_control.pack(expand=1, fill='both')

    # SVC servers
    svc_tab_control = ttk.Notebook(tab2)
    svc_tab1 = ttk.Frame(svc_tab_control)
    svc_tab2 = ttk.Frame(svc_tab_control)
    svc_tab3 = ttk.Frame(svc_tab_control)
    svc_tab_control.add(svc_tab1, text='INT')
    svc_tab_control.add(svc_tab2, text='STG')
    svc_tab_control.add(svc_tab3, text='PROD')
    svc_tab_control.pack(expand=1, fill='both')

    # Create screen
    web_int_text1 = scrolledtext.ScrolledText(web_tab1, width=110, height=42, wrap='word')
    web_stg_text1 = scrolledtext.ScrolledText(web_tab2, width=110, height=42, wrap='word')
    web_prod_text1 = scrolledtext.ScrolledText(web_tab3, width=110, height=42, wrap='word')
    svc_int_text1 = scrolledtext.ScrolledText(svc_tab1, width=110, height=42, wrap='word')
    svc_stg_text1 = scrolledtext.ScrolledText(svc_tab2, width=110, height=42, wrap='word')
    svc_prod_text1 = scrolledtext.ScrolledText(svc_tab3, width=110, height=42, wrap='word')

    # adding txtbox
    web_int_text1.place(x=5, y=50)
    web_stg_text1.place(x=5, y=50)
    web_prod_text1.place(x=5, y=50)
    svc_int_text1.place(x=5, y=50)
    svc_stg_text1.place(x=5, y=50)
    svc_prod_text1.place(x=5, y=50)

    #Populating server list
    print_list(ALL_INT_WEB,web_int_text1)
    print_list(ALL_INT_SVC, svc_int_text1)
    print_list(ALL_STG_WEB, web_stg_text1)
    print_list(ALL_STG_SVC, svc_stg_text1)
    print_list(ALL_PROD_WEB, web_prod_text1)
    print_list(ALL_PROD_SVC, svc_prod_text1)

    # Adding buttons
    sl_btn1 = Button(web_tab1, text="Update", fg="black", bg="lightblue", width=12, height=1)
    sl_btn2 = Button(web_tab2, text="Update", fg="black", bg="lightblue", width=12, height=1)
    sl_btn3 = Button(web_tab3, text="Update", fg="black", bg="lightblue", width=12, height=1)
    sl_btn4 = Button(svc_tab1, text="Update", fg="black", bg="lightblue", width=12, height=1)
    sl_btn5 = Button(svc_tab2, text="Update", fg="black", bg="lightblue", width=12, height=1)
    sl_btn6 = Button(svc_tab3, text="Update", fg="black", bg="lightblue", width=12, height=1)
    sl_btn1.place(x=913, y=50)
    sl_btn2.place(x=913, y=50)
    sl_btn3.place(x=913, y=50)
    sl_btn4.place(x=913, y=50)
    sl_btn5.place(x=913, y=50)
    sl_btn6.place(x=913, y=50)

    # Run the app
    app3.mainloop()
def notepad():
    app1 = Tk()
    app1.geometry('1024x900')
    app1.title("OCN_Notes")
    tab_control = ttk.Notebook(app1)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Recording')
    tab_control.add(tab2, text='Reading')
    tab_control.pack(expand=1, fill='both')

    # Adding Scrolled box to Tab1
    canvas1 = scrolledtext.ScrolledText(tab1, width=115, height=51)
    canvas1.place(x=5, y=30)
    canvas1.delete(1.0, END)  # Delete the entire content
    canvas1.insert(INSERT, "")  # Inserting items in box

    # Adding bottons to Tab1
    n_save1 = Button(tab1, text="Save Log", fg="black", bg="lightblue", command=file_save_as)
    n_save1.place(x=950, y=30)

    # Adding Scrolled box to Tab2
    canvas2 = scrolledtext.ScrolledText(tab2, width=115, height=51)
    canvas2.place(x=5, y=30)
    canvas2.delete(1.0, END)  # Delete the entire content
    canvas2.insert(INSERT, "")  # Inserting items in box

    # Adding bottons to Tab2
    n_save2 = Button(tab2, text="Read Log", fg="black", bg="lightblue", command= lambda: open_logs)
    n_save2.place(x=950, y=30)

    # need more code

    app1.mainloop()
def about_us():
    message =   "" \
                " This application consists of a collection of open sourced tools used by " \
                "network engineers to complete daily tasks. The product contains " \
                "proprietory code that should not be distributed to any third party without a" \
                " written consent from NSECON04 LLC."
    messagebox.showinfo('Disclaimer', message)         # Info message
def file_save_as():
    fileExt = [
        ('All Files', '*.*'),
        ('Python Files', '*.py'),
        ('Text Document', '*.txt'),
        ('PowerShell', '*.ps1'),
        ('JSON File', '*.json'),
        ('YAML File', '*.yaml')
    ]
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes = fileExt)
    if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(stext1.get(1.0, END)) # starts from `1.0`, not `0.0`
    file.write(text2save)
    file.close()
def open_file():
    fileExt = [
        ('All Files', '*.*'),
        ('Python Files', '*.py'),
        ('Text Document', '*.txt'),
        ('PowerShell', '*.ps1'),
        ('JSON File', '*.json'),
        ('YAML File', '*.yaml')
    ]
    stext1.delete(1.0,END)
    file = filedialog.askopenfile(mode ='r', filetypes = fileExt)
    if file is not None:
        content = file.read()
        #print(content)
        stext1.insert(INSERT, content)
def open_logs():
    fileExt = [
        ('All Files', '*.*'),
        ('Python Files', '*.py'),
        ('Text Document', '*.txt'),
        ('PowerShell', '*.ps1'),
        ('JSON File', '*.json'),
        ('YAML File', '*.yaml')
    ]
    canvas2.delete(1.0,END)
    file = filedialog.askopenfile(mode ='r', filetypes = fileExt)
    if file is not None:
        content = file.read()
        #print(content)
        canvas2.insert(INSERT, content)
def all_dc():
    if chk_state_all.get() == True:
        chk_state_ch2.set(True)
        chk_state_pdc.set(True)
        chk_state_wc.set(True)
        chkbox3.config(state=DISABLED)
        chkbox4.config(state=DISABLED)
        chkbox5.config(state=DISABLED)
    if chk_state_all.get() == False:
        chk_state_ch2.set(False)
        chk_state_pdc.set(False)
        chk_state_wc.set(False)
        chkbox3.config(state=NORMAL)
        chkbox4.config(state=NORMAL)
        chkbox5.config(state=NORMAL)
def chkbtn_state():
    # Client State
    if chk_state_cl_all.get() == True:
        chk_state_cl_p1.set(True)
        chk_state_cl_s2.set(True)
        chk_state_cl_s3.set(True)
        chk_state_cl_t0.set(True)
        chk_state_cl_t1.set(True)
        chk_state_cl_t2.set(True)
        chkbox6.config(state=DISABLED)
        chkbox7.config(state=DISABLED)
        chkbox8.config(state=DISABLED)
        chkbox9.config(state=DISABLED)
        chkbox10.config(state=DISABLED)
        chkbox11.config(state=DISABLED)


    if chk_state_cl_all.get() == False:
        chk_state_cl_p1.set(False)
        chk_state_cl_s2.set(False)
        chk_state_cl_s3.set(False)
        chk_state_cl_t0.set(False)
        chk_state_cl_t1.set(False)
        chk_state_cl_t2.set(False)
        chkbox6.config(state=NORMAL)
        chkbox7.config(state=NORMAL)
        chkbox8.config(state=NORMAL)
        chkbox9.config(state=NORMAL)
        chkbox10.config(state=NORMAL)
        chkbox11.config(state=NORMAL)

    # Server State
    if chk_state_sl_all.get() == True:
        chk_state_sl_p1.set(True)
        chk_state_sl_s2.set(True)
        chk_state_sl_s3.set(True)
        chk_state_sl_t0.set(True)
        chk_state_sl_t1.set(True)
        chk_state_sl_t2.set(True)
        chkbox13.config(state=DISABLED)
        chkbox14.config(state=DISABLED)
        chkbox15.config(state=DISABLED)
        chkbox16.config(state=DISABLED)
        chkbox17.config(state=DISABLED)
        chkbox18.config(state=DISABLED)


    if chk_state_sl_all.get() == False:
        chk_state_sl_p1.set(False)
        chk_state_sl_s2.set(False)
        chk_state_sl_s3.set(False)
        chk_state_sl_t0.set(False)
        chk_state_sl_t1.set(False)
        chk_state_sl_t2.set(False)
        chkbox13.config(state=NORMAL)
        chkbox14.config(state=NORMAL)
        chkbox15.config(state=NORMAL)
        chkbox16.config(state=NORMAL)
        chkbox17.config(state=NORMAL)
        chkbox18.config(state=NORMAL)

    if local_remote.get() == 1:
        chkbox3.config(state=NORMAL)
        chkbox4.config(state=NORMAL)
        chkbox5.config(state=NORMAL)
        chkbox51.config(state=NORMAL)
        chkbox1.config(state=NORMAL)
        chkbox2.config(state=NORMAL)
        chkbox02.config(state=NORMAL)
    if local_remote.get() == 0:
        #
        chkbox3.config(state=DISABLED)
        chkbox4.config(state=DISABLED)
        chkbox5.config(state=DISABLED)
        chkbox51.config(state=DISABLED)
        chkbox1.config(state=DISABLED)
        chkbox2.config(state=DISABLED)
        chkbox02.config(state=DISABLED)
        #
        chkbox3.config(bg='ivory4')
        chkbox4.config(bg='ivory4')
        chkbox5.config(bg='ivory4')
        chkbox51.config(bg='ivory4')
        chkbox1.config(bg='ivory4')
        chkbox2.config(bg='ivory4')
        chkbox02.config(bg='ivory4')

    window.update()
def recomm_ciphers():
    # Client protocols state
    chk_state_cl_p1.set(False)
    chk_state_cl_s2.set(False)
    chk_state_cl_s3.set(False)
    chk_state_cl_t0.set(False)
    chk_state_cl_t1.set(False)
    chk_state_cl_t2.set(True)
    chk_state_cl_all.set(False)

    # Server Protocols state
    chk_state_sl_p1.set(False)
    chk_state_sl_s2.set(False)
    chk_state_sl_s3.set(False)
    chk_state_sl_t0.set(False)
    chk_state_sl_t1.set(False)
    chk_state_sl_t2.set(True)
    chk_state_sl_all.set(False)

    # hashes
    chk_state_h_md.set(False)
    chk_state_h_s1.set(False)
    chk_state_h_s2.set(False)
    chk_state_h_s3.set(False)
    chk_state_h_s4.set(True)

    # Key Exchanges
    chk_state_ke_dh.set(False)
    chk_state_ke_pk.set(True)
    chk_state_ke_ec.set(True)

    # Ciphers
    chk_state_c_null.set(False)
    chk_state_c_d.set(False)
    chk_state_c_ra.set(False)
    chk_state_c_rb.set(False)
    chk_state_c_rc.set(False)
    chk_state_c_rw.set(False)
    chk_state_c_rx.set(False)
    chk_state_c_ry.set(False)
    chk_state_c_rz.set(False)
    chk_state_c_t.set(False)
    chk_state_c_a1.set(True)
    chk_state_c_a2.set(True)
def all_servers():
    if chk_state_both.get() == True:
        chk_state_web.set(True)
        chk_state_svc.set(True)
        chkbox1.config(state=DISABLED)
        chkbox2.config(state=DISABLED)
    if chk_state_both.get() == False:
        chk_state_web.set(False)
        chk_state_svc.set(False)
        chkbox1.config(state=NORMAL)
        chkbox2.config(state=NORMAL)
def run_conn_test():
    pass
def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
def show_msg(count=None):
    """Loops through message automatically"""
    if count is not None:
        if count <= 5:
            txt = 'This is {} times though the loop.'.format(count)
            textw.delete('1.0', 'end')
            textw.insert('end', txt)
            count += 1
            root.after(1000, lambda: show_msg(count))
    else:
        show_msg(1)
def status():
    """Actual input from user"""
    stext1.delete(1.0, END)

    # environment
    env = env_switcher(environment.get())
    print("Enviroment: \n\t" + str(env))
    stext1.insert(INSERT, ("Enviroment: \n\t" + str(env) + "\n"))

    # Server type
    server_type = []
    if chk_state_web.get() == True:
        server_type.append("Web")
    if chk_state_svc.get() == True:
        server_type.append("Svc")
    if chk_state_both.get() == True:
        server_type = ["Web", "Svc"]
    print("Server Type: ")
    stext1.insert(END, ("Server Type: \n"))
    for item in server_type:
        print("\t" + str(item))
        stext1.insert(END, ("\t" + str(item) + "\n"))

    # Selected DC
    data_center = []
    if chk_state_ch2.get() == True:
        data_center.append("CH2")
    if chk_state_pdc.get() == True:
        data_center.append("PDC")
    if chk_state_wc.get() == True:
        data_center.append("WC")
    if chk_state_all.get() == True:
        data_center = ["CH2", "PDC", "WC"]
    print("Data Center: ")
    stext1.insert(END, ("Data Center: \n"))
    for dc in data_center:
        print("\t" + str(dc))
        stext1.insert(END, ("\t" + str(dc) + "\n"))

    # Port numbers
    print("Ports: ")
    ports = []
    stext1.insert(END, ("Ports: \n"))
    rough_ports = re.split(', |;|:|,| |_|-|!', input_box3.get())
    print("rough_Length = " + str(len(rough_ports)))
    for raw in rough_ports:
        raw.strip()
        raw.strip(',')
        if raw != "":
            ports.append(raw)
    print("good_Length = " + str(len(ports)))
    for port in ports:
        print(str(port))
        stext1.insert(END, ("\t" + str(port) + "\n"))

    # Destination
    print("Destinations: ")
    destinations = []
    stext1.insert(END, ("Destinations: \n"))
    rough_dst = re.split(', |;|:|,| |_|-|!', input_box2.get())
    print("rough_Length = " + str(len(rough_dst)))
    for raw1 in rough_dst:
        raw1.strip()
        raw1.strip(',')
        if raw1 != "":
            destinations.append(raw1)
    print("good_Length = " + str(len(destinations)))
    for dst in destinations:
        print(str(dst))
        stext1.insert(END, ("\t" + str(dst) + "\n"))
def powershell_script():
    remoteservers_list = []
    remoteservers = []
    env = env_switcher(environment.get())
    # INT SVC servers
    if ((env == "INT") and (chk_state_svc.get() == True) and (chk_state_ch2.get() == True)):
        for item in INT_SVC_CH2:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_svc.get() == True) and (chk_state_pdc.get() == True)):
        for item in INT_SVC_PDC:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_svc.get() == True) and (chk_state_wc.get() == True)):
        for item in INT_SVC_WC:
            remoteservers.append(item)
    # INT WEB servers
    if ((env == "INT") and (chk_state_web.get() == True) and (chk_state_ch2.get() == True)):
        for item in INT_WEB_CH2:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_web.get() == True) and (chk_state_pdc.get() == True)):
        for item in INT_WEB_PDC:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_web.get() == True) and (chk_state_wc.get() == True)):
        for item in INT_WEB_WC:
            remoteservers.append(item)

    # STG SVC servers
    if ((env == "STG") and (chk_state_svc.get() == True) and (chk_state_ch2.get() == True)):
        for item in STG_SVC_CH2:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_svc.get() == True) and (chk_state_pdc.get() == True)):
        for item in STG_SVC_PDC:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_svc.get() == True) and (chk_state_wc.get() == True)):
        for item in STG_SVC_WC:
            remoteservers.append(item)
    # STG WEB servers
    if ((env == "STG") and (chk_state_web.get() == True) and (chk_state_ch2.get() == True)):
        for item in STG_WEB_CH2:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_web.get() == True) and (chk_state_pdc.get() == True)):
        for item in STG_WEB_PDC:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_web.get() == True) and (chk_state_wc.get() == True)):
        for item in STG_WEB_WC:
            remoteservers.append(item)

    # PROD SVC servers
    if ((env == "PROD") and (chk_state_svc.get() == True) and (chk_state_ch2.get() == True)):
        for item in PROD_SVC_CH2:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_svc.get() == True) and (chk_state_pdc.get() == True)):
        for item in PROD_SVC_PDC:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_svc.get() == True) and (chk_state_wc.get() == True)):
        for item in PROD_SVC_WC:
            remoteservers.append(item)
    # PROD WEB servers
    if ((env == "PROD") and (chk_state_web.get() == True) and (chk_state_ch2.get() == True)):
        for item in PROD_WEB_CH2:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_web.get() == True) and (chk_state_pdc.get() == True)):
        for item in PROD_WEB_PDC:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_web.get() == True) and (chk_state_wc.get() == True)):
        for item in PROD_WEB_WC:
            remoteservers.append(item)

    # Destinations
    destinations = []
    rough_dst = re.split(', |;|:|,| |_|-|!', input_box2.get())
    for raw1 in rough_dst:
        raw1.strip()
        raw1.strip(',')
        if raw1 != "":
            destinations.append(raw1)

    # Ports
    ports = []
    rough_ports = re.split(', |;|:|,| |_|-|!', input_box3.get())
    for raw in rough_ports:
        raw.strip()
        raw.strip(',')
        if raw != "":
            ports.append(raw)
    # timeout
    timeout = "3"

    stext1.delete(1.0, END)
    #process = subprocess.Popen(["powershell", "Get-Childitem C:\\Windows\\*.log"], stdout=subprocess.PIPE);
    for remoteserver in remoteservers:
        for node in destinations:
            for port in ports:
                successMsg = "Connection ESTABLISHED from " + remoteserver + " to " +node+ " on PORT "+port
                failedMsg = "Connection FAILED from "+remoteserver + " to " +node+ " on PORT " +port
                cmd01 = "Get-Childitem C:\\Windows\\*.log"
                cmd02 = "(New-Object System.Net.Sockets.TcpClient).Connect(\""+node+"\","+port+")"      # Working
                connectCmd = "try {" + cmd02 + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"                                                              # Test
                invokeRemoteCmd = "Invoke-Command -ComputerName " + remoteserver + " -ScriptBlock { " + connectCmd + " }"  # Test
                process = subprocess.Popen(["powershell", invokeRemoteCmd], stdout=subprocess.PIPE);
                answer = process.communicate()[0]
                answer01 = str(answer.decode()).replace("\n", " ")
                stext1.insert('end', answer01)
                stext1.insert('end', "\n")
                print("Now on "+ remoteserver)
                window.update()
def powershell_test():
    stext1.delete(1.0, END)
    process = subprocess.Popen(["powershell", "Get-Childitem C:\\Windows\\*.log"], stdout=subprocess.PIPE);
    result = process.communicate()[0]
    print(result)
    stext1.insert(END, result)
def conn_screen_delete():
    stext1.delete(1.0, END)
    stext2.delete(1.0, END)
    # Reset button
    btn20.configure(bg='lightgreen')
    btn21.configure(bg='lightgreen')
    btn22.configure(bg='lightgreen')
    btn23.configure(bg='lightgreen')
    btn24.configure(bg='lightgreen')
    # Button
    btn3.place_forget()
    btn4.place_forget()
    btn5.place_forget()
    btn6.place_forget()
    btn7.place_forget()
    btn8.place_forget()
    btn9.place_forget()
    btn10.place_forget()
    btn12.place_forget()
    conn_test.place_forget()
    dns_test.place_forget()
    host_entry.place_forget()
    gen_csr.place_forget()
    val_csr.place_forget()
    sec_proto.place_forget()
    btn13.place_forget()
    btn14.place_forget()
    btn15.place_forget()
    btn16.place_forget()
    btn17.place_forget()
    btn18.place_forget()
    btn19.place_forget()
    btn20.place_forget()
    btn21.place_forget()
    btn22.place_forget()
    btn23.place_forget()
    btn24.place_forget()
    btn25.place_forget()
    btn26.place_forget()
    #
    env_label1.place_forget()
    env_label2.place_forget()
    env_label4.place_forget()
    env_label5.place_forget()
    env_label6.place_forget()
    env_label7.place_forget()
    env_label8.place_forget()
    env_label9.place_forget()
    env_label10.place_forget()
    env_label11.place_forget()
    env_label12.place_forget()
    env_label13.place_forget()
    env_label14.place_forget()
    env_label15.place_forget()
    env_label16.place_forget()
    #
    input_box2.place_forget()
    input_box3.place_forget()
    input_box4.place_forget()
    input_box5.place_forget()
    input_box6.place_forget()
    #
    chkbox1.place_forget()
    chkbox2.place_forget()
    chkbox02.place_forget()
    chkbox3.place_forget()
    chkbox4.place_forget()
    chkbox5.place_forget()
    chkbox51.place_forget()
    chkbox6.place_forget()
    chkbox7.place_forget()
    chkbox8.place_forget()
    chkbox9.place_forget()
    chkbox10.place_forget()
    chkbox11.place_forget()
    chkbox12.place_forget()
    chkbox13.place_forget()
    chkbox14.place_forget()
    chkbox15.place_forget()
    chkbox16.place_forget()
    chkbox17.place_forget()
    chkbox18.place_forget()
    chkbox19.place_forget()
    chkbox20.place_forget()
    chkbox21.place_forget()
    chkbox22.place_forget()
    chkbox23.place_forget()
    chkbox24.place_forget()
    chkbox25.place_forget()
    chkbox26.place_forget()
    chkbox27.place_forget()
    chkbox28.place_forget()
    chkbox29.place_forget()
    chkbox30.place_forget()
    chkbox31.place_forget()
    chkbox32.place_forget()
    chkbox33.place_forget()
    chkbox34.place_forget()
    chkbox35.place_forget()
    chkbox36.place_forget()
    chkbox37.place_forget()
    chkbox38.place_forget()
    chkbox39.place_forget()
    chkbox40.place_forget()
    #
    rad1.place_forget()
    rad2.place_forget()
    rad3.place_forget()
    rad04.place_forget()
    rad05.place_forget()
    #
    stext1.place_forget()
    stext2.place_forget()
    #
    spin1.place_forget()
    #
    lf.place_forget()
    lf1.place_forget()
    #

    window.update()
def conn_screen_create():
    conn_screen_delete()
    #
    chk_state_web.set(False)
    chk_state_svc.set(False)
    chk_state_both.set(False)
    chk_state_ch2.set(False)
    chk_state_pdc.set(False)
    chk_state_wc.set(False)
    chk_state_all.set(False)
    #
    chkbox3.config(state=NORMAL)
    chkbox4.config(state=NORMAL)
    chkbox5.config(state=NORMAL)
    chkbox51.config(state=NORMAL)
    chkbox1.config(state=NORMAL)
    chkbox2.config(state=NORMAL)
    chkbox02.config(state=NORMAL)
    # Buttons
    btn1.place(x=0, y=0)
    btn2.place(x=150, y=0)
    btn4.place(x=950, y=150)
    btn5.place(x=950, y=180)
    btn6.place(x=950, y=210)
    btn7.place(x=950, y=240)
    btn8.place(x=800, y=100)
    btn9.place(x=920, y=100)
    btn10.place(x=920, y=70)
    btn11.place(x=930, y=0)
    #btn12.place(x=930, y=0)
    #
    env_label1.place(x=0, y=50)
    env_label2.place(x=195, y=50)
    env_label4.place(x=5, y=150)
    env_label5.place(x=684, y=50)
    env_label6.place(x=464, y=50)
    #
    input_box2.place(x=114, y=150)
    input_box3.place(x=682, y=102)
    #
    chkbox1.place(x=195, y=100)
    chkbox2.place(x=250, y=100)
    chkbox02.place(x=300, y=100)
    chkbox3.place(x=415, y=100)
    chkbox4.place(x=475, y=100)
    chkbox5.place(x=535, y=100)
    chkbox51.place(x=590, y=100)
    #
    rad1.place(x=0, y=100)
    rad2.place(x=48, y=100)
    rad3.place(x=98, y=100)
    #
    stext1.place(x=5, y=180)
    #
    window.update()
def host_editor():
    conn_screen_delete()
    stext1.place(x=5, y=120)
    env_label8.place(x=10, y=50)
    env_label9.place(x=200, y=50)
    input_box5.place(x=43, y=52)
    input_box6.place(x=249, y=52)
    btn15.place(x=555, y=50)
    btn16.place(x=580, y=50)
    env_label10.place(x=10, y=80)
    spin1.place(x=115,y=81)
    btn17.place(x=180,y=78)
    btn18.place(x=247, y=78)
    btn19.place(x=328, y=78)
    filepath = "C:\Windows\System32\drivers\etc\hosts"
    # Open file
    stext1.delete(1.0, END)
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 0
        while line:
            #print("Line {}: {}".format(cnt, line.strip()))
            stext1.insert(END, ("Line {}: {}\n".format(cnt, line.strip())))
            line = fp.readline()
            cnt += 1
    fp.close()
    window.update()
def comment_host():
    filename = "C:\Windows\System32\drivers\etc\hosts"
    file = open(filename, "w+")
    lines = file.readlines()
    index = int(spin1.get())
    current = lines[index]
    print(current)
    if not current.startswith("#"):
        newfile = "# " + current
        file.writelines(newfile)
        print(newfile)
    file.close()
def uncomment_host():
    filename = "C:\Windows\System32\drivers\etc\hosts"
    file = open(filename, "w+")
    lines = file.readlines()
    index = int(spin1.get())
    current = lines[index]
    print(current)
    if current.startswith("#"):
        newfile = current.replace('#', '')
        file.writelines(newfile)
        print(newfile)
    file.close()
def crypto():
    conn_screen_delete()
    btn20.place(x=5, y=50)      # Client
    btn21.place(x=160, y=50)    # Server
    btn22.place(x=315, y=50)    # Ciphers
    btn23.place(x=470, y=50)    # Hash
    btn24.place(x=625, y=50)    # Key Exchange
    #seperator_h.place(x=4,y=90)
def cry_SChannel():
    # Reset checkboxes
    # Client protocols state
    chk_state_cl_p1.set(False)
    chk_state_cl_s2.set(False)
    chk_state_cl_s3.set(False)
    chk_state_cl_t0.set(False)
    chk_state_cl_t1.set(False)
    chk_state_cl_t2.set(False)
    chk_state_cl_all.set(False)

    # Server Protocols state
    chk_state_sl_p1.set(False)
    chk_state_sl_s2.set(False)
    chk_state_sl_s3.set(False)
    chk_state_sl_t0.set(False)
    chk_state_sl_t2.set(False)
    chk_state_sl_all.set(False)

    # hashes
    chk_state_h_md.set(False)
    chk_state_h_s1.set(False)
    chk_state_h_s2.set(False)
    chk_state_h_s3.set(False)
    chk_state_h_s4.set(False)

    # Key Exchanges
    chk_state_ke_dh.set(False)
    chk_state_ke_pk.set(False)
    chk_state_ke_ec.set(False)

    # Ciphers
    chk_state_c_null.set(False)
    chk_state_c_d.set(False)
    chk_state_c_ra.set(False)
    chk_state_c_rb.set(False)
    chk_state_c_rc.set(False)
    chk_state_c_rw.set(False)
    chk_state_c_rx.set(False)
    chk_state_c_ry.set(False)
    chk_state_c_rz.set(False)
    chk_state_c_t.set(False)
    chk_state_c_a1.set(False)
    chk_state_c_a2.set(False)

    # Update with current settings
    schannel_get_status()

    conn_screen_delete()
    btn20.configure(bg='orange')
    btn20.place(x=5, y=50)  # Schannel
    btn21.place(x=160, y=50) # Ciphers
    btn22.place(x=315, y=50) # Site Scanner
    btn23.place(x=470, y=50) # Templates
    btn24.place(x=625, y=50)  # More
    btn25.place(x=840, y=115)  # Apply
    btn26.place(x=840, y=155)  # Recommendation
    # heading labels
    env_label11.place(x=45,y=115) # Client
    env_label12.place(x=45, y=385) # Server
    env_label13.place(x=480, y=115) # Ciphers
    env_label14.place(x=265, y=385) # Hash
    env_label15.place(x=265, y=115) # Key Exchange
    env_label16.place(x=840, y=250) # Advance_schannel
    # LF
    lf.place(x=840, y=340)
    lf1.place(x=40, y=644)
    # client protocols
    chkbox6.place(x=50,y=150)
    chkbox7.place(x=50, y=180)
    chkbox8.place(x=50, y=210)
    chkbox9.place(x=50, y=240)
    chkbox10.place(x=50, y=270)
    chkbox11.place(x=50, y=300)
    chkbox12.place(x=50, y=330)
    # server protocols
    chkbox13.place(x=50, y=420)
    chkbox14.place(x=50, y=450)
    chkbox15.place(x=50, y=480)
    chkbox16.place(x=50, y=510)
    chkbox17.place(x=50, y=540)
    chkbox18.place(x=50, y=570)
    chkbox19.place(x=50, y=600)
    # hashes
    chkbox20.place(x=270, y=420)
    chkbox21.place(x=270, y=450)
    chkbox22.place(x=270, y=480)
    chkbox23.place(x=270, y=510)
    chkbox24.place(x=270, y=540)
    # Key Exchanges
    chkbox25.place(x=270, y=150)
    chkbox26.place(x=270, y=180)
    chkbox27.place(x=270, y=210)
    # Ciphers
    chkbox28.place(x=485, y=150)
    chkbox29.place(x=485, y=180)
    chkbox30.place(x=485, y=210)
    chkbox31.place(x=485, y=240)
    chkbox32.place(x=485, y=270)
    chkbox33.place(x=485, y=300)
    chkbox34.place(x=485, y=330)
    chkbox35.place(x=485, y=360)
    chkbox36.place(x=485, y=390)
    chkbox37.place(x=485, y=420)
    chkbox38.place(x=485, y=450)
    chkbox39.place(x=485, y=480)
    #
    chkbox40.place(x=920, y=115)
    #
    rad04.place(x=840, y=300)
    rad05.place(x=920, y=300)
    #
    chkbox3.place(x=847, y=370)
    chkbox4.place(x=847, y=403)
    chkbox5.place(x=847, y=436)
    chkbox51.place(x=847, y=469)
    #
    chkbox1.place(x=924, y=373)
    chkbox2.place(x=924, y=406)
    chkbox02.place(x=924, y=439)
    #
    chk_state_web.set(False)
    chk_state_svc.set(False)
    chk_state_both.set(False)
    chk_state_ch2.set(False)
    chk_state_pdc.set(False)
    chk_state_wc.set(False)
    chk_state_all.set(False)
    #
    chkbox3.config(state=DISABLED)
    chkbox4.config(state=DISABLED)
    chkbox5.config(state=DISABLED)
    chkbox51.config(state=DISABLED)
    chkbox1.config(state=DISABLED)
    chkbox2.config(state=DISABLED)
    chkbox02.config(state=DISABLED)
    #
    chkbox3.config(bg='ivory4')
    chkbox4.config(bg='ivory4')
    chkbox5.config(bg='ivory4')
    chkbox51.config(bg='ivory4')
    chkbox1.config(bg='ivory4')
    chkbox2.config(bg='ivory4')
    chkbox02.config(bg='ivory4')
    #
    stext2.place(x=45, y=650)
    #
    window.update()
def cry_Ciphers():
    conn_screen_delete()
    btn20.place(x=5, y=50)  # Client
    btn21.place(x=160, y=50)  # Server
    btn22.place(x=315, y=50)  # Ciphers
    btn23.place(x=470, y=50)  # Hash
    btn24.place(x=625, y=50)  # Key Exchange
def cry_SiteScanner():
    conn_screen_delete()
    btn20.place(x=5, y=50)  # Client
    btn21.place(x=160, y=50)  # Server
    btn22.place(x=315, y=50)  # Ciphers
    btn23.place(x=470, y=50)  # Hash
    btn24.place(x=625, y=50)  # Key Exchange
def cry_Templates():
    conn_screen_delete()
    btn20.place(x=5, y=50)  # Client
    btn21.place(x=160, y=50)  # Server
    btn22.place(x=315, y=50)  # Ciphers
    btn23.place(x=470, y=50)  # Hash
    btn24.place(x=625, y=50)  # Key Exchange
def cry_More():
    conn_screen_delete()
    btn20.place(x=5, y=50)  # Client
    btn21.place(x=160, y=50)  # Server
    btn22.place(x=315, y=50)  # Ciphers
    btn23.place(x=470, y=50)  # Hash
    btn24.place(x=625, y=50)  # Key Exchange
def ssh_example():
    ssh = subprocess.Popen(["ssh", "-i .ssh/id_rsa", "user@host"],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           bufsize=0)

    # Send ssh commands to stdin
    ssh.stdin.write("uname -a\n")
    ssh.stdin.write("uptime\n")
    ssh.stdin.close()

    # Fetch output
    for line in ssh.stdout:
        print(line.strip())
def schannel_actions():
    #command_varibles
    c_pct1 = ""
    c_ssl2 = ""
    c_ssl3 = ""
    c_tls1 = ""
    c_tls2 = ""
    c_tls3 = ""
    c_all1 = ""

    s_pct1 = ""
    s_ssl2 = ""
    s_ssl3 = ""
    s_tls1 = ""
    s_tls2 = ""
    s_tls3 = ""
    s_all1 = ""

    h_md5 = ""
    h_sha = ""
    h_sha2 = ""
    h_sha3 = ""
    h_sha5 = ""

    ke_dh = ""
    ke_pk = ""
    ke_ec = ""

    ci_null = ""
    ci_des = ""
    ci_rc24 = ""
    ci_rc25 = ""
    ci_rc212 = ""
    ci_rc44 = ""
    ci_rc45 = ""
    ci_rc46 = ""
    ci_rc412 = ""
    ci_tdes = ""
    ci_aes1 = ""
    ci_aes2 = ""

    # Create list of commands
    command_list = [
        c_pct1,
        c_ssl2,
        c_ssl3,
        c_tls1,
        c_tls2,
        c_tls3,
        c_all1,
        s_pct1,
        s_ssl2,
        s_ssl3,
        s_tls1,
        s_tls2,
        s_tls3,
        s_all1,
        h_md5,
        h_sha,
        h_sha2,
        h_sha3,
        h_sha5,
        ke_dh,
        ke_pk,
        ke_ec,
        ci_null,
        ci_des,
        ci_rc24,
        ci_rc25,
        ci_rc212,
        ci_rc44,
        ci_rc45,
        ci_rc46,
        ci_rc412,
        ci_tdes,
        ci_aes1,
        ci_aes2,
    ]

    # Client Protocols
    if chk_state_cl_p1.get() == True:
        c_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_cl_s2.get() == True:
        c_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_cl_s3.get() == True:
        c_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_cl_t0.get() == True:
        c_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_cl_t1.get() == True:
        c_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_cl_t2.get() == True:
        c_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_cl_all.get() == True:
        c_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
        c_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
        c_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
        c_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
        c_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
        c_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'DisabledByDefault' -Value '0x00000000'"
    #
    if chk_state_cl_p1.get() == False:
        c_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_cl_s2.get() == False:
        c_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_cl_s3.get() == False:
        c_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_cl_t0.get() == False:
        c_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_cl_t1.get() == False:
        c_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_cl_t2.get() == False:
        c_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_cl_all.get() == False:
        c_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
        c_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
        c_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
        c_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
        c_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Client' -Name 'DisabledByDefault' -Value '0x00000001'"
        c_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'DisabledByDefault' -Value '0x00000001'"

    # Sever Protocols
    if chk_state_sl_p1.get() == True:
        s_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_sl_s2.get() == True:
        s_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_sl_s3.get() == True:
        s_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_sl_t0.get() == True:
        s_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_sl_t1.get() == True:
        s_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_sl_t2.get() == True:
        s_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
    if chk_state_sl_all.get() == True:
        s_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
        s_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
        s_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
        s_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
        s_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
        s_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'Enabled' -Value '0x00000001'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'DisabledByDefault' -Value '0x00000000'"
        #
        #
    #
    if chk_state_sl_p1.get() == False:
        s_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_sl_s2.get() == False:
        s_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_sl_s3.get() == False:
        s_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_sl_t0.get() == False:
        s_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_sl_t1.get() == False:
        s_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_sl_t2.get() == False:
        s_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
    if chk_state_sl_all.get() == False:
        s_pct1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\PCT 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
        s_ssl2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
        s_ssl3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
        s_tls1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
        s_tls2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.1\Server' -Name 'DisabledByDefault' -Value '0x00000001'"
        s_tls3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'Enabled' -Value '0x00000000'; " \
                 "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'DisabledByDefault' -Value '0x00000001'"

    #	Hashes
    if chk_state_h_md.get() == True:
        h_md5 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_h_s1.get() == True:
        h_sha = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_h_s2.get() == True:
        h_sha2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA256' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_h_s3.get() == True:
        h_sha3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA384' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_h_s4.get() == True:
        h_sha5 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA512' -Name 'Enabled' -Value '0x00000001'"
    #
    if chk_state_h_md.get() == False:
        h_md5 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_h_s1.get() == False:
        h_sha = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_h_s2.get() == False:
        h_sha2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA256' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_h_s3.get() == False:
        h_sha3 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA384' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_h_s4.get() == False:
        h_sha5 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\SHA512' -Name 'Enabled' -Value '0x00000000'"

    # Key Exchanges
    if chk_state_ke_dh.get() == True:
        ke_dh = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\Diffie-Hellman' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_ke_pk.get() == True:
        ke_pk = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\PKCS' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_ke_ec.get() == True:
        ke_ec = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\ECDH' -Name 'Enabled' -Value '0x00000001'"
    #
    if chk_state_ke_dh.get() == False:
        ke_dh = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\Diffie-Hellman' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_ke_pk.get() == False:
        ke_pk = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\PKCS' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_ke_ec.get() == False:
        ke_ec = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\ECDH' -Name 'Enabled' -Value '0x00000001'"

    # Ciphers
    if chk_state_c_null.get() == True:
        ci_null = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\\NULL' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_d.get() == True:
        ci_des = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\DES 56/56' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_ra.get() == True:
        ci_rc24 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 40/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_rb.get() == True:
        ci_rc25 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 56/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_rc.get() == True:
        ci_rc212 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 128/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_rw.get() == True:
        ci_rc44 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 40/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_rx.get() == True:
        ci_rc45 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 56/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_ry.get() == True:
        ci_rc46 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 64/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_rz.get() == True:
        ci_rc412 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 128/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_t.get() == True:
        ci_tdes = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\Triple DES 168' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_a1.get() == True:
        ci_aes1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\AES 128/128' -Name 'Enabled' -Value '0x00000001'"
    if chk_state_c_a2.get() == True:
        ci_aes2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\AES 256/256' -Name 'Enabled' -Value '0x00000001'"
    #
    if chk_state_c_null.get() == False:
        ci_null = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\\NULL' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_d.get() == False:
        ci_des = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\DES 56/56' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_ra.get() == False:
        ci_rc24 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 40/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_rb.get() == False:
        ci_rc25 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 56/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_rc.get() == False:
        ci_rc212 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC2 128/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_rw.get() == False:
        ci_rc44 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 40/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_rx.get() == False:
        ci_rc45 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 56/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_ry.get() == False:
        ci_rc46 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 64/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_rz.get() == False:
        ci_rc412 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\RC4 128/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_t.get() == False:
        ci_tdes = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\Triple DES 168' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_a1.get() == False:
        ci_aes1 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\AES 128/128' -Name 'Enabled' -Value '0x00000000'"
    if chk_state_c_a2.get() == False:
        ci_aes2 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\AES 256/256' -Name 'Enabled' -Value '0x00000000'"

    ###################################
    remoteservers_list = []
    remoteservers = []
    env = env_switcher(environment.get())
    # INT SVC servers
    if ((env == "INT") and (chk_state_svc.get() == True) and (chk_state_ch2.get() == True)):
        for item in INT_SVC_CH2:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_svc.get() == True) and (chk_state_pdc.get() == True)):
        for item in INT_SVC_PDC:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_svc.get() == True) and (chk_state_wc.get() == True)):
        for item in INT_SVC_WC:
            remoteservers.append(item)
    # INT WEB servers
    if ((env == "INT") and (chk_state_web.get() == True) and (chk_state_ch2.get() == True)):
        for item in INT_WEB_CH2:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_web.get() == True) and (chk_state_pdc.get() == True)):
        for item in INT_WEB_PDC:
            remoteservers.append(item)
    if ((env == "INT") and (chk_state_web.get() == True) and (chk_state_wc.get() == True)):
        for item in INT_WEB_WC:
            remoteservers.append(item)

    # STG SVC servers
    if ((env == "STG") and (chk_state_svc.get() == True) and (chk_state_ch2.get() == True)):
        for item in STG_SVC_CH2:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_svc.get() == True) and (chk_state_pdc.get() == True)):
        for item in STG_SVC_PDC:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_svc.get() == True) and (chk_state_wc.get() == True)):
        for item in STG_SVC_WC:
            remoteservers.append(item)
    # STG WEB servers
    if ((env == "STG") and (chk_state_web.get() == True) and (chk_state_ch2.get() == True)):
        for item in STG_WEB_CH2:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_web.get() == True) and (chk_state_pdc.get() == True)):
        for item in STG_WEB_PDC:
            remoteservers.append(item)
    if ((env == "STG") and (chk_state_web.get() == True) and (chk_state_wc.get() == True)):
        for item in STG_WEB_WC:
            remoteservers.append(item)

    # PROD SVC servers
    if ((env == "PROD") and (chk_state_svc.get() == True) and (chk_state_ch2.get() == True)):
        for item in PROD_SVC_CH2:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_svc.get() == True) and (chk_state_pdc.get() == True)):
        for item in PROD_SVC_PDC:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_svc.get() == True) and (chk_state_wc.get() == True)):
        for item in PROD_SVC_WC:
            remoteservers.append(item)
    # PROD WEB servers
    if ((env == "PROD") and (chk_state_web.get() == True) and (chk_state_ch2.get() == True)):
        for item in PROD_WEB_CH2:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_web.get() == True) and (chk_state_pdc.get() == True)):
        for item in PROD_WEB_PDC:
            remoteservers.append(item)
    if ((env == "PROD") and (chk_state_web.get() == True) and (chk_state_wc.get() == True)):
        for item in PROD_WEB_WC:
            remoteservers.append(item)

    # Credentials
    credentials = "Get-Credential -Credential .\\administrator"

    if local_remote.get() == 1:
        # Remote computer changes
        for remoteserver in remoteservers:
            for cmd in command_list:
                successMsg = cmd + " : Apply Success : "+ remoteserver
                failedMsg = cmd + " : Apply Failed : "+ remoteserver
                connectCmd = "try {" + cmd + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"
                #connectCmd1 = "try {Enter-PSSession -ComputerName " + remoteserver + " -Credential " + credential + "; " + cmd + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"
                #invokeRemoteCmd1 = "Invoke-Command -ComputerName " + remoteserver + " -ScriptBlock { " + connectCmd + " }"
                invokeRemoteCmd = "Invoke-Command -ComputerName " + remoteserver + " -Credential " + credential + " -ScriptBlock { " + connectCmd + " }"
                process = subprocess.Popen(["powershell", invokeRemoteCmd], stdout=subprocess.PIPE);
                answer = process.communicate()[0]
                answer01 = str(answer.decode()).replace("\n", " ")
                print("Now on " + remoteserver)
                print(answer01)

    if local_remote.get() == 0:
        for cmd in command_list:
            # Local Machine changes
            successMsg = cmd + " : Apply Success : "
            failedMsg = cmd + " : Apply Failed : "
            connectCmd = "try {" + cmd + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"
            # connectCmd1 = "try {Enter-PSSession -ComputerName " + remoteserver + " -Credential " + credential + "; " + cmd + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"
            # invokeRemoteCmd1 = "Invoke-Command -ComputerName " + remoteserver + " -ScriptBlock { " + connectCmd + " }"
            #invokeRemoteCmd = "Invoke-Command -ComputerName " + remoteserver + " -Credential " + credential + " -ScriptBlock { " + connectCmd + " }"
            process = subprocess.Popen(["powershell", connectCmd], stdout=subprocess.PIPE);
            answer = process.communicate()[0]
            answer01 = str(answer.decode()).replace("\n", " ")
            stext2.insert('end', answer01)
            stext2.insert('end', "\n")
            print(answer01)
    window.update()
def schannel_get_status():
    machine = ['Client', 'Server']
    protocols = ['PCT 1.0','SSL 2.0','SSL 3.0','TLS 1.0','TLS 1.1','TLS 1.2']
    hashes = ['MD5','SHA','SHA256','SHA384','SHA512']
    key_exch = ['Diffie-Hellman','ECDH','PKCS']
    ciphers = ['NULL','AES 128/128','AES 256/256','DES 56/56','RC2 128/128','RC2 40/128','RC2 56/128','RC4 128/128','RC4 40/128','RC4 56/128','RC4 64/128','Triple DES 168']
    client_dict_proto = {'PCT 1.0':'chk_state_cl_p1','SSL 2.0':'chk_state_cl_s2','SSL 3.0':'chk_state_cl_s3','TLS 1.0':'chk_state_cl_t0','TLS 1.1':'chk_state_cl_t1','TLS 1.2':'chk_state_cl_t2'}
    server_dict_proto = {'PCT 1.0':'chk_state_sl_p1', 'SSL 2.0': 'chk_state_sl_s2', 'SSL 3.0': 'chk_state_sl_s3','TLS 1.0': 'chk_state_sl_t0', 'TLS 1.1': 'chk_state_sl_t1', 'TLS 1.2': 'chk_state_sl_t2'}
    hash_dict = {'MD5':'chk_state_h_md','SHA':'chk_state_h_s1','SHA256':'chk_state_h_s2','SHA384':'chk_state_h_s3','SHA512':'chk_state_h_s4'}
    ciphers_dict = {'NULL':'chk_state_c_null','AES 128/128':'chk_state_c_a1','AES 256/256':'chk_state_c_a2','DES 56/56':'chk_state_c_d','RC2 128/128':'chk_state_c_rc','RC2 40/128':'chk_state_c_ra',\
                    'RC2 56/128':'chk_state_c_rb','RC4 128/128':'chk_state_c_rz','RC4 40/128':'chk_state_c_rw','RC4 56/128':'chk_state_c_rx','RC4 64/128':'chk_state_c_ry','Triple DES 168':'chk_state_c_t'}
    ke_dict = {'Diffie-Hellman':'chk_state_ke_dh','ECDH':'chk_state_ke_ec','PKCS':'chk_state_ke_pk'}
    # Get Protocols
    #check if Local or remote machine execution
    # local = 0; remote = 1
    if local_remote.get() == 0:
        for p in protocols:
            for m in machine:
                try:
                    cmd1 = ("get-ItemPropertyValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\\"+p+"\\"+m+ "' -Name 'Enabled' ")
                    process1 = subprocess.Popen(["powershell", cmd1], stdout=subprocess.PIPE);
                    answer1 = process1.communicate()[0]
                    answer1 = str(answer1.decode())
                    #answer1 == 0
                    #if (answer1 != "0") or (answer1 is not str(0)) or (hex(answer1) != '0x00000000'):
                    if (answer1 != "0") or (answer1 is not 0) or (answer1 != "0x00000000") or (answer1 != hex(0)) or (answer1 != str(0)) :
                        if m == "Client":
                            if p == 'PCT 1.0':
                                chk_state_cl_p1.set(True)
                            if p == 'SSL 2.0':
                                chk_state_cl_s2.set(True)
                            if p == 'SSL 3.0':
                                chk_state_cl_s3.set(True)
                            if p == 'TLS 1.0':
                                chk_state_cl_t0.set(True)
                            if p == 'TLS 1.1':
                                chk_state_cl_t1.set(True)
                            if p == 'TLS 1.2':
                                chk_state_cl_t2.set(True)
                        if m == "Server":
                            obj1 = globals() [server_dict_proto[p]]
                            obj1.set(True)
                    print("answer1: "+m+ " : "+p+": Value: "+ answer1)
                    print(type(answer1))
                except:
                    print("No Such "+ m +" Protocol: "+ p)

        # Get hash
        for h in hashes:
            cmd2 = ("get-ItemPropertyValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\\" + h +"' -Name 'Enabled' ")
            process2 = subprocess.Popen(["powershell", cmd2], stdout=subprocess.PIPE);
            answer2 = process2.communicate()[0]
            answer2 = str(answer2.decode())
            # answer2 == 0
            #if (answer2 != "0") or (answer2 is not str(0)) or (hex(answer2) != '0x00000000'):
            if (answer2 is "0"):
                obj2 = globals() [hash_dict[h]]
                obj2.set(True)
            print("answer2: " + h+ ": Value: " + answer2)
            print(type(answer2))
        # Key Exchanges
        for k in key_exch:
            cmd3 = ("get-ItemPropertyValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\KeyExchangeAlgorithms\\" + k +"' -Name 'Enabled' ")
            process3 = subprocess.Popen(["powershell", cmd3], stdout=subprocess.PIPE);
            answer3 = process3.communicate()[0]
            answer3 = str(answer3.decode())
            # answer3 == 0
            #if (answer3 != "0") or (answer3 is not str(0)) or (hex(answer3) != '0x00000000'):
            if (answer3 is "0"):
                obj3 = globals() [ke_dict[k]]
                obj3.set(True)
            print("answer3: " + k + ": Value: " + answer3)
            print(type(answer3))

        # Ciphers
        for c in ciphers:
            cmd4 = ("get-ItemPropertyValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Ciphers\\" + c +"' -Name 'Enabled' ")
            process4 = subprocess.Popen(["powershell", cmd4], stdout=subprocess.PIPE);
            answer4 = process4.communicate()[0]
            answer4 = str(answer4.decode())
            # answer4 == 0
            #if (answer4 != "0") or (answer4 is not str(0)) or (hex(answer4) != '0x00000000'):
            if (answer4 is "0"):
                obj4 = globals() [ciphers_dict[c]]
                obj4.set(True)
            print("answer4: " + c + ": Value: " + answer4)
            print(type(answer4))
    else:
        print("Not yet configured for remote operations")

    # get-ItemPropertyValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'Enabled'


#main window
window = Tk()

# Set default windows dimension (wxh)
window.geometry('1024x900')
window.configure(background='ivory4')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.title("OCN_APP")

# Set windows styles
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='black')
style.configure("green.Horizontal.TProgressbar", background='green')
style.configure("TSeparator", background='green')
#
# Seperators
#seperator_h = ttk.Separator(window, orient=HORIZONTAL, style='TSeparator')
#seperator_v = ttk.Separator(window, orient=VERTICAL)
# Label Frames
lf = LabelFrame(window, text="Env", width=170, height=200, bg='ivory4')
lf1 = LabelFrame(window, width=953, height=243, bg='ivory4')

# Adding buttons
btn1 = Button(window, text="Connectivity Test", fg="black", bg="lightblue", width=20, height=2, command=conn_screen_create)
btn2 = Button(window, text="View Server List", fg="black", bg="lightblue", width=20, height=2, command=server_info)
btn3 = Button(window, text="Add", fg="black", bg="lightblue", width=5, height=1)
btn4 = Button(window, text="Save", fg="black", bg="lightblue", width=8, height=1, command=file_save_as)
btn5 = Button(window, text="Open", fg="black", bg="lightblue", width=8, height=1, command=open_file)
btn6 = Button(window, text="Reload", fg="black", bg="lightblue", width=8, height=1)
btn7 = Button(window, text="Recent", fg="black", bg="lightblue", width=8, height=1)
btn8 = Button(window, text="Validate Selection", fg="black", bg="lightblue", width=14, height=1, command=status)
btn9 = Button(window, text="Run", fg="black", bg="lightblue", width=12, height=1, command=powershell_script)
btn10 = Button(window, text="Powershell Test", fg="black", bg="lightblue", width=12, height=1, command=powershell_test)
btn11 = Button(window, text="Hide", fg="black", bg="lightblue", width=12, height=1, command=conn_screen_delete)
btn12 = Button(window, text="Show", fg="black", bg="lightblue", width=12, height=1, command=conn_screen_create)
btn01 = Button(window, text="Network Tools", fg="black", bg="lightblue", width=20, height=2, command=network_tools)
btn02 = Button(window, text="Security Tools", fg="black", bg="lightblue", width=20, height=2, command=security_tools)
btn13 = Button(window, text="From List", fg="black", bg="lightblue", width=8, height=1)
btn14 = Button(window, text="Lookup", fg="black", bg="lightgreen", width=16, height=1)
btn15 = Button(window, text="+", fg="black", bg="lightblue", width=2, height=1, activebackground='cyan', foreground='red')
btn16 = Button(window, text="-", fg="black", bg="lightblue", width=2, height=1, activebackground='cyan', foreground='red')
btn17 = Button(window, text="comment", fg="black", bg="lightgreen", width=8, height=1, command=comment_host)
btn18 = Button(window, text="uncomment", fg="black", bg="lightgreen", width=10, height=1, command=uncomment_host)
btn19 = Button(window, text="delete", fg="black", bg="lightgreen", width=10, height=1)
btn20 = Button(window, text="SChannel", fg="black", bg="lightgreen", width=20, height=1, command=cry_SChannel)
btn21 = Button(window, text="Ciphers", fg="black", bg="lightgreen", width=20, height=1, command=cry_Ciphers)
btn22 = Button(window, text="Site Scanner", fg="black", bg="lightgreen", width=20, height=1, command=cry_SiteScanner)
btn23 = Button(window, text="Templates", fg="black", bg="lightgreen", width=20, height=1, command=cry_Templates)
btn24 = Button(window, text="More", fg="black", bg="lightgreen", width=20, height=1, command=cry_More)
btn25 = Button(window, text="Apply", fg="black", bg="orange", width=8, height=1, command=schannel_actions)
btn26 = Button(window, text="Recommendation", fg="black", bg="lightgreen", width=20, height=1, command=recomm_ciphers)
conn_test = Button(window, text="Connectivity Test", fg="black", bg="lightblue", width=20, height=2, activebackground='cyan', foreground='green', command=conn_screen_create)
dns_test = Button(window, text="DNS Resolution", fg="black", bg="lightblue", width=20, height=2,activebackground='cyan', foreground='green', command=dns_resolution)
host_entry = Button(window, text="Host Editor", fg="black", bg="lightblue", width=20, height=2, activebackground='cyan', foreground='green', command=host_editor)
gen_csr = Button(window, text="Generate CSR", fg="black", bg="lightblue", width=20, height=2, activebackground='cyan', foreground='red')
val_csr = Button(window, text="Validate CSR+Cert+Key", fg="black", bg="lightblue", width=20, height=2, activebackground='cyan', foreground='red')
sec_proto = Button(window, text="Crypto Editor", fg="black", bg="lightblue", width=20, height=2, activebackground='cyan', foreground='red', command=crypto)
btn1.place(x=0, y=0)
btn2.place(x=150, y=0)
btn01.place(x=300, y=0)
btn02.place(x=450, y=0)
btn11.place(x=930, y=0)

# adding labels
env_label1 = Label(window, text="Environment", font=("Arial Bold", 12), width=15, height=2)
env_label2 = Label(window, text="Server Type", font=("Arial Bold", 12), width=15, height=2)
env_label4 = Label(window, text="Destinations:", font=("Arial Bold", 10), width=12, height=1)
env_label5 = Label(window, text="Ports", font=("Arial Bold", 12), width=8, height=2)
env_label6 = Label(window, text="Data Center", font=("Arial Bold", 12), width=12, height=2)
env_label7 = Label(window, text="Host", font=("Arial Bold", 12), width=8, height=1, bg='ivory3')
env_label8 = Label(window, text="IP", font=("Arial Bold", 10), width=3, height=1, bg='ivory3')
env_label9 = Label(window, text="FQDN", font=("Arial Bold", 10), width=5, bg='ivory3')
env_label10 = Label(window, text="Line Entry", font=("Arial Bold", 10), width=12, bg='ivory3')
#
env_label11 = Label(window, text="Client Protocol", font=("Arial Bold", 10), width=12, bg='ivory3')
env_label12 = Label(window, text="Server Protocol", font=("Arial Bold", 10), width=12, bg='ivory3')
env_label13 = Label(window, text="Ciphers", font=("Arial Bold", 10), width=12, bg='ivory3')
env_label14 = Label(window, text="Hashes", font=("Arial Bold", 10), width=12, bg='ivory3')
env_label15 = Label(window, text="Key Exchanges", font=("Arial Bold", 10), width=12, bg='ivory3')
#
env_label16 = Label(window, text="Advanced", font=("Arial Bold", 12), width=15, height=1, bg='ivory3')
#
# Adding textbox
input_box2 = Entry(window, width=135)   # Location box
input_box3 = Entry(window, width=14)    # Port box
input_box4 = Entry(window, width=83)    # Endpoint DNS Lookup box
input_box5 = Entry(window, width=20)    # IP in Host Editor
input_box6 = Entry(window, width=50)    # FQDN in Host Editor

# Adding combobox
# Combobox allow user to select from a drop-down menu
combo1 = Combobox(window)
combo1['values']= range(1,100,1)
#combo1.current(0)       # setting the default value

# Adding checkbox
# Checking state of checkbox
chk_state_web = BooleanVar()
chk_state_svc = BooleanVar()
chk_state_both = BooleanVar()
chk_state_ch2 = BooleanVar()
chk_state_pdc = BooleanVar()
chk_state_wc = BooleanVar()
chk_state_all = BooleanVar()
# Client protocols state
chk_state_cl_p1 = BooleanVar()
chk_state_cl_s2 = BooleanVar()
chk_state_cl_s3 = BooleanVar()
chk_state_cl_t0 = BooleanVar()
chk_state_cl_t1 = BooleanVar()
chk_state_cl_t2 = BooleanVar()
chk_state_cl_all = BooleanVar()
# Server Protocols state
chk_state_sl_p1 = BooleanVar()
chk_state_sl_s2 = BooleanVar()
chk_state_sl_s3 = BooleanVar()
chk_state_sl_t0 = BooleanVar()
chk_state_sl_t1 = BooleanVar()
chk_state_sl_t2 = BooleanVar()
chk_state_sl_all = BooleanVar()
# hashes
chk_state_h_md = BooleanVar()
chk_state_h_s1 = BooleanVar()
chk_state_h_s2 = BooleanVar()
chk_state_h_s3 = BooleanVar()
chk_state_h_s4 = BooleanVar()
#
# Key Exchanges
chk_state_ke_dh = BooleanVar()
chk_state_ke_pk = BooleanVar()
chk_state_ke_ec = BooleanVar()
# Ciphers
chk_state_c_null = BooleanVar()
chk_state_c_d = BooleanVar()
chk_state_c_ra = BooleanVar()
chk_state_c_rb = BooleanVar()
chk_state_c_rc = BooleanVar()
chk_state_c_rw = BooleanVar()
chk_state_c_rx = BooleanVar()
chk_state_c_ry = BooleanVar()
chk_state_c_rz = BooleanVar()
chk_state_c_t = BooleanVar()
chk_state_c_a1 = BooleanVar()
chk_state_c_a2 = BooleanVar()
#
chk_state_reboot = BooleanVar()
#
#
#chk_state.set(True)      # Set state to be True
#chk_state.set(False)     # Set state to be False
chkbox1 = Checkbutton(window, text="Web", var=chk_state_web, bg='ivory4')
chkbox2 = Checkbutton(window, text="Svc", var=chk_state_svc, bg='ivory4')
chkbox02 = Checkbutton(window, text="Both", var=chk_state_both, bg='ivory4', command=all_servers)
chkbox3 = Checkbutton(window, text="CH2", var=chk_state_ch2, bg='ivory4')
chkbox4 = Checkbutton(window, text="PDC", var=chk_state_pdc, bg='ivory4')
chkbox5 = Checkbutton(window, text="WC", var=chk_state_wc, bg='ivory4')
chkbox51 = Checkbutton(window, text="ALL", var=chk_state_all, bg='ivory4', command=all_dc)
# Client Protocols
chkbox6 = Checkbutton(window, text="PCT 1.0", var=chk_state_cl_p1, bg='ivory4')
chkbox7 = Checkbutton(window, text="SSL 2.0", var=chk_state_cl_s2, bg='ivory4')
chkbox8 = Checkbutton(window, text="SSL 3.0", var=chk_state_cl_s3, bg='ivory4')
chkbox9 = Checkbutton(window, text="TLS 1.0", var=chk_state_cl_t0, bg='ivory4')
chkbox10 = Checkbutton(window, text="TLS 1.1", var=chk_state_cl_t1, bg='ivory4')
chkbox11 = Checkbutton(window, text="TLS 1.2", var=chk_state_cl_t2, bg='ivory4')
chkbox12 = Checkbutton(window, text="ALL Protocols", var=chk_state_cl_all, bg='ivory4', command=chkbtn_state)
# Server Protocols
chkbox13 = Checkbutton(window, text="PCT 1.0", var=chk_state_sl_p1, bg='ivory4')
chkbox14 = Checkbutton(window, text="SSL 2.0", var=chk_state_sl_s2, bg='ivory4')
chkbox15 = Checkbutton(window, text="SSL 3.0", var=chk_state_sl_s3, bg='ivory4')
chkbox16 = Checkbutton(window, text="TLS 1.0", var=chk_state_sl_t0, bg='ivory4')
chkbox17 = Checkbutton(window, text="TLS 1.1", var=chk_state_sl_t1, bg='ivory4')
chkbox18 = Checkbutton(window, text="TLS 1.2", var=chk_state_sl_t2, bg='ivory4')
chkbox19 = Checkbutton(window, text="ALL Protocols", var=chk_state_sl_all, bg='ivory4', command=chkbtn_state)
#
chkbox20 = Checkbutton(window, text="MD5", var=chk_state_h_md, bg='ivory4')
chkbox21 = Checkbutton(window, text="SHA", var=chk_state_h_s1, bg='ivory4')
chkbox22 = Checkbutton(window, text="SHA 256", var=chk_state_h_s2, bg='ivory4')
chkbox23 = Checkbutton(window, text="SHA 384", var=chk_state_h_s3, bg='ivory4')
chkbox24 = Checkbutton(window, text="SHA 512", var=chk_state_h_s4, bg='ivory4')
#
chkbox25 = Checkbutton(window, text="Diffie-Hellman", var=chk_state_ke_dh, bg='ivory4')
chkbox26 = Checkbutton(window, text="PKCS", var=chk_state_ke_pk, bg='ivory4')
chkbox27 = Checkbutton(window, text="ECDH", var=chk_state_ke_ec, bg='ivory4')
#
chkbox28 = Checkbutton(window, text="NULL", var=chk_state_c_null, bg='ivory4', command=chkbtn_state)
chkbox29 = Checkbutton(window, text="DES 56/56", var=chk_state_c_d, bg='ivory4')
chkbox30 = Checkbutton(window, text="RC2 40/128", var=chk_state_c_ra, bg='ivory4')
chkbox31 = Checkbutton(window, text="RC2 56/128", var=chk_state_c_rb, bg='ivory4')
chkbox32 = Checkbutton(window, text="RC2 128/128", var=chk_state_c_rc, bg='ivory4')
chkbox33 = Checkbutton(window, text="RC4 40/128", var=chk_state_c_rw, bg='ivory4')
chkbox34 = Checkbutton(window, text="RC4 56/128", var=chk_state_c_rx, bg='ivory4')
chkbox35 = Checkbutton(window, text="RC4 64/128", var=chk_state_c_ry, bg='ivory4')
chkbox36 = Checkbutton(window, text="RC4 128/128", var=chk_state_c_rz, bg='ivory4')
chkbox37 = Checkbutton(window, text="Triple DES 168", var=chk_state_c_t, bg='ivory4')
chkbox38 = Checkbutton(window, text="AES 128/128", var=chk_state_c_a1, bg='ivory4')
chkbox39 = Checkbutton(window, text="AES 256/256", var=chk_state_c_a2, bg='ivory4')
#
chkbox40 = Checkbutton(window, text="reboot", var=chk_state_c_a2, bg='ivory4')
#

#
# Adding Radio buttons
# checking state
environment = IntVar()
src_location = IntVar()
local_remote = IntVar()
rad1 = Radiobutton(window, text="INT", value=1, variable=environment, bg='ivory4')
rad2 = Radiobutton(window, text="STG", value=2, variable=environment, bg='ivory4')
rad3 = Radiobutton(window, text="PROD", value=3, variable=environment, bg='ivory4')
#rad2.select()   # default value
rad01 = Radiobutton(window, text="AWS", value=1, variable=src_location, command=mutable)
rad02 = Radiobutton(window, text="On-Prem", value=2, variable=src_location, command=mutable)
rad03 = Radiobutton(window, text="Other", value=3, variable=src_location, command=input_box, width=10)
#
rad04 = Radiobutton(window, text="Local", value=0, variable=local_remote, bg='ivory4', command=chkbtn_state)
rad05 = Radiobutton(window, text="Remote", value=1, variable=local_remote, bg='ivory4',command=chkbtn_state)


# Adding scrolledText
# Specify deminsion of scrolledText
stext1 = scrolledtext.ScrolledText(window, width=115, height=40, wrap='word')       # main windows
stext2 = scrolledtext.ScrolledText(window, width=115, height=14, wrap='word')       # crypto_window
stext1.delete(1.0, END)  # Delete the entire content
stext2.delete(1.0, END)  # Delete the entire content
#stext1.place(x=5, y=180)
stext1.insert(INSERT, "")          # Inserting items in box


# Adding message boxes
#messagebox.showinfo('Message Title', 'Message Content')         # Info message
#messagebox.showwarning('Message Title', 'Message Content')      # Warming message
#messagebox.showerror('Message Title', 'Message Content')        # Asking message
#messagebox.askquestion('Message title','Message content')       # Asking message
#messagebox.askyesno('Message title','Message content')          # Asking message
#messagebox.askyesnocancel('Message title','Message content')    # Asking message
#messagebox.askokcancel('Message title','Message content')       # Asking message
#messagebox.askretrycancel('Message title','Message content')    # Asking message

# Adding spinboxes
# A selection of numbers
#spin_var = IntVar()
#spin_var.set(20)        # Set default value
spin1 = Spinbox(window, from_=0, to=100, width=8)         # host line number
#spin = Spinbox(window, values=(3,8,11,15,20), width=8)   # provided values
#spin1.grid(column=0, row=16)

# Adding progess bar
#bar = Progressbar(window, length=200, style='green.Horizontal.TProgressbar')
#bar['value'] = 70
#bar.grid(column=0, row=16)

# Adding Menu Bar
# adding menus
menu1 = Menu(window)
file_menu = Menu(menu1, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=file_save_as)
file_menu.add_command(label='Save As..', command=file_save_as)
file_menu.add_command(label='Close..')
file_menu.add_separator()
file_menu.add_command(label='Exit', command=master_kill)
menu1.add_cascade(label='File', menu=file_menu)
# edit menu
edit_menu = Menu(menu1, tearoff=0)
edit_menu.add_command(label='Notes', command=notepad)
edit_menu.add_command(label='Canvas', command=canvas_window)
menu1.add_cascade(label='Edit', menu=edit_menu)
# option menu
options_menu = Menu(menu1, tearoff=0)
options_menu.add_command(label='Connectivity Test', command=reachability)
options_menu.add_command(label='DNS Resolution', command=dns_resolution)
menu1.add_cascade(label='Options', menu=options_menu)
# Categories
menu1.add_command(label='Categories', command=categories)
# other menu labels
menu1.add_command(label='About', command=about_us)
window.config(menu=menu1)

# running the app
window.mainloop()