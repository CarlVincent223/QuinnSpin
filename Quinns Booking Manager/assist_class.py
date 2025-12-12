import hashlib
import requests
from datetime import datetime
import pytz
UTC = pytz.utc
ph_tz = pytz.timezone('Asia/Manila')
import calendar

from tkinter import messagebox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import numpy as np
from PIL import ImageColor

from generate_docs import write_docs_class
gen_docs = write_docs_class()

class processor_mthd:

    def __init__(self, g_var) -> None:
        self.g_var = g_var
        self.days_ctr = {}
        i=0
        for i in range(len(g_var.days)):
            self.days_ctr[g_var.days[i]] = 0
        self.days_ctr['highest'] = 0

        self.months_ctr = {}
        i=0
        for i in range(len(g_var.months)):
            self.months_ctr[g_var.months[i]] = 0
        self.months_ctr['highest'] = 0

    def get_hash_value(self, val):
        h = hashlib.new("SHA256")
        h.update(val.encode(encoding='utf-8'))
        
        return h.hexdigest()

    def set_custom_cbox_inp(self, obj, val):
        obj.config(state="normal")
        obj.delete(0, tk.END)
        obj.insert(0, val)
        obj.config(state="readonly")

    def format_std_code(self, code, num, max_len):
        res = ""
        ctr = len(num)
        while ctr < max_len:
            res += "0"
            ctr += 1

        return code+res+num
    
    def get_default_dt(self):
        return datetime.now(ph_tz)
    
    def get_days_in_month(self, year, month):
        num_days = calendar.monthrange(year, month)
        return num_days
    
    def get_datetime(self):
        dt_now = datetime.now(ph_tz)
        dt_now = dt_now.strftime("%Y-%m-%d %H:%M:%S")

        return dt_now  
    
    def format_std_datetime(self, val):
        new_dt = val.strftime("%Y-%m-%d %H:%M:%S")

        return new_dt 
    
    def load_resource_data(self, url, type):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if type == "products":
                    self.g_var.products_arr = data
                else:
                    for item in data:
                        if type == "services":
                            ind = f"{item['category']}-{item['id']}"
                            self.g_var.services_arr[ind] = {}
                            self.g_var.services_arr[ind]['name'] = item['sub_title']
                            self.g_var.services_arr[ind]['price'] = item['price']
                            self.g_var.services_arr[ind]['qty'] = item['quantity']
                            self.g_var.services_arr[ind]['unit'] = item['unit']
                        elif type == "addons":
                            ind = f"{item['category']}-{item['id']}"
                            self.g_var.addons_arr[ind] = {}
                            self.g_var.addons_arr[ind]['name'] = item['description']
                            self.g_var.addons_arr[ind]['price'] = item['price']
                
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    def load_sub_data(self, url, obj):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                str1 = ""
                str2 = ""
                str3 = ""
                for item in data:
                    try:
                        str1 += self.g_var.services_arr[f"{item['prod_type']}-{item['service_id']}"]['name']+"\n"
                    except:
                        pass

                    try:
                        if item['prod_type'] == "addon_drymin":
                            str3 += "  • "+self.g_var.addons_arr[f"{item['prod_type']}-{item['service_id']['name']}"]+"\n"
                        else:
                            str2 += "  • "+self.g_var.addons_arr[f"{item['prod_type']}-{item['service_id']['name']}"]+"\n"
                    except:
                        pass

                obj.config(text=str1+str3+str2, justify="left")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    def load_request_data(self, url, tbl, content):
        self.g_var.url = url
        self.g_var.tbl = tbl
        self.g_var.content = content
        tbl.tag_configure("oddrow", background=self.g_var.tbl_style['row_odd'])
        tbl.tag_configure("evenrow", background=self.g_var.tbl_style['row_even'])
        tbl.tag_configure("oddrow_bold", background=self.g_var.tbl_style['row_odd'], font=('Arial', 11, 'bold'))
        tbl.tag_configure("evenrow_bold", background=self.g_var.tbl_style['row_even'], font=('Arial', 11, 'bold'))
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                tbl.delete(*tbl.get_children())
                
                if content == "customers":
                    tmp_cur_pts = {}
                    for item in data[0]:
                        tmp_cur_pts[item['id']] = 0
                    for item in data[1]:
                        tmp_cur_pts[item['id']] += item['sum']
                    for item in data[2]:
                        tmp_cur_pts[item['id']] -= item['sum']
                    
                    data = data[0]
                elif content == "billings":
                    tmp_amt_due = {}
                    for item in data[1]:
                        if item['sum'] == None:
                            tmp_amt_due[item['id']] = 0
                        else:
                            tmp_amt_due[item['id']] = item['sum']

                    data = data[0]

                elif content == "logistics":
                    riders_list = {}
                    self.g_var.riders_arr = []
                    self.g_var.riders_list = []
                    self.g_var.riders_ids = {}
                    i = 0
                    for item in data[1]:

                        riders_list[item['id']] = f"{item['first_name']} {item['last_name']}"
                        self.g_var.riders_arr.insert(i, {'id':item['id'], 'name':riders_list[item['id']], 'addr':item['address'], 'status':item['status']})
                        self.g_var.riders_list.insert(i, riders_list[item['id']])
                        self.g_var.riders_ids[item['id']] = i
                        i+=1

                    data = data[0]

                tmp_ind = 0
                for item in data:
                    if tmp_ind % 2 == 0:
                        tags_indc = "oddrow"
                    else:
                        tags_indc = "evenrow"

                    if content == "bookings":
                        self.g_var.tbl_data[item['id']] = item
                        
                        try:
                            if self.g_var.booking_ntfy_list[item['id']] == "unread":
                                tags_indc = f"{tags_indc}_bold"
                        except:
                            pass
                        
                        tbl.insert('', 'end', text="", values=(item['id'], self.format_std_code("QLH", str(item['id']), 6), item['client'], item['contact'], item['quantity'], item['status']), tags=(tags_indc,))
                    elif content == "services":
                        self.g_var.tbl_data[item['id']] = item
                        tbl.insert('', 'end', text="", values=(item['id'], self.g_var.prod_type_arr[item['prod_type']], item['title'], item['description'], item['price'], item['quantity'], item['unit']), tags=(tags_indc,))
                    elif content == "addons":
                        self.g_var.tbl_data[item['id']] = item
                        tbl.insert('', 'end', text="", values=(item['id'], item['title'], item['description'], item['price']), tags=(tags_indc,))
                    elif content == "rewards":
                        self.g_var.tbl_data[item['id']] = item
                        tbl.insert('', 'end', text="", values=(item['id'], item['title'], item['description'], item['pts_req'], item['status']), tags=(tags_indc,))
                    elif content == "billings":
                        self.g_var.tbl_data[item['id']] = item
                        tbl.insert('', 'end', text="", values=(item['id'], self.format_std_code("QLH", str(item['booking_id']), 6), item['client'], "{:.2f}".format((float(tmp_amt_due[item['id']])+float(item['logistics_fee']))), "{:.2f}".format(float(item['amount'])), item['mode'], item['ref_num']), tags=(tags_indc,))
                    elif content == "messages":
                        self.g_var.tbl_data[item['id']] = item
                        try:
                            if self.g_var.message_ntfy_list[str(item['id'])] == "unread":
                                tags_indc = f"{tags_indc}_bold"
                        except:
                            pass
                        tbl.insert('', 'end', text="", values=(item['id'], self.format_std_code("QLH", str(item['id']), 6), f"{item['first_name']} {item['last_name']}"), tags=(tags_indc,))
                    elif content == "customers":
                        self.g_var.tbl_data[item['id']] = item
                        tbl.insert('', 'end', text="", values=(item['id'], f"{item['first_name']} {item['last_name']}", f"{item['address']}", tmp_cur_pts[item['id']], f"{item['status']}"), tags=(tags_indc,))
                    elif content == "riders":
                        self.g_var.tbl_data[item['id']] = item
                        tbl.insert('', 'end', text="", values=(item['id'], f"{item['first_name']} {item['last_name']}", f"{item['address']}", f"{item['status']}"), tags=(tags_indc,))
                    elif content == "logistics":
                        try:
                            tmp_rider = riders_list[item['rider_id']]
                        except:
                            tmp_rider = ""

                        try:
                            if self.g_var.logistics_ntfy_list[item['id']] == "unread":
                                tags_indc = f"{tags_indc}_bold"
                        except:
                            pass

                        self.g_var.tbl_data[item['id']] = item
                        if item['client'] != None:
                            tbl.insert('', 'end', text="", values=(item['id'], self.format_std_code("QLH", str(item['booking_id']), 6), f"{item['client']}", f"{item['pickup_loc']}", f"{item['task_type']}", tmp_rider, f"{item['status']}"), tags=(tags_indc,))

                    tmp_ind += 1

            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def reload_table_content(self):
        self.load_request_data(self.g_var.url, self.g_var.tbl, self.g_var.content)

    def load_billing_data(self, url, bill_data):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response
                service_data = []
                addon_data = []
                serv_ind = 0
                adon_ind = 0
                # for item in data:
                #     #print(item)
                #     ind = f"{item['prod_type']}-{item['service_id']}"
                #     try:
                #         service_data.insert(serv_ind, {
                #             'name':self.g_var.services_arr[ind]['name'], 
                #             'price':self.g_var.services_arr[ind]['price'], 
                #             'qty':self.g_var.services_arr[ind]['qty'], 
                #             'unit':self.g_var.services_arr[ind]['unit'], 
                #             'net_qty':item['quantity'],
                #             'net_unit':item['unit']
                #         })
                #         serv_ind+=1
                #     except:
                #         addon_data.insert(adon_ind, {
                #             'name':self.g_var.addons_arr[ind]['name'], 
                #             'price':self.g_var.addons_arr[ind]['price']
                #         })
                #         adon_ind+=1
                
                # gen_docs.generate_customer_billing(bill_data, service_data, addon_data)
                gen_docs.generate_customer_billing(bill_data, data[1])
                #gen_docs.generate_customer_billing(data[0], data[1])
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def load_admin_messages(self, tbl, url): 
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # tbl.tag_configure("oddrow", background=self.g_var.tbl_style['row_odd'])
                # tbl.tag_configure("evenrow", background=self.g_var.tbl_style['row_even'])
                data = response.json()  # Parse the JSON response
                
                tbl.config(state="normal")
                tbl.delete('1.0', tk.END)
                tbl.tag_config("client", foreground="black", font=("Arial", 12), justify="left")
                tbl.tag_config("admin", foreground="black", font=("Arial", 12), justify="right")
                tbl.tag_config("client_sender", foreground="green", font=("Arial", 10), justify="left")
                tbl.tag_config("admin_sender", foreground="blue", font=("Arial", 10), justify="right")
                tbl.tag_config("r_indent", rmargin=100, lmargin1=5)
                tbl.tag_config("l_indent", rmargin=5, lmargin1=100)
                i=0
                chat_msg = ""
                line_space = ""
                start = "1.0"
                add_ext = 0
                for item in data:
                    if i > 0:
                        line_space = "\n\n"
                        start = end
                        add_ext = 1.0

                    if item['sender_type'] == "client":
                        chat_msg = f"{line_space}[ {item['first_name']} : {item['timestamp']} ]\n{item['message']}"
                        tbl.insert(tk.END, chat_msg, "r_indent")
                        end = tbl.index('end')
                        tbl.tag_add('client', start, f"{int(float(end)-1.0)}.end")
                        tbl.tag_add('client_sender', start, f"{int(float(start)+add_ext)}.end")
                    elif item['sender_type'] == "rider":
                        chat_msg = f"{line_space}[ Rider : {item['timestamp']} ]\n{item['message']}"
                        tbl.insert(tk.END, chat_msg, "r_indent")
                        end = tbl.index('end')
                        tbl.tag_add('client', start, f"{int(float(end)-1.0)}.end")
                        tbl.tag_add('client_sender', start, f"{int(float(start)+add_ext)}.end")
                    else:
                        chat_msg = f"{line_space}[ {'Admin'} : {item['timestamp']} ]\n{item['message']}"
                        tbl.insert(tk.END, chat_msg, "l_indent")
                        end = tbl.index('end')
                        tbl.tag_add('admin', start, f"{int(float(end)-1.0)}.end")
                        tbl.tag_add('admin_sender', start, f"{int(float(start)+add_ext)}.end")

                    i+=1

                tbl.see(tk.END)
                tbl.config(state="disabled")

                # tbl.delete(*tbl.get_children())
                
                # tmp_ind = 0
                # for item in data:
                #     if tmp_ind % 2 == 0:
                #         tags_indc = "oddrow"
                #     else:
                #         tags_indc = "evenrow"

                #     if item['sender'] == '0':
                #         item['sender'] = "Admin"
                #     else:
                #         item['sender'] = "Client"
                #     tbl.insert('', 'end', text="", values=(item['message'], item['timestamp'], item['sender']), tags=(tags_indc,))

                #     tmp_ind += 1

            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def load_completed_bookings(self, url): 
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.g_var.g_comp_bookings = response.json()  # Parse the JSON response
                
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def load_completed_bookings2(self, url): 
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.g_var.g_comp_bookings2 = response.json()  # Parse the JSON response
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def what_fg(self, val):
        res = ImageColor.getcolor(val, 'RGB')
        sum = res[0]+res[1]+res[2]
        if sum < 255:
            return "#FFFFFF"
        else:
            return "#000000"

    def global_styling(self, g_var, style):
        bgc = g_var.tbl_style['h_bg']
        fgc = g_var.tbl_style['h_fg']
        
        style.theme_use("alt")
        style.configure("Treeview.Heading", background=bgc, foreground=fgc, font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.map("Treeview.Heading", 
                        background=[('active', g_var.tbl_style['hl_bg'])],
                        foreground=[('active', g_var.tbl_style['hl_fg'])]
        )

        style.configure("TCombobox", 
                        fieldbackground=g_var.cbox_style['f_bg'], 
                        foreground=self.what_fg(g_var.cbox_style['bg']),
                        #selectbackground=g_var.scroll_style['btn_bg'], 
                        #selectforeground=self.what_fg(g_var.cbox_style['f_bg']),
                        background=g_var.scroll_style['btn_bg'], 
                        arrowcolor=g_var.scroll_style['arw']
        )
        style.map("TCombobox", 
                        background=[('active', g_var.scroll_style['btn_bg'])],
                        arrowcolor=[('active', g_var.scroll_style['arw'])]
        )
        
        style.configure("vertical", background=g_var.scroll_style['btn_bg'], arrowcolor=g_var.scroll_style['arw'], troughcolor=g_var.scroll_style['bg'])
        
        style.configure("Vertical.TScrollbar", 
                        background=g_var.scroll_style['btn_bg'], 
                        arrowcolor=g_var.scroll_style['arw'], 
                        troughcolor=g_var.scroll_style['bg']
        )
        style.map("Vertical.TScrollbar", 
                        background=[('disabled', g_var.scroll_style['btn_bg'])]
        )
        style.configure("Horizontal.TScrollbar", 
                        background=g_var.scroll_style['btn_bg'], 
                        arrowcolor=g_var.scroll_style['arw'], 
                        troughcolor=g_var.scroll_style['bg']
        )
        style.map("Horizontal.TScrollbar", 
                        background=[('disabled', g_var.scroll_style['btn_bg'])]
        )
    def get_sched_dates(self):
        day_ind = {'Sunday':0,'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6}
        day_names = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
        day_list = {}
        cur_dt = datetime.now()
        start_dec = day_ind[cur_dt.strftime("%A")]*86400
        #print(cur_dt)

        tmp_arr = str(cur_dt).split(" ")
        tmp_dt = (tmp_arr[0]).split("-")
        #print(tmp_dt)

        given_datetime = datetime(int(tmp_dt[0]), int(tmp_dt[1]), int(tmp_dt[2]))
        timestamp = given_datetime.timestamp()-86400
        #print(f"Datetime object: {timestamp}")

        i=0
        for i in range(7):
            timestamp = timestamp+86400
            dt_object_local = datetime.fromtimestamp(timestamp)
            day_list[dt_object_local.strftime("%A")] = f"{dt_object_local.strftime("%B")} {dt_object_local.strftime("%d")}, {dt_object_local.strftime("%Y")}"
            #day_list[dt_object_local.strftime("%A")] = (str(dt_object_local).split(" "))[0]
        
        return day_list
    
    def format_checkbox_value(self, cnd, val):
        if cnd == "opt_hr":
            if val == 1:
                return "open"
            else:
                return "closed"
            
    def format_cbox_time_value(self, val):
        arr = val.split("-")

        return arr
    
    def update_request_data(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.g_var.headers)
            if response.status_code == 200:
                #print(response.json())
                if data['data']['timestamp'] == "":
                    self.reload_table_content()
                else:
                    self.load_admin_messages(self.g_var.threads_msg_table, self.g_var.g_host+f"get_thread_messages_admin/{self.g_var.thread_id}")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    def update_data(self, tbl, target):
        if target == "threads" or target == "thread_msg":
            cur_item = tbl.item(tbl.focus())
            if cur_item['values'] != "":
                if target == "threads":
                    tmp_tid = cur_item['values'][0]
                    tmp_sender = ""
                    tmp_tstamp = ""
                elif target == "thread_msg":
                    tmp_tid = self.g_var.thread_id
                    tmp_sender = "0"
                    tmp_tstamp = cur_item['values'][1]
                    
                data = {
                    'tok':self.g_var.app_token,
                    'act':"Delete",
                    'data':{'thread_id':tmp_tid, 'sender':tmp_sender, "timestamp":tmp_tstamp}
                }

                #if (target == "thread_msg" and cur_item['values'][2] != "") or target == "threads":
                self.update_request_data(self.g_var.g_host+"mod_tbl_threads", data)
                
            else:
                messagebox.showinfo("Notice", "Select a table enrty first!")
                
    def update_buttons_indc(self, obj, type, ctr):
        if type == "bookings":
            if ctr == 0:
                obj.config(text=f"Bookings")
            else:
                obj.config(text=f"Bookings ({ctr})")
        elif type == "messages":
            if ctr == 0:
                obj.config(text=f"Messages")
            else:
                obj.config(text=f"Messages ({ctr})")
        elif type == "logistics":
            if ctr == 0:
                obj.config(text=f"Logistics")
            else:
                obj.config(text=f"Logistics ({ctr})")
        
    def format_12hr(self, val):
        arr = val.split(' ')
        sub_arr = arr[1].split(':')
        if int(sub_arr[0]) == 0:
            sub_arr[0] = int(sub_arr[0])+12
            arr[1] = f"{sub_arr[0]}:{sub_arr[1]}:{sub_arr[2]}am"
        elif int(sub_arr[0]) > 12:
            sub_arr[0] = int(sub_arr[0])-12
            arr[1] = f"{sub_arr[0]}:{sub_arr[1]}:{sub_arr[2]}pm"
        else:
            arr[1] = f"{sub_arr[0]}:{sub_arr[1]}:{sub_arr[2]}am"

        return f"{arr[0]} {arr[1]}"
        

    def format_day_num(self, val):
        if val == 0:
            return ""
        else:
            return val

    def chart_generator(self, holder, month, week, year, filter):
        tmp_mm = int(self.g_var.months.index(month.get()))+1
        tmp_tdays = self.get_days_in_month(int(year.get()), tmp_mm)

        i=1
        wk_beg = int(tmp_tdays[0])
        wk_cnt = 1
        self.g_var.wk_set_arr[wk_cnt] = [0,0,0,0,0,0,0]

        for i in range(int(tmp_tdays[1])+1):
            self.g_var.wk_set_arr[wk_cnt][wk_beg] = i
            if wk_beg == 6:
                wk_cnt+=1
                wk_beg = 0
                self.g_var.wk_set_arr[wk_cnt] = [0,0,0,0,0,0,0]
            else:
                wk_beg+=1
            i+=1

        x_label = month.get()
        if filter != "week":
            i = 0
            self.g_var.wk_arr = []
            for i in range(wk_cnt+1):
                if i == 0:
                    self.g_var.wk_arr.insert(i, f"All")
                else:
                    self.g_var.wk_arr.insert(i, f"Week {i}")
                i+=1

            week.config(values = self.g_var.wk_arr)


        #print(self.g_var.wk_set_arr)
        
        wk_ind = self.g_var.wk_arr.index(week.get())
        if wk_ind == 0:
            x_label = f"{month.get()} 1 - {tmp_tdays[1]}"

            days_label = self.g_var.days_short
            filter_report = (f"{year.get()}-{tmp_mm}-01", f"{year.get()}-{tmp_mm}-{self.format_std_code("",str(tmp_tdays[1]),2)}")
        else:
            start_ind = self.g_var.wk_set_arr[wk_ind][0]
            end_ind = self.g_var.wk_set_arr[wk_ind][6]
            if wk_ind == 1:
                start_ind = self.g_var.wk_set_arr[wk_ind][int(tmp_tdays[0])+1]
            elif wk_ind == len(self.g_var.wk_arr)-1:
                end_ind = tmp_tdays[1]

            days_label = [
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][0])} Sun",
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][1])} Mon",
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][2])} Tue",
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][3])} Wed",
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][4])} Thu",
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][5])} Fri",
                f"{self.format_day_num(self.g_var.wk_set_arr[wk_ind][6])} Sat"
            ]
            
            x_label = f"{month.get()} {start_ind} - {end_ind}"
            
            filter_report = (f"{year.get()}-{tmp_mm}-{self.format_std_code("",str(start_ind),2)}", f"{year.get()}-{tmp_mm}-{self.format_std_code("",str(end_ind),2)}")
        
        self.load_completed_bookings(self.g_var.g_host+'get_all_bookings/{"key":"'+self.g_var.app_token+'","point_a":"'+filter_report[0]+'","point_b":"'+filter_report[1]+'"}')
        self.load_completed_bookings2(self.g_var.g_host+'get_completed_bookings/{"key":"'+self.g_var.app_token+'","point_a":"'+filter_report[0]+'","point_b":"'+filter_report[1]+'"}')
        #print(self.g_var.g_comp_bookings)
        self.g_var.g_export_filename = x_label

        months_data = []
        for item in self.g_var.g_comp_bookings2:
            item['sched'] = (item['sched'].split(" "))[0]
            time_arr = self.format_cbox_time_value(item['sched'])
            date_object = datetime(int(time_arr[0]),int(time_arr[1]),int(time_arr[2]))
            full_month_name = date_object.strftime("%B")
            
            try:
                self.months_ctr[full_month_name] += 1
            except:
                self.months_ctr[full_month_name] = 1

            if self.months_ctr['highest'] < self.months_ctr[full_month_name]:
                self.months_ctr['highest'] = self.months_ctr[full_month_name]
        
        i=0
        for i in range(len(self.g_var.months)):
            months_data.insert(i, self.months_ctr[self.g_var.months[i]])
        
        days_data = []
        for item in self.g_var.g_comp_bookings2:
            try:
                self.days_ctr[item['schedule']] += 1
            except:
                self.days_ctr[item['schedule']] = 1

            if self.days_ctr['highest'] < self.days_ctr[item['schedule']]:
                self.days_ctr['highest'] = self.days_ctr[item['schedule']]

        i=0
        for i in range(len(self.g_var.days)):
            days_data.insert(i, self.days_ctr[self.g_var.days[i]])

        fig = Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # ypoints = np.array(sales_data)
        # ax.plot(self.g_var.months_short, ypoints, color = 'skyblue')
        from matplotlib.ticker import FormatStrFormatter

        ax.set_title(f'({x_label}) Reports')
        ax.set_ylabel(f'{len(self.g_var.g_comp_bookings2)} Rendered Services')
        ax.set_xlabel("")
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        
        # if month.get() == "Months":
        #     ax.set_ylim(0, self.months_ctr['highest']+5)
        #     ax.bar(self.g_var.months_short, months_data, color='skyblue')
        # else:
        ax.set_ylim(0, self.days_ctr['highest']+5)
        ax.bar(days_label, days_data, color='skyblue')
            
        ax.tick_params(axis='x', rotation=35)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=holder)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10,10))
        canvas.draw()

        file_path = "assets/images/"+self.g_var.g_export_filename+" Reports.png"  # Specify the desired file path and format
        fig.savefig(file_path, dpi=500)