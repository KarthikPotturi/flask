import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class user_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host=dbconfig['hostname'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.conn.autocommit=True
            self.cur = self.conn.cursor(dictionary=True)
            print('Connection success')
        except:
            print('Connection failed')

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM user_table")
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload":result},200)
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        else:
            return make_response({"message":"No data found"},204)
    
    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO user_table(name, email, phone, role_id, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role_id']}', '{data['password']}')")
        return make_response({"message":"User created successfully"},201)

    def user_update_model(self,data):
        self.cur.execute(f"update user_table set name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role_id='{data['role_id']}',password='{data['password']}' where id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User updated successfully"},201)
        else:
            return make_response({"message":"No records to update"},202)
    
    def user_delete_model(self,id):
        self.cur.execute(f"delete from user_table where id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User deleted"},200)
        else:
            return make_response({"message":"No records found to delete"},202)
    
    def user_patch_model(self,id,data):
        query = "update user_table set "
        for key in data:
            query = query + "{}='{}', ".format(key,data[key])
        query = query[:-2] + " where id={}".format(id)
        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return make_response({"message":"{} row updated successfully".format(self.cur.rowcount)},201)
        else:
            return make_response({"message":"No rows updated"},202)
    
    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page*limit) - limit
        query = f"select * from user_table limit {start}, {limit}"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload":result, "page_no":page, "limit":limit},200)
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        else:
            return make_response({"message":"No data found"},204)

    def user_upload_avatar_model(self,uid,filepath):
        self.cur.execute("update user_table set avatar = '{}' where id = '{}'".format(filepath,uid))
        if self.cur.rowcount > 0:
            return make_response({"message": "Avatar updated successfully"},201)
        else:
            return make_response({"message":"No records to update"},202)
    
    def user_login_model(self, data):
        self.cur.execute("select id, name, email, phone, avatar, role_id from user_table where email = '{}' and password = '{}'".format(data['email'],data['password']))
        result = self.cur.fetchall()
        print(result)
        user_data = str(result[0])
        expiration_time = datetime.now() + timedelta(minutes=15)
        exp_eopch_time = int(expiration_time.timestamp())
        payload = {"payload":user_data, "exp":exp_eopch_time}
        token = jwt.encode(payload, "sri", algorithm="HS256")
        return make_response({"token":token},200)