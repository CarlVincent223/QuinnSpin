class strg_class:
    con = ""

    def __init__(self, con, assist_con) -> None:
        self.assist_con = assist_con
        self.unlocked = True

        self.con = con
        self.query_lib = {}
        self.query_lib['tbl_system'] = "(user_name, password, cookie)"
        
    def create_tables(self):
        cur = self.con.cursor()
        new_table = False
        res = ""
        try:
            res = self.get_query_single_data("tbl_system", "*", "", "1")
        except:
            res = ("admin", self.assist_con.get_hash_value('12345678'), False)
            cur.execute("""CREATE TABLE tbl_system (
                        user_name TEXT NOT NULL,
                        password TEXT NOT NULL,
                        cookie BOOLEAN)
            """)
            cur.execute(f"INSERT INTO tbl_system {self.query_lib['tbl_system']} VALUES ('{res[0]}', '{res[1]}', {res[2]})")
            new_table = True

        if self.unlocked and new_table:
            print("Commit")
            self.con.commit()

        return res
    
    def update_admin_data(self, tbl, val, condition):
        sql = f"UPDATE {tbl} SET {val} WHERE {condition}"
        cur = self.con.cursor()
        cur.execute(sql)
        #print(sql)
        if self.unlocked:
            self.con.commit()
    
    def get_current_user(self):
        cur = self.con.cursor()
        try: 
            res = cur.execute("SELECT * FROM tbl_system WHERE 1")
            row = res.fetchone()
            return row
        except:
            print("Create users accounts table")
    
    def get_query_single_data(self, table, fields, join, condition):
        sql = f"""SELECT 
                          {fields} 
                          FROM 
                          {table} 
                          {join} 
                          WHERE 
                          {condition}
                        """
        cur = self.con.cursor()
        res = cur.execute(sql)
        row = res.fetchone()
        #self.con.close()
        return row