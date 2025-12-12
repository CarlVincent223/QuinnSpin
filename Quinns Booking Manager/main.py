import sqlite3
import subprocess
import requests, threading, time, platform, os, shutil, math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk 
from tkinter import filedialog
from PIL import Image, ImageTk
import xlsxwriter

from datetime import date
from global_var import g_var
from display_class import obj_dsp_class
dsp_con = obj_dsp_class(g_var)
from assist_class import processor_mthd
assist_con = processor_mthd(g_var)
from popup_class import multi_popup_class
popup_con = multi_popup_class(g_var)
from db_class import strg_class

def exit_application():
    if messagebox.askyesno(message="Are you sure, do you want to exit the application?", icon='question', title="Terminate System"):
        root.destroy()
        try:
            subprocess.call("TASKKILL /F /IM App_Manager.exe", shell=True)
        except:
            pass

def make_cbox(holder, x, y, w, val_list, font, state):
    cb_var = tk.StringVar()
    combo_box = ttk.Combobox(holder, textvariable=cb_var, state=state, values=val_list, font=font)
    combo_box.place(x=x, y=y, width=w)
        
    return combo_box

def make_label(holder, x, y, w, text, font, bg, fg, anch):
    lbl = tk.Label(holder, text=text, bg=bg, fg=fg, font=font, anchor=anch)
    lbl.place(x=x, y=y, width=w)

    return lbl

def update_request_data(url, data):
    try:
        response = requests.post(url, json=data, headers=g_var.headers)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            if data == "valid":
                messagebox.showinfo("Notice", "Update complete.")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def print_billing(tbl):
    values = tbl.item(tbl.focus())
    if values['values'] != "":
        #print(g_var.tbl_data)
        #print(g_var.tbl_data[values['values'][0]])

        response = requests.get(g_var.g_host+'get_shop')
        shop_details = (response.json())[0]
        
        ind = values['values'][0]
        bill_data = [
            {0:'shop_name',1:shop_details['shop_name']},
            {0:'owner',1:shop_details['owner']},
            {0:'tin',1:shop_details['tin']},
            {0:'shop_address',1:shop_details['address']},
            {0:'shop_contact',1:shop_details['contact']},
            {0:'fb_page',1:shop_details['fb_page']},
            {0:'booking_id',1:values['values'][1]},
            {0:'date',1:assist_con.get_datetime()},
            {0:'client',1:g_var.tbl_data[ind]['client']},
            {0:'contact',1:g_var.tbl_data[ind]['contact']},
            {0:'address',1:g_var.tbl_data[ind]['pickup_loc']},
            {0:'logistics',1:g_var.tbl_data[ind]['logistics_fee']},
            {0:'quantity',1:g_var.tbl_data[ind]['basket_qty']}
        ]
        # gen_docs.generate_customer_billing(bill_data)
        #print(g_var.tbl_data[ind])
        assist_con.load_billing_data(f"{g_var.g_host}get_billing_payments/{values['values'][0]}", bill_data)

def page_action(cmd, type, tbl):
    if type == "Add":
        if g_var.popup_on == False:
            if cmd == "rewards":
                g_var.popup_on = True
                popup_con.form_global_popup(cmd, type, {'id':"",'title':"",'description':"",'pts_req':"",'status':"Active"}, "")
            elif cmd == "services":
                popup_con.form_global_popup(cmd, type, {'id':"auto",'title':"",'description':"",'price':"",'quantity':"",'unit':"",'prod_type':"service",'status':"Active"}, "")
            elif cmd == "addons":
                popup_con.form_global_popup(cmd, type, {'id':"auto",'title':"",'description':"",'price':"",'quantity':"",'unit':"",'prod_type':"addon",'status':"Active"}, "")
            elif cmd == "riders":
                popup_con.form_global_popup(cmd, type, {'id':"auto",'user_name':"",'password':"",'first_name':"",'last_name':"",'address':"",'mobile_no':"",'status':"Active"}, "")

        else:
            g_var.push_popup_front()

    elif type == "Delete":
        values = tbl.item(tbl.focus())
        if cmd == "rewards" and values['values'] != "":
            if messagebox.askyesno(message=f"Are you sure you want to delete {values['values'][1]}?", icon='question', title="Confirm"):
                popup_con.update_request_data(g_var.g_host+"mod_tbl_rewards", {'tok':g_var.app_token, 'act':type, 'data':{'id':values['values'][0]}})
        elif cmd == "bookings" and values['values'] != "":
            if messagebox.askyesno(message=f"Are you sure you want to delete {values['values'][1]}?", icon='question', title="Confirm"):
                popup_con.update_request_data(g_var.g_host+"mod_tbl_bookings", {'tok':g_var.app_token, 'act':type, 'data':{'booking_id':values['values'][0]}, 'items':''})
        elif (cmd == "services" or cmd == "addons") and values['values'] != "":
            if messagebox.askyesno(message=f"Are you sure you want to delete {values['values'][2]} ({values['values'][1]})?", icon='question', title="Confirm"):
                popup_con.update_request_data(g_var.g_host+"mod_tbl_products", {'tok':g_var.app_token, 'act':type, 'data':{'id':values['values'][0]}})
        elif cmd == "customers" and values['values'] != "":
            if messagebox.askyesno(message=f"Are you sure you want to delete {values['values'][1]}?", icon='question', title="Confirm"):
                popup_con.update_request_data(g_var.g_host+"mod_tbl_users", {'tok':g_var.app_token, 'act':type, 'data':{'id':values['values'][0]}})
        elif cmd == "riders" and values['values'] != "":
            if messagebox.askyesno(message=f"Are you sure you want to delete {values['values'][1]}?", icon='question', title="Confirm"):
                popup_con.update_request_data(g_var.g_host+"mod_tbl_riders", {'tok':g_var.app_token, 'act':type, 'data':{'id':values['values'][0]}})

    elif type == "Reply":
        if g_var.popup_on == False:
            children = g_var.threads_msg_table.get_children()
            if children:
                g_var.popup_on = True
                g_var.threads_msg_table.focus(children[0])
                g_var.threads_msg_table.selection_set(children[0])
                cur_item = g_var.threads_msg_table.item(g_var.threads_msg_table.focus())
                popup_con.form_global_chatbox(cur_item['values'])
        else:
            g_var.push_popup_front()

    elif type == "Refresh Messages":
        open_page(g_var.cur_page)

    elif type == "Save":
        if cmd == "shop":
            data = {
                'tok':g_var.app_token,
                'shop_name':f"{tbl['shop_name'].get()}",
                'owner':f"{tbl['owner'].get()}",
                'tin':f"{tbl['tin'].get()}",
                'address':f"{(tbl['address'].get("1.0", tk.END)).strip()}",
                'contact':f"{tbl['contact'].get()}",
                'fb_page':f"{tbl['fb_page'].get()}",
                'logistics':f"{tbl['logistics'].get()}",
                'free_threshold':f"{tbl['free_threshold'].get()}",
                'sunday':f"{tbl['sun_beg'].get()}-{tbl['sun_end'].get()}",
                'monday':f"{tbl['mon_beg'].get()}-{tbl['mon_end'].get()}",
                'tuesday':f"{tbl['tue_beg'].get()}-{tbl['tue_end'].get()}",
                'wednesday':f"{tbl['wed_beg'].get()}-{tbl['wed_end'].get()}",
                'thursday':f"{tbl['thu_beg'].get()}-{tbl['thu_end'].get()}",
                'friday':f"{tbl['fri_beg'].get()}-{tbl['fri_end'].get()}",  
                'saturday':f"{tbl['sat_beg'].get()}-{tbl['sat_end'].get()}"
            }
            
            update_request_data(g_var.g_host+"mod_tbl_shop", {'tok':g_var.app_token, 'act':type, 'data':data})

            tmp_uname = tbl['uname'].get()
            tmp_upass = tbl['upass'].get()
            if tmp_uname != "" and tmp_upass.strip() != "":
                tmp_upass = assist_con.get_hash_value(tmp_upass)
                g_var.db_con.update_admin_data("tbl_system", f"user_name='{tmp_uname}', password='{tmp_upass}'", "1")
                tbl['upass'].delete(0, tk.END)
    else:
        if g_var.popup_on == False:
            values = tbl.item(tbl.focus())
            if values['values'] != "":
                g_var.popup_on = True

                try:
                    try:
                        del g_var.booking_ntfy_list[int(values['values'][0])]
                    except:
                        del g_var.booking_ntfy_list[values['values'][0]]

                    assist_con.update_buttons_indc(btn_mng_book, "bookings", len(g_var.booking_ntfy_list))

                    selected_item = tbl.selection()[0]

                    if tbl.index(selected_item)%2 == 1:
                        tbl.item(selected_item, text="blub", tags="evenrow")
                    else:
                        tbl.item(selected_item, text="blub", tags="oddrow")

                except:
                    pass

                try:
                    del g_var.logistics_ntfy_list[int(values['values'][0])]
                    assist_con.update_buttons_indc(btn_logistics, "logistics", len(g_var.logistics_ntfy_list))

                    selected_item = tbl.selection()[0]

                    if tbl.index(selected_item)%2 == 1:
                        tbl.item(selected_item, text="blub", tags="evenrow")
                    else:
                        tbl.item(selected_item, text="blub", tags="oddrow")

                except:
                    pass
                
                popup_con.form_global_popup(cmd, type, g_var.tbl_data[values['values'][0]], values['values'])
        else:
            g_var.push_popup_front()

def open_threads(event):
    row_id = event.widget.identify_row(event.y)
    col_id = event.widget.identify_column(event.x)
    target_click = event.widget.identify("region", event.x, event.y)

    if target_click == "cell":
        cur_item = event.widget.item(event.widget.focus())
        g_var.thread_id = cur_item['values'][0]

        try:
            del g_var.message_ntfy_list[str(g_var.thread_id)]
            assist_con.update_buttons_indc(btn_mng_msg, "messages", len(g_var.message_ntfy_list))

            selected_item = g_var.threads_table.selection()[0]

            if g_var.threads_table.index(selected_item)%2 == 1:
                g_var.threads_table.item(selected_item, text="blub", tags="evenrow")
            else:
                g_var.threads_table.item(selected_item, text="blub", tags="oddrow")

        except:
            pass

        g_var.threads_frame.config(text=f"{cur_item['values'][1]} Thread Messages")
        assist_con.load_admin_messages(g_var.threads_msg_table, g_var.g_host+f"get_thread_messages_admin/{cur_item['values'][0]}")

def open_chat_box(event):
    if g_var.popup_on == False:
        row_id = event.widget.identify_row(event.y)
        col_id = event.widget.identify_column(event.x)
        target_click = event.widget.identify("region", event.x, event.y)

        if target_click == "cell":
            g_var.popup_on = True
            cur_item = event.widget.item(event.widget.focus())
            popup_con.form_global_chatbox(cur_item['values'])
    else:
        g_var.push_popup_front()

def init_open_page(cnd):
    if g_var.popup_on == False:
        open_page(cnd)
    else:
        g_var.push_popup_front()

def open_page(cnd):
    try:
        bookings_table = ""
        content.place_forget()
    except:
        pass
    
    

    content_col = 5
    content = tk.Frame(root, bg=g_bgc, relief=tk.FLAT, bd=2, padx=math.ceil(app_w*.01))
    content.columnconfigure(0, minsize=math.ceil(app_w*.15), weight=1)
    content.columnconfigure(1, minsize=math.ceil(app_w*.23), weight=1)
    content.columnconfigure(2, minsize=math.ceil(app_w*.15), weight=1)
    content.columnconfigure(3, minsize=math.ceil(app_w*.15), weight=1)
    content.columnconfigure(4, minsize=math.ceil(app_w*.15), weight=1)
    content.rowconfigure(0, minsize=math.ceil(app_h*.05), weight=1)
    content.rowconfigure(1, minsize=math.ceil(app_h*.67), weight=1)
    content.rowconfigure(2, minsize=math.ceil(app_h*.18), weight=1)
    content.rowconfigure(3, minsize=math.ceil(app_h*.07), weight=1)
    g_var.g_content = content
    
    content_w = app_w*.83
    btn_padx = (10,0)

    if cnd != "logout":
        g_var.cur_page = cnd
        btn_mng_book.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_serv.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_addn.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_rwrd.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_bill.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_msg.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_cust.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_reports.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_logistics.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_riders.config(bg=g_bgc, fg=btn_dfgc, state="normal")
        btn_mng_shop.config(bg=g_bgc, fg=btn_dfgc, state="normal")
    btn_logout.config(bg=g_bgc, fg=btn_dfgc, state="normal")
    
    if cnd == "bookings":
        btn_mng_book.config(image=icon_book)
        lbl_bok.config(text=f"Bookings")
        btn_mng_book.config(bg=btn_bgc, fg=btn_fgc)
        bookings_table = dsp_con.layout_manage_bookings(content, content_w, app_h, 1, content_col, g_var)
        bookings_table.tag_configure('evenrow', background='lightblue') 
        assist_con.load_request_data(g_var.g_host+"active_bookings", bookings_table, cnd)
        assist_con.load_resource_data(g_var.g_host+"get_products/all", "products")

        icon = create_button_icon(content, "assets/images/delete_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:page_action(cnd, "Delete", bookings_table))
        btn3.grid(row=3, column=0, padx=btn_padx, pady=5, sticky="ws")
        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", bookings_table))
        btn1.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")
        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", bookings_table))
        btn2.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")
    
    elif cnd == "services":
        btn_mng_serv.config(bg=btn_bgc, fg=btn_fgc)
        bookings_table = dsp_con.layout_manage_services(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"get_products/"+cnd, bookings_table, cnd)

        icon = create_button_icon(content, "assets/images/delete_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:page_action(cnd, "Delete", bookings_table))
        btn1.grid(row=3, column=0, padx=btn_padx, pady=5, sticky="ws")
        
        icon = create_button_icon(content, "assets/images/add_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Add", font=("Arial", 12), command=lambda:page_action(cnd, "Add", bookings_table))
        btn2.grid(row=3, column=2, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", bookings_table))
        btn3.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn4 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", bookings_table))
        btn4.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "addons":
        btn_mng_addn.config(bg=btn_bgc, fg=btn_fgc)
        bookings_table = dsp_con.layout_manage_addons(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"get_products/"+cnd, bookings_table, cnd)

        icon = create_button_icon(content, "assets/images/delete_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:page_action(cnd, "Delete", bookings_table))
        btn1.grid(row=3, column=0, padx=btn_padx, pady=5, sticky="ws")
        
        icon = create_button_icon(content, "assets/images/add_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Add", font=("Arial", 12), command=lambda:page_action(cnd, "Add", bookings_table))
        btn2.grid(row=3, column=2, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", bookings_table))
        btn3.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn4 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", bookings_table))
        btn4.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "rewards":
        btn_mng_rwrd.config(bg=btn_bgc, fg=btn_fgc)
        bookings_table = dsp_con.layout_manage_rewards(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"get_rewards_list", bookings_table, cnd)

        icon = create_button_icon(content, "assets/images/delete_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:page_action(cnd, "Delete", bookings_table))
        btn1.grid(row=3, column=0, padx=btn_padx, pady=5, sticky="ws")
        
        icon = create_button_icon(content, "assets/images/add_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Add", font=("Arial", 12), command=lambda:page_action(cnd, "Add", bookings_table))
        btn2.grid(row=3, column=2, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", bookings_table))
        btn3.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn4 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", bookings_table))
        btn4.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")
    
    elif cnd == "billings":
        btn_mng_bill.config(bg=btn_bgc, fg=btn_fgc)
        g_var.tbl = dsp_con.layout_manage_billings(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"get_billing_payments/All", g_var.tbl, cnd)

        g_var.g_cbox['filter'] = make_cbox(content, app_w*.73, app_h*.02, app_w*.1, ('All', 'Unpaid', 'Paid'), ('Arial', 12), "readonly")
        g_var.g_cbox['filter'].set('All')
        g_var.g_cbox['filter'].bind("<<ComboboxSelected>>", set_billing_filter)

        icon = create_button_icon(content, "assets/images/print_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Print", font=("Arial", 12), command=lambda:print_billing(g_var.tbl))
        btn1.grid(row=3, column=2, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", g_var.tbl))
        btn2.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", g_var.tbl))
        btn3.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "messages":
        btn_mng_msg.config(image=icon_msg)
        lbl_msg.config(text=f"Messages")
        btn_mng_msg.config(bg=btn_bgc, fg=btn_fgc)
        temp_res = dsp_con.layout_manage_messages(content, content_w, app_h, 1, content_col, g_var)
        g_var.threads_table = temp_res[0]
        g_var.threads_msg_table = temp_res[1]
        assist_con.load_request_data(g_var.g_host+f"get_threads_admin", g_var.threads_table, cnd)
        g_var.threads_table.bind("<Double-1>", open_threads)
        #g_var.threads_msg_table.bind("<Double-1>", open_chat_box)

        icon = create_button_icon(content, "assets/images/refresh_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Refresh", font=("Arial", 12), command=lambda:page_action(cnd, "Refresh Messages", ""))
        btn3.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

        # icon = create_button_icon(content, "assets/images/reply_button.png", 115, 40)
        # btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Reply", font=("Arial", 12), command=lambda:page_action(cnd, "Reply", ""))
        # btn3.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")
    
    elif cnd == "customers":
        btn_mng_cust.config(bg=btn_bgc, fg=btn_fgc)
        bookings_table = dsp_con.layout_manage_customers(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"users/all", bookings_table, cnd)

        icon = create_button_icon(content, "assets/images/delete_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:page_action(cnd, "Delete", bookings_table))
        btn1.grid(row=3, column=0, padx=btn_padx, pady=5, sticky="ws")

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", bookings_table))
        btn1.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", bookings_table))
        btn2.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "reports":
        cur_dt = assist_con.get_default_dt()
        full_month_name = cur_dt.strftime("%B")

        lbl = make_label(content, app_w*.32, app_h*.03, app_w*.15, "Coverage", ('Arial', 12), g_bgc, g_fgc, 'e')
        g_var.g_cbox['months'] = make_cbox(content, app_w*.48, app_h*.03, app_w*.15, g_var.months, ('Arial', 12), "readonly")
        g_var.g_cbox['months'].set(full_month_name)
        g_var.g_cbox['months'].bind("<<ComboboxSelected>>", set_chart_month_filter)
        g_var.g_cbox['weeks'] = make_cbox(content, app_w*.64, app_h*.03, app_w*.1, ('All','Week 1','Week 2','Week 3','Week 4'), ('Arial', 12), "readonly")
        g_var.g_cbox['weeks'].set("All")
        g_var.g_cbox['weeks'].bind("<<ComboboxSelected>>", set_chart_week_filter)
        g_var.g_cbox['year'] = make_cbox(content, app_w*.75, app_h*.03, app_w*.075, g_var.year_range, ('Arial', 12), "readonly")
        g_var.g_cbox['year'].set(cur_dt.strftime("%Y"))
        g_var.g_cbox['year'].bind("<<ComboboxSelected>>", set_chart_yr_filter)

        btn_reports.config(bg=btn_bgc, fg=btn_fgc)
        dsp_con.layout_manage_reports(content, content_w, app_h, 1, content_col, g_var, '')

        icon = create_button_icon(content, "assets/images/export_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Export", font=("Arial", 12), command=lambda:export_report())
        btn1.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")
        
        icon = create_button_icon(content, "assets/images/download_button.png", 135, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Download", font=("Arial", 12), command=lambda:download_chart())
        btn2.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "logistics":
        btn_logistics.config(image=icon_logistics)
        lbl_logistics.config(text=f"Logistics")
        btn_logistics.config(bg=btn_bgc, fg=btn_fgc)
        g_var.tbl = dsp_con.layout_manage_logistics(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"get_rider_assigned/All", g_var.tbl, cnd)

        g_var.g_cbox['filter'] = make_cbox(content, app_w*.73, app_h*.02, app_w*.1, ('All', 'Pending', 'Assigned', 'Completed'), ('Arial', 12), "readonly")
        g_var.g_cbox['filter'].set('All')
        g_var.g_cbox['filter'].bind("<<ComboboxSelected>>", set_billing_filter)

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", g_var.tbl))
        btn2.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", g_var.tbl))
        btn3.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "riders":
        btn_riders.config(bg=btn_bgc, fg=btn_fgc)
        bookings_table = dsp_con.layout_manage_riders(content, content_w, app_h, 1, content_col, g_var)
        assist_con.load_request_data(g_var.g_host+"get_riders/all", bookings_table, cnd)

        icon = create_button_icon(content, "assets/images/delete_button.png", 115, 40)
        btn1 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Delete", font=("Arial", 12), command=lambda:page_action(cnd, "Delete", bookings_table))
        btn1.grid(row=3, column=0, padx=btn_padx, pady=5, sticky="ws")

        icon = create_button_icon(content, "assets/images/add_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Add", font=("Arial", 12), command=lambda:page_action(cnd, "Add", bookings_table))
        btn2.grid(row=3, column=2, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/update_button.png", 115, 40)
        btn3 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Update", font=("Arial", 12), command=lambda:page_action(cnd, "Update", bookings_table))
        btn3.grid(row=3, column=3, padx=btn_padx, pady=5, sticky="es")

        icon = create_button_icon(content, "assets/images/view_button.png", 115, 40)
        btn4 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="View", font=("Arial", 12), command=lambda:page_action(cnd, "View", bookings_table))
        btn4.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    elif cnd == "shop":
        shop_data = requests.get(g_var.g_host+'get_shop')
        shop_data = shop_data.json()
        btn_mng_shop.config(bg=btn_bgc, fg=btn_fgc)
        inp_shop_details = dsp_con.layout_manage_shop(content, content_w, app_h, 1, content_col, g_var, assist_con.get_sched_dates(), shop_data[0], shop_data[1], root)

        icon = create_button_icon(content, "assets/images/save_button.png", 115, 40)
        btn2 = tk.Button(content, bg=g_bgc, relief="flat", image=icon, anchor="center", text="Save", font=("Arial", 12), command=lambda:page_action(cnd, "Save", inp_shop_details))
        btn2.grid(row=3, column=4, padx=btn_padx, pady=5, sticky="es")

    if cnd == "logout":
        #btn_logout.config(bg=btn_bgc, fg=btn_fgc)
        if messagebox.askyesno(message="Are you sure, do you want to logout and exit the application?", icon='question', title="Terminate System"):
            g_var.db_con.update_admin_data("tbl_system", "cookie=0", "1")
            root.destroy()
            try:
                subprocess.call("TASKKILL /F /IM App_Manager.exe", shell=True)
            except:
                pass
    else:
        content.place(x=app_w*.15, y=0)
        root.update()
        # root.mainloop()

def export_report():   
    if len(g_var.g_comp_bookings2) > 0:
        source_file = "assets/docs/"+g_var.g_export_filename+" Reports.xlsx" 
        workbook = xlsxwriter.Workbook(source_file)
        worksheet = workbook.add_worksheet()   
        bold = workbook.add_format({'bold': 1})
        money_format = workbook.add_format({'num_format': '₱#,##0.00'})
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy hh:mm AM/PM'})
        
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 35)
        worksheet.set_column(4, 6, 15)
        worksheet.set_column(7, 7, 20)
        worksheet.set_column(8, 8, 15)
        
        row = 0
        worksheet.write(row, 0, "Booking ID", bold)
        worksheet.write(row, 1, "Client", bold)
        worksheet.write(row, 2, "Contact", bold)
        worksheet.write(row, 3, "Address", bold)
        worksheet.write(row, 4, "Day", bold)
        worksheet.write(row, 5, "Mode", bold)
        worksheet.write(row, 6, "Date", bold)
        worksheet.write(row, 7, "Service", bold)
        worksheet.write(row, 8, "Amount", bold)
        row = 1
        for item in g_var.g_comp_bookings2:
            worksheet.write(row, 0, assist_con.format_std_code("QLH", str(item['id']), 6))
            worksheet.write(row, 1, item['client'])
            worksheet.write(row, 2, item['contact'])
            worksheet.write(row, 3, item['pickup_loc'])
            worksheet.write(row, 4, item['schedule'])
            worksheet.write(row, 5, item['mode'])
            worksheet.write(row, 6, assist_con.format_12hr(item['completed']))
            worksheet.write(row, 7, item['title'])
            worksheet.write(row, 8, float(item['amount']), money_format) 
        #[{'amount': '470', 'client': 'Marlone Medina', 'contact': '09095767863', 'mode': 'Drop off', 'pickup_loc': 'Pacol, Naga City', 'sched': '2025-10-31', 'schedule': 'Friday', 'title': 'Heavy Loads'}]
            row += 1
        
        workbook.close()

        directory_path = filedialog.askdirectory(
            initialdir="/",
            title="Select a directory"
        )
        
        if directory_path:
            destination_path = os.path.join(directory_path, os.path.basename(source_file))
            shutil.move(source_file, destination_path)
            messagebox.showinfo("Success!", "The file succesfully exported to your desired location.")
    else:
        messagebox.showinfo("Notice", "There's nothing to export.")

def download_chart():
    if len(g_var.g_comp_bookings2) > 0:
        source_file = "assets/images/"+g_var.g_export_filename+" Reports.png" 
        
        directory_path = filedialog.askdirectory(
            initialdir="/",
            title="Select a directory"
        )
        
        if directory_path:
            destination_path = os.path.join(directory_path, os.path.basename(source_file))
            shutil.move(source_file, destination_path)
            messagebox.showinfo("Success!", "The file succesfully downloaded to your desired location.")
    else:
        messagebox.showinfo("Notice", "The chart is empty.")

def set_billing_filter(event):
    assist_con.load_request_data(g_var.g_host+"get_billing_payments/"+g_var.g_cbox['filter'].get(), g_var.tbl, "billings")

def set_chart_yr_filter(event):
    #print("Year")
    dsp_con.layout_manage_reports(g_var.g_content, app_w*.83, app_h, 1, 5, g_var, 'year')
        
def set_chart_month_filter(event):
    #print("Month")
    dsp_con.layout_manage_reports(g_var.g_content, app_w*.83, app_h, 1, 5, g_var, 'month')

def set_chart_week_filter(event):
    #print("Week")
    dsp_con.layout_manage_reports(g_var.g_content, app_w*.83, app_h, 1, 5, g_var, 'week')

def load_notification_data(url):   
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            try:
                i=0
                for i in range(len(data['bok'])):
                    g_var.booking_ntfy_list[data['bok'][i]] = "unread"
            except:
                pass

            try:
                i=0
                for i in range(len(data['can'])):
                    g_var.booking_ntfy_list[data['can'][i]] = "unread"
            except:
                pass
            
            try:
                i=0
                for i in range(len(data['msg'])): 
                    g_var.message_ntfy_list[data['msg'][i]] = "unread"   
            except:
                pass

            try:
                i=0
                for i in range(len(data['com'])): 
                    g_var.logistics_ntfy_list[data['com'][i]] = "unread"   
            except:
                pass
            
            if len(data['bok']) != 0 and len(data['msg']) != 0 and len(data['com']) != 0:
                messagebox.showinfo("Notice", "New booking(s) and Message(s) received!")
                #btn_mng_book.config(text=f"Bookings ({len(data[0])})")
                #btn_mng_msg.config(text=f"Messages ({len(data[1])})")
                lbl_bok.config(text=f"Bookings ({len(data['bok'])})")
                lbl_msg.config(text=f"Messages ({len(data['msg'])})")
                lbl_logistics.config(text=f"Logistics ({len(data['com'])})")
                btn_mng_book.config(image=icon_book_hl)
                btn_mng_msg.config(image=icon_msg_hl)
                btn_logistics.config(image=icon_logistics_hl)
                root.update()

                if g_var.cur_page == "bookings" or g_var.cur_page == "messages":
                    open_page(g_var.cur_page)

            elif len(data['bok']) != 0:
                messagebox.showinfo("Notice", "New booking received!")
                #btn_mng_book.config(text=f"Bookings ({len(data['bok'])})")
                lbl_bok.config(text=f"Bookings ({len(data['bok'])})")
                btn_mng_book.config(image=icon_book_hl)
                root.update()

                if g_var.cur_page == "bookings":
                    open_page(g_var.cur_page)

            elif len(data['can']) != 0:
                messagebox.showinfo("Notice", "Booking cancelled!")
                #btn_mng_book.config(text=f"Bookings ({len(data['bok'])})")
                lbl_bok.config(text=f"Bookings ({len(data['can'])})")
                btn_mng_book.config(image=icon_book_hl)
                root.update()

                if g_var.cur_page == "bookings":
                    open_page(g_var.cur_page)
                
            elif len(data['msg']) != 0:
                messagebox.showinfo("Notice", "New message received!")
                #btn_mng_msg.config(text=f"Messages ({len(data['msg'])})")
                lbl_msg.config(text=f"Messages ({len(data['msg'])})")
                btn_mng_msg.config(image=icon_msg_hl)
                root.update()

                if g_var.cur_page == "messages":
                    open_page(g_var.cur_page)
            
            elif len(data['com']) != 0:
                messagebox.showinfo("Notice", "New rider task completion received!")
                lbl_logistics.config(text=f"Logistics ({len(data['com'])})")
                btn_logistics.config(image=icon_logistics_hl)
                root.update()

                if g_var.cur_page == "logistics":
                    open_page(g_var.cur_page)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def check_messages():
    while True:
        time.sleep(10)
        load_notification_data(g_var.g_host+"get_admin_notifications")

def make_label(holder, x, y, w, text, font, bg, fg, anch):
    lbl = tk.Label(holder, text=text, bg=bg, fg=fg, font=font, anchor=anch)
    lbl.place(x=x, y=y, width=w)

    return lbl

def create_button_icon(holder, src, w, h):
    photo = Image.open(src)
    resized_image = photo.resize((w, h), Image.LANCZOS)
    icon = ImageTk.PhotoImage(resized_image)

    img_ref = tk.Label(holder, image=icon)
    img_ref.image = icon 

    return icon

if __name__ == "__main__":
    import sys

    con = sqlite3.connect("sytem.db")
    g_var.db_con = strg_class(con, assist_con)
    res = g_var.db_con.create_tables()

    if res[2] == 0:
        popup_con.system_setup(res)
    else:
        g_var.auth_user = True

    if g_var.auth_user == False:
        sys.exit("Exiting from my_function.")
            
    yr = int((assist_con.get_default_dt()).strftime("%Y"))
    while yr >= g_var.year_start:
        g_var.year_range.insert(0, yr)
        yr -= 1
    g_var.year_range = tuple(g_var.year_range)

    message_thread = threading.Thread(target=check_messages)
    message_thread.start()
    # message_thread.join()

    root = tk.Tk()
    app_w = math.ceil(root.winfo_screenwidth()*g_var.app_w)
    app_h = math.ceil(root.winfo_screenheight()*g_var.app_h)
    anchor_x = math.ceil((root.winfo_screenwidth()-app_w)*.4)
    anchor_y = math.ceil(app_h*.01)
    root.geometry(f"{app_w}x{app_h}+{anchor_x}+{anchor_y}")
    root.title("Quinn's Laundry House Booking Manager")
    root.configure(bg='lightblue')

    g_var.g_font1 = ('Arial',math.ceil(app_w*.007))
    g_var.g_font_sm = ('Arial',math.ceil(app_w*.006))

    try:
        response = requests.get(g_var.g_host)
        if response.status_code == 200:
            print(f"Connected: {response.status_code} - {response.text}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showinfo("Notice", "Unable to connect to server. Please check your config.txt file.")
        root.destroy()
        exit(0)

    #assist_con.load_resource_data(g_var.g_host+"get_products/all", "products")
    #assist_con.load_resource_data(g_var.g_host+"services/all", "services")
    #assist_con.load_resource_data(g_var.g_host+"addons/all", "addons")
    
    device_info = platform.uname()
    g_bgc = g_var.default_sys_config['background']['bg']
    g_fgc = g_var.default_sys_config['background']['fg']
    btn_dbgc = g_var.default_sys_config['button']['bg']
    btn_dfgc = g_var.default_sys_config['button']['fg']
    btn_bgc = g_var.default_sys_config['button']['hl']
    btn_fgc = g_var.default_sys_config['button']['hlfg']

    root.config(bg=g_bgc, padx=0)

    menu = tk.Frame(root, bg=g_bgc, relief=tk.FLAT, bd=2)
    menu.columnconfigure(0, minsize=math.ceil(app_w*.15), weight=1)
    menu.columnconfigure(1, minsize=math.ceil(app_w*.85), weight=1)
    menu.rowconfigure(0, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(1, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(2, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(3, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(4, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(5, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(6, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(7, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(8, minsize=math.ceil(app_h*.05), weight=1)
    menu.rowconfigure(9, minsize=math.ceil(app_h*.55), weight=1)

    grid_y = (10, 120, 230, 340, 450, 560)
    grid_x = (10, 105)
    menu_area = tk.LabelFrame(menu, text='', bg=g_bgc, fg=g_fgc, font=("Arial", 10, "bold"))
    menu_area.grid(row=0, column=0, padx=10, pady=10, sticky="news", columnspan=1, rowspan=10)
    icon_w = math.ceil(app_w*.04)
    icon_h = math.ceil(app_w*.04)

    # photo = Image.open("assets/images/booking.png")
    # resized_image = photo.resize((math.ceil(app_w*.04), math.ceil(app_w*.04)), Image.LANCZOS)
    # icon = ImageTk.PhotoImage(resized_image)

    icon_book = create_button_icon(menu_area, "assets/images/bookings_icon.png", icon_w, icon_w)
    icon_book_hl = create_button_icon(menu_area, "assets/images/bookings_icon_hl.png", icon_w, icon_w)
    btn_mng_book = tk.Button(menu_area, image=icon_book, anchor="center", text="Bookings", font=("Arial", 12), relief="flat", command=lambda:init_open_page('bookings'))
    #btn_mng_book.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
    btn_mng_book.place(x=grid_x[0], y=grid_y[0])
    lbl_bok = make_label(menu_area, grid_x[0], grid_y[0]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Bookings", g_var.g_font_sm, g_bgc, g_fgc, "center")
    lbl_bok.config(wraplength=math.ceil(app_w*.045))

    icon = create_button_icon(menu_area, "assets/images/services_icon.png", icon_w, icon_w)
    btn_mng_serv = tk.Button(menu_area, image=icon, anchor="center", text="Services", font=("Arial", 12), relief="flat", command=lambda:init_open_page('services'))
    #btn_mng_serv.grid(row=1, column=0, padx=5, pady=5, sticky="new")
    btn_mng_serv.place(x=grid_x[1], y=grid_y[0])
    lbl = make_label(menu_area, grid_x[1], grid_y[0]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Services", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon = create_button_icon(menu_area, "assets/images/addons_icon.png", icon_w, icon_w)
    btn_mng_addn = tk.Button(menu_area, image=icon, anchor="center", text="Addons", font=("Arial", 12), relief="flat", command=lambda:init_open_page('addons'))
    #btn_mng_addn.grid(row=2, column=0, padx=5, pady=5, sticky="new")
    btn_mng_addn.place(x=grid_x[0], y=grid_y[1])
    lbl = make_label(menu_area, grid_x[0], grid_y[1]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Addons", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon = create_button_icon(menu_area, "assets/images/rewards_icon.png", icon_w, icon_w)
    btn_mng_rwrd = tk.Button(menu_area, image=icon, anchor="center", text="Rewards", font=("Arial", 12), relief="flat", command=lambda:init_open_page('rewards'))
    #btn_mng_rwrd.grid(row=3, column=0, padx=5, pady=5, sticky="new")
    btn_mng_rwrd.place(x=grid_x[1], y=grid_y[1])
    lbl = make_label(menu_area, grid_x[1], grid_y[1]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Rewards", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon = create_button_icon(menu_area, "assets/images/billings_icon.png", icon_w, icon_w)
    btn_mng_bill = tk.Button(menu_area, image=icon, anchor="center", text="Billing", font=("Arial", 12), relief="flat", command=lambda:init_open_page('billings'))
    #btn_mng_bill.grid(row=4, column=0, padx=5, pady=5, sticky="new")
    btn_mng_bill.place(x=grid_x[0], y=grid_y[2])
    lbl = make_label(menu_area, grid_x[0], grid_y[2]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Billing", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon_msg = create_button_icon(menu_area, "assets/images/messaging_icon.png", icon_w, icon_w)
    icon_msg_hl = create_button_icon(menu_area, "assets/images/messaging_icon_hl.png", icon_w, icon_w)
    btn_mng_msg = tk.Button(menu_area, image=icon_msg, anchor="center", text="Messages", font=("Arial", 12), relief="flat", command=lambda:init_open_page('messages'))
    #btn_mng_msg.grid(row=5, column=0, padx=5, pady=5, sticky="new")
    btn_mng_msg.place(x=grid_x[1], y=grid_y[2])
    lbl_msg = make_label(menu_area, grid_x[1], grid_y[2]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Messages", g_var.g_font_sm, g_bgc, g_fgc, "center")
    lbl_msg.config(wraplength=math.ceil(app_w*.045))
    
    icon = create_button_icon(menu_area, "assets/images/customers_icon.png", icon_w, icon_w)
    btn_mng_cust = tk.Button(menu_area, image=icon, anchor="center", text="Customers", font=("Arial", 12), relief="flat", command=lambda:init_open_page('customers'))
    #btn_mng_cust.grid(row=6, column=0, padx=5, pady=5, sticky="new")
    btn_mng_cust.place(x=grid_x[0], y=grid_y[3])
    lbl = make_label(menu_area, grid_x[0], grid_y[3]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Customers", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon = create_button_icon(menu_area, "assets/images/reports_icon.png", icon_w, icon_w)
    btn_reports = tk.Button(menu_area, image=icon, anchor="center", text="Reports", font=("Arial", 12), relief="flat", command=lambda:init_open_page('reports'))
    #btn_reports.grid(row=7, column=0, padx=5, pady=5, sticky="new")
    btn_reports.place(x=grid_x[1], y=grid_y[3])
    lbl = make_label(menu_area, grid_x[1], grid_y[3]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Reports", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon_logistics = create_button_icon(menu_area, "assets/images/logistics_icon.png", icon_w, icon_w)
    icon_logistics_hl = create_button_icon(menu_area, "assets/images/logistics_icon_hl.png", icon_w, icon_w)
    btn_logistics = tk.Button(menu_area, image=icon_logistics, anchor="center", text="Logistics", font=("Arial", 12), relief="flat", command=lambda:init_open_page('logistics'))
    #btn_logistics.grid(row=8, column=0, padx=5, pady=5, sticky="new")
    btn_logistics.place(x=grid_x[0], y=grid_y[4])
    #lbl = make_label(menu_area, grid_x[0], grid_y[4]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Logistics", g_var.g_font_sm, g_bgc, g_fgc, "center")
    lbl_logistics = make_label(menu_area, grid_x[0], grid_y[4]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Logistics", g_var.g_font_sm, g_bgc, g_fgc, "center")
    lbl_logistics.config(wraplength=math.ceil(app_w*.045))

    icon = create_button_icon(menu_area, "assets/images/rider_icon.png", icon_w, icon_w)
    btn_riders = tk.Button(menu_area, image=icon, anchor="center", text="Riders", font=("Arial", 12), relief="flat", command=lambda:init_open_page('riders'))
    #btn_riders.grid(row=8, column=0, padx=5, pady=5, sticky="new")
    btn_riders.place(x=grid_x[1], y=grid_y[4])
    lbl = make_label(menu_area, grid_x[1], grid_y[4]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Riders", g_var.g_font_sm, g_bgc, g_fgc, "center")
    
    icon = create_button_icon(menu_area, "assets/images/shop_settings_icon.png", icon_w, icon_w)
    btn_mng_shop = tk.Button(menu_area, image=icon, anchor="center", text="Settings", font=("Arial", 12), relief="flat", command=lambda:init_open_page('shop'))
    #btn_mng_shop.grid(row=8, column=0, padx=5, pady=5, sticky="new")
    btn_mng_shop.place(x=grid_x[0], y=grid_y[5])
    lbl = make_label(menu_area, grid_x[0], grid_y[5]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Settings", g_var.g_font_sm, g_bgc, g_fgc, "center")

    icon = create_button_icon(menu_area, "assets/images/logout.png", icon_w, icon_w)
    btn_logout = tk.Button(menu_area, image=icon, anchor="center", text="Logout", font=("Arial", 12), relief="flat", command=lambda:init_open_page('logout'))
    #btn_logout.grid(row=8, column=0, padx=5, pady=5, sticky="new")
    btn_logout.place(x=grid_x[1], y=grid_y[5])
    lbl = make_label(menu_area, grid_x[1], grid_y[5]+math.ceil(app_w*.045), math.ceil(app_w*.045), "Logout", g_var.g_font_sm, g_bgc, g_fgc, "center")

    style = ttk.Style(root)
    assist_con.global_styling(g_var, style)
    
    g_var.popup_holder_win = root
    menu.place(x=0, y=0)
    init_open_page("bookings")
    
    root.protocol("WM_DELETE_WINDOW", lambda:exit_application())
    root.resizable(FALSE,FALSE)
    root.focus_force()
    root.update()
    root.mainloop()