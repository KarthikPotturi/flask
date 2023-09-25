from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, send_file, get_flashed_messages, render_template, flash, redirect, url_for, session, jsonify
import jwt
from datetime import datetime
obj = user_model()
auth = auth_model()

app.secret_key = "sri"

@app.route('/user/getall')
@auth.token_auth()
def user_getall_controller():
    return obj.user_getall_model()

@app.route('/user/view_details/<user_id>')
def user_view_details(user_id):
    user_details_response = obj.user_view_details(user_id)
    if user_details_response.status_code == 200:
        data = user_details_response.json.get('payload')
        print(data)
        return render_template('dashboard.html',user_details=data)

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

@app.route('/user/patch/<id>',methods=['PATCH','POST'])
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
    messages = get_flashed_messages(category_filter=['success','danger'])
    return render_template("index.html",messages=messages)

@app.route('/process',methods=['POST'])
def process():
    data = {"username":request.form['username'],"password":request.form['password']}
    token_response = obj.user_login_model(data)
    token = token_response.json.get('token',None)
    if token:
        jwt_decoded_token = jwt.decode(token, "sri", algorithms="HS256")
        user_details_list = eval(jwt_decoded_token['payload'])
        user_name = user_details_list['name']
        u_id = user_details_list['id']
        session['user_name'] = user_name
        session['u_id'] = u_id
        print('User id after decoding the token {}'.format(u_id))
        return redirect(url_for('user_dashboard'))
    else:
        flash('Login failed ! Invalid credentials','danger')
        return redirect(url_for('user_login_controller'))

@app.route('/user/signup',methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/user/dashboard',methods=['GET','POST'])
def user_dashboard():
    if "user_name" in session:
        return render_template('dashboard.html')

@app.route('/user/aboutus',methods=['GET'])
def about_us_controller():
    return render_template('about.html')

@app.route('/user/contact',methods=['GET'])
def contact_us_controller():
    return render_template('contact.html')

@app.route('/user/logout')
def logout_controller():
    return obj.user_logout_model()

@app.route('/user/reset_password',methods=['GET'])
def reset_password_controller():
    messages = get_flashed_messages(category_filter=['danger'])
    return render_template('forgot_password.html',messages = messages)

@app.route('/user/password_reset_controller',methods = ['POST'])
def user_reset_password_controller():
    return obj.user_reset_password_model(request.form)