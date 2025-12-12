import requests
import tkinter as tk
from tkinter import ttk
import math
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

from assist_class import processor_mthd

class multi_popup_class:

    def __init__(self, g_var) -> None:
        self.g_var = g_var
        self.assist_con = processor_mthd(g_var)
        self.popup_bgc = g_var.default_sys_config['background']['bg']# "#c0c0c0"
        self.popup_fgc = g_var.default_sys_config['background']['fg']# "#000000"
        self.app_w = 0
        self.app_h = 0
        self.popup_data = {}
        self.cur_id = ''
        self.cur_uid = ''
        self.prod_type_arr = {'full_service':0,'comforter':1,'self_service':2}
        self.prod_type_ind = {'Full Service':'full_service','Comforter':'comforter','Self Service':'self_service'}
        self.prod_type_list = ('Full Service','Comforter','Self Service')
        self.units_arr = {'kg':0,'pc':1}
        self.units_list = ('kg','pc')
        self.p_mode_arr = {'GCash':0,'Maya':1,'Cash':2,'Points':3}
        self.p_mode_list = ('GCash','Maya','Cash','Points')
        self.b_status_arr = {}
        self.b_status_list = ()
        self.b_logistics_fee = ("{:.2f}".format(35),"{:.2f}".format(0))
        self.r_status_arr = {'Active':0,'Inactive':1}
        self.r_status_list = ('Active','Inactive')
        self.p_status_arr = {'Unpaid':0,'Paid':1}
        self.p_status_list = ('Unpaid','Paid')

        self.prod_arr = {}
        self.prod_tbl = ""

        self.temp_data = {}

        self.prod_items = {}

    def make_table_scrollbar(self, holder, obj, row, col, padx, pady, pos, scroll_type, rowspan):
        if scroll_type == "vertical":
            table_scrlbar = ttk.Scrollbar(holder, orient=scroll_type, command=obj.yview)
            obj.configure(yscrollcommand = table_scrlbar.set)
        else:
            table_scrlbar = ttk.Scrollbar(holder, orient=scroll_type, command=obj.xview)
            obj.configure(xscrollcommand = table_scrlbar.set)

        table_scrlbar.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, rowspan=rowspan)

    def load_request_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.prod_items = response.json()  # Parse the JSON response
                
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def update_threads_data(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.g_var.headers)
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                self.close_global_popup()
                self.assist_con.load_admin_messages(self.g_var.threads_msg_table, self.g_var.g_host+f"get_thread_messages_admin/{self.g_var.thread_id}")
                #self.assist_con.reload_table_content()
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def update_request_data(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.g_var.headers)
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                if data == "taken":
                    messagebox.showinfo("Notice", "The item wont be deleted permanently, already have linkage that may affect your records.")
                elif data == "exist":
                    messagebox.showinfo("Notice", "Account already registered.")
                    self.g_var.push_popup_front()
                elif data == "invalid":
                    messagebox.showinfo("Notice", "Unable to modify the item.")
                else:
                    self.close_global_popup()
                    self.assist_con.reload_table_content()
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def close_global_popup(self):
        try:
            self.popup_global_win.destroy()
            self.g_var.popup_on = False
        except:
            pass

    def update_data(self, target):
        if target == "bookings":
            #if self.temp_data['quantity'].get() != "":
            tmp_prod_items = []
            for item in self.prod_arr:
                if self.prod_arr[item]['act'] != '':
                    tmp_prod_items.insert(0, {'service_id':item, 'qty':self.prod_arr[item]['val']})

            data = {
                'tok':self.g_var.app_token,
                'act':"Update",
                'data':{'booking_id':self.cur_id, 'uid':self.cur_uid, 'status':self.temp_data['cb_stat_inp'].get(), 'logistics_fee':self.temp_data['cb_fee_inp'].get(), 'cancel_reason':self.temp_data['cancel'].get(), 'cancelled_by':'admin'},
                'items':tmp_prod_items
            }
            
            if self.temp_data['cb_stat'].get() != "Pending":
                self.update_request_data(self.g_var.g_host+"mod_tbl_bookings", data)
            else:
                self.g_var.warn_popup("Warning", "Quantity is required!")
                
        elif target == "services":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'prod_type':target, 'id':self.cur_id, "title":self.temp_data['title'].get(), "description":self.temp_data['description'].get(), "price":self.temp_data['price'].get(), "quantity":self.temp_data['quantity'].get(), 'unit':self.temp_data['cb_unit_inp'].get(), 'status':self.temp_data['cb_stat_inp'].get()}
            }
            self.update_request_data(self.g_var.g_host+"mod_tbl_products", data)

        elif target == "addons":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'prod_type':target, 'id':self.cur_id, "title":self.temp_data['title'].get(), "description":self.temp_data['description'].get(), "price":self.temp_data['price'].get(), 'status':self.temp_data['cb_stat_inp'].get()}
            }
            self.update_request_data(self.g_var.g_host+"mod_tbl_products", data)

        elif target == "billings":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'id':self.cur_id, 'uid':self.cur_uid, "mode":self.temp_data['cb_mode_inp'].get(), "ref_num":self.temp_data['ref_num'].get(), "amount":self.temp_data['amount'].get(), 'status':'Paid', 'points':self.temp_data['points'].get(), "description":self.temp_data['description'].get(), 'payment_status':self.popup_data['status'], 'booking_id':self.popup_data['booking_id']}
            }
            
            if self.temp_data['amount'].get() != "":
                if self.temp_data['cb_mode_inp'].get() == "Points":
                    if float(self.temp_data['amount'].get()) != 0:
                        #print(data)
                        self.update_request_data(self.g_var.g_host+"mod_tbl_billings", data)
                else:
                    if "{:.2f}".format(float(self.temp_data['amount'].get())) == self.temp_data['amount_due'].get():
                        #print(data)
                        self.update_request_data(self.g_var.g_host+"mod_tbl_billings", data)

        elif target == "rewards":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'id':self.cur_id, "title":self.temp_data['title'].get(), "description":self.temp_data['description'].get(), "pts_req":self.temp_data['pts_req'].get(), 'status':self.temp_data['cb_stat_inp'].get()}
            }
            self.update_request_data(self.g_var.g_host+"mod_tbl_rewards", data)
        
        elif target == "customers":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'id':self.cur_id, 'status':self.temp_data['cb_stat_inp'].get()}
            }
            self.update_request_data(self.g_var.g_host+"mod_tbl_users", data)
        elif target == "riders":
            if self.temp_data['password'].get() == "********" or self.temp_data['password'].get() == "":
                tmp_password = ""
            else:
                tmp_password = self.assist_con.get_hash_value(self.temp_data['password'].get())
                
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'id':self.cur_id, "user_name":self.temp_data['user_name'].get(), "password":tmp_password, "first_name":self.temp_data['first_name'].get(), "last_name":self.temp_data['last_name'].get(), "address":self.temp_data['address'].get(), "mobile_no":self.temp_data['mobile_no'].get(), 'status':self.temp_data['cb_stat_inp'].get()}
            }
            #print(data)
            self.update_request_data(self.g_var.g_host+"mod_tbl_riders", data)
        elif target == "logistics":
            tmp_ind = self.temp_data['rider_assigned'].current()
            data = {
                'tok':self.g_var.app_token, 
                'act':"Update",
                'data':{'id':self.cur_id, "rider_id":self.g_var.riders_arr[tmp_ind]['id'], 'task':self.popup_data['task_type'], 'status':"Assigned"}
            }
            #print(data)
            self.update_request_data(self.g_var.g_host+"mod_tbl_rider_assigned", data)

    def add_data(self, target):
        if target == "rewards":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Add",
                'data':{'id':self.cur_id, "title":self.temp_data['title'].get(), "description":self.temp_data['description'].get(), "pts_req":self.temp_data['pts_req'].get(), 'status':self.temp_data['cb_stat_inp'].get()}
            }
            self.update_request_data(self.g_var.g_host+"mod_tbl_rewards", data)
        elif target == "services":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Add",
                'data':{'id':self.cur_id, "title":self.temp_data['title'].get(), "description":self.temp_data['description'].get(), "price":self.temp_data['price'].get(),  "quantity":self.temp_data['quantity'].get(), "unit":self.temp_data['cb_unit_inp'].get(), "prod_type":self.prod_type_ind[self.temp_data['cb_type_inp'].get()], "status":self.temp_data['cb_stat_inp'].get()}
            }
            #print(data)
            self.update_request_data(self.g_var.g_host+"mod_tbl_products", data)
        elif target == "addons":
            data = {
                'tok':self.g_var.app_token, 
                'act':"Add",
                'data':{'id':self.cur_id, "title":self.temp_data['title'].get(), "description":(self.temp_data['description'].get("1.0", tk.END)).strip(), "price":self.temp_data['price'].get(),  "quantity":"1", "unit":"none", "prod_type":"addons",'status':self.temp_data['cb_stat_inp'].get()}
            }
            #print(data)
            self.update_request_data(self.g_var.g_host+"mod_tbl_products", data)
        elif target == "riders":
            tmp_password = self.assist_con.get_hash_value(self.temp_data['password'].get())
            data = {
                'tok':self.g_var.app_token, 
                'act':"Add",
                'data':{'id':self.cur_id, "user_name":self.temp_data['user_name'].get(), "password":tmp_password, "first_name":self.temp_data['first_name'].get(), "last_name":self.temp_data['last_name'].get(), "address":self.temp_data['address'].get(), "mobile_no":self.temp_data['mobile_no'].get(), 'status':self.temp_data['cb_stat_inp'].get()}
            }
            #print(data)
            self.update_request_data(self.g_var.g_host+"mod_tbl_riders", data)

    def make_label(self, holder, row, col, padx, pady, pos, text, font, anch, colspan, rowspan):
        lbl = tk.Label(holder, text=text, bg=self.popup_bgc, fg=self.popup_fgc, font=font, anchor=anch)
        lbl.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        return lbl
    
    def make_label2(self, holder, x, y, w, text, font, bg, fg, anch):
        lbl = tk.Label(holder, text=text, bg=bg, fg=fg, font=font, anchor=anch)
        lbl.place(x=x, y=y, width=w)

        return lbl
    
    def make_input2(self, holder, x, y, w, text, font, align, state):
        inp = tk.Entry(holder, bg="#FFFFFF", fg=self.popup_fgc, bd=1, relief="sunken", font=font, insertbackground=self.popup_fgc, justify=align)
        inp.place(x=x, y=y, width=w)
        inp.insert(0,text)
        inp.config(state=state)
        return inp
    
    def make_cbox2(self, holder, x, y, w, data, cb_var, font, s_ind):
        combo_box = ttk.Combobox(holder, textvariable=cb_var, state="readonly", values=data, font=font)
        combo_box.place(x=x, y=y, width=w)
        combo_box.current(s_ind)

        return combo_box
    
    def make_input_dummy(self, holder, row, col, padx, pady, pos, text, font, anch, colspan, rowspan):
        lbl = tk.Label(holder, text=text, bg=self.popup_bgc, fg=self.popup_fgc, font=font, anchor=anch, relief="sunken")
        lbl.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        return lbl
    
    def make_input(self, holder, inp_var, row, col, padx, pady, pos, font, colspan, rowspan, align):
        inp = tk.Entry(holder, textvariable=inp_var, bg="#ffffff", fg=self.popup_fgc, bd=1, relief="sunken", font=font, insertbackground=self.popup_fgc, justify=align)
        inp.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        return inp
    
    def make_input_multi(self, holder, inp_var, h, w, row, col, padx, pady, pos, font, colspan, rowspan):
        inp = ScrolledText(holder, bg="#ffffff", height=h, width=w, font=font)
        #inp = tk.Entry(holder, textvariable=inp_var, bg="#ffffff", fg=self.popup_fgc, bd=1, relief="sunken", font=font, insertbackground=self.popup_fgc)
        inp.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        return inp
    
    def make_cbox(self, holder, row, col, padx, pady, pos, data, cb_var, font, rowspan, colspan, s_ind):
        combo_box = ttk.Combobox(holder, textvariable=cb_var, state="readonly", values=data, font=font)
        combo_box.grid(row=row, column=col, padx=padx, pady=pady, sticky=pos, columnspan=colspan, rowspan=rowspan)
        combo_box.current(s_ind)

        return combo_box
    
    def layout_booking_update(self):
        pass

    
    def change_qty(self, cnd):
        
        cur_item = self.prod_tbl.item(self.prod_tbl.focus())
        sel_ind = cur_item['values']
        
        if sel_ind != "":
            if cnd == '-':
                if self.prod_arr[sel_ind[0]]['val'] > 0:
                    self.prod_arr[sel_ind[0]]['val'] -= 1
            else:
                self.prod_arr[sel_ind[0]]['val'] += 1

            self.prod_arr[sel_ind[0]]['act'] = "edit"
            selected_item = self.prod_tbl.selection()[0]
            self.prod_tbl.item(selected_item, text="blub", values=(sel_ind[0], sel_ind[1], sel_ind[2], self.prod_arr[sel_ind[0]]['val']))
        else:
            print("Highlight a a product from list.")

    def set_form_booking_update(self, holder, type):
        
        tmp_lbl_pos = (5, 30)
        tmp_inp_pos = (45, 0)
        h_w = self.app_w*.5

        # lbl = self.make_label(holder, 1, 0, 0, tmp_lbl_pos, "nw", "Services Acquired", ("Arial", 12), "w", 1, 1)
        # if type == "Update":
        #     inp_qty = tk.StringVar()
        #     inp_box = self.make_input_multi(holder, inp_qty, 10, 50, 1, 0, (0,10), (45,5), "news", ("Arial", 12), 1, 3)
        # else:
        
        header_data = ("ID", "Product", "Type", "Quantity")
        self.prod_tbl = ttk.Treeview(holder, columns=header_data, show='headings', selectmode="browse")
        self.prod_tbl.grid(row=0, column=0, padx=(0, 30), pady=(10,0), sticky="news", columnspan=1, rowspan=1)
        self.prod_tbl.column("0", width=0, anchor ='c')
        self.prod_tbl.column("1", width=math.ceil(h_w*.45), anchor ='w')
        self.prod_tbl.column("2", width=math.ceil(h_w*.25), anchor ='c')
        self.prod_tbl.column("3", width=math.ceil(h_w*.2), anchor ='c')
        self.prod_tbl.heading("0", text=header_data[0])
        self.prod_tbl.heading("1", text=header_data[1])
        self.prod_tbl.heading("2", text=header_data[2])
        self.prod_tbl.heading("3", text=header_data[3])

        tmp_acquired_prod = {}
        for item in self.prod_items[1]:
            tmp_acquired_prod[item['id']] = int(item['item_qty'])

        for item in self.g_var.products_arr:
            self.prod_arr[item['id']] = {}

            try:
                self.prod_arr[item['id']]['val'] = tmp_acquired_prod[item['id']]
            except:
                self.prod_arr[item['id']]['val'] = 0

            self.prod_arr[item['id']]['act'] = ''
            self.prod_tbl.insert('', 'end', text="", values=(item['id'], item['title'], self.g_var.prod_type_arr[item['prod_type']], self.prod_arr[item['id']]['val']))

        self.prod_tbl["displaycolumns"] = ("Product", "Type", "Quantity")

        self.make_table_scrollbar(holder, self.prod_tbl, 0, 0, (0,15), (10,0), (tk.NS, tk.E), "vertical", 1)

        if type == "Update":
            btn_minus = tk.Button(holder, width=2, bg=self.popup_bgc, relief="raised", anchor="center", text="-", font=("Arial", 15), command=lambda:self.change_qty('-'))
            btn_minus.grid(row=1, column=0, padx=(0, 0), pady=0, sticky="w")
            btn_plus = tk.Button(holder, width=2, bg=self.popup_bgc, relief="raised", anchor="center", text="+", font=("Arial", 15), command=lambda:self.change_qty('+'))
            btn_plus.grid(row=1, column=0, padx=(50, 0), pady=0, sticky="w")

        #lbl = self.make_input_dummy(holder, 1, 0, (0,10), tmp_inp_pos, "news", "", ("Arial", 12), "nw", 1, 4)
        #lbl.config(wraplength=math.ceil(self.app_w*.18))
        #self.assist_con.load_sub_data(f"{self.g_var.g_host}get_booking_pack/{self.popup_data['id']}", lbl)

        cust_info = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        cust_info.grid(row=0, column=1, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)
        
        self.make_label2(cust_info, h_w*.25, 0, h_w*.7, self.popup_data['timestamp'], ('Arial', 12), self.popup_bgc, self.popup_fgc, 'e')
        self.make_label2(cust_info, 0, 40, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 70, h_w*.25, "Client:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 100, h_w*.25, "Contact:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 130, h_w*.25, "Location:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 160, h_w*.25, "Schedule:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 190, h_w*.25, "Mode:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 220, h_w*.25, "Notes:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 250, h_w*.25, "Basket Count:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 280, h_w*.25, "Logistics Fee:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_label2(cust_info, 0, 310, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        
        try:
            tmp_date_sched = f"  ({self.prod_items[0][0]['sched']})"
        except:
            tmp_date_sched = ""

        self.make_input2(cust_info, h_w*.25, 40, h_w*.7, f"{self.assist_con.format_std_code("QLH", str(self.popup_data['id']), 6)}", ('Arial', 12), 'left', 'readonly')
        self.make_input2(cust_info, h_w*.25, 70, h_w*.7, self.popup_data['client'], ('Arial', 12), 'left', 'readonly')
        self.make_input2(cust_info, h_w*.25, 100, h_w*.7, self.popup_data['contact'], ('Arial', 12), 'left', 'readonly')
        self.make_input2(cust_info, h_w*.25, 130, h_w*.7, self.popup_data['pickup_loc'], ('Arial', 12), 'left', 'readonly')
        self.make_input2(cust_info, h_w*.25, 160, h_w*.7, self.popup_data['schedule']+tmp_date_sched, ('Arial', 12), 'left', 'readonly')
        if self.popup_data['mode'] == "Drop off":
            try:
                self.make_input2(cust_info, h_w*.25, 190, h_w*.7, self.popup_data['mode']+"  ("+self.popup_data['dropoff_time']+")", ('Arial', 12), 'left', 'readonly')
            except:
                self.make_input2(cust_info, h_w*.25, 190, h_w*.7, self.popup_data['mode'], ('Arial', 12), 'left', 'readonly')
        else:
            self.make_input2(cust_info, h_w*.25, 190, h_w*.7, self.popup_data['mode'], ('Arial', 12), 'left', 'readonly')
        self.make_input2(cust_info, h_w*.25, 220, h_w*.7, self.popup_data['notes'], ('Arial', 12), 'left', 'readonly')
        self.make_input2(cust_info, h_w*.25, 250, h_w*.7, self.popup_data['quantity'], ('Arial', 12), 'left', 'readonly')

        tmp_fee = self.popup_data['logistics_fee']
        if tmp_fee == None:
            tmp_fee = 0

        if type == "Update":
            stat_var = tk.StringVar()
            self.temp_data['cb_fee'] = self.make_cbox2(cust_info, h_w*.25, 280, h_w*.7, self.b_logistics_fee, stat_var, ('Arial', 12), 0)
            if float(tmp_fee) <= 0:
                self.temp_data['cb_fee'].current(1)
            
            self.temp_data['cb_fee'].index = "cb_fee_inp"
            self.temp_data['cb_fee'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)
            self.temp_data['cb_fee_inp'] = self.make_input2(cust_info, h_w*.25, 280, h_w*.67, "{:.2f}".format(float(tmp_fee)), ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_fee_inp'], self.temp_data['cb_fee'].get())

        else:
            self.make_input2(cust_info, h_w*.25, 280, h_w*.7, "{:.2f}".format(float(tmp_fee)), ('Arial', 12), 'left', 'readonly')
            
        if self.popup_data['mode'] == "Drop off":
            self.b_status_arr = {'Pending':0,'Confirmed':1,'Arrived':2,'Ongoing':3,'To Receive':4,'Completed':5,'Cancelled':6}
            self.b_status_list = ('Pending','Confirmed','Arrived','Ongoing','To Receive','Completed','Cancelled')
        else:
            self.b_status_arr = {'Pending':0,'Confirmed':1,'Pickup':2,'Ongoing':3,'Delivery':4,'Completed':5,'Cancelled':6}
            self.b_status_list = ('Pending','Confirmed','Pickup','Ongoing','Delivery','Completed','Cancelled')

        if type == "Update":
            stat_var = tk.StringVar()
            self.temp_data['cb_stat'] = self.make_cbox2(cust_info, h_w*.25, 310, h_w*.7, self.b_status_list, stat_var, ('Arial', 12), 0)
            self.temp_data['cb_stat'].current(self.b_status_arr[(self.popup_data['status']).rstrip()])
            self.temp_data['cb_stat'].index = "cb_stat_inp"
            self.temp_data['cb_stat'].id = "bookings"
            self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_stat_inp'] = self.make_input2(cust_info, h_w*.25, 310, h_w*.67, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        else:
            self.make_input2(cust_info, h_w*.25, 310, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')

        if self.popup_data['cancel_reason'] == None:
            self.popup_data['cancel_reason'] = ""
        
        if type == "Update":
            self.make_label2(cust_info, 0, 340, h_w*.25, "Reason:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
            self.temp_data['cancel'] = self.make_input2(cust_info, h_w*.25, 340, h_w*.7, self.popup_data['cancel_reason'], ('Arial', 12), 'left', 'readonly')
        else:
            if self.popup_data['status'] == "Cancelled":
                #self.temp_data['cancel'] = self.make_input2(cust_info, h_w*.25, 340, h_w*.7, self.popup_data['cancel_reason'], ('Arial', 12), 'left', 'readonly')
                self.make_label2(cust_info, h_w*.25, 340, h_w*.7, f"Cancelled by: {self.popup_data['cancelled_by']}", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
                self.make_label2(cust_info, h_w*.25, 360, h_w*.7, f"Reason: {self.popup_data['cancel_reason']}", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        pady = (0,5)

        if type == "Update":
            lbl = self.make_label(holder, 1, 0, (h_w*.25,h_w*.025), 0, "new", "Highlight an entry to update the item quantity", ("Arial", 11), "e", 1, 1)
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("bookings"))
            btn_save.grid(row=1, column=1, padx=(5,170), pady=pady, sticky="es")
            
        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=1, padx=5, pady=pady, sticky="es")
        self.g_var.popup_holder_win.update()

    def custom_dropdown_action(self, event):
        try:
            if event.widget.id == "bookings":
                if event.widget.get() == "Cancelled":
                    self.temp_data['cancel'].config(state="normal")
                else:
                    self.temp_data['cancel'].config(state="readonly")
        except:
            pass

        self.assist_con.set_custom_cbox_inp(self.temp_data[event.widget.index], event.widget.get())

    def create_button_icon(self, holder, qr_src, w, h):
        from PIL import Image, ImageTk

        original_image = Image.open(qr_src)
        resized_image = original_image.resize((w, h), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(resized_image)
        
        img_ref = tk.Label(holder, image=photo_image)
        img_ref.image = photo_image 

        return photo_image

    def set_form_shop_services(self, holder, type):

        h_w = self.app_w*.97
        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        # self.make_label2(form_area, 0, 5, h_w*.25, "Service ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 5, h_w*.25, "Product Type:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            unit_var = tk.StringVar()
            self.temp_data['cb_type'] = self.make_cbox2(form_area, h_w*.25, 5, h_w*.73, self.prod_type_list, unit_var, ('Arial', 12), 0)
            try: 
                self.temp_data['cb_type'].current(self.prod_type_arr[(self.popup_data['prod_type']).rstrip()]) 
            except: 
                pass

            self.temp_data['cb_type'].index = "cb_type_inp"
            self.temp_data['cb_type'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_type_inp'] = self.make_input2(form_area, h_w*.25, 5, h_w*.7, self.popup_data['prod_type'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_type_inp'], self.temp_data['cb_type'].get())
        else:
            self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.g_var.prod_type_arr[self.popup_data['prod_type']], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 35, h_w*.25, "Title:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['title'] = self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['title'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['title'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 65, h_w*.25, "Description:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['description'] = self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'readonly')
           
        self.make_label2(form_area, 0, 95, h_w*.25, "Price:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['price'] = self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['price'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['price'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 125, h_w*.25, "Quantity:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['quantity'] = self.make_input2(form_area, h_w*.25, 125, h_w*.73, self.popup_data['quantity'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 125, h_w*.73, self.popup_data['quantity'], ('Arial', 12), 'left', 'readonly')
            
        self.make_label2(form_area, 0, 155, h_w*.25, "Unit:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            unit_var = tk.StringVar()
            self.temp_data['cb_unit'] = self.make_cbox2(form_area, h_w*.25, 155, h_w*.73, self.units_list, unit_var, ('Arial', 12), 0)
            try: 
                self.temp_data['cb_unit'].current(self.units_arr[self.popup_data['unit']]) 
            except: 
                pass

            self.temp_data['cb_unit'].index = "cb_unit_inp"
            self.temp_data['cb_unit'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_unit_inp'] = self.make_input2(form_area, h_w*.25, 155, h_w*.7, self.popup_data['unit'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_unit_inp'], self.temp_data['cb_unit'].get())
        else:
            self.make_input2(form_area, h_w*.25, 155, h_w*.73, self.popup_data['unit'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 185, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            stat_var = tk.StringVar()
            self.temp_data['cb_stat'] = self.make_cbox2(form_area, h_w*.25, 185, h_w*.73, self.r_status_list, stat_var, ('Arial', 12), 0)
            self.temp_data['cb_stat'].current(self.r_status_arr[(self.popup_data['status']).rstrip()])
            self.temp_data['cb_stat'].index = "cb_stat_inp"
            self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_stat_inp'] = self.make_input2(form_area, h_w*.25, 185, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        else:
            self.make_input2(form_area, h_w*.25, 185, h_w*.73, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
           
        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("services"))
            btn_save.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")
        elif type == "Add":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_add = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.add_data("services"))
            btn_add.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=(0,5), pady=pady, sticky="es")

    def set_form_shop_addons(self, holder, type):
        h_w = self.app_w*.97

        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        # self.make_label2(form_area, 0, 5, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 5, h_w*.25, "Title", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['title'] = self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['title'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['title'], ('Arial', 12), 'left', 'readonly')
          
        self.make_label2(form_area, 0, 35, h_w*.25, "Price:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['price'] = self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['price'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['price'], ('Arial', 12), 'left', 'readonly')
            
        self.make_label2(form_area, 0, 65, h_w*.25, "Description:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['description'] = self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'readonly')
           
        self.make_label2(form_area, 0, 95, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            stat_var = tk.StringVar()
            self.temp_data['cb_stat'] = self.make_cbox2(form_area, h_w*.25, 95, h_w*.73, self.r_status_list, stat_var, ('Arial', 12), 0)
            self.temp_data['cb_stat'].current(self.r_status_arr[(self.popup_data['status']).rstrip()])
            self.temp_data['cb_stat'].index = "cb_stat_inp"
            self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_stat_inp'] = self.make_input2(form_area, h_w*.25, 95, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        else:
            self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'readonly')

        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("addons"))
            btn_save.grid(row=1, column=0, padx=170, pady=pady, sticky="es")
        elif type == "Add":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_add = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.add_data("addons"))
            btn_add.grid(row=1, column=0, padx=170, pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=5, pady=pady, sticky="es")

    def set_form_shop_rewards(self, holder, type):
        
        h_w = self.app_w*.97
        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        # self.make_label2(form_area, 0, 5, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 5, h_w*.25, "Title:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['title'] = self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['title'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['title'], ('Arial', 12), 'left', 'readonly')
            
        self.make_label2(form_area, 0, 35, h_w*.25, "Points Required:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['pts_req'] = self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['pts_req'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['pts_req'], ('Arial', 12), 'left', 'readonly')
           
        self.make_label2(form_area, 0, 65, h_w*.25, "Description:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['description'] = self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 95, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            stat_var = tk.StringVar()
            self.temp_data['cb_stat'] = self.make_cbox2(form_area, h_w*.25, 95, h_w*.73, self.r_status_list, stat_var, ('Arial', 12), 0)
            self.temp_data['cb_stat'].current(self.r_status_arr[self.popup_data['status']])
            self.temp_data['cb_stat'].index = "cb_stat_inp"
            self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_stat_inp'] = self.make_input2(form_area, h_w*.25, 95, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        else:
            self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')

        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("rewards"))
            btn_save.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")
        elif type == "Add":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_add = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.add_data("rewards"))
            btn_add.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=(0,5), pady=pady, sticky="es")

    def set_form_billing_payments(self, holder, type):
       
        h_w = self.app_w*.97
        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        # self.make_label2(form_area, 0, 5, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 5, h_w*.25, "Booking ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.assist_con.format_std_code("QLH", str(self.popup_data['booking_id']), 6), ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 35, h_w*.25, "Amount Due:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['amount_due'] = self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.tbl_field[3], ('Arial', 12), 'left', 'readonly')
            
        self.make_label2(form_area, 0, 65, h_w*.25, "Amount Paid:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if self.popup_data['mode'] != "Points":
            self.popup_data['amount'] = "{:.2f}".format(float(self.popup_data['amount']))

        if type == "Update":
            self.temp_data['amount'] = self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['amount'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['amount'], ('Arial', 12), 'left', 'readonly')

        # self.make_label2(form_area, 0, 95, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # if type == "Update":
        #     stat_var = tk.StringVar()
        #     self.temp_data['cb_stat'] = self.make_cbox2(form_area, h_w*.25, 95, h_w*.73, self.p_status_list, stat_var, ('Arial', 12), 0)
        #     if self.popup_data['status'] == "":
        #         self.popup_data['status'] = "Unpaid"

        #     self.temp_data['cb_stat'].current(self.p_status_arr[self.popup_data['status']])
        #     self.temp_data['cb_stat'].index = "cb_stat_inp"
        #     self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

        #     self.temp_data['cb_stat_inp'] = self.make_input2(form_area, h_w*.25, 95, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
        #     self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        # else:
        #     self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            
        self.make_label2(form_area, 0, 95, h_w*.25, "Payment Mode:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update":
            mode_var = tk.StringVar()
            self.temp_data['cb_mode'] = self.make_cbox2(form_area, h_w*.25, 95, h_w*.73, self.p_mode_list, mode_var, ('Arial', 12), 0)
            if self.popup_data['mode'] == "":
                self.popup_data['mode'] = "GCash"

            self.temp_data['cb_mode'].current(self.p_mode_arr[self.popup_data['mode']])
            self.temp_data['cb_mode'].index = "cb_mode_inp"
            self.temp_data['cb_mode'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_mode_inp'] = self.make_input2(form_area, h_w*.25, 95, h_w*.7, self.popup_data['mode'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_mode_inp'], self.temp_data['cb_mode'].get())
        else:
            self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['mode'], ('Arial', 12), 'left', 'readonly')
           
        self.make_label2(form_area, 0, 125, h_w*.25, "Reference No:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update":
            self.temp_data['ref_num'] = self.make_input2(form_area, h_w*.25, 125, h_w*.73, self.popup_data['ref_num'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 125, h_w*.73, self.popup_data['ref_num'], ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 155, h_w*.25, "Reward Points:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update":
            self.temp_data['points'] = self.make_input2(form_area, h_w*.25, 155, h_w*.73, '', ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 155, h_w*.73, '', ('Arial', 12), 'left', 'readonly')
            
        self.make_label2(form_area, 0, 185, h_w*.25, "Reward Description:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            self.temp_data['description'] = self.make_input2(form_area, h_w*.25, 185, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'normal')
        else:
            self.make_input2(form_area, h_w*.25, 185, h_w*.73, self.popup_data['description'], ('Arial', 12), 'left', 'readonly')
            
        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("billings"))
            btn_save.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=(0,5), pady=pady, sticky="es")

    def set_form_user_account(self, holder, type):
        tmp_points = 0
        try:
            response = requests.get(f"{self.g_var.g_host}user_points/{self.popup_data['id']}")
            if response.status_code == 200:
                data = response.json()
                tmp_points = data
                   
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        tmp_lbl_pos = (5, 30)
        tmp_inp_pos = (45, 0)

        h_w = self.app_w*.97
        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        # self.make_label2(form_area, 0, 5, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 5, h_w*.25, "Available Points:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 5, h_w*.73, tmp_points, ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 35, h_w*.25, "User Name:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['user_name'], ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 65, h_w*.25, "Password:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['password'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 95, h_w*.25, "Email:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['email'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 125, h_w*.25, "First Name:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 125, h_w*.73, self.popup_data['first_name'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 155, h_w*.25, "Last Name:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 155, h_w*.73, self.popup_data['last_name'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 185, h_w*.25, "Mobile No:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 185, h_w*.73, self.popup_data['mobile_no'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 215, h_w*.25, "Address:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 215, h_w*.73, self.popup_data['address'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 245, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            stat_var = tk.StringVar()
            inp_stat = tk.StringVar()
            self.temp_data['cb_stat'] = self.make_cbox2(form_area, h_w*.25, 245, h_w*.73, self.r_status_list, stat_var, ('Arial', 12), 0)
            self.temp_data['cb_stat'].current(self.r_status_arr[self.popup_data['status']])
            self.temp_data['cb_stat'].index = "cb_stat_inp"
            self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_stat_inp'] = self.make_input2(form_area, h_w*.25, 245, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        else:
            self.make_input2(form_area, h_w*.25, 245, h_w*.73, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')

        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("customers"))
            btn_save.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=(0,5), pady=pady, sticky="es")
        
    def set_form_riders_assignment(self, holder, type):

        h_w = self.app_w*.97
        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        # self.make_label2(form_area, 0, 2, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 5, h_w*.25, "Booking ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.assist_con.format_std_code("QLH", str(self.popup_data['booking_id']), 6), ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 35, h_w*.25, "Client:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['client'], ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 65, h_w*.25, "Address:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['pickup_loc'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 95, h_w*.25, "Task:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['task_type'], ('Arial', 12), 'left', 'readonly')

        # self.make_label2(form_area, 0, 155, h_w*.25, "Rider:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 155, h_w*.73, self.popup_data['rider_id'], ('Arial', 12), 'left', 'readonly')

        self.make_label2(form_area, 0, 125, h_w*.25, "Rider:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')

        if self.popup_data['rider_id'] == None:
            cur_ind = 0
            cur_rider = ""
        else:
            cur_ind = self.g_var.riders_ids[self.popup_data['rider_id']]
            cur_rider = f"{self.g_var.riders_arr[cur_ind]['name']} ({self.g_var.riders_arr[cur_ind]['status']})" #self.g_var.riders_list[cur_ind]

        if type == "Update":
            stat_var = tk.StringVar()
            self.temp_data['rider_assigned'] = self.make_cbox2(form_area, h_w*.25, 125, h_w*.73, self.g_var.riders_list, stat_var, ('Arial', 12), 0)
            self.temp_data['rider_assigned'].current(cur_ind)
            self.temp_data['rider_assigned'].index = "rider_assigned_inp"
            self.temp_data['rider_assigned'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['rider_assigned_inp'] = self.make_input2(form_area, h_w*.25, 125, h_w*.7, cur_rider, ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['rider_assigned_inp'], self.temp_data['rider_assigned'].get())
        else:
            if self.popup_data['rider_id'] == None:
                self.make_input2(form_area, h_w*.25, 125, h_w*.73, "", ('Arial', 12), 'left', 'readonly')
            else:
                self.make_input2(form_area, h_w*.25, 125, h_w*.73, cur_rider, ('Arial', 12), 'left', 'readonly')

        if self.popup_data['date_assigned'] != None:
            self.make_label2(form_area, 0, 155, h_w*.25, "Date Assigned:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
            self.make_input2(form_area, h_w*.25, 155, h_w*.73, self.popup_data['date_assigned'], ('Arial', 12), 'left', 'readonly')
        
        if self.popup_data['date_completed'] != None:
            self.make_label2(form_area, 0, 185, h_w*.25, "Date Completed:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
            self.make_input2(form_area, h_w*.25, 185, h_w*.73, self.popup_data['date_completed'], ('Arial', 12), 'left', 'readonly')

        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("logistics"))
            btn_save.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=(0,5), pady=pady, sticky="es")
    
    def set_form_riders_account(self, holder, type):
       
        h_w = self.app_w*.97
        form_area = tk.LabelFrame(holder, text='', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        form_area.grid(row=0, column=0, padx=(0,5), pady=(10,0), sticky="news", columnspan=1, rowspan=1)

        input_type = 'readonly'
        self.popup_data['password'] = "********"
        if type == "Update" or type == "Add":
            input_type = 'normal'
            if type == "Add":
                self.popup_data['password'] = ""
        
        # self.make_label2(form_area, 0, 2, h_w*.25, "ID:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        # self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['id'], ('Arial', 12), 'left', 'readonly')
        
        self.make_label2(form_area, 0, 5, h_w*.25, "User Name:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['user_name'] = self.make_input2(form_area, h_w*.25, 5, h_w*.73, self.popup_data['user_name'], ('Arial', 12), 'left', input_type)
        
        self.make_label2(form_area, 0, 35, h_w*.25, "Password:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['password'] = self.make_input2(form_area, h_w*.25, 35, h_w*.73, self.popup_data['password'], ('Arial', 12), 'left', input_type)
        self.temp_data['password'].config(show="*")

        self.make_label2(form_area, 0, 65, h_w*.25, "First Name:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['first_name'] = self.make_input2(form_area, h_w*.25, 65, h_w*.73, self.popup_data['first_name'], ('Arial', 12), 'left', input_type)

        self.make_label2(form_area, 0, 95, h_w*.25, "Last Name:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['last_name'] = self.make_input2(form_area, h_w*.25, 95, h_w*.73, self.popup_data['last_name'], ('Arial', 12), 'left', input_type)

        self.make_label2(form_area, 0, 125, h_w*.25, "Mobile No:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['mobile_no'] = self.make_input2(form_area, h_w*.25, 125, h_w*.73, self.popup_data['mobile_no'], ('Arial', 12), 'left', input_type)

        self.make_label2(form_area, 0, 155, h_w*.25, "Address:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        self.temp_data['address'] = self.make_input2(form_area, h_w*.25, 155, h_w*.73, self.popup_data['address'], ('Arial', 12), 'left', input_type)

        self.make_label2(form_area, 0, 185, h_w*.25, "Status:", ('Arial', 12), self.popup_bgc, self.popup_fgc, 'w')
        if type == "Update" or type == "Add":
            stat_var = tk.StringVar()
            inp_stat = tk.StringVar()
            self.temp_data['cb_stat'] = self.make_cbox2(form_area, h_w*.25, 185, h_w*.73, self.r_status_list, stat_var, ('Arial', 12), 0)
            self.temp_data['cb_stat'].current(self.r_status_arr[self.popup_data['status']])
            self.temp_data['cb_stat'].index = "cb_stat_inp"
            self.temp_data['cb_stat'].bind("<<ComboboxSelected>>", self.custom_dropdown_action)

            self.temp_data['cb_stat_inp'] = self.make_input2(form_area, h_w*.25, 185, h_w*.7, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')
            self.assist_con.set_custom_cbox_inp(self.temp_data['cb_stat_inp'], self.temp_data['cb_stat'].get())
        else:
            self.make_input2(form_area, h_w*.25, 185, h_w*.73, self.popup_data['status'], ('Arial', 12), 'left', 'readonly')

        pady = (0,5)

        if type == "Update":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_save = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.update_data("riders"))
            btn_save.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")
        elif type == "Add":
            icon = self.create_button_icon(holder, "assets/images/save_button.png", 115, 40)
            btn_add = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:self.add_data("riders"))
            btn_add.grid(row=1, column=0, padx=(0,170), pady=pady, sticky="es")

        icon = self.create_button_icon(holder, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(holder, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=1, column=0, padx=(0,5), pady=pady, sticky="es")

    def setup_frame_layout(self, holder, app_w, app_h, prc_w, prc_h):
        i = 0
        for item in prc_w:
            holder.columnconfigure(i, minsize=math.ceil(app_w*item), weight=1)
            i+=1

        i = 0
        for item in prc_h:
            holder.rowconfigure(i, minsize=math.ceil(app_h*item), weight=1)
            i+=1

    def form_global_popup(self, cmd, type, tbl_data, tbl):
        self.temp_data = {}
        self.popup_data = tbl_data
        self.cur_id = tbl_data['id']
        self.tbl_field = tbl
        
        #self.popup_global_win = tk.Tk()
        self.popup_global_win = tk.Toplevel(bg=self.popup_bgc)
        if cmd == "bookings":
            self.cur_uid = tbl_data['user_id']
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.7)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.6)
            prc_w = (.49, .49)
            prc_h = (.82,.15)
            
            self.load_request_data(self.g_var.g_host+'get_booking_details/{"key":"'+self.g_var.app_token+'","id":"'+str(self.cur_id)+'"}')

        elif cmd == "services":
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.35)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        elif cmd == "addons":
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.35)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        elif cmd == "rewards":
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.35)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        elif cmd == "billings":
            self.cur_uid = tbl_data['user_id']
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.41)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        elif cmd == "customers":
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.35)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        elif cmd == "logistics":
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.35)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        elif cmd == "riders":
            self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.35)
            self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.5)
            prc_w = (.98,)
            prc_h = (.82,.15)
        
        anchor_x = math.ceil((self.popup_global_win.winfo_screenwidth()-self.app_w)/2)
        anchor_y = math.ceil((self.popup_global_win.winfo_screenheight()-self.app_h)/2)
        self.popup_global_win.geometry(f"{self.app_w}x{self.app_h}+{anchor_x}+{anchor_y}")
        self.popup_global_win.title(type)
        self.popup_global_win.resizable(tk.FALSE, tk.FALSE)
        self.popup_global_win.protocol("WM_DELETE_WINDOW", lambda:self.close_global_popup())
        form = tk.Frame(self.popup_global_win, bg=self.popup_bgc, relief=tk.FLAT, bd=2, padx=(self.app_w*.01))
        self.setup_frame_layout(form, self.app_w, self.app_h, prc_w, prc_h)

        if cmd == "bookings":
            self.set_form_booking_update(form, type)
        elif cmd == "services":
            self.set_form_shop_services(form, type)
        elif cmd == "addons":
            self.set_form_shop_addons(form, type)
        elif cmd == "rewards":
            self.set_form_shop_rewards(form, type)
        elif cmd == "billings":
            self.set_form_billing_payments(form, type)
        elif cmd == "customers":
            self.set_form_user_account(form, type)
        elif cmd == "logistics":
            self.set_form_riders_assignment(form, type)
        elif cmd == "riders":
            self.set_form_riders_account(form, type)

        form.pack()
        self.g_var.set_active_popup(self.popup_global_win)
        self.popup_global_win.update()    
        self.popup_global_win.after(1, lambda: self.popup_global_win.focus_force())
        self.popup_global_win.mainloop()

    def reply_threads(self, msg):
        data = {
            'tok':self.g_var.app_token, 
            'act':"Update",
            'data':{'thread_id':self.g_var.thread_id, "sender_id":"0", "message":msg}
        }  
        if msg.strip() != "":
            self.update_threads_data(self.g_var.g_host+"set_thread_reply_admin", data)

    def form_global_chatbox(self, popup_data):
        
        #self.popup_global_win = tk.Tk()
        self.popup_global_win = tk.Toplevel(bg=self.popup_bgc)

        self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.3)
        self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.4)
        prc_w = (.49,.49)
        prc_h = (.35,.35,.2)
        
        anchor_x = math.ceil((self.popup_global_win.winfo_screenwidth()-self.app_w)/2)
        anchor_y = math.ceil((self.popup_global_win.winfo_screenheight()-self.app_h)/2)
        self.popup_global_win.geometry(f"{self.app_w}x{self.app_h}+{anchor_x}+{anchor_y}")
        self.popup_global_win.resizable(tk.FALSE, tk.FALSE)
        self.popup_global_win.protocol("WM_DELETE_WINDOW", lambda:self.close_global_popup())
        form = tk.Frame(self.popup_global_win, bg=self.popup_bgc, relief=tk.FLAT, bd=2, padx=(self.app_w*.01))
        self.setup_frame_layout(form, self.app_w, self.app_h, prc_w, prc_h)
        #self.set_form_billing_payments(form, type)
        
        if popup_data[2] == "":
            #msg_str = f"Client: {popup_data[0]}"
            self.popup_global_win.title("Client >>")
        else:
            #msg_str = f"Admin: {popup_data[0]}"
            self.popup_global_win.title("Admin >>")

        msg_area = tk.LabelFrame(form, text='Message', bg=self.popup_bgc, fg="#181818", font=("Arial", 10, "bold"))
        msg_area.grid(row=0, column=0, padx=(0,5), pady=(0,20), sticky="news", columnspan=2, rowspan=1)

        lbl = self.make_label(msg_area, 0, 0, 0, (0,10), "news", popup_data[0], self.g_var.g_font1, "w", 2, 1)
        lbl.config(wraplength=self.app_w*.95, fg="#1e1e1e", justify="left")
        #inp_var2 = tk.StringVar()
        #lbl = self.make_input_multi(form, inp_var2, 10, 50, 0, 0, (0,10), (45,5), "news", ("Arial", 12), 2, 1)
        
        inp_var = tk.StringVar()
        inp = self.make_input_multi(form, inp_var, 10, 50, 1, 0, (0,5), (5,5), "news", ("Arial", 12), 2, 1)

        icon = self.create_button_icon(form, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(form, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=lambda:self.close_global_popup())
        btn_close.grid(row=2, column=1, padx=(0,10), pady=0)

        icon = self.create_button_icon(form, "assets/images/send_button.png", 115, 40)
        btn_save = tk.Button(form, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Reply", font=("Arial", 12), command=lambda:self.reply_threads((inp.get("1.0", tk.END)).strip()))
        btn_save.grid(row=2, column=0, padx=(0,10), pady=0)
        
        form.pack()
        self.g_var.set_active_popup(self.popup_global_win)
        self.popup_global_win.update()    
        self.popup_global_win.after(1, lambda: self.popup_global_win.focus_force())
        self.popup_global_win.mainloop()
        
    def login_admin(self):
        if self.temp_data['user_name'].get() == self.admin_data[0] and self.assist_con.get_hash_value(self.temp_data['password'].get()) == self.admin_data[1]:
            self.g_var.auth_user = True
            self.g_var.db_con.update_admin_data("tbl_system", "cookie=1", "1")
            self.close_global_popup()
        else:
            self.g_var.warn_popup("Access Denied", "Invalid login account!")

    def show_password(self, event):
        self.temp_data['password'].config(show="")

    def hide_password(self, event):
        self.temp_data['password'].config(show="*")

    def system_setup(self, data):
        
        self.admin_data = data
        self.popup_global_win = tk.Tk()
        #self.popup_global_win = tk.Toplevel(bg=self.popup_bgc)

        self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.25)
        self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.3)
        prc_w = (.49,.49)
        prc_h = (.15,.15,.15,.15,.1,.3)
        
        anchor_x = math.ceil((self.popup_global_win.winfo_screenwidth()-self.app_w)/2)
        anchor_y = math.ceil((self.popup_global_win.winfo_screenheight()-self.app_h)/2)
        self.popup_global_win.geometry(f"{self.app_w}x{self.app_h}+{anchor_x}+{anchor_y}")
        self.popup_global_win.resizable(tk.FALSE, tk.FALSE)
        self.popup_global_win.protocol("WM_DELETE_WINDOW", lambda:self.close_global_popup())
        form = tk.Frame(self.popup_global_win, bg=self.popup_bgc, relief=tk.FLAT, bd=2, padx=(self.app_w*.01))
        self.setup_frame_layout(form, self.app_w, self.app_h, prc_w, prc_h)

        self.popup_global_win.title("Admin Login")

        lbl = self.make_label(form, 0, 0, 0, 0, "s", "User Name", ("Arial", 12), "w", 2, 1)
        inp_uname = tk.StringVar()
        self.temp_data['user_name'] = self.make_input(form, inp_uname, 1, 0, (30,30), (5,5), "news", ("Arial", 12), 2, 1, "center")
        self.temp_data['user_name'].insert(0, data[0])

        lbl = self.make_label(form, 2, 0, 0, 0, "s", "Password", ("Arial", 12), "w", 2, 1)
        inp_upass = tk.StringVar()
        self.temp_data['password'] = self.make_input(form, inp_upass, 3, 0, (30,30), (5,5), "news", ("Arial", 12), 2, 1, "center")
        self.temp_data['password'].config(show="*")
        icon = self.create_button_icon(form, "assets/images/eye_dark.png", 22, 22)
        btn_show = tk.Button(form, bg="#ffffff", relief="flat", image=icon, anchor="center", text="Login", font=("Arial", 12))
        btn_show.bind("<ButtonPress-1>", self.show_password)
        btn_show.bind("<ButtonRelease-1>", self.hide_password)
        btn_show.grid(row=3, column=0, padx=(0,31), pady=(1,0), sticky="e", columnspan=2)

        icon = self.create_button_icon(form, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(form, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=self.close_global_popup)
        btn_close.grid(row=5, column=1, padx=(0,10), pady=0)

        icon = self.create_button_icon(form, "assets/images/login_button.png", 115, 40)
        btn_save = tk.Button(form, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Login", font=("Arial", 12), command=self.login_admin)
        btn_save.grid(row=5, column=0, padx=(0,10), pady=0)
        
        form.pack()
        self.g_var.set_active_popup(self.popup_global_win)
        self.popup_global_win.update()    
        self.popup_global_win.after(1, lambda: self.popup_global_win.focus_force())
        self.popup_global_win.mainloop()

    def update_day_off_data(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.g_var.headers)
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                
                if data != "valid":
                    self.g_var.day_off_list.clear()
                    self.listbox.delete(*self.listbox.get_children())
                    self.listbox.tag_configure("oddrow", background=self.g_var.tbl_style['row_odd'])
                    self.listbox.tag_configure("evenrow", background=self.g_var.tbl_style['row_even'])
                    i=1
                    for item in data:
                        tmp_ind = item['sched_date'].split('-')
                        self.g_var.day_off_list.insert(i, {'month':int(tmp_ind[0]), 'day':int(tmp_ind[1]), 'desc':item['description']})
                    
                        if i % 2 == 0:
                            tags_indc = "oddrow"
                        else:
                            tags_indc = "evenrow"
                        
                        self.listbox.insert('', 'end', text="", values=(i, f"{self.g_var.months[int(tmp_ind[0])-1]} {int(tmp_ind[1])}"), tags=(tags_indc,))
                        i+=1

                    self.close_global_popup()
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def set_month_days(self):
        i=0
        data = []
        for i in range(self.g_var.month_days[self.inp_month.current()]):
            data.insert(i, i+1)

        self.inp_day.config(values=data)
        self.inp_day.current(0)

    def set_month(self, event):
        self.set_month_days()

    def set_shop_day_off(self, act):
        tmp_mm = self.assist_con.format_std_code("", str(self.inp_month.current()+1), 2)
        tmp_dd = self.assist_con.format_std_code("", self.inp_day.get(), 2)
        
        data = {
            'tok': self.g_var.app_token,
            'act': act,
            'data': {'sched_date':f"{tmp_mm}-{tmp_dd}", 'description':self.inp_desc.get()}
        }
        
        self.update_day_off_data(self.g_var.g_host+"mod_tbl_day_off", data)

    def mod_shop_day_off(self, ind, listbox):
        self.listbox = listbox
        #self.popup_global_win = tk.Tk()
        self.popup_global_win = tk.Toplevel(bg=self.popup_bgc)
        
        self.app_w = math.ceil(self.popup_global_win.winfo_screenwidth()*.25)
        self.app_h = math.ceil(self.popup_global_win.winfo_screenheight()*.3)
        prc_w = (.49,.49)
        prc_h = (.15,.15,.15,.15,.1,.3)
        
        anchor_x = math.ceil((self.popup_global_win.winfo_screenwidth()-self.app_w)/2)
        anchor_y = math.ceil((self.popup_global_win.winfo_screenheight()-self.app_h)/2)
        self.popup_global_win.geometry(f"{self.app_w}x{self.app_h}+{anchor_x}+{anchor_y}")
        self.popup_global_win.resizable(tk.FALSE, tk.FALSE)
        self.popup_global_win.protocol("WM_DELETE_WINDOW", lambda:self.close_global_popup())
        form = tk.Frame(self.popup_global_win, bg=self.popup_bgc, relief=tk.FLAT, bd=2, padx=(self.app_w*.01))
        self.setup_frame_layout(form, self.app_w, self.app_h, prc_w, prc_h)

        if ind == "":
            act = "add"
            self.popup_global_win.title("Add Day Off Date")
        else:
            act = "update"
            self.popup_global_win.title("Modify Day Off Event")
    
        lbl = self.make_label(form, 0, 0, 0, 0, "ws", "Date", ("Arial", 12), "w", 2, 1)
        var_month = tk.StringVar()
        self.inp_month = self.make_cbox(form, 1, 0, (0,70), (5,5), "news", self.g_var.months, var_month, ("Arial", 12), 1, 2, 0)
        self.inp_month.bind("<<ComboboxSelected>>", self.set_month)
       
        var_day = tk.StringVar()
        self.inp_day = self.make_cbox(form, 1, 0, (200,5), (5,5), "nes", (1, 2, 3), var_day, ("Arial", 12), 1, 2, 0)
        self.inp_day.config(width=4, justify="center")
        self.set_month_days()
        
        
        lbl = self.make_label(form, 2, 0, 0, 0, "ws", "Event", ("Arial", 12), "w", 2, 1)
        var_desc = tk.StringVar()
        self.inp_desc = self.make_input(form, var_desc, 3, 0, (0,5), (5,5), "news", ("Arial", 12), 2, 1, "left")

        if ind != "":
            self.inp_month.current(int(self.g_var.day_off_list[ind-1]['month'])-1)
            self.inp_day.current(int(self.g_var.day_off_list[ind-1]['day'])-1)
            self.inp_desc.insert(0,self.g_var.day_off_list[ind-1]['desc'])
            self.inp_month.config(state="disabled")
            self.inp_day.config(state="disabled")
            

        icon = self.create_button_icon(form, "assets/images/close_button.png", 115, 40)
        btn_close = tk.Button(form, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Close", font=("Arial", 12), command=self.close_global_popup)
        btn_close.grid(row=5, column=1, padx=(0,10), pady=0)

        icon = self.create_button_icon(form, "assets/images/set_button.png", 115, 40)
        btn_save = tk.Button(form, bg=self.popup_bgc, relief="flat", image=icon, anchor="center", text="Set", font=("Arial", 12), command=lambda:self.set_shop_day_off(act))
        btn_save.grid(row=5, column=0, padx=(0,10), pady=0)
        
        form.pack()
        self.g_var.set_active_popup(self.popup_global_win)
        self.popup_global_win.update()    
        self.popup_global_win.after(1, lambda: self.popup_global_win.focus_force())
        self.popup_global_win.mainloop()