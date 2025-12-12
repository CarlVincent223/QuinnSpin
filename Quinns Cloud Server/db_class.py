import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor # Or DictCursor
import random
from datetime import datetime, timedelta
import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, messaging
#cred = credentials.Certificate("quinns-laundry-house-5d121-cad4a86b8589.json")
#firebase_admin.initialize_app(cred)

os.environ['SERVICE_ACCOUNT_JSON'] = 'eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInF1aW5ucy1sYXVuZHJ5LWhvdXNlLTVkMTIxIiwgInByaXZhdGVfa2V5X2lkIjogImNhZDRhODZiODU4OWI3MDc2ZTA0ZmE4N2EzOTllOWU5OGEwYjc5YzYiLCAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdmdJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLZ3dnZ1NrQWdFQUFvSUJBUUM3aVNIK3haemZpRGY0XG51bkMrRytBRVUzcENMSjMvSjVYZ0NTcm1xeDBDTUZsMUdJQXpuUTdTd3pUc3RRZ3pHbkMwZFVqSFRuZmZtWDJXXG5iZzNYNXBEVXVmRTdmM2JZRzhWNzdBV09ZTFVUYmNGczBxM2cydXhFbklSRVljb2NQSGlIclhsSzhuT05OODgzXG5Sa1N5UG1NWVBIdmdhcjk3eFFXMWVVcXFKOEdUTXMyZzZ5RExkYys0dlVmaWtxRndBcFFaOFNYVkd0MHM0eVNDXG5lUWF6dmorSXh4YjlTNnQ5S0hXMG51YzNYTVg4c3BrVTYvdUttRHFKdk5SZHU3SlpwNTNMN0hFSmp1elBwYjhtXG4zUi9hM25Kbi82dzJ2MW8vbGp2ZG9rRTQ0ZVc5ZXgyYUl5amhPWjVrRGNrWWNQWlRSTHUwWXlSdWxKWFRXejZXXG5VNjJsNWxGakFnTUJBQUVDZ2dFQUNLdWdiTDBLTWJPRWt2VmJ2UTVnM3hKVTlyWkZYOFNldzBycE50ejJiR0Y3XG40VlFPcVZRN21UYjVQWEJwUHFPY1RsdVZ6OUVxN2FXVkR0MXJ1bTJvaUkxSVArMzJ1cXNlQ0VxelB3L3RqMFpsXG55UGc4bmNiQlliS3kwczZLbjUrVUd3SEVOOWpaeXMrbnZ2QjZ3SnJ0emZNTjd5UkFVaUtienZZYW81OU83ZFU1XG5JdkQrRlFMWkNQUllUVHBCZVpYbG02OE9SbThUdTRrNTdWNGROSkh4bVJIUkc1Snh4ZFN4elNIV3hzNDVDVHBuXG55Wnk1SVMrT2xsZzNNZTNrZDg0V2UvNkZBTWZTRXlWeEFaSGZXU0VTTVJZSlgvbmNMWUZXWVg4MVltS1c3NmFtXG5YU2R3V3RWa1p2NUpKd1p4N0w4RWRjbUo5SXZ2bUFlWUZsbmdJb3EzY1FLQmdRRHVvWThvRWNhQ0pGbTcrVHRSXG5TelFqdFBYSXpYU2pwL1NPSVd4Z1VNalVxT2wrTkVpT2l2MTg5bHM2eG04Y2JleWZVbGNZT1k2UWtUUUFZSmJzXG43bVJhMjVRY3Fad3dNZ2NpaGRWYzFHNi90TTYzbXpUY3ZMTFp5aEMvZ0VEOFFBT3RrYlNYcEFVVi90UjdEYkFlXG43TU9RUkUvTHlwV3pqQWJSNkx2OTBnc09yd0tCZ1FESkw0RzhabmcyY2s3VFFYLzZKZCtTNXJNMnR4b2c5eitTXG5uSWFhVk5Za2ZwV1pBWDBBTWxidnpWVnNnMjV2cFNBZm5BTC9peHVZUEpCNGoyTEFpMUpHcGorVEg5WWJmOEJrXG44ejl5VnFvNHIzUlduUFVhQ1pxUVRqenhua1UzQjdtQm40T1AzVDlwY0tmNDc1VC9BbVFBOU9RNU5DUmlpUFlnXG5JdDJhS2NzMWpRS0JnUURhbktsd2RQQmRzMzE5cG5NQUk1d3RoZytSR1IvYytmWWg2MTdFMGQxYWJUQVRUVVNYXG5TWisyUmw4SGRsaStPN29GcjBKWTBBbmFTUnZScUtzN2ZaMzBXcXJTbzFPU0Y1TFB2cm5icEVXZFhML3dGc0VUXG40ODhabEhOSmJPNmI2TzAxcW9FK1ZxWE9JN2wyemZCbU5GTm9yQnhLUDFwcnRVRmVOZzliRlh6Snd3S0JnQXUyXG5GMEJIV3NJWW4xd08yUXRQdnhjSEZQR2ZjUWJ3UGFRa05uV3ZjSlBKUnA0VWh4bEcxT2E2dGpsTjRWVGdjT0ZHXG5MS3FCaDRheUo5ck14ZnZkWUZtNmZjTHJ2SVAzU05UWGtCN3d5cEhvTE1hSjluNmdobjNXQUJnMGxXVGhyenZMXG5kRllnay90b1VtN2NTM2tZdzRlR3VlNVdpYk91czEwbGltN1o5ZmxWQW9HQkFKS0E2bnptQlREQW5pZGZveWZBXG4vT05UWHUweDdFU3paS0N0aUJIV25LMElSdGRBUDZ0Nm40R2tpWTRQcDl1RkprdSt2NmVFbk1Mc3dwN21mVDZpXG42T3UxbXpNR3YwNGNNQlZGdHhyMkN6aVVZZVMvS1NnWE94WTMwc0ZYT0lDRURtS1d1enJha0hLYzg1UytmejJTXG5Sc3g4WTFEUWxoR1oxZkJZQ2VLMjFYVENcbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsICJjbGllbnRfZW1haWwiOiAiZmlyZWJhc2UtYWRtaW5zZGstZmJzdmNAcXVpbm5zLWxhdW5kcnktaG91c2UtNWQxMjEuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiY2xpZW50X2lkIjogIjExNzM3MDQ0MjkwMDM1NjIxODA1NCIsICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLCAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L2ZpcmViYXNlLWFkbWluc2RrLWZic3ZjJTQwcXVpbm5zLWxhdW5kcnktaG91c2UtNWQxMjEuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAidW5pdmVyc2VfZG9tYWluIjogImdvb2dsZWFwaXMuY29tIn0='
encoded_key = os.getenv("SERVICE_ACCOUNT_JSON")
if not encoded_key:
    raise ValueError("The SERVICE_ACCOUNT_JSON environment variable is not set.")

service_account_info = json.loads(base64.b64decode(encoded_key).decode('utf-8'))
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

import pytz
UTC = pytz.utc
ph_tz = pytz.timezone('Asia/Manila')

class db_strg:
    otp_list = {}
    ntfy_list = {}
    client_ntfy_tok = {}
    client_ntfy_dat = {}
    rider_ntfy_tok = {}
    rider_ntfy_dat = {}
    new_msg = []
    new_booking = []
    new_rider_completion = []
    cancelled_booking = []

    def __init__(self) -> None:
        creden_arr = {}
        try:
            with open("credentials.txt", "r") as f:
                data = f.readlines()
            f.close()
            for item in data:
                arr = item.split("=")
                creden_arr[arr[0]] = (arr[1]).strip()      
        except:
            pass

        services_data = {}
        try:
            with open("products.txt", "r") as f:
                services_data = f.readlines()
            f.close()
        except:
            pass
        
        try:
            self.conn = psycopg2.connect(database=creden_arr['database'], user=creden_arr['user'], password=creden_arr['password'], host=creden_arr['host'], port=creden_arr['port'])
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            #self.cur = self.conn.cursor()
            #conn.close()
            try:
                self.cur.execute('''CREATE TABLE tbl_users (id SERIAL PRIMARY KEY, user_name TEXT NOT NULL, password TEXT NOT NULL, email TEXT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT, mobile_no TEXT, timestamp TIMESTAMP, status TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_pts_earned (user_id INT, amount INT, source TEXT, timestamp TIMESTAMP);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_pts_used (user_id INT, amount INT, benefit TEXT, timestamp TIMESTAMP);''')
                self.db_commit()
            except:
                self.conn.rollback() 

            try:
                self.cur.execute('''CREATE TABLE tbl_booking (id SERIAL PRIMARY KEY, user_id INT, schedule TEXT, mode TEXT, client TEXT, contact TEXT, pickup_loc TEXT, quantity TEXT, unit TEXT, timestamp TIMESTAMP, status TEXT, gps_coordinate TEXT, logistics_fee NUMERIC, notes TEXT, dropoff_time TEXT, cancel_reason TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_products (id SERIAL PRIMARY KEY, title TEXT, description TEXT, price numeric, quantity numeric, unit TEXT, prod_type TEXT, status TEXT);''')
                for item in services_data:
                    arr = item.split("::")
                    sql = f"INSERT INTO tbl_products (title,description,price,quantity,unit,prod_type,status) VALUES (\'{arr[1]}\', \'{arr[2]}\', \'{arr[3]}\', \'{arr[4]}\', \'{arr[5]}\', \'{arr[0]}\', \'{(arr[6]).strip()}\')"
                    self.cur.execute(sql)
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_booking_items (booking_id INT, service_id INT, quantity numeric);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_threads (id SERIAL PRIMARY KEY, booking_id INT, timestamp TIMESTAMP, status TEXT, viewed TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_thread_messages (thread_id INT, sender TEXT, message TEXT, timestamp TIMESTAMP, sender_type TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_payments (id SERIAL PRIMARY KEY, booking_id INT, mode TEXT, ref_num TEXT, amount NUMERIC, timestamp TIMESTAMP, status TEXT, add_charges NUMERIC, description TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_rewards (id SERIAL PRIMARY KEY, title TEXT, description TEXT, pts_req INT, status TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_qouta (date TEXT PRIMARY KEY, day TEXT, min_qouta INT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_day_off (sched_date TEXT, description TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_book_tracking (booking_id INT, sched TEXT, accepted TEXT, pickup TEXT, drop_off TEXT, arrived TEXT, processing TEXT, outgoing TEXT, completed TEXT, cancelled TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_riders (id SERIAL PRIMARY KEY, user_name TEXT NOT NULL, password TEXT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT, mobile_no TEXT, timestamp TIMESTAMP, status TEXT);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_rider_assigned (id SERIAL PRIMARY KEY, booking_id INT, rider_id INT, task_type TEXT, status TEXT, date_assigned TIMESTAMP, date_completed TIMESTAMP);''')
                self.db_commit()
            except:
                self.conn.rollback()

            try:
                self.cur.execute('''CREATE TABLE tbl_shop (shop_name TEXT, owner TEXT, tin TEXT, address TEXT, contact TEXT, fb_page TEXT, logistics NUMERIC, free_threshold NUMERIC, 
                                 sunday TEXT,
                                 monday TEXT,
                                 tuesday TEXT,
                                 wednesday TEXT,
                                 thursday TEXT,
                                 friday TEXT,
                                 saturday TEXT
                                 );''')
                
                sql = f"""
                INSERT INTO tbl_shop (shop_name,owner,tin,address,contact,fb_page,logistics,free_threshold,sunday,monday,tuesday,wednesday,thursday,friday,saturday) VALUES (
                'Quinns Laundry House',
                'Marian Ricafort',
                '487-529-480-00000',
                'Zone 6, Bagong Sirang San Felipe, Naga City / beside Blue Spring Water Refilling Station',
                '+639761082555',
                'https://www.facebook.com/quinns.laundryhouse',
                35.0,
                3,
                '8:00 am-9:00 pm',
                '8:00 am-9:00 pm',
                '8:00 am-9:00 pm',
                '8:00 am-9:00 pm',
                '8:00 am-9:00 pm',
                '8:00 am-9:00 pm',
                '8:00 am-9:00 pm'
                )
                """
                self.cur.execute(sql)
                self.db_commit()

            except:
                self.conn.rollback()
            
        except:
            print("Database connection error!") 

    def db_commit(self):
        self.conn.commit()
        #pass

    def get_hash_value(self, val):
        h = hashlib.new("SHA256")
        h.update(val.encode(encoding='utf-8'))
        
        return h.hexdigest()

    def send_otp(self, otp_code, recipient):
        subject = "OTP verification code"
        message = f"""
        Hi!
        <br/><br/>
        Your OTP verification code is <b>{otp_code}</b>. Do not share you code to anyone.
        <br/>
        Ignore this message if you don't recognized this request.
        <br/><br/>
        Thanks
        """
        print("Send OTP")

    def format_std_code(self, code, num, max_len):
        res = ""
        ctr = len(num)
        while ctr < max_len:
            res += "0"
            ctr += 1

        return code+res+num

    def gen_rand_num_codes(self, len):
        i=0
        code = ""
        while i < len:
            code += str(random.randint(0, 9))
            i += 1
            
        return code   

    def get_datetime(self):
        dt_now = datetime.now(ph_tz)
        dt_now = dt_now.strftime("%Y-%m-%d %H:%M:%S")

        return dt_now 
    
    def get_admin_notifications(self):  
        res1 = self.new_booking
        res2 = self.new_msg
        res3 = self.new_rider_completion
        res4 = self.cancelled_booking
        self.new_msg = []
        self.new_booking = []
        self.new_rider_completion = []
        self.cancelled_booking = []

        return {'bok':res1, 'msg':res2, 'com':res3, 'can':res4}

    def clear_notification(self, uid, type):
        res = "success"
        try:
            if type == "client":
                del self.client_ntfy_dat[self.client_ntfy_tok[int(uid)]]
            else:
                del self.rider_ntfy_dat[self.client_ntfy_tok[int(uid)]]
        except:
            res = "failed"
        
        return res
    
    def set_notification_token(self, data, type):
        if type == "client":
            self.client_ntfy_tok[data['id']] = data['token_id']
        else:
            self.rider_ntfy_tok[data['id']] = data['token_id']

    def send_notification(self, uid, type):
        
        try:
            if type == "client":
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Quinns Laundry House", 
                        body=self.client_ntfy_dat[self.client_ntfy_tok[uid]]['content'], 
                    ),
                    data={
                        'title':self.client_ntfy_dat[self.client_ntfy_tok[uid]]['title'],
                        'type':self.client_ntfy_dat[self.client_ntfy_tok[uid]]['type'],
                        'msg':self.client_ntfy_dat[self.client_ntfy_tok[uid]]['msg'],
                        'id':self.client_ntfy_dat[self.client_ntfy_tok[uid]]['id'],
                    },
                    token=self.client_ntfy_tok[uid],
                )
            else:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Quinns Laundry House", 
                        body=self.rider_ntfy_dat[self.rider_ntfy_tok[uid]]['content'], 
                    ),
                    data={
                        'title':self.rider_ntfy_dat[self.rider_ntfy_tok[uid]]['title'],
                        'msg':self.rider_ntfy_dat[self.rider_ntfy_tok[uid]]['msg'],
                        'id':self.rider_ntfy_dat[self.rider_ntfy_tok[uid]]['id'],
                    },
                    token=self.rider_ntfy_tok[uid],
                )
            response = messaging.send(message)  
            #print("Successfully sent message:", response)
            #del self.client_ntfy_dat[self.client_ntfy_tok[uid]]
        except Exception as e:
            print("Error sending notification", e)            

    def create_user(self, arr):
        self.cur.execute(f"SELECT id, email from tbl_users WHERE email='{arr['email']}'")
        res = self.cur.fetchone()
        if res == None:
            sql = f"INSERT INTO tbl_users (user_name,password,email,first_name,last_name,address,mobile_no,timestamp,status) VALUES (\'{arr['email']}\', \'{arr['upass']}\', \'{arr['email']}\', \'{arr['fname']}\', \'{arr['lname']}\', \'{arr['addr']}\', \'{arr['mobile_no']}\', \'{self.get_datetime()}\', 'Active') RETURNING id"
            try:
                self.cur.execute(sql)
                id = (self.cur.fetchone())['id']
                self.db_commit()
                res = {'id': id}
            except:
                res = "invalid"
                self.conn.rollback()
        else:
            if res['email'] == arr['email']:
                res = "email"

        return res 
    
    def create_booking(self, arr):
        sql = f"INSERT INTO tbl_booking (user_id, schedule, mode, client, contact, pickup_loc, quantity, unit, timestamp, status, notes, dropoff_time) VALUES (\'{arr['uid']}\', \'{arr['sched']}\', \'{arr['mode']}\', \'{arr['client']}\', \'{arr['contact']}\', \'{arr['ploc']}\', \'{arr['quantity']}\', '', \'{self.get_datetime()}\', 'Pending', \'{arr['notes']}\', \'{arr['dt']}\') RETURNING id"
        
        try:
            self.cur.execute(sql)
            id = (self.cur.fetchone())['id']
            sql = f"INSERT INTO tbl_threads (booking_id, timestamp, status, viewed) VALUES (\'{id}\', \'{self.get_datetime()}\', 'Open', '') RETURNING id"
            self.cur.execute(sql)

            sql = f"INSERT INTO tbl_book_tracking (booking_id, sched) VALUES (\'{id}\', \'{arr['sched_date']}\')"
            self.cur.execute(sql)
            self.db_commit()
            self.new_booking.insert(0, id)

            res = id
        except:
            res = "invalid"
            self.conn.rollback()
            
        return res 
    
    def cancel_booking(self, arr):
        try:
            self.cur.execute(f"UPDATE tbl_booking SET status='Cancelled', cancel_reason='{arr['cancel_reason']}', cancelled_by='{arr['cancelled_by']}' WHERE id={arr['id']}")
            self.cur.execute(f"UPDATE tbl_book_tracking SET cancelled='{self.get_datetime()}' WHERE booking_id={arr['id']}")
            self.db_commit()
            self.cancelled_booking.insert(0, int(arr['id']))
            res = "valid"
        except:
            res = "invalid"
            self.conn.rollback()
        
        return res 

    def validate_user(self, arr):
        self.cur.execute(f"SELECT id, password, first_name, last_name, address, mobile_no, status from tbl_users WHERE email='{arr['email']}' AND password='{arr['upass']}' AND status='Active'")
        res = self.cur.fetchone()
        if res == None:
            res = "invalid"
        
        return res
    
    def request_reset_password(self, user_name):
        self.cur.execute(f"SELECT id from tbl_users WHERE user_name='{user_name}'")
        res = self.cur.fetchone()
        if res == None:
            res = "invalid"

        return res
    
    def reset_password(self, arr):
        self.cur.execute(f"SELECT id from tbl_users WHERE user_name='{arr['email']}'")
        res = self.cur.fetchone()
        if res == None:
            res = "invalid"
        else:
            try:
                res = self.cur.execute(f"UPDATE tbl_users SET password='{arr['upass']}' WHERE email='{arr['email']}'")
                self.db_commit()
                res = "valid"
            except:
                res = "invalid"
                self.conn.rollback()
        
        return res
    
    def check_otp(self, arr):
        if self.otp_list[arr['user_id']] == arr['otp']:
            try:
                res = self.cur.execute(f"UPDATE tbl_users SET status='Active' WHERE id={arr['user_id']}")
                self.db_commit()
                self.otp_list.pop(arr['user_id'])
                res = "valid"
            except:
                res = "invalid"
                self.conn.rollback()
        else:
            res = "invalid"
        
        return res
    
    def retrieve_otp(self, arr):
        self.otp_list[arr['user_id']] = self.gen_rand_num_codes(4)
        res = self.otp_list[arr['user_id']]

        self.cur.execute(f"SELECT email from tbl_users WHERE id={arr['user_id']}")
        otp_recv = self.cur.fetchone()
        self.send_otp(res, otp_recv['email'])

        return res
    
    def get_user(self, id):
        if id == "all":
            self.cur.execute(f"SELECT * FROM tbl_users ORDER BY timestamp DESC")
            res = self.cur.fetchall()

            self.cur.execute(f"""SELECT SUM(PE.amount), U.id FROM tbl_pts_earned PE 
                             LEFT JOIN tbl_users U ON PE.user_id=U.id 
                             GROUP BY U.id""")
            res2 = self.cur.fetchall()
            self.cur.execute(f"""SELECT SUM(PU.amount), U.id FROM tbl_pts_used PU 
                             LEFT JOIN tbl_users U ON PU.user_id=U.id 
                             GROUP BY U.id""")
            res3 = self.cur.fetchall()

            res = [res, res2, res3]
        else:
            self.cur.execute(f"SELECT * FROM tbl_users WHERE id={id}")
            res = self.cur.fetchone()

        return res
    
    def get_riders(self, id):
        if id == "all":
            self.cur.execute(f"SELECT * FROM tbl_riders ORDER BY id DESC")
            res = self.cur.fetchall()
        else:
            self.cur.execute(f"SELECT * FROM tbl_riders WHERE id={id}")
            res = self.cur.fetchone()

        return res
    
    def get_rider_assigned(self, filter):
        self.cur.execute(f"SELECT id, first_name, last_name, address, status FROM tbl_riders")
        res1 = self.cur.fetchall()
        spc_code = "TO_CHAR(RA.date_assigned,'YYYY-MM-DD HH:MI:SS AM') date_assigned, TO_CHAR(RA.date_completed,'YYYY-MM-DD HH:MI:SS AM') date_completed"
        if filter == "All":
            self.cur.execute(f"""SELECT RA.*, {spc_code}, B.client, B.pickup_loc FROM tbl_rider_assigned RA 
                             LEFT JOIN tbl_booking B ON RA.booking_id=B.id 
                             ORDER BY RA.id DESC""")
            res = self.cur.fetchall()
        elif filter == "Pending" or filter == "Assigned" or filter == "Completed":
            self.cur.execute(f"""SELECT RA.*, B.client, B.pickup_loc FROM tbl_rider_assigned RA 
                             LEFT JOIN tbl_booking B ON RA.booking_id=B.id 
                             WHERE RA.status='{filter}' ORDER BY RA.id DESC""")
            res = self.cur.fetchall()
        else:
            self.cur.execute(f"""SELECT RA.*, B.client, B.pickup_loc FROM tbl_rider_assigned RA 
                             LEFT JOIN tbl_booking B ON RA.booking_id=B.id 
                             WHERE RA.id={filter}""")
            res = self.cur.fetchone()
        res = [res, res1]

        return res
    
    def get_rider_task(self, id, rid):
        if id == "all":
            self.cur.execute(f"""SELECT RA.id, RA.booking_id, RA.task_type, RA.status, B.client, B.pickup_loc, B.contact, B.quantity FROM tbl_rider_assigned RA 
                             LEFT JOIN tbl_booking B ON RA.booking_id=B.id 
                             WHERE RA.rider_id={rid} ORDER BY RA.id DESC""")
            res = self.cur.fetchall()
        else:
            self.cur.execute(f"""SELECT RA.id, RA.booking_id, RA.task_type, RA.status, B.client, B.pickup_loc, B.contact, B.quantity FROM tbl_rider_assigned RA 
                             LEFT JOIN tbl_booking B ON RA.booking_id=B.id 
                             WHERE RA.id={id}""")
            res = self.cur.fetchone()
        
        return res
    
    def get_admin_products(self, id):
        if id == "all":
            self.cur.execute(f"SELECT * FROM tbl_products ORDER BY id DESC")
            res = self.cur.fetchall()
        elif id == "services":
            self.cur.execute(f"SELECT * FROM tbl_products WHERE prod_type<>'addons' ORDER BY id DESC")
            res = self.cur.fetchall()
        elif id == "addons":
            self.cur.execute(f"SELECT * FROM tbl_products WHERE prod_type='addons' ORDER BY id DESC")
            res = self.cur.fetchall()
        else:
            self.cur.execute(f"SELECT * FROM tbl_products WHERE id={id}")
            res = self.cur.fetchone()

        return res
    
    def get_services(self, id):
        if id == "all":
            self.cur.execute(f"SELECT * FROM tbl_products ORDER BY id ASC")
            res = self.cur.fetchall()
        else:
            self.cur.execute(f"SELECT * FROM tbl_products WHERE id={id}")
            res = self.cur.fetchone()

        return res
    
    def get_booking(self, id):
        
        self.cur.execute(f"""SELECT B.id, B.mode, B.timestamp AS sched_date, B.status, BT.* FROM tbl_booking B 
                         LEFT JOIN tbl_book_tracking BT ON B.id=BT.booking_id 
                         WHERE B.user_id={id} ORDER BY B.timestamp DESC""")
        res = self.cur.fetchall()
        
        return res
    
    def get_booking_details(self, id):
        
        self.cur.execute(f"""SELECT B.*, BT.* FROM tbl_booking B 
                         LEFT JOIN tbl_book_tracking BT ON B.id=BT.booking_id 
                         WHERE B.id={id}""")
        res1 = self.cur.fetchall()

        self.cur.execute(f"""SELECT P.*, BI.quantity AS item_qty FROM tbl_booking_items BI 
                         LEFT JOIN tbl_products P ON BI.service_id=P.id 
                         WHERE BI.booking_id={id}""")
        res2 = self.cur.fetchall()
        
        return [res1, res2]
    
    def get_addons(self, id):
        if id == "all":
            self.cur.execute(f"SELECT * FROM tbl_addons ORDER BY id ASC")
            res = self.cur.fetchall()
        else:
            self.cur.execute(f"SELECT * FROM tbl_addons WHERE id={id}")
            res = self.cur.fetchone()

        return res
    
    def get_user_points(self, id):
    
        self.cur.execute(f"SELECT SUM(amount) FROM tbl_pts_earned WHERE user_id={id}")
        try:
            res_earned = self.cur.fetchone()['sum']
        except:
            res_earned = 0
        
        if res_earned == None:
            res_earned = 0

        self.cur.execute(f"SELECT SUM(amount) FROM tbl_pts_used WHERE user_id={id}")
        try:
            res_used = self.cur.fetchone()['sum']
        except:
            res_used = 0
        
        if res_used == None:
            res_used = 0
        
        return res_earned-res_used

    def get_earned_points(self, id):

        self.cur.execute(f"SELECT * FROM tbl_pts_earned WHERE user_id={id}")
        res = self.cur.fetchall()
        
        return res
    
    def get_points_history(self, id):
        self.cur.execute(f"SELECT * FROM tbl_pts_earned WHERE user_id={id} ORDER BY timestamp DESC")
        res1 = self.cur.fetchall()
        self.cur.execute(f"SELECT * FROM tbl_pts_used WHERE user_id={id} ORDER BY timestamp DESC")
        res2 = self.cur.fetchall()
        
        return [res1, res2]
    
    def get_usaged_points(self, id):

        self.cur.execute(f"SELECT * FROM tbl_pts_used WHERE user_id={id}")
        res = self.cur.fetchall()
        
        return res
    
    def get_points_reward(self, status):

        self.cur.execute(f"SELECT * FROM tbl_rewards WHERE status='{status}' ORDER BY pts_req DESC")
        res = self.cur.fetchall()
        
        return res
    
    # new mod

    
    
    def get_booking_services(self, arr):
        self.cur.execute(f"""SELECT BA.*, B.timestamp FROM tbl_users U 
                         LEFT OUTER JOIN tbl_booking B ON B.user_id=U.id 
                         LEFT OUTER JOIN tbl_booking_addon BA ON BA.booking_id=B.id 
                         WHERE U.id={arr['id']} ORDER BY {arr['sort']}""")
        res = self.cur.fetchall()
        return res
    
    def get_booking_tracks(self, arr):
        self.cur.execute(f"SELECT * FROM tbl_book_tracking WHERE booking_id={arr['id']} ORDER BY {arr['sort']}")
        res = self.cur.fetchall()
        
        return res
    
    def get_booking_payments(self, arr):
        self.cur.execute(f"SELECT * FROM tbl_payments WHERE booking_id={arr['id']} ORDER BY {arr['sort']}")
        res = self.cur.fetchall()
        
        return res
    
    def set_update_field(self, arr):
        res = "valid"
        try:
            self.cur.execute(f"UPDATE {arr['table']} SET {arr['field']}='{arr['value']}' WHERE {arr['ref_field']}={arr['ref_value']}")
            self.db_commit()
        except:
            res = "invalid"
            self.conn.rollback()
            
        return res
    
    def rider_update_field(self, arr):
        res = "valid"
        try:
            if arr['field'] == "password":
                arr['value'] = self.get_hash_value(arr['value'])
                
            self.cur.execute(f"UPDATE {arr['table']} SET {arr['field']}='{arr['value']}' WHERE {arr['ref_field']}={arr['ref_value']}")
            self.db_commit()
        except:
            res = "invalid"
            self.conn.rollback()
            
        return res
    
    # new mod
    
    def get_booked_services(self):
        self.cur.execute(f"SELECT B.*, TO_CHAR(B.timestamp,'YYYY-MM-DD HH:MI:SS AM') timestamp FROM tbl_booking B ORDER BY B.timestamp DESC")
        res = self.cur.fetchall()
        
        return res
    
    def get_all_bookings(self, arr):
        self.cur.execute(f"""SELECT B.client, B.contact, B.pickup_loc, B.mode, B.schedule, BT.sched FROM tbl_booking B 
                         LEFT OUTER JOIN tbl_book_tracking BT ON B.id=BT.booking_id 
                         WHERE BT.sched >= '{arr['point_a']}' AND BT.sched <= '{arr['point_b']}' AND B.status<>'Cancelled'""")
        res = self.cur.fetchall()
        
        return res

    def get_completed_bookings(self, arr):
        self.cur.execute(f"""SELECT B.id, B.client, B.contact, B.pickup_loc, B.mode, B.schedule, BT.sched, BT.completed, P.title, PY.amount FROM tbl_booking B 
                         LEFT OUTER JOIN tbl_payments PY ON B.id=PY.booking_id 
                         LEFT OUTER JOIN tbl_book_tracking BT ON B.id=BT.booking_id 
                         LEFT OUTER JOIN tbl_booking_items BI ON B.id=BI.booking_id 
                         LEFT OUTER JOIN tbl_products P ON BI.service_id=P.id 
                         WHERE BT.sched >= '{arr['point_a']}' AND BT.sched <= '{arr['point_b']}' AND P.prod_type<>'addons' AND PY.status='Paid' AND B.status='Completed'""")
        res = self.cur.fetchall()
        
        return res
    
    def set_booked_threads(self, arr):
        res = "valid"
        try:
            self.cur.execute(f"UPDATE tbl_threads SET viewed='{arr['user_id']}' WHERE id={arr['thread_id']}")
            sql = f"INSERT INTO tbl_thread_messages (thread_id, sender, message, timestamp, sender_type) VALUES (\'{arr['thread_id']}\', \'{arr['user_id']}\', \'{arr['message']}\', \'{self.get_datetime()}\', \'{arr['sender_type']}\')"
            self.cur.execute(sql)
            self.db_commit()
            self.new_msg.insert(0, arr['thread_id'])
        except:
            res = "invalid"
        
        return res
    
    def get_booked_threads(self, arr):
        self.cur.execute(f"SELECT T.*, TM.* FROM tbl_threads T LEFT OUTER JOIN tbl_booking B ON B.id=T.booking_id LEFT OUTER JOIN tbl_thread_messages TM ON T.id=TM.thread_id "+arr['filter']+" ORDER BY TM.timestamp ASC")
        res = self.cur.fetchall()
        
        return res
    
    # Admin queries

    def validate_rider(self, arr):
        self.cur.execute(f"SELECT id, user_name, password, first_name, last_name, address, mobile_no, status from tbl_riders WHERE user_name='{arr['uname']}' AND password='{self.get_hash_value(arr['upass'])}' AND status='Active'")
        res = self.cur.fetchone()
        if res == None:
            res = "invalid"
        
        return res

    def get_day_off(self):
        
        self.cur.execute(f"SELECT * FROM tbl_day_off ORDER BY sched_date ASC")
        res = self.cur.fetchall()

        return res

    def get_shop(self):
        self.cur.execute(f"SELECT * FROM tbl_shop")
        res1 = self.cur.fetchone()

        self.cur.execute(f"SELECT * FROM tbl_day_off ORDER BY sched_date ASC")
        res2 = self.cur.fetchall()

        return [res1, res2]
    
    def mod_tbl_shop(self, arr):
        res = "valid"
        try:    
            self.cur.execute(f"""UPDATE tbl_shop SET 
                            shop_name = '{arr['shop_name']}',
                            owner = '{arr['owner']}',
                            tin = '{arr['tin']}',
                            address = '{arr['address']}',
                            contact = '{arr['contact']}',
                            fb_page = '{arr['fb_page']}',
                            logistics = '{arr['logistics']}',
                            free_threshold = '{arr['free_threshold']}',
                            sunday = '{arr['sunday']}',
                            monday = '{arr['monday']}',
                            tuesday = '{arr['tuesday']}',
                            wednesday = '{arr['wednesday']}',
                            thursday = '{arr['thursday']}',
                            friday = '{arr['friday']}',
                            saturday = '{arr['saturday']}'
                            """)
            self.db_commit()
        except:
            res = "invalid"
            self.conn.rollback()

        return res
    
    def mod_tbl_day_off(self, act, arr):
        res = "valid"
        
        try:

            if act == 'add':
                self.cur.execute(f"SELECT sched_date FROM tbl_day_off WHERE sched_date='{arr['sched_date']}'")
                exist = self.cur.fetchone()
                if exist == None:
                    sql = f"INSERT INTO tbl_day_off (sched_date, description) VALUES (\'{arr['sched_date']}\', \'{arr['description']}\')"
                else:
                    sql = f"UPDATE tbl_day_off SET description='{arr['description']}' WHERE sched_date='{arr['sched_date']}'"
            elif act == 'update':
                sql = f"UPDATE tbl_day_off SET sched_date='{arr['sched_date']}', description='{arr['description']}' WHERE sched_date='{arr['sched_date']}'"
            elif act == 'delete':
                sql = f"DELETE FROM tbl_day_off WHERE sched_date='{arr['sched_date']}'"
  
            self.cur.execute(sql)
            self.db_commit()

            self.cur.execute(f"SELECT * FROM tbl_day_off ORDER BY sched_date ASC")
            res = self.cur.fetchall()
        except:
            res = "invalid"
            self.conn.rollback()

        return res

    def get_threads_admin(self):
        self.cur.execute(f"""
                         SELECT DISTINCT T.id, T.*, U.first_name, U.last_name FROM tbl_threads T 
                         LEFT OUTER JOIN tbl_thread_messages TM ON T.id=TM.thread_id 
                         LEFT OUTER JOIN tbl_users U ON CAST(TM.sender AS INT)=U.id 
                         WHERE T.status='Open' AND sender<>'0' ORDER BY T.timestamp DESC""")
        res = self.cur.fetchall()

        return res
    
    def get_thread_messages_admin(self, id):
        self.cur.execute(f"""
                         SELECT DISTINCT TM.*, TO_CHAR(TM.timestamp,'YYYY-MM-DD HH:MI:SS AM') timestamp, U.first_name, R.first_name AS rider_name FROM tbl_threads T 
                         LEFT OUTER JOIN tbl_thread_messages TM ON T.id=TM.thread_id 
                         LEFT OUTER JOIN tbl_users U ON CAST(TM.sender AS INT)=U.id 
                         LEFT OUTER JOIN tbl_riders R ON CAST(TM.sender AS INT)=R.id
                         WHERE T.id={id} AND T.status='Open' ORDER BY TM.timestamp ASC""")
        res = self.cur.fetchall()

        return res
    
    def set_thread_reply_admin(self, arr):
        res = "valid"
        try:
            sql = f"INSERT INTO tbl_thread_messages (thread_id, sender, message, timestamp, sender_type) VALUES (\'{arr['thread_id']}\', \'{arr['sender_id']}\', \'{arr['message']}\', \'{self.get_datetime()}\', \'{arr['sender_type']}\')"
            self.cur.execute(sql)
            self.db_commit()
        except:
            res = "invalid"

        if res == "valid":
            
            try:
                ntfy_msg = ""
                if arr['message'] != "":
                    ntfy_msg = arr['message']

                if ntfy_msg != "":
                    self.cur.execute(f"""
                         SELECT DISTINCT B.user_id FROM tbl_threads T 
                         LEFT OUTER JOIN tbl_booking B ON T.booking_id=B.id 
                         WHERE T.id={arr['thread_id']}""")
                    res = self.cur.fetchone()
                    user_id = res['user_id']
                    
                    pending_ntfy = 0
                    try:
                        pending_ntfy = self.client_ntfy_dat[self.client_ntfy_tok[user_id]]['content']
                    except:
                        pass
                    
                    if pending_ntfy == 0:
                        self.client_ntfy_dat[self.client_ntfy_tok[user_id]] = {}
                        self.client_ntfy_dat[self.client_ntfy_tok[user_id]]['content'] = "Admin replied to your thread"
                        self.client_ntfy_dat[self.client_ntfy_tok[user_id]]['type'] = "message"
                        self.client_ntfy_dat[self.client_ntfy_tok[user_id]]['title'] = "Admin Reply"
                        self.client_ntfy_dat[self.client_ntfy_tok[user_id]]['msg'] = ntfy_msg
                        self.client_ntfy_dat[self.client_ntfy_tok[user_id]]['id'] = str(arr['thread_id'])
                        self.send_notification(user_id, 'client')

            except:
                pass

        return res
    
    def mod_tbl_threads(self, act, arr):
        if act == "Delete":
            res = "valid"
            try:
                if arr['timestamp'] == "": 
                    self.cur.execute(f"DELETE FROM tbl_threads WHERE id = {arr['thread_id']}")
                    self.cur.execute(f"DELETE FROM tbl_thread_messages TM USING tbl_threads T WHERE T.booking_id = {arr['thread_id']} AND TM.thread_id = T.id")
                else:
                    if arr['sender'] == '0':
                        self.cur.execute(f"DELETE FROM tbl_thread_messages WHERE thread_id = {arr['thread_id']} AND timestamp = '{arr['timestamp']}'")
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()

        return res
    
    def get_booking_pack(self, id):
        self.cur.execute(f"SELECT * FROM tbl_booking_addon WHERE booking_id={id}")
        res = self.cur.fetchall()

        return res

    def mod_tbl_bookings(self, act, arr, arr2):
        if act == "Delete":
            res = "valid"
            try:
                self.cur.execute(f"DELETE FROM tbl_booking WHERE id = '{arr['booking_id']}'")
                self.cur.execute(f"DELETE FROM tbl_booking_items WHERE booking_id = '{arr['booking_id']}'")
                self.cur.execute(f"DELETE FROM tbl_book_tracking WHERE booking_id = '{arr['booking_id']}'")
                self.cur.execute(f"DELETE FROM tbl_payments WHERE booking_id = '{arr['booking_id']}'")
                self.cur.execute(f"DELETE FROM tbl_threads WHERE booking_id = '{arr['booking_id']}'")
                self.cur.execute(f"DELETE FROM tbl_thread_messages TM USING tbl_threads T WHERE T.booking_id = '{arr['booking_id']}' AND TM.thread_id = T.id")
                self.cur.execute(f"DELETE FROM tbl_rider_assigned WHERE booking_id = '{arr['booking_id']}'")
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()
        elif act == "Update": 
            res = "valid"
            try:
                self.cur.execute(f"UPDATE tbl_booking SET status='{arr['status']}', logistics_fee='{arr['logistics_fee']}', cancel_reason='{arr['cancel_reason']}', cancelled_by='{arr['cancelled_by']}' WHERE id={arr['booking_id']}")
                stat_arr = {'Pending':'sched','Confirmed':'accepted','Pickup':'pickup','Drop Off':'drop_off','Arrived':'arrived','Ongoing':'processing','Delivery':'outgoing','To Receive':'outgoing','Completed':'completed','Cancelled':'cancelled'}
                self.cur.execute(f"UPDATE tbl_book_tracking SET {stat_arr[arr['status']]}='{self.get_datetime()}' WHERE booking_id={arr['booking_id']}")
                
                if arr['status'] == "Pickup" or arr['status'] == "Delivery":
                    self.cur.execute(f"SELECT id from tbl_rider_assigned WHERE booking_id={arr['booking_id']} AND task_type='{arr['status']}'")
                    exist = self.cur.fetchone()
                    if exist == None:
                        sql = f"INSERT INTO tbl_rider_assigned (booking_id,task_type,status) VALUES (\'{arr['booking_id']}\',\'{arr['status']}\','Pending')"
                        self.cur.execute(sql)
                
                if arr['status'] == "Delivery" or arr['status'] == "To Receive":
                    self.cur.execute(f"SELECT id from tbl_payments WHERE booking_id={arr['booking_id']}")
                    res = self.cur.fetchone()

                    if res == None:
                        sql = f"INSERT INTO tbl_payments (booking_id,mode,ref_num,amount,timestamp,status,add_charges,description) VALUES (\'{arr['booking_id']}\','','',0,'{self.get_datetime()}','Unpaid',0,'')"
                        self.cur.execute(sql)
                    #print((self.cur.fetchone())['id'])
                
                for item in arr2:
                    self.cur.execute(f"UPDATE tbl_booking_items SET quantity={item['qty']} WHERE booking_id={arr['booking_id']} AND service_id={item['service_id']} RETURNING quantity")    
                    upres = self.cur.fetchone()
                    
                    if upres == None:
                        self.cur.execute(f"INSERT INTO tbl_booking_items (booking_id,service_id,quantity) VALUES ({arr['booking_id']},{item['service_id']},{item['qty']})")
                    else:
                        if item['qty'] == 0:
                            self.cur.execute(f"DELETE FROM tbl_booking_items WHERE booking_id={arr['booking_id']} AND service_id={item['service_id']}")

                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()

            try:
                ntfy_msg = ""
                if arr['status'] != "" and arr['status'] != "Pending":
                    ntfy_msg = arr['status']

                if ntfy_msg != "":
                    pending_ntfy = 0
                    try:
                        pending_ntfy = self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['content']
                    except:
                        pass
                        
                    if pending_ntfy == 0:
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]] = {}
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['content'] = f"Booking {self.format_std_code("QLH", str(arr['booking_id']), 6)} update."
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['type'] = "booking"
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['title'] = "Booking Update" #f"Booking {self.format_std_code("QLH", str(arr['booking_id']), 6)} Status: {arr['status']}"
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['msg'] = ntfy_msg
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['id'] = str(arr['booking_id'])
                        self.send_notification(arr['uid'], 'client')

            except:
                pass
        
        return res
    
    def get_rewards_list(self):
        self.cur.execute(f"SELECT * FROM tbl_rewards ORDER BY pts_req DESC")
        res = self.cur.fetchall()
        
        return res
    
    def mod_tbl_rewards(self, act, arr):
        if act == "Add":
            try:
                sql = f"INSERT INTO tbl_rewards (title, description, pts_req, status) VALUES (\'{arr['title']}\', \'{arr['description']}\', \'{arr['pts_req']}\', \'{arr['status']}\') RETURNING id"
                self.cur.execute(sql)
                self.db_commit()
                res = (self.cur.fetchone())['id']
            except:
                res = "invalid"
        elif act == "Update":
            res = "valid"
            try:
                self.cur.execute(f"UPDATE tbl_rewards SET title='{arr['title']}', description='{arr['description']}', pts_req='{arr['pts_req']}', status='{arr['status']}' WHERE id={arr['id']}")
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()
        elif act == "Delete":
            res = "valid"
            try:
                self.cur.execute(f"DELETE FROM tbl_rewards WHERE id={arr['id']}")
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()

        return res
    
    def get_billing_payments(self, id):
        self.cur.execute(f"""SELECT SUM(P.price*BI.quantity), PY.id FROM tbl_payments PY 
                            LEFT OUTER JOIN tbl_booking_items BI ON PY.booking_id=BI.booking_id 
                            LEFT OUTER JOIN tbl_products P ON BI.service_id=P.id 
                            GROUP BY PY.id""")
        res3 = self.cur.fetchall()
        
        if id == "All":
            self.cur.execute(f"""SELECT P.*, B.user_id, B.client, B.contact, B.pickup_loc, B.logistics_fee, B.quantity AS basket_qty FROM tbl_payments P 
                            LEFT OUTER JOIN tbl_booking B ON P.booking_id=B.id 
                            ORDER BY P.id DESC""")
            res = self.cur.fetchall()
            res = [res, res3]
        elif id == "Paid":
            self.cur.execute(f"""SELECT P.*, B.user_id, B.client, B.contact, B.pickup_loc, B.logistics_fee FROM tbl_payments P 
                            LEFT OUTER JOIN tbl_booking B ON P.booking_id=B.id 
                            WHERE P.status='{id}' ORDER BY P.id DESC""")
            res = self.cur.fetchall()
            res = [res, res3]
        elif id == "Unpaid":
            self.cur.execute(f"""SELECT P.*, B.user_id, B.client, B.contact, B.pickup_loc, B.logistics_fee FROM tbl_payments P 
                            LEFT OUTER JOIN tbl_booking B ON P.booking_id=B.id 
                            WHERE P.status='{id}' ORDER BY P.id DESC""")
            res = self.cur.fetchall()
            res = [res, res3]
        else:
            self.cur.execute(f"""SELECT B.* FROM tbl_booking B 
                            LEFT OUTER JOIN tbl_payments P ON B.id=P.booking_id 
                            WHERE P.id={id}""")
            res1 = self.cur.fetchone()

            self.cur.execute(f"""SELECT P.*, BI.quantity AS item_qty FROM tbl_products P 
                            LEFT OUTER JOIN tbl_booking_items BI ON P.id=BI.service_id 
                            LEFT OUTER JOIN tbl_payments PY ON BI.booking_id=PY.booking_id
                            WHERE PY.id={id}""")
            res2 = self.cur.fetchall()

            res = [res1, res2]
        
        return res

    def mod_tbl_products(self, act, arr):
        if act == "Add":
            try:
                sql = f"INSERT INTO tbl_products (title, description, price, quantity, unit, prod_type, status) VALUES (\'{arr['title']}\', \'{arr['description']}\', \'{arr['price']}\', \'{arr['quantity']}\', \'{arr['unit']}\', \'{arr['prod_type']}\', \'{arr['status']}\') RETURNING id"
                self.cur.execute(sql)
                self.db_commit()
                res = (self.cur.fetchone())['id']
            except:
                res = "invalid"
        elif act == "Update":
            res = "valid"
            try:
                if arr['prod_type'] == "addons":
                    self.cur.execute(f"UPDATE tbl_products SET title='{arr['title']}', description='{arr['description']}', price='{arr['price']}', status='{arr['status']}' WHERE id={arr['id']}")
                else:
                    self.cur.execute(f"UPDATE tbl_products SET title='{arr['title']}', description='{arr['description']}', price='{arr['price']}', quantity='{arr['quantity']}', unit='{arr['unit']}', status='{arr['status']}' WHERE id={arr['id']}")
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()
        elif act == "Delete":
            res = "valid"
            self.cur.execute(f"SELECT service_id FROM tbl_booking_items WHERE service_id={arr['id']}")
            exist = self.cur.fetchone()
            try:
                if exist == None:
                    self.cur.execute(f"DELETE FROM tbl_products WHERE id={arr['id']}")
                else:
                    self.cur.execute(f"UPDATE tbl_products SET status='Deleted' WHERE id={arr['id']}")
                    res = "taken"
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()

        return res
    
    def mod_tbl_riders(self, act, arr):
        res = "valid"
        
        if act == "Add":
            self.cur.execute(f"SELECT id FROM tbl_riders WHERE user_name='{arr['user_name']}'")
            exist = self.cur.fetchone()
            try:
                if exist == None:
                    sql = f"INSERT INTO tbl_riders (user_name, password, first_name, last_name, address, mobile_no, timestamp, status) VALUES (\'{arr['user_name']}\', \'{arr['password']}\', \'{arr['first_name']}\', \'{arr['last_name']}\', \'{arr['address']}\', \'{arr['mobile_no']}\', \'{self.get_datetime()}\', \'{arr['status']}\') RETURNING id"
                    self.cur.execute(sql)
                    self.db_commit()
                    res = (self.cur.fetchone())['id']
                else:
                    res = "exist"
            except:
                res = "invalid"
        elif act == "Update":
            self.cur.execute(f"SELECT id FROM tbl_riders WHERE user_name='{arr['user_name']}' AND id<>{arr['id']}")
            exist = self.cur.fetchone()
            try:
                if exist == None:
                    if arr['password'] == "":
                        self.cur.execute(f"UPDATE tbl_riders SET user_name='{arr['user_name']}', first_name='{arr['first_name']}', last_name='{arr['last_name']}', address='{arr['address']}', mobile_no='{arr['mobile_no']}', status='{arr['status']}' WHERE id={arr['id']}")
                    else:
                        self.cur.execute(f"UPDATE tbl_riders SET user_name='{arr['user_name']}', password='{arr['password']}', first_name='{arr['first_name']}', last_name='{arr['last_name']}', address='{arr['address']}', mobile_no='{arr['mobile_no']}', status='{arr['status']}' WHERE id={arr['id']}")
                    self.db_commit()
                else:
                    res = "exist"
            except:
                res = "invalid"
                self.conn.rollback()
        elif act == "Delete":
            self.cur.execute(f"SELECT id FROM tbl_rider_assigned WHERE rider_id={arr['id']}")
            exist = self.cur.fetchone()
            try:
                if exist == None:
                    self.cur.execute(f"DELETE FROM tbl_riders WHERE id={arr['id']}") 
                else:
                    self.cur.execute(f"UPDATE tbl_riders SET status='Inactive' WHERE id={arr['id']}")
                    res = "taken"
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()

        return res
    
    def mod_tbl_rider_assigned(self, act, arr):
        res = "valid"
        
        if act == "Update":
            try:
                self.cur.execute(f"UPDATE tbl_rider_assigned SET rider_id='{arr['rider_id']}', status='{arr['status']}', date_assigned='{self.get_datetime()}' WHERE id={arr['id']}")
                self.db_commit()
                try:
                    self.rider_ntfy_dat[self.rider_ntfy_tok[arr['rider_id']]] = {}
                    self.rider_ntfy_dat[self.rider_ntfy_tok[arr['rider_id']]]['content'] = f"New task has been assigned to you."
                    self.rider_ntfy_dat[self.rider_ntfy_tok[arr['rider_id']]]['title'] = "New Task"
                    self.rider_ntfy_dat[self.rider_ntfy_tok[arr['rider_id']]]['msg'] = arr['task']
                    self.rider_ntfy_dat[self.rider_ntfy_tok[arr['rider_id']]]['id'] = str(id)
                    self.send_notification(arr['rider_id'], 'rider') 
                except:
                    pass
            except:
                res = "invalid"
                self.conn.rollback()
        
        return res
    
    def set_rider_assigned(self, id, status):
        res = "valid"
        try:
            self.cur.execute(f"UPDATE tbl_rider_assigned SET status='{status}', date_completed='{self.get_datetime()}' WHERE id={id}")
            self.db_commit()
            self.new_rider_completion.insert(0, id)
        except:
            res = "invalid"
            self.conn.rollback()
        
        return res
    
    def mod_tbl_billings(self, act, arr):
        if act == "Update":
            res = "valid"
            send_ntfy = 0
            try:
                self.cur.execute(f"UPDATE tbl_payments SET mode='{arr['mode']}', ref_num='{arr['ref_num']}', amount='{arr['amount']}', status='{arr['status']}' WHERE id={arr['id']}")
                if arr['payment_status'] == "Unpaid":
                    if arr['mode'] == "Points":
                        sql = f"INSERT INTO tbl_pts_used (user_id,amount,benefit,timestamp) VALUES (\'{arr['uid']}\',\'{arr['amount']}\','Payment for booking {self.format_std_code("QLH", str(arr['booking_id']), 6)}',\'{self.get_datetime()}\')"
                        self.cur.execute(sql)
                    if arr['status'] == "Paid":
                        if arr['points'] != '' and arr['points'] != '0':
                            sql = f"INSERT INTO tbl_pts_earned (user_id,amount,source,timestamp) VALUES (\'{arr['uid']}\',\'{arr['points']}\',\'{arr['description']}\',\'{self.get_datetime()}\')"
                            #sql = f"INSERT INTO tbl_pts_used (user_id,amount,benefit,timestamp) VALUES (\'{arr['uid']}\',\'{arr['points']}\',\'{arr['description']}\',\'{self.get_datetime()}\')"
                            self.cur.execute(sql)
                        
                        self.cur.execute(f"UPDATE tbl_booking SET status='Completed' WHERE id={arr['booking_id']}")
                        self.cur.execute(f"UPDATE tbl_book_tracking SET completed=\'{self.get_datetime()}\' WHERE booking_id={arr['booking_id']}")
                        send_ntfy = 1

                self.db_commit()
            except:
                print("Billing error")
                res = "invalid"
                self.conn.rollback()

            if send_ntfy == 1:
                pending_ntfy = 0
                try:
                    pending_ntfy = self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['content']
                except:
                    pass
                
                try:
                    if pending_ntfy == 0:
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]] = {}
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['content'] = f"Booking {self.format_std_code("QLH", str(arr['booking_id']), 6)} update."
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['type'] = "booking"
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['title'] = "Booking Update"
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['msg'] = "Completed"
                        self.client_ntfy_dat[self.client_ntfy_tok[arr['uid']]]['id'] = str(arr['booking_id'])
                        self.send_notification(arr['uid'], 'client')
                except:
                    pass

        return res
    
    def mod_tbl_users(self, act, arr):
        if act == "Update":
            res = "valid"
            try:
                self.cur.execute(f"UPDATE tbl_users SET status='{arr['status']}' WHERE id={arr['id']}")
                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()
        elif act == "Delete":
            res = "valid"
            self.cur.execute(f"SELECT id FROM tbl_booking WHERE user_id={arr['id']}")
            exist = self.cur.fetchone()
            try:
                if exist == None:
                    self.cur.execute(f"DELETE FROM tbl_users WHERE id={arr['id']}")
                else:
                    self.cur.execute(f"UPDATE tbl_users SET user_name='', email='' WHERE id={arr['id']}")
                    res = "taken"

                self.db_commit()
            except:
                res = "invalid"
                self.conn.rollback()

        return res
    
    # Admin queries