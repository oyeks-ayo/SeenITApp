from functools import wraps
from datetime import datetime
import json,os, secrets
from flask import redirect, url_for,render_template,session,flash,request,jsonify
# from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash

from pkg import app
from pkg.models import db, Users, ContactSeenIT,Profile,ProfileSkill,ProfileService,Project,ProjectMedia
from pkg.forms import ContactUs, SignUpF, UserLogin, AdminLogin,ProfileForm


# ***************************** SIGN UP TO DB *************************************************

@app.route('/signup/submit/',methods=['POST'])
def signup_db():
   

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    mname = request.form.get('mname')
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pwd = request.form.get('password')
    cpwd = request.form.get('cpassword')
    terms = request.form.get('terms')

    check = db.session.query(Users).filter((Users.username == username)|(Users.email == email)|(Users.phone == phone)).first()

    if fname != '' and lname != '' and username != '' and email != '' and phone != '' and pwd != '':
        if pwd != cpwd:
            data2return = {'status':'danger', 'message':'passwords do not match!'}
            return json.dumps(data2return)
        elif terms != 'y':
            data2return = {'status':'danger', 'message':'Kindly agree to terms'}
            return json.dumps(data2return)
        elif check: 
            if check.username == username:
                data2return = {'status':'username', 'message':'Username already taken!'}
                return json.dumps(data2return)
            if check.email == email:
                data2return = {'status':'email', 'message':'Email already taken!'}
                return json.dumps(data2return)
            if check.phone == phone:
                data2return = {'status':'phone', 'message':'Phone Number already taken!'}
                return json.dumps(data2return)
        else:
            terms='Agreed'
            hashed_pwd = generate_password_hash(pwd)
            insert_to_db = Users(fname=fname, 
                                lname=lname, 
                                mname=mname, 
                                username=username, 
                                email=email, 
                                phone=phone, 
                                user_pwd=hashed_pwd, 
                                terms=terms)
            db.session.add(insert_to_db)
            db.session.commit()
            user_id = insert_to_db.id

            if user_id:
                data2return = {'status':'success', 'message':'You have successfully signed up to SeenIT, kindly login to do more'}
                return json.dumps(data2return)
    else:
        data2return = {'status':'danger', 'message': 'Fields with * cannot be empty!'}
        return json.dumps(data2return)

# ***************************** SIGN UP TO DB *************************************************

# ***************************** DECORATOR *************************************************


def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if session.get('isonline') != None:
            return f(*args,**kwargs)
        else:
            flash('You need to be logged in', category='error')
            return redirect(url_for('userLogin'))
    return login_decorator

# ***************************** DECORATOR *************************************************

# ***************************** LOGIN TO DB *************************************************
@app.route('/userlogin/submit/',methods=['POST'])
def userlogin_db():
    access = request.form.get('uname')
    pwd = request.form.get('password')

    if access != '' and pwd !='':

        from_db = db.session.query(Users).filter((Users.email == access) | (Users.username == access) | (Users.phone == access)).first()

        if from_db:
            hashed = from_db.user_pwd
            confirm_pwd = check_password_hash(hashed,pwd)

            if confirm_pwd:
                session['isonline'] = from_db.id
                data2send = {'status':'success','message':f'/profile/page/{session['isonline']}'}
                return json.dumps(data2send)
            else:
                data2send = {'status':'danger','message':'Invalid Password!'}
                return json.dumps(data2send)
        else:
            data2send = {'status':'danger','message':f'{access} is not a registered account, kindly Sign Up'}
            return data2send
    else:
        data2send = {'status':'empty','message':'Input fields cannot be empty!'}
        return json.dumps(data2send)

# ***************************** LOGIN TO DB *************************************************


# ***************************** PROFILE FORM TO DB *************************************************

@app.route("/profileform/update/<int:id>/",methods=["POST"])
def profile_update(id):


    db_profile_pix_name = None
    db_cover_pix_name = None
    profile_pix = None
    cover_pix = None

    if not session.get('isonline'):
        return jsonify({'status':'loggedout', 'msg':'/userlogin/'})

    try:
        user = db.session.query(Users).get_or_404(id)


        fname = request.form.get('fname')
        lname = request.form.get('lname')
        mname = request.form.get('mname')
        dob = request.form.get('dob')
        username = request.form.get('username')
        phone = request.form.get('phone')
        profile_pix = request.files.get('profile_pix')
        cover_pix = request.files.get('cover_pix')
        gender = request.form.get('gender')
        tagline = request.form.get('tagline')
        about = request.form.get('about_me')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        state = request.form.get('state','0')
        web_blog = request.form.get('web_blog')
        social_m = request.form.get('social_m')
        category = request.form.get('category','1')
        services = request.form.getlist('service_type')
        skills = request.form.getlist('skill_set')

        

        
        format = ['.jpg', '.png', '.jpeg', '.webp']

        if profile_pix and profile_pix.filename:
            user_profile_pix_name = profile_pix.filename
            _, ext = os.path.splitext(user_profile_pix_name)
            if ext.lower() in format:
                db_profile_pix_name = secrets.token_hex(10) + ext
                profile_pix.save('pkg/static/uploads/profile_pix/'+db_profile_pix_name)
            else:
                data2send = {'status':'profilepix', "msg":"Invalid image format!"}
                return jsonify(data2send)


        if cover_pix and cover_pix.filename:
            user_cover_pix_name = cover_pix.filename
            _, ext = os.path.splitext(user_cover_pix_name)
            if ext.lower() in format:
                db_cover_pix_name = secrets.token_hex(10) + ext
                cover_pix.save('pkg/static/uploads/cover_pix/'+db_cover_pix_name)
            else:
                data2send = {'status':'profilepix', "msg":"Invalid image format!"}
                return jsonify(data2send)

        if fname =='' or lname == '':
            data2send = {'status':'danger', 'msg':'First name and last name are required!'}
            return jsonify(data2send)

        if not user.profile:
            if state == '0':
                data2send = {'status':'state','msg':'You need to pick your state of residence'}
                return jsonify(data2send)
            
            elif category == '0':
                data2send = {'status':'category','msg':'You need to pick a category'}
                return jsonify(data2send)
            else:
                profile = Profile(
                    user_id = user.id,
                    dob = dob,
                    gender = gender,
                    address1 = address1,
                    address2 = address2,
                    profile_pix = db_profile_pix_name,
                    cover_pix = db_cover_pix_name,
                    slogan = tagline,
                    bio = about,
                    social_media = social_m,
                    blog = web_blog,
                    state_id = int(state),
                    category_id = int(category)
                )
                db.session.add(profile)
                db.session.commit()
                
        else:

            user.fname = fname.upper()
            user.lname = lname.upper()

            if mname:                         
                user.mname = mname.upper()

            if not username:
                data2send = {'status':'no_username','msg':'username cannot be empty!'}
                return  jsonify(data2send)
            else:
                existing_user = db.session.query(Users).filter((Users.username==username), Users.id != id).first()
                if existing_user:
                    if existing_user.username:
                        data2send = {'status':'existing_user','msg':'username taken'}
                        return  jsonify(data2send)
                    else:
                        user.username = username


            if not phone:
                data2send = {'status':'no_phone','msg':'phone number cannot be empty!'}
                return  jsonify(data2send)
            else:
                existing_phone = db.session.query(Users).filter((Users.phone==phone), Users.id != id).first()
                if existing_phone:
                    data2send = {'status':'phone','msg':'phone number is taken'}
                    return jsonify(data2send)
                else:
                    user.phone = phone
            
            profile = user.profile

            if dob == '':
                dob = None
            elif dob:
                dob = datetime.strptime(dob, '%Y-%m-%d')
                profile.dob = dob

            if not gender:
                data2send = {'status':'gender', 'msg':'Please select your gender'}
                return jsonify(data2send)
    
            profile.gender = gender
            profile.address1 = address1
            profile.address2 = address2
            profile.slogan = tagline
            profile.bio = about
            profile.social_media = social_m
            profile.blog = web_blog

            if state == '0':
                data2send = {'status':'state','msg':'You need to pick your state of residence'}
                return jsonify(data2send)
            else:
                profile.state_id = int(state)

            if category == '0':
                data2send = {'status':'category','msg':'You need to pick your category'}
                return jsonify(data2send)
            else:
                profile.category_id = int(category)
                    

            if db_profile_pix_name is not None: 
                profile.profile_pix = db_profile_pix_name
            if db_cover_pix_name is not None:
                profile.cover_pix = db_cover_pix_name


            if services:
                ProfileService.query.filter_by(profile_id=profile.id).delete()
                for service_id in services:
                    pSe = ProfileService(profile_id=profile.id,service_id=int(service_id))
                    db.session.add(pSe)
                    db.session.commit()
                    
            else:
                data2send = {'status':'services','msg':'You need to pick at least one service'}
                return jsonify(data2send)

            if skills:
                ProfileSkill.query.filter_by(profile_id=profile.id).delete()
                for skill_id in skills:
                    pSk = ProfileSkill(profile_id=profile.id,skill_id=int(skill_id))
                    db.session.add(pSk)
                    db.session.commit()
                    
            else:
                data2send = {'status':'skills','msg':'You need to pick at least one skill'}
                return jsonify(data2send)

        db.session.commit()

        data2send = {'status':'success', 'msg':'You profile update was successful!'}
        return jsonify(data2send)
    except Exception as e:
        db.session.rollback()
        return jsonify({'status':'error', 'msg':f'An error occurred: {str(e)}'})
    

        



# ***************************** PROFILE FORM TO DB *************************************************


# *********************************** SEENIT HUB PROJECT TO DB **************************************************
@app.route('/seenIT/hub/db/', methods=['POST'])
@login_required
def seenITHub_db():
    
    user_id = session.get('isonline')

    user = Users.query.get(user_id)

    profile = user.profile

    title = request.form.get('title')
    description = request.form.get('description')
    projects = request.files.getlist('projects')
    print(projects)

    if not title:
        return jsonify({'status':'empty', "msg":"Title is required!"})
    
    if not projects:
        return jsonify({'status':'empty', "msg":"You need to upload a project!"})
    
    pix_format = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    video_format = ['.mp4', '.mov', '.webm']

    processed_files = False
    
    db_project = None

    for media in projects:
        print(media)

        if media.filename == '':
            continue

        media_name = media.filename
        _, ext = os.path.splitext(media_name)

        if ext.lower() in pix_format:
            file_type = 'image'
            db_project = secrets.token_hex(10) + ext
            media.save('pkg/static/uploads/project/project_pix/'+db_project)
            print(f'pictures ===> {db_project}')

        elif ext.lower() in video_format:
            file_type = 'video'
            db_project = secrets.token_hex(10) + ext
            media.save('pkg/static/uploads/project/project_video/'+db_project)
            print(f'video ===> {db_project}')

        else:
            continue
        
        if db_project:
            print(f'pictures ===> {db_project}')
            print(f'video ===> {db_project}')
            

            newP = Project(
            user_id = user_id,
            title=title,
            description=description,
            profile_id=profile.id 
        )

            db.session.add(newP)
            db.session.commit()

            newM = ProjectMedia(project_id=newP.project_id, 
                                file_type=file_type, 
                                filename=db_project
                                )
            db.session.add(newM)
            db.session.commit()

            processed_files = True

    if processed_files:
        return jsonify({'status':'success', "msg":"All files processed successfully!"})
    else:
        return jsonify({'status':'empty', "msg":"No valid files were uploaded!"})
    

# *********************************** SEENIT HUB PROJECT TO DB **************************************************




# ***************************** CONTACT US TO DB *************************************************
@app.route('/contactus/submit/')
def contact_submit():
        fname = request.args.get('fname')
        lname = request.args.get('lname')
        email = request.args.get('email')
        message = request.args.get('message')

        if fname != '' and lname != '' and email != '' and message != '':
            contact_db = ContactSeenIT(fname=fname, lname=lname, email=email, message=message)
            db.session.add(contact_db)
            db.session.commit()
            id =contact_db.contact_id

            if id:
                data2return = {'status':'success', 'message': 'You have been added to our list'}
                return json.dumps(data2return)
            else:
                data2return = {'status':'danger', 'message': 'Error adding your message'}
            return json.dumps(data2return)
        else:
            data2return = {'status':'danger', 'message': 'Complete the fields!'}
            return json.dumps(data2return)

# ***************************** CONTACT US TO DB *************************************************


