import socket
import os
from tkinter import messagebox
import math
class g_var:
    host = socket.gethostbyname(socket.gethostname())
    g_host = f"http://{host}:5000/"
    app_w = 1
    app_h = 1
    popup_holder_win = ""
    g_font1 = ('Arial', 12)
    g_chart_holder = ""
    g_content = ""
    g_cbox = {}
    g_comp_bookings = {}
    g_comp_bookings2 = {}
    g_export_filename = ""
    fullscreen_mode = 1

    config_path = "config.txt"
    if os.path.exists(config_path):
        config_data = ""
        with open(config_path, "r") as f:
            config_data = f.readlines()
        f.close()

        if config_data != "":
            arr = {}
            for item in config_data:
                tmp_ind = item.split("=")
                arr[tmp_ind[0]] = tmp_ind[1]

            try:
                app_w = int(arr["app_width_percentage"].strip())/100
                app_h = int(arr["app_height_percentage"].strip())/100
                g_host = arr['host'].strip()
            except:
                pass

    headers = {
        "Content-Type": "application/json",
        "Authorization": "qlh-20080104"
    }
    app_token = "qlh-20080104"

    auth_user = False
    db_con = ""
    url = ""
    tbl = ""
    content = ""
    thread_id = ""
    tbl_data = {}
    popup_on = False

    products_arr = {}
    services_arr = {}
    addons_arr = {}
    booking_ntfy_list = {}
    message_ntfy_list = {}
    logistics_ntfy_list = {}
    year_start = 2025
    year_range = []
    wk_arr = []
    wk_set_arr = {}
    riders_arr = []
    riders_list = []
    riders_ids = {}

    cur_page = ""
    booking_mode = ""
    threads_frame = ""
    threads_table = ""
    threads_msg_table = ""

    day_off_list = []
    month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
    months_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
    days_short = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    prod_type_arr = {'full_service':'Full Service', 'comforter':'Comforter', 'self_service':'Self Service', 'addons':'Addons'}

    default_sys_config = {
        'button':{'bg':'#F0F0F0', 'fg':'#000000', 'hl':'#6699ff', 'hlfg':'#FFFFFF'},
        'background':{'bg':"#cbdbfb", 'fg':'#000000'},
    }

    tbl_style = {
        'h_bg':"#58A8C0", 'hl_bg':"#20748D", 'h_fg':"#1E1E1E", 'hl_fg':'#FFFFFF',
        'row_odd':"#9dbeff", 'row_even':"#d2e1ff"
    }

    cbox_style = {
        'f_bg':"#024bde", 'bg':'#ffffff'
    }

    scroll_style = {
        'btn_bg':"#4A91A7", 'arw':"#282828", 'bg':"#76a4ff"
    }

    inp_style = {
        'bg':"#024bde", 'fg':'#ffffff', 
    }



    def __init__(self) -> None:
        pass

    def set_active_popup(win_popup):
        global popup_win
        popup_win = win_popup

    def push_popup_front():
        try:
            popup_win.attributes("-topmost", True)
            popup_win.attributes("-topmost", False)
            popup_win.after(1, lambda: popup_win.focus_force())
        except:
            pass

    def warn_popup(title, msg):
        messagebox.showinfo(title, msg)
        popup_win.attributes("-topmost", True)
        popup_win.wm_attributes("-topmost", False)
        popup_win.after(1, lambda: popup_win.focus_force())