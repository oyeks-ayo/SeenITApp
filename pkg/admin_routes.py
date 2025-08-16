from functools import wraps
from flask import render_template,request,redirect,url_for,flash,make_response,session
from flask_wtf.csrf import CSRFError # type: ignore
from werkzeug.security import check_password_hash # type: ignore
from pkg import app,csrf
from pkg.forms import AdminLogin,AdminPasswordReset
from pkg.models import db, Admin, Users, Project
# from pkg.forms import 


# *********************************** LOGIN DECORATOR **************************************************

def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if session.get('adminisonline') != None:
            return f(*args,**kwargs)
        else:
            flash('You need to be logged in before you can visit page', category='error')
            return redirect(url_for('AdminLogin'))
    return login_decorator
# *********************************** LOGIN DECORATOR **************************************************
# *********************************** ADMIN LOGIN **************************************************
@app.route('/admin/login/', methods=['POST', 'GET'])
def adminlogin():
    form = AdminLogin()

    if form.is_submitted():
        print("Form submitted")
        print("Form errors:", form.errors)
        
    if form.validate_on_submit():
        username = form.uname.data
        pwd = form.password.data
        print("Form validated")

        print(f"Username: {username}, Password: {pwd}")  # Debugging line
        
        admin = db.session.query(Admin).filter((Admin.email == username) | (Admin.username == username) | (Admin.phone == username)).first()
        print(f"Admin found: {admin}")  # Debugging line
        if admin:
            # hashed = admin.admin_pwd
            # confirm_pwd = check_password_hash(hashed,pwd)
            # if confirm_pwd:
            session['admin'] = admin.username
            session['adminisonline'] = admin.id
            flash(message='Login successful!', category='success')
            print("Redirecting to admin dashboard") 
            return redirect(url_for('admin_dashboard'))
        else:
            flash(message='Incorrect username or password!', category='error')
    return render_template('admin/admin_login.html',form=form)

# *********************************** ADMIN LOGIN **************************************************

# *********************************** ADMIN DASHBOARD **************************************************
@app.route('/admin/dashboard/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if 'admin' not in session:
        flash(message='You must be logged in to access the dashboard!', category='error')
        return redirect(url_for('adminlogin'))
    form= AdminLogin()
    admin = db.session.query(Admin).get(session['adminisonline'])
    if not admin:
        flash(message='Admin not found!', category='error')
        return redirect(url_for('adminlogin'))
    
    
    # Fetching all users and projects for the admin dashboard
    users = db.session.query(Users).all()
    project_count = db.session.query(Project).count()

    selected_user = None
    selected_project = None
    if request.method == 'POST':
        if 'selected_user' in request.form and request.form['selected_user']:
            selected_user = db.session.query(Users).get(int(request.form['selected_user']))
        if 'selected_project' in request.form and request.form['selected_project']:
            selected_project = db.session.query(Project).get(int(request.form['selected_project']))
    

    if 'action' in request.form:
            if request.form['action'] == 'delete_user':
                if not selected_user:
                    flash(message='No user selected!', category='error')
                    return redirect(url_for('admin_dashboard'))
                db.session.delete(selected_user)
                db.session.commit()
                flash(message='User deleted successfully!', category='success')
                return redirect(url_for('admin_dashboard'))
            elif request.form['action'] == 'delete_project':
                if not selected_project:
                    flash(message='No project selected!', category='error')
                    return redirect(url_for('admin_dashboard'))
                db.session.delete(selected_project)
                db.session.commit()
                flash(message='Project deleted successfully!', category='success')
                return redirect(url_for('admin_dashboard'))

    return render_template('admin/admin.html',
                           admin=admin,
                           users=users,
                           selected_user=selected_user,
                           selected_project=selected_project,
                            form=form,  # Pass the form for potential use in the template
                            project_count=project_count)
# *********************************** ADMIN DASHBOARD **************************************************


# *********************************** ADMIN PASSWORD RESET **************************************************
@app.route('/admin/reset/')
def adminresetpwd():
    form = AdminPasswordReset()

    return render_template('admin/admin_reset_password.html', form=form)

# *********************************** ADMIN PASSWORD RESET **************************************************

# *********************************** ADMIN LOGOUT **************************************************
@app.route('/user/logout/')
@login_required
def admin_logout():
    if session.get('adminisonline') != None and session.get('admin') != None:
        session.pop('adminisonline',None)
        session.pop('admin', None)        
    return redirect(url_for('adminlogin'))

# *********************************** ADMIN LOGOUT **************************************************