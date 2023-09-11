from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, send_file
from datetime import datetime
from flask import render_template
obj = user_model()
auth = auth_model()

@app.route('/user/getall')
@auth.token_auth()
def user_getall_controller():
    return obj.user_getall_model()

@app.route('/user/addone',methods=['POST'])
#@auth.token_auth()
def user_addone_controller():
    return obj.user_addone_model(request.form)

@app.route('/user/update',methods=['PUT'])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route('/user/delete/<id>',methods=['DELETE'])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route('/user/patch/<id>',methods=['PATCH'])
def user_patch_controller(id):
    return obj.user_patch_model(id,request.form)

@app.route('/user/getall/limit/<limit>/page/<page>',methods=['GET'])
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)

@app.route('/user/<uid>/upload/avatar',methods=['PUT'])
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    unique_filename = str(datetime.now().timestamp()).replace('.','')
    fileNameSplit = file.filename.split('.')
    extension = fileNameSplit[len(fileNameSplit)-1]
    finalFilePath = f"uploads/{unique_filename}.{extension}"
    file.save(finalFilePath)
    return obj.user_upload_avatar_model(uid,finalFilePath)

@app.route('/uploads/<filename>')
def user_get_avatar_controller(filename):
    return send_file('uploads/{}'.format(filename))

@app.route('/user/login')
def user_login_controller():
    return render_template("index.html")

@app.route('/process',methods=['POST'])
def process():
    data = {"username":request.form['username'],"password":request.form['password']}
    print(type(data))
    return obj.user_login_model(data)

@app.route('/user/signup',methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')