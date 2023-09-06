import mysql.connector
import json
from flask import make_response
import jwt
from flask import request
import re
from functools import wraps

class auth_model():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='localhost',user='root',password='',database='flask_tutorial')
            self.conn.autocommit=True
            self.cur = self.conn.cursor(dictionary=True)
            print('Connection success')
        except:
            print('Connection failed')
    
    def token_auth(self,endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint)
                authorization = request.headers.get('Authorization')
                if re.match("Bearer *([^ ]+) *$",authorization,flags = 0):
                    token = authorization.split(' ')[1]
                    try:
                        jwt_decoded = jwt.decode(token, "sri", algorithms="HS256")
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR":"Token expired"},401)
                    role_id_dict = eval(jwt_decoded['payload'])
                    role_id = role_id_dict['role_id']
                    self.cur.execute("select roles from accessibility_view where endpoint = '{}'".format(endpoint))
                    result = self.cur.fetchall()
                    if len(result) >0:
                        allowed_roles = json.loads(result[0]['roles'])
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"ERROR":"Invalid role"},404)    
                    else:
                        return make_response({"ERROR":"Invalid endpoint"},404)
                else:
                    make_response({"Error":"Invalid token"},401)
            return inner2
        return inner1