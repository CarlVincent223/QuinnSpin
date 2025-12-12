import requests
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile 
from tkinter import messagebox
import math
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from assist_class import processor_mthd
from popup_class import multi_popup_class

class obj_dsp_class:
    
    def __init__(self, g_var) -> None:
        self.g_var = g_var
        self.assist_con = processor_mthd(g_var)
        self.popup_con = multi_popup_class(self.g_var)
        hr = 1
        ind = 0
        self.opt_clock = []
        while hr <= 24:
            if hr == 12:
                add_str = "nn"
            elif hr > 23:
                add_str = "mn"
            elif hr < 12:
                add_str = "am"
            else:
                add_str = "pm"

            if hr>12:
                str = f"{hr-12}:00 {add_str}"
            else:
                str = f"{hr}:00 {add_str}"

            self.opt_clock.insert(ind, str)
            
            ind += 1
            hr += 1 

        self.temp_data = {}
        self.qr_img = {}

    def layout_manage_bookings(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Bookings", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Booking ID", "Client", "Contact", "Basket Count", "Status")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)
        
        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("2", width = math.ceil(content_w*.31), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("4", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("5", width = math.ceil(content_w*.15), anchor ='c')

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])
        bookings_table.heading("4", text = header_data[4])
        bookings_table.heading("5", text = header_data[5])

        bookings_table["displaycolumns"] = ("Booking ID", "Client", "Contact", "Basket Count", "Status")

        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table
    
    def layout_manage_services(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Services", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Category", "Title", "Description", "Pricing", "Quantity", "Unit")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.1), anchor ='w')
        bookings_table.column("2", width = math.ceil(content_w*.15), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.36), anchor ='w')
        bookings_table.column("4", width = math.ceil(content_w*.1), anchor ='c')
        bookings_table.column("5", width = math.ceil(content_w*.1), anchor ='c')
        bookings_table.column("6", width = math.ceil(content_w*.1), anchor ='c')

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])
        bookings_table.heading("4", text = header_data[4])
        bookings_table.heading("5", text = header_data[5])
        bookings_table.heading("6", text = header_data[6])

        bookings_table["displaycolumns"] = ("Category", "Title", "Description", "Pricing", "Quantity", "Unit")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table
    
    def layout_manage_addons(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Addons", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Title", "Description", "Pricing")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.33), anchor ='w')
        bookings_table.column("2", width = math.ceil(content_w*.33), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.25), anchor ='c')

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])

        bookings_table["displaycolumns"] = ("Title", "Description", "Pricing")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table
    
    def layout_manage_rewards(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Rewards", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Title", "Description", "Points Required", "Status")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.15), anchor ='w')
        bookings_table.column("2", width = math.ceil(content_w*.46), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("4", width = math.ceil(content_w*.15), anchor ='c')

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])
        bookings_table.heading("4", text = header_data[4])

        bookings_table["displaycolumns"] = ("Title", "Description", "Points Required", "Status")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table

    def layout_manage_billings(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Billing", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Booking ID", "Client", "Amount Due", "Amount Paid", "Mode", "Reference No.")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("2", width = math.ceil(content_w*.20), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("4", width = math.ceil(content_w*.15), anchor ='c')
        bookings_table.column("5", width = math.ceil(content_w*.11), anchor ='c')
        bookings_table.column("6", width = math.ceil(content_w*.15), anchor ='c')
        

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])
        bookings_table.heading("4", text = header_data[4])
        bookings_table.heading("5", text = header_data[5])
        bookings_table.heading("6", text = header_data[6])
        
        bookings_table["displaycolumns"] = ("Booking ID", "Client", "Amount Due", "Amount Paid", "Mode", "Reference No.")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table
    
    def make_table_scrollbar(self, holder, obj, row, col, padx, pady, pos, scroll_type, rowspan):
        if scroll_type == "vertical":
            table_scrlbar = ttk.Scrollbar(holder, orient=scroll_type, command=obj.yview)
            obj.configure(yscrollcommand = table_scrlbar.set)
        else:
            table_scrlbar = ttk.Scrollbar(holder, orient=scroll_type, command=obj.xview)
            obj.configure(xscrollcommand = table_scrlbar.set)

        table_scrlbar.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, rowspan=rowspan)
    
    def make_cbox(self, holder, x, y, w, val_list, font, state):
        cb_var = tk.StringVar()
        combo_box = ttk.Combobox(holder, textvariable=cb_var, state=state, values=val_list, font=font)
        combo_box.place(x=x, y=y, width=w)
        
        return combo_box
    
    def make_label(self, holder, x, y, w, text, font, bg, fg, anch):
        lbl = tk.Label(holder, text=text, bg=bg, fg=fg, font=font, anchor=anch)
        lbl.place(x=x, y=y, width=w)

        return lbl
    
    def make_input(self, holder, x, y, w, text, font, align):
        inp_var = tk.StringVar()
        inp = tk.Entry(holder, textvariable=inp_var, bd=1, relief="sunken", font=font, justify=align)
        inp.place(x=x, y=y, width=w)

        return inp
    
    def make_input_multi(self, holder, x, y, w, h, text, font):
        inp = ScrolledText(holder, height=h, width=w, font=font)
        inp.place(x=x, y=y, width=w, height=h)

        return inp
    
    def make_checkbox(self, holder, x, y, text, font, bg, fg, ind):
        self.temp_data[ind] = tk.IntVar()
        chkbox = tk.Checkbutton(holder, text=text, font=font, bg=bg, fg=fg, variable=self.temp_data[ind])
        chkbox.place(x=x, y=y)

        return chkbox
    
    def update_threads_data(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.g_var.headers)
            if response.status_code == 200:
                self.chatbox.delete('1.0', tk.END)
                data = response.json()  # Parse the JSON response
                self.assist_con.load_admin_messages(self.g_var.threads_msg_table, self.g_var.g_host+f"get_thread_messages_admin/{self.g_var.thread_id}")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    def reply_threads(self):
        msg = (self.chatbox.get("1.0", tk.END)).strip()
        data = {
            'tok':self.g_var.app_token, 
            'act':"Update",
            'data':{'thread_id':self.g_var.thread_id, "sender_id":"0", "message":msg, "sender_type":"admin"}
        }  
        
        if msg.strip() != "" and  self.g_var.thread_id != '':
            self.update_threads_data(self.g_var.g_host+"set_thread_reply_admin", data)
    
    def layout_manage_messages(self, holder, content_w, content_h, rowspan, colspan, g_var):
        
        assist_con = processor_mthd(g_var)

        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Messages", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        lay_bgc = g_var.default_sys_config['background']['bg']
        lay_fgc = g_var.default_sys_config['background']['fg']

        clients = tk.LabelFrame(holder, text='Client Threads (Double click to view)', bg=lay_bgc, fg="#181818", font=("Arial", 10, "bold"))
        clients.grid(row=1, column=0, padx=10, pady=10, sticky="news", columnspan=2, rowspan=2)
        
        header_data = ("ID", "Booking ID", "Client")
        clients_table = ttk.Treeview(clients, columns=header_data, show='headings', height=math.ceil((content_h*.85)/40), selectmode="browse")
        clients_table.grid(row=1, column=0, padx=(10, 0), pady=(5,15), sticky="news", columnspan=colspan, rowspan=2)
        clients_table.place(x=10, y=10)
        
        clients_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        clients_table.column("1", width = math.ceil(content_w*.15), anchor ='c')
        clients_table.column("2", width = math.ceil(content_w*.266), anchor ='w')

        clients_table.heading("0", text = header_data[0])
        clients_table.heading("1", text = header_data[1])
        clients_table.heading("2", text = header_data[2])
        clients_table["displaycolumns"] = ("Booking ID", "Client")

        vsb = ttk.Scrollbar(clients, orient="vertical", command=clients_table.yview)
        clients_table.configure(yscrollcommand=vsb.set)
        vsb.place(height=math.ceil(content_h*.69), x=math.ceil(content_w*.415), y=10)
        
        icon = self.create_button_icon(clients, "assets/images/delete_button.png", 115, 40)
        btn_delete = tk.Button(clients, bg=bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:assist_con.update_data(clients_table, "threads"))
        btn_delete.place(x=10, y=content_h*.73)

        g_var.threads_frame = tk.LabelFrame(holder, text='Thread Messages', bg=lay_bgc, fg="#181818", font=("Arial", 10, "bold"))
        g_var.threads_frame.grid(row=1, column=2, padx=(10,0), pady=10, sticky="news", columnspan=colspan, rowspan=2)

        threads_table = self.make_input_multi(g_var.threads_frame, 10, 10, math.ceil(content_w*.51), math.ceil(content_h*.69), "", ('Arial', 12))
        threads_table.config(state="disabled")
        #threads_table = ScrolledText(g_var.threads_frame, bg="#ffffff", height=32, width=86, font=("Arial", 10))
        #threads_table.grid(row=1, column=0, padx=(10, 0), pady=(5,15), sticky="news", columnspan=colspan, rowspan=2)
        self.chatbox = self.make_input_multi(g_var.threads_frame, 10, math.ceil(content_h*.69)+20, math.ceil(content_w*.40), math.ceil(content_h*.07), "", ('Arial', 12))
        icon = self.create_button_icon(clients, "assets/images/send_button.png", 115, 40)
        btn_send = tk.Button(g_var.threads_frame, bg=bgc, relief="flat", image=icon, anchor="center", text="Send", font=("Arial", 12), command=self.reply_threads)
        btn_send.place(x=math.ceil(content_w*.40)+20, y=math.ceil(content_h*.69)+25)

        # threads_table.config(state="normal")
        # chat_data = [
        #     {'sender':'client','msg':'Hello.'},
        #     {'sender':'client','msg':'Hello.'},
        #     {'sender':'client','msg':'Hello.'},
        #     {'sender':'admin','msg':'Hi!'},
        #     {'sender':'client','msg':'Hello.'},
        #     {'sender':'admin','msg':'Test message...'},
        # ]
        # threads_table.tag_config("client", foreground="black", font=("Arial", 12), justify="left")
        # threads_table.tag_config("admin", foreground="blue", font=("Arial", 12), justify="right")
        # threads_table.tag_config("r_indent", rmargin=100, lmargin1=5)
        # threads_table.tag_config("l_indent", rmargin=5, lmargin1=100)
        # i=0
        # chat_msg = ""
        # line_space = ""
        # start = "1.0"
        # for item in chat_data:
        #     if i > 0:
        #         line_space = "\n\n"
        #         start = end #str(float(threads_table.index('end'))+1.0)

        #     chat_msg = f"{line_space}[ {item['sender']} ]\n{item['msg']}"
        #     if item['sender'] == "client":
        #         threads_table.insert(tk.END, chat_msg, "r_indent")
        #     else:
        #         threads_table.insert(tk.END, chat_msg, "l_indent")

        #     end = threads_table.index('end')
        #     threads_table.tag_add(item['sender'], start, f"{int(float(end)-1.0)}.end")

        #     i+=1

        # threads_table.see(tk.END)
        # threads_table.config(state="disabled")

        # header_data = ("Message", "Timestamp", "Sender")
        # threads_table = ttk.Treeview(g_var.threads_frame, columns=header_data, show='headings', height=math.ceil((content_h*.85)/40), selectmode="browse")
        # threads_table.grid(row=1, column=0, padx=(10, 0), pady=(5,15), sticky="news", columnspan=colspan, rowspan=2)
        # threads_table.place(x=10, y=10)

        # threads_table.column("0", width = math.ceil(content_w*.26), anchor ='w')
        # threads_table.column("1", width = math.ceil(content_w*.15), anchor ='c')
        # threads_table.column("2", width = math.ceil(content_w*.1), anchor ='c')

        # threads_table.heading("0", text = header_data[0])
        # threads_table.heading("1", text = header_data[1])
        # threads_table.heading("2", text = header_data[2])
        # #g_var.message_table = threads_table

        # icon = self.create_button_icon(clients, "assets/images/delete_button.png", 115, 40)
        # btn_delete = tk.Button(g_var.threads_frame, bg=bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:assist_con.update_data(threads_table, "thread_msg"))
        # btn_delete.place(x=10, y=content_h*.73)

        return (clients_table,threads_table)
    
    def layout_manage_customers(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Customers", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Name", "Address", "Points", "Status")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.28), anchor ='w')
        bookings_table.column("2", width = math.ceil(content_w*.38), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.10), anchor ='c')
        bookings_table.column("4", width = math.ceil(content_w*.15), anchor ='c')

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])
        bookings_table.heading("4", text = header_data[4])

        bookings_table["displaycolumns"] = ("Name", "Address", "Points", "Status")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table
    
    def layout_manage_reports(self, holder, content_w, content_h, rowspan, colspan, g_var, filter):
        
        assist_con = processor_mthd(g_var)

        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Reports", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="nw", columnspan=colspan, rowspan=rowspan)

        lay_bgc = g_var.default_sys_config['background']['bg']
        lay_fgc = g_var.default_sys_config['background']['fg']

        self.g_var.g_chart_holder = tk.LabelFrame(holder, text='Chart', bg=lay_bgc, fg="#181818", font=("Arial", 10, "bold"))
        self.g_var.g_chart_holder.grid(row=1, column=0, padx=10, pady=10, sticky="news", columnspan=5, rowspan=2)

        assist_con.chart_generator(self.g_var.g_chart_holder, self.g_var.g_cbox['months'], self.g_var.g_cbox['weeks'], self.g_var.g_cbox['year'], filter)

    def create_button_icon(self, holder, qr_src, w, h):
        original_image = Image.open(qr_src)
        resized_image = original_image.resize((w, h))
        photo_image = ImageTk.PhotoImage(resized_image)
        
        img_ref = tk.Label(holder, image=photo_image)
        img_ref.image = photo_image 

        return photo_image
    
    def upload_qr(self, file_name, my_shop, w, h, root):
        file_path = askopenfile(mode='r', filetypes=[('Image Files', '*.jpeg *.png *.jpg')])
        if file_path is not None:
            res = f"assets/images/{file_name}.png"
            shutil.copyfile(file_path.name, res)
            self.qr_img[file_name].config(image=self.create_button_icon(my_shop, f"assets/images/{file_name}.png", w, h))
            root.update()

    def set_list_box(self, data):
        self.listbox.tag_configure("oddrow", background=self.g_var.tbl_style['row_odd'])
        self.listbox.tag_configure("evenrow", background=self.g_var.tbl_style['row_even'])
        i=1
        for item in data:
            tmp_ind = item['sched_date'].split('-')
            self.g_var.day_off_list.insert(i, {'month':int(tmp_ind[0]), 'day':int(tmp_ind[1]), 'desc':item['description']})
            
            #self.listbox.insert(tk.END, f"{self.g_var.months[int(tmp_ind[0])-1]} {int(tmp_ind[1])}")
            
            if i % 2 == 0:
                tags_indc = "oddrow"
            else:
                tags_indc = "evenrow"
            self.listbox.insert('', 'end', text="", values=(i, f"{self.g_var.months[int(tmp_ind[0])-1]} {int(tmp_ind[1])}",), tags=(tags_indc,))
            i+=1

    def update_day_off_data(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.g_var.headers)
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                if data != "invalid":
                    self.g_var.day_off_list.clear()
                    self.listbox.delete(*self.listbox.get_children())
                    self.set_list_box(data)
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def modify_shop_day_off(self, act):
        if self.g_var.popup_on == False:
            if act == "add":
                    self.g_var.popup_on = True
                    self.popup_con.mod_shop_day_off('', self.listbox)
            else:
                values = self.listbox.item(self.listbox.focus())
                
                if values['values'] != "":
                    ind = values['values'][0]-1
                    tmp_mm = self.assist_con.format_std_code("", str(self.g_var.day_off_list[ind]['month']), 2)
                    tmp_dd = self.assist_con.format_std_code("", str(self.g_var.day_off_list[ind]['day']), 2)

                    data = {
                        'tok': self.g_var.app_token,
                        'act': act,
                        'data': {'sched_date':f"{tmp_mm}-{tmp_dd}"}
                    }
                    #print(data)
                    if messagebox.askyesno(message="Are you sure you want to remove this day off?", icon='question', title="Remove Entry"):
                        self.update_day_off_data(self.g_var.g_host+"mod_tbl_day_off", data)
        else:
            self.g_var.push_popup_front()
    
    def handle_item_select(self, event):
        if self.g_var.popup_on == False:
            values = self.listbox.item(self.listbox.focus())
            
            if values != "":
                self.g_var.popup_on = True
                self.popup_con.mod_shop_day_off(values['values'][0], self.listbox)

        else:
            self.g_var.push_popup_front()

    def layout_manage_logistics(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Riders Assignment", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Booking ID", "Client", "Address", "Task", "Rider", "Status")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.10), anchor ='c')
        bookings_table.column("2", width = math.ceil(content_w*.15), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.20), anchor ='w')
        bookings_table.column("4", width = math.ceil(content_w*.10), anchor ='c')
        bookings_table.column("5", width = math.ceil(content_w*.15), anchor ='w')
        bookings_table.column("6", width = math.ceil(content_w*.10), anchor ='c')
        

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])
        bookings_table.heading("4", text = header_data[4])
        bookings_table.heading("5", text = header_data[5])
        bookings_table.heading("6", text = header_data[6])
        
        bookings_table["displaycolumns"] = ("Booking ID", "Client", "Address", "Task", "Rider", "Status")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table
    
    def layout_manage_riders(self, holder, content_w, content_h, rowspan, colspan, g_var):
        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Riders", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        temp_h = math.ceil(content_h*.47/22)
        header_data = ("ID", "Name", "Address", "Status")
        bookings_table = ttk.Treeview(holder, columns=header_data, show='headings', height=temp_h, selectmode="browse")
        bookings_table.grid(row=1, column=0, padx=(10, 15), pady=5, sticky="news", columnspan=colspan, rowspan=2)

        bookings_table.column("0", width = math.ceil(content_w*.05), anchor ='c')
        bookings_table.column("1", width = math.ceil(content_w*.31), anchor ='w')
        bookings_table.column("2", width = math.ceil(content_w*.40), anchor ='w')
        bookings_table.column("3", width = math.ceil(content_w*.20), anchor ='c')

        bookings_table.heading("0", text = header_data[0])
        bookings_table.heading("1", text = header_data[1])
        bookings_table.heading("2", text = header_data[2])
        bookings_table.heading("3", text = header_data[3])

        bookings_table["displaycolumns"] = ("Name", "Address", "Status")
        self.make_table_scrollbar(holder, bookings_table, 1, 4, 0, 5, (tk.NS, tk.E), "vertical", 2)
        #self.make_table_scrollbar(holder, bookings_table, 0, 0, (4, 20), 0, (tk.EW, tk.S), "horizontal", 2)

        return bookings_table

    def layout_manage_shop(self, holder, content_w, content_h, rowspan, colspan, g_var, sched_dates, shop_details, shop_day_off, root):
        tmp = list(sched_dates.keys())
        hl_day = tmp[0]
        temp_lbl = {}

        assist_con = processor_mthd(g_var)

        bgc = g_var.default_sys_config['background']['bg']
        lbl_user = tk.Label(holder, text="Manage Shop", bg=bgc, fg="#333333", font=("Arial", 15, "bold"), anchor="w")
        lbl_user.grid(row=0, column=0, padx=10, pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        lay_bgc = g_var.default_sys_config['background']['bg']
        lay_fgc = g_var.default_sys_config['background']['fg']

        grid_y = (10, 60, 110, 160, 260, 310, 370, 560)
        grid_x = (30, 130, content_w*.12)
        my_shop = tk.LabelFrame(holder, text='My Shop', bg=lay_bgc, fg="#181818", font=("Arial", 10, "bold"))
        my_shop.grid(row=1, column=0, padx=10, pady=10, sticky="news", columnspan=2, rowspan=2)

        lbl = self.make_label(my_shop, grid_x[0], grid_y[0], 100, "Name", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        self.temp_data['shop_name'] = self.make_input(my_shop, grid_x[1], grid_y[0], content_w*.3, "", ('Arial', 12), "left")
        self.temp_data['shop_name'].insert(0, shop_details['shop_name'])

        lbl = self.make_label(my_shop, grid_x[0], grid_y[1], 100, "Owner", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        self.temp_data['owner'] = self.make_input(my_shop, grid_x[1], grid_y[1], content_w*.3, "", ('Arial', 12), "left")
        self.temp_data['owner'].insert(0, str(shop_details['owner']))

        lbl = self.make_label(my_shop, grid_x[0], grid_y[2], 100, "TIN", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        self.temp_data['tin'] = self.make_input(my_shop, grid_x[1], grid_y[2], content_w*.3, "", ('Arial', 12), "left")
        self.temp_data['tin'].insert(0, str(shop_details['tin']))

        lbl = self.make_label(my_shop, grid_x[0], grid_y[3], 100, "Address", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        self.temp_data['address'] = self.make_input_multi(my_shop, grid_x[1], grid_y[3], math.ceil(content_w*.3), 70, "", ('Arial', 12))
        self.temp_data['address'].insert(tk.END, shop_details['address'])

        lbl = self.make_label(my_shop, grid_x[0], grid_y[4], 100, "Contact #", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        self.temp_data['contact'] = self.make_input(my_shop, grid_x[1], grid_y[4], content_w*.3, "", ('Arial', 12), "left")
        self.temp_data['contact'].insert(0, shop_details['contact'])

        lbl = self.make_label(my_shop, grid_x[0], grid_y[5], 100, "FB Page", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        self.temp_data['fb_page'] = self.make_input(my_shop, grid_x[1], grid_y[5], content_w*.3, "", ('Arial', 12), "left")
        self.temp_data['fb_page'].insert(0, shop_details['fb_page'])
        
        w = math.ceil(content_w*.15)
        h = math.ceil(content_w*.15)
        self.qr_img['gcash_qr'] = tk.Button(my_shop, image=self.create_button_icon(my_shop, "assets/images/gcash_qr.png", w, h), anchor="center", text="View GCash QR", font=("Arial", 12), command=lambda:self.upload_qr("gcash_qr", my_shop, w, h, root))
        self.qr_img['gcash_qr'].place(x=grid_x[0], y=grid_y[6])
        lbl = self.make_label(my_shop, grid_x[0], grid_y[7], w, "GCash", ('Arial', 12), lay_bgc, lay_fgc, 'c')

        self.qr_img['maya_qr'] = tk.Button(my_shop, image=self.create_button_icon(my_shop, "assets/images/maya_qr.png", w, h), anchor="center", text="View Maya QR", font=("Arial", 12), command=lambda:self.upload_qr("maya_qr", my_shop, w, h, root))
        self.qr_img['maya_qr'].place(x=(w*.7)+w, y=grid_y[6])
        lbl = self.make_label(my_shop, (w*.7)+w, grid_y[7], w, "Maya", ('Arial', 12), lay_bgc, lay_fgc, 'c')

        schedules_opt = tk.LabelFrame(holder, text='Operating Hours', bg=lay_bgc, fg="#181818", font=("Arial", 10, "bold"))
        schedules_opt.grid(row=1, column=2, padx=(10,0), pady=10, sticky="news", columnspan=colspan, rowspan=rowspan)

        _font = ('Arial',math.ceil(content_w*.01))
        grid_y = (10, 50, 90, 130, 170, 210, 250, 320, 360, 380)
        grid_x = (10, (content_w*.14), (content_w*.25), (content_w*.35), (content_w*.5))

        temp_lbl['Sunday'] = self.make_label(schedules_opt, grid_x[0], grid_y[0], 95, "Sunday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[0], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[0], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['sun_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[0], 100, self.opt_clock, _font, "readonly")
        self.temp_data['sun_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[0], 100, self.opt_clock, _font, "readonly")
        time_arr = assist_con.format_cbox_time_value(shop_details['sunday'])
        self.temp_data['sun_beg'].set(time_arr[0])
        self.temp_data['sun_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[0], 150, sched_dates['Sunday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[0], "", ('Arial', 14), lay_bgc, lay_fgc, "sun_chk")
        # if shop_details['sun_stat'] == "open":
        #     cbox.invoke()
            
        temp_lbl['Monday'] = self.make_label(schedules_opt, grid_x[0], grid_y[1], 95, "Monday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[1], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[1], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['mon_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[1], 100, self.opt_clock, _font, "readonly")
        self.temp_data['mon_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[1], 100, self.opt_clock, _font, "readonly")    
        time_arr = assist_con.format_cbox_time_value(shop_details['monday'])
        self.temp_data['mon_beg'].set(time_arr[0])
        self.temp_data['mon_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[1], 150, sched_dates['Monday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[1], "", _font, lay_bgc, lay_fgc, "mon_chk")
        # if shop_details['mon_stat'] == "open":
        #    cbox.invoke()
            
        temp_lbl['Tuesday'] = self.make_label(schedules_opt, grid_x[0], grid_y[2], 95, "Tuesday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[2], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[2], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['tue_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[2], 100, self.opt_clock, _font, "readonly")
        self.temp_data['tue_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[2], 100, self.opt_clock, _font, "readonly") 
        time_arr = assist_con.format_cbox_time_value(shop_details['tuesday'])
        self.temp_data['tue_beg'].set(time_arr[0])
        self.temp_data['tue_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[2], 150, sched_dates['Tuesday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[2], "", _font, lay_bgc, lay_fgc, "tue_chk")
        # if shop_details['tue_stat'] == "open":
        #     cbox.invoke()

        temp_lbl['Wednesday'] = self.make_label(schedules_opt, grid_x[0], grid_y[3], 95, "Wednesday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[3], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[3], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['wed_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[3], 100, self.opt_clock, _font, "readonly")
        self.temp_data['wed_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[3], 100, self.opt_clock, _font, "readonly")
        time_arr = assist_con.format_cbox_time_value(shop_details['wednesday'])
        self.temp_data['wed_beg'].set(time_arr[0])
        self.temp_data['wed_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[3], 150, sched_dates['Wednesday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[3], "", _font, lay_bgc, lay_fgc, "wed_chk")
        # if shop_details['wed_stat'] == "open":
        #     cbox.invoke()
            
        temp_lbl['Thursday'] = self.make_label(schedules_opt, grid_x[0], grid_y[4], 95, "Thursday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[4], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[4], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['thu_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[4], 100, self.opt_clock, _font, "readonly")
        self.temp_data['thu_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[4], 100, self.opt_clock, _font, "readonly")
        time_arr = assist_con.format_cbox_time_value(shop_details['thursday'])
        self.temp_data['thu_beg'].set(time_arr[0])
        self.temp_data['thu_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[4], 150, sched_dates['Thursday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[4], "", _font, lay_bgc, lay_fgc, "thu_chk")
        # if shop_details['thu_stat'] == "open":
        #     cbox.invoke()
            
        temp_lbl['Friday'] = self.make_label(schedules_opt, grid_x[0], grid_y[5], 95, "Friday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[5], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[5], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['fri_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[5], 100, self.opt_clock, _font, "readonly")
        self.temp_data['fri_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[5], 100, self.opt_clock, _font, "readonly")
        time_arr = assist_con.format_cbox_time_value(shop_details['friday'])
        self.temp_data['fri_beg'].set(time_arr[0])
        self.temp_data['fri_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[5], 150, sched_dates['Friday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[5], "", _font, lay_bgc, lay_fgc, "fri_chk")
        # if shop_details['fri_stat'] == "open":
        #     cbox.invoke()

        temp_lbl['Saturday'] = self.make_label(schedules_opt, grid_x[0], grid_y[6], 95, "Saturday", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1]-50, grid_y[6], 50, "From", _font, lay_bgc, lay_fgc, 'w')
        self.make_label(schedules_opt, grid_x[1], grid_y[6], (grid_x[2]-grid_x[1])+100, "To", _font, lay_bgc, lay_fgc, 'c')
        self.temp_data['sat_beg'] = self.make_cbox(schedules_opt, grid_x[1], grid_y[6], 100, self.opt_clock, _font, "readonly")
        self.temp_data['sat_end'] = self.make_cbox(schedules_opt, grid_x[2], grid_y[6], 100, self.opt_clock, _font, "readonly")
        time_arr = assist_con.format_cbox_time_value(shop_details['saturday'])
        self.temp_data['sat_beg'].set(time_arr[0])
        self.temp_data['sat_end'].set(time_arr[1])
        # lbl = self.make_label(schedules_opt, grid_x[3], grid_y[6], 150, sched_dates['Saturday'], _font, lay_bgc, lay_fgc, 'w')
        # cbox = self.make_checkbox(schedules_opt, grid_x[4], grid_y[6], "", _font, lay_bgc, lay_fgc, "sat_chk")
        # if shop_details['sat_stat'] == "open":
        #     cbox.invoke()

        lbl = self.make_label(schedules_opt, grid_x[0], grid_y[7], 150, "Logistics Fee", _font, lay_bgc, lay_fgc, 'w')
        self.temp_data['logistics'] = self.make_input(schedules_opt, grid_x[2], grid_y[7], 100, "", _font, "right")
        self.temp_data['logistics'].insert(0, "{:.2f}".format(float(shop_details['logistics'])))

        lbl = self.make_label(schedules_opt, grid_x[0], grid_y[8], 220, "Free Logistics Service", _font, lay_bgc, lay_fgc, 'w')
        self.temp_data['free_threshold'] = self.make_input(schedules_opt, grid_x[2], grid_y[8], 100, "", _font, "center")
        self.temp_data['free_threshold'].insert(0, shop_details['free_threshold'])

        lbl = self.make_label(schedules_opt, grid_x[0], grid_y[9], 200, "Threshold in kilometer (km)", ('Arial', 11, 'italic'), lay_bgc, 'green', 'w')

        lbl = self.make_label(schedules_opt, grid_x[3], grid_y[0], 150, "Day Off's", _font, lay_bgc, lay_fgc, 'w')
        btn_delete = tk.Button(schedules_opt, width=2, bg=lay_bgc, relief="raised", anchor="center", text="-", font=("Arial", 12), command=lambda:self.modify_shop_day_off('delete'))
        btn_delete.place(x=grid_x[4]-50, y=grid_y[0])
        btn_add = tk.Button(schedules_opt, width=2, bg=lay_bgc, relief="raised", anchor="center", text="+", font=("Arial", 12), command=lambda:self.modify_shop_day_off('add'))
        btn_add.place(x=grid_x[4], y=grid_y[0])
        # self.listbox = tk.Listbox(schedules_opt, width=24, height=12, font=('Arial', 11))
        # self.listbox.place(x=grid_x[3], y=grid_y[1])

        # self.listbox.bind('<Double-1>', self.handle_item_select)
        # self.set_list_box(shop_day_off)
        # vsb = tk.Scrollbar(schedules_opt, orient="vertical", command=self.listbox.yview)
        # self.listbox.configure(yscrollcommand=vsb.set)
        # vsb.place(height=220, x=grid_x[4]+10, y=grid_y[1])

        header_data = ("ID", "Day Off List",)
        self.listbox = ttk.Treeview(schedules_opt, columns=header_data, show="", height=13, selectmode="browse")
        self.listbox.place(x=grid_x[3], y=grid_y[1], width=210)
        self.listbox.column("0", width=0, anchor ='c')
        self.listbox.column("1", width=100, anchor ='w')
        self.listbox.heading("0", text=header_data[0])
        self.listbox.heading("1", text=header_data[1])
        self.listbox.bind('<Double-1>', self.handle_item_select)
        self.listbox["displaycolumns"] = ("Day Off List",)

        self.set_list_box(shop_day_off)
        vsb = ttk.Scrollbar(schedules_opt, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=vsb.set)
        vsb.place(height=math.ceil(content_h*.505), x=grid_x[4]+10, y=grid_y[1])

        # i=0
        # for item in shop_day_off:
        #     tmp_ind = item['sched_date'].split('-')
        #     self.g_var.day_off_list.insert(i, {'month':int(tmp_ind[0]), 'day':int(tmp_ind[1]), 'desc':item['description']})
        #     i+=1
        #     self.listbox.insert(tk.END, f"{self.g_var.months[int(tmp_ind[0])-1]} {int(tmp_ind[1])}")

        grid_y = (0, 60)
        grid_x = (30, 130)
        label_frame2 = tk.LabelFrame(holder, text='Admin Credentials', bg=lay_bgc, fg="#181818", font=("Arial", 10, "bold"))
        label_frame2.grid(row=2, column=2, padx=(10,0), pady=0, sticky="news", columnspan=colspan, rowspan=rowspan)

        system_secure = tk.Frame(label_frame2, bg=lay_bgc, relief=tk.FLAT, bd=2)
        system_secure.columnconfigure(0, minsize=math.ceil(content_w*.085), weight=1)
        system_secure.columnconfigure(1, minsize=math.ceil(content_w*.1), weight=1)
        system_secure.columnconfigure(2, minsize=math.ceil(content_w*.085), weight=1)
        system_secure.columnconfigure(3, minsize=math.ceil(content_w*.1), weight=1)
        system_secure.rowconfigure(0, minsize=math.ceil(content_h*.07), weight=1)
        system_secure.rowconfigure(1, minsize=math.ceil(content_h*.07), weight=1)
        system_secure.place(x=grid_x[0], y=grid_y[0])
        
        #lbl = self.make_label(label_frame2, grid_x[0], grid_y[0], 220, "User Name", _font, lay_bgc, lay_fgc, 'w')
        #self.temp_data['user_name'] = self.make_input(label_frame2, grid_x[1], grid_y[0], 200, "", _font, "center")

        credentials = self.g_var.db_con.get_current_user()
        
        uname_var = tk.StringVar()
        self.make_label_grid(system_secure, 0, 0, 0, 0, "ew", "User Name", _font, "w", lay_bgc, lay_fgc, 1, 1)
        self.temp_data['uname'] = self.make_input_grid(system_secure, uname_var, 0, 1, 0, 0, "ew", _font, lay_fgc, 1, 1, 'center')
        self.temp_data['uname'].insert(0, credentials[0])

        upass_var = tk.StringVar()
        self.make_label_grid(system_secure, 0, 2, 0, 0, "ew", "Password", _font, "w", lay_bgc, lay_fgc, 1, 1)
        self.temp_data['upass'] = self.make_input_grid(system_secure, upass_var, 0, 3, 0, 0, "ew", _font, lay_fgc, 1, 1, 'center')
        self.temp_data['upass'].config(show="*", bg="#fcf38e")

        self.make_label_grid(system_secure, 1, 0, 0, 0, "ew", "Server URL", _font, "w", lay_bgc, lay_fgc, 1, 1)
        lbl = self.make_label_grid(system_secure, 1, 1, 0, 0, "ew", f"{g_var.g_host}", _font, "w", lay_bgc, lay_fgc, 3, 1)
        lbl.config(relief="sunken")

        #lbl = self.make_label(label_frame2, grid_x[0], grid_y[1], content_w*.48, f"{g_var.g_host}", ('Arial', 12), lay_bgc, lay_fgc, 'w')
        #lbl.config(relief="sunken")

        # self.temp_data['host'] = self.make_input(label_frame2, grid_x[1], grid_y[0], content_w*.4, g_var.g_host, ('Arial', 12), "left")
        # self.temp_data['host'].insert(0, g_var.g_host)
        # self.temp_data['host'].config(state="readonly")

        temp_lbl[tmp[0]].config(bg="#6699ff")

        return self.temp_data
    
    def make_label_grid(self, holder, row, col, padx, pady, pos, text, font, anch, bgc, fgc, colspan, rowspan):
        lbl = tk.Label(holder, text=text, bg=bgc, fg=fgc, font=font, anchor=anch)
        lbl.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        return lbl
    
    def make_input_grid(self, holder, inp_var, row, col, padx, pady, pos, font, fgc, colspan, rowspan, align):
        inp = tk.Entry(holder, textvariable=inp_var, bg="#ffffff", fg=fgc, bd=1, relief="sunken", font=font, insertbackground=fgc, justify=align)
        inp.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        return inp