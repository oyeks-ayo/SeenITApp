import logging
from datetime import datetime
from functools import wraps
import json
from sqlalchemy import func # type: ignore
from flask import Blueprint,render_template,request,redirect,url_for,flash,make_response,session
from flask_wtf.csrf import CSRFError, generate_csrf # type: ignore
from pkg import csrf
from pkg.models import db,ContactSeenIT, Users,Profile,Skill,Category,Service,State,ProfileService,ProfileSkill,Project
from pkg.forms import ContactUs,SignUpF, ProfileForm, UserLogin,UserPasswordReset,SeenITHubUpload

# Create blueprint instead of using app directly
user_bp = Blueprint('user', __name__)

logger = logging.getLogger(__name__)
# *********************************** HOMEPAGE **************************************************


# *********************************** INJECTIONS **************************************************
@user_bp.context_processor
def inject_users():

# **************FOR NAVBAR****************
    user = None
    navuser = None
    if 'isonline' in session:
        navuser = db.session.query(Users).get(session['isonline'])
# **************FOR NAVBAR****************

# **************FOR CSRF TOKEN AND SERACH BOX****************
    users = db.session.query(Users).all()
    for user in users:
        user_id = user.id

    return dict(navuser=navuser,
                users=users,
                user=user, 
                user_id=user_id,
                csrf_token=generate_csrf)
# **************FOR CSRF TOKEN AND SERACH BOX****************

# *********************************** INJECTIONS **************************************************


@user_bp.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response


@user_bp.route('/')
def home():
    return render_template('users/homepage.html')

# *********************************** HOMEPAGE **************************************************

# *********************************** ABOUT US **************************************************

@user_bp.route('/aboutUs/')
def about_us():
    try:
        # Fetch the total number of users from the database
        no_users = db.session.query(Users).count()
        return render_template('users/About_Us.html',users=no_users)

    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        db.session.rollback()
        flash(f'An error occurred: {e}', 'error')
        return redirect(url_for('user.home'))

# *********************************** ABOUT US **************************************************
    
    
# *********************************** SIGN UP **************************************************

@user_bp.route('/signUp/')
def signUp():
    form = SignUpF()
    return render_template('users/sign_up.html',form=form)

# *********************************** SIGN UP **************************************************

# *********************************** LOGIN **************************************************

@user_bp.route('/userlogin/')
def userLogin():
    form = UserLogin()
    return render_template('users/user_login.html',form=form)

# *********************************** LOGIN **************************************************

# *********************************** LOGIN DECORATOR **************************************************

def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if session.get('isonline') != None:
            return f(*args,**kwargs)
        else:
            flash('You need to be logged in before you can visit page', category='error')
            return redirect(url_for('user.userLogin'))
    return login_decorator
# *********************************** LOGIN DECORATOR **************************************************

# *********************************** USER LOGOUT **************************************************
@user_bp.route('/user/logout/')
@login_required
def user_logout():
    if session.get('isonline') != None:
        session.pop('isonline',None)        
    return redirect(url_for('user.userLogin'))
# *********************************** USER LOGOUT **************************************************


# *********************************** CONTACT US **************************************************



@user_bp.get('/contactus/')
def contact():
    form = ContactUs()
    return render_template('users/contact_us.html', form=form)



# *********************************** CONTACT US **************************************************


# *********************************** HUB **************************************************

@user_bp.route('/seenIT/hub/project/<int:project_id>', methods=['GET'])
@login_required
def seenITHubProject(project_id):
    try:
        user_id = session.get('isonline')
        user = db.session.query(Users).get_or_404(user_id)
        project = Project.query.get_or_404(project_id)

        return render_template(
            'users/seenITHub.html',
            project=project,
            user=user
        )
    except CSRFError as e:
        flash(f'CSRF Error: {e}', 'error')
        return redirect(url_for('user.seenITHub'))
    
# *********************************** HUB **************************************************


# *********************************** SEENIT HUB PAGE **************************************************
@user_bp.route('/seenIT/hub/', methods=['GET'])
@login_required
def seenITHub():

    try:
        user_id = session.get('isonline')
        user = db.session.query(Users).get_or_404(user_id)
        profile = user.profile
        all_users = db.session.query(Users).filter(Users.projects != None).all()
        all_projects = db.session.query(Project).order_by(Project.datereg_project.desc()).all()
        # all_users = db.session.query(Users).filter(Users.profile != None).filter(Profile.projects.any()).order_by(Users.datereg_signup.desc()).all()
        skills = Skill.query.order_by(Skill.name).all()
        services = Service.query.order_by(Service.name).all()
        categories = Category.query.order_by(Category.name).all()
        states = State.query.order_by(State.name).all()
        profile_pix = profile.profile_pix if profile else None
        cover_pix = profile.cover_pix if profile else None

        for pro in all_projects:
            for media in pro.media:
                if media.file_type == 'image':
                    img = media.filename
                elif media.file_type == 'video':
                    vid = media.filename

        return render_template(
            'users/seenITHub.html',
            form=SeenITHubUpload(),
            users=all_users,
            profile_pix=profile_pix,
            cover_pix=cover_pix,
            categories=categories,
            services=services,
            skills=skills,
            states=states,
            projects=all_projects,
            user=user,
            user_projects=profile.projects if profile else [])
    except CSRFError as e:
        flash(f'CSRF Error: {e}', 'error')
        return redirect(url_for('user.seenITHub'))
                 

# *********************************** SEENIT HUB PAGE **************************************************

# *********************************** SEENIT HUB PAGE CATEGORY SEARCH **************************************************


# *********************************** SEENIT HUB PAGE CATEGORY SEARCH**************************************************
@user_bp.route('/category/filter/')
@login_required
def category_filter():
    try:
        cat_id = request.form.get('category_id')
        
        # Fetch projects based on filter
        if cat_id:
            projects = db.session.query(Project).filter(Project.category_id == cat_id).all()
        else:
            # If no category is selected, get all projects
            projects = db.session.query(Project).all()
            
        # Check if the request is an AJAX request (for filtering)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Render JUST the project grid HTML using a template string or a Jinja macro
            data2send = render_template('users/projectfilter.html', projects=projects)
        
        return data2send
    except Exception as e:
        logger.error(f"Error in category_filter: {str(e)}", exc_info=True)
        flash('An error occurred while filtering projects.', 'error')
        return redirect(url_for('seenITHub'))
    except CSRFError as e:
        flash(f'CSRF Error: {e}', 'error')
        return redirect(url_for('user.seenITHub'))



# *********************************** PROFILE PAGE **************************************************
@user_bp.route('/profile/page/<int:id>/')
@login_required
def profile_page(id):

    try:
        s_id = session['isonline']
        user = db.session.query(Users).get_or_404(id)

        profile = user.profile
        project = user.projects

        if profile:

            blog = profile.blog
            link = profile.social_media
            category = profile.category
            social = profile.social_media
            profile_pix = profile.profile_pix
            cover_pix = profile.cover_pix
            bio = profile.bio
            dob = profile.dob.strftime('%b %d') if profile.dob else None
            slogan = profile.slogan
            state = profile.state.name
            skills = profile.profile_skills if profile else []
            # services = profile.service if profile else []
            services = profile.profile_services if user.profile else []
            projects = profile.projects if profile.projects else []

        else:

            projects = project if project else []
            blog = ''
            link = ''
            category = None
            social = ''
            profile_pix = None
            cover_pix = None
            slogan = ''
            bio = ''
            state = ''
            skills = []
            services = []

        # If the user does not have a profile, we can still access its attributes
        # If the user has a profile, we can access its attributes

        name = user.fname + ' ' + user.lname
        username = user.username
        phone = user.phone
        email = user.email
    

        return render_template('users/profile_page.html',user=user,
                                                        name=name,
                                                        username=username,
                                                        phone=phone,
                                                        email=email,
                                                        blog=blog,
                                                        link=link,
                                                        skills=skills,
                                                        bio=bio,
                                                        category=category,
                                                        services=services,
                                                        social=social,
                                                        state=state,
                                                        slogan=slogan,
                                                        profile_pix=profile_pix,
                                                        cover_pix=cover_pix,
                                                        s_id=s_id,
                                                        dob=dob,
                                                        projects=projects)
    except CSRFError as e:
        flash(f'CSRF Error: Token error', 'error')
        return redirect(url_for('user.seenITHub'))
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        db.session.rollback()
        flash(f'An error occurred: {e}', 'error')
        return redirect(url_for('user.profile_page',id=id))

# *********************************** PROFILE PAGE **************************************************

# *********************************** PROFILE FORM **************************************************
@user_bp.route('/profileform/<int:id>/')
@login_required
def profile_form(id):

    try:
        user_p = (
            db.session.query(Users)
            .join(Profile, Users.id == Profile.user_id)
            .outerjoin(ProfileSkill, Profile.id == ProfileSkill.profile_id)
            .outerjoin(ProfileService, Profile.id == ProfileService.profile_id)
            .outerjoin(Skill, ProfileSkill.skill_id == Skill.id)
            .outerjoin(Service, ProfileService.service_id == Service.id)
            .outerjoin(Category, Profile.category_id == Category.id)
            .filter(Users.id == id)
            .first()
        )

        user = db.session.query(Users).get_or_404(id)

        form = ProfileForm(obj=user)

        skills = Skill.query.order_by(Skill.name).all()
        services = Service.query.order_by(Service.name).all()
        category = Category.query.order_by(Category.name).all()
        state  = State.query.order_by(State.name).all()
        profile = user.profile if user.profile else None

        return render_template('users/profile_form.html',form=form,
                                                    category=category,
                                                    skills=skills,
                                                    services=services,
                                                    state=state,
                                                    user=user if not user_p else user_p,
                                                    profile=profile)
    except CSRFError as e:
        flash(f'CSRF Error: {e}', 'error')
        return redirect(url_for('user.profile_page', id=id))
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        db.session.rollback()
        flash(f'An error occurred: {e}', 'error')
        return redirect(url_for('user.profile_page', id=id))
                                                    

  

# *********************************** PROFILE FORM **************************************************

# *********************************** ALL PROJECTS **************************************************
@user_bp.route('/all/projects/<int:id>/')
@login_required
def all_projects(id):
    user = Users.query.get_or_404(id)
    projects = Project.query.filter_by(user_id=user.id)\
              .order_by(Project.datereg_project.desc())\
              .all()
    profile = db.session.query(Profile).filter(Profile.user_id == id).first()
    media = db.session.query(Project).join(Project.media).filter(Project.user_id == id).all()
    return render_template('users/all_projects.html', user=user,
                                                    projects=projects,
                                                    profile=profile,
                                                    media=media)
# *********************************** ALL PROJECTS **************************************************

# *********************************** A SINGLE PROJECT'S PAGE **************************************************
@user_bp.route('/project/<int:id>/<title>/<profile_id>/')
@login_required
def project(id, title, profile_id):
    print(title)
    user = Users.query.get_or_404(id)
    project = db.session.query(Project).filter(Project.user_id == id, Project.profile_id == profile_id, Project.title == title).first() 
    # project = db.session.query(Project).join(Users, Project.user_id == Users.id).filter(Project.profile_id == profile_id, Project.datereg_project == date).all()
    profile = db.session.query(Profile).get_or_404(profile_id)

    return render_template('users/project_page.html',
                           user=user,
                           project=project,
                           profile=profile)

# *********************************** A SINGLE PROJECT'S PAGE **************************************************


# *********************************** PROFILE PAGE OF ANOTHER **************************************************
@user_bp.route('/profile/another/')
@login_required
def profileAnother():
    return render_template('users/profile_page_of_another.html')

# *********************************** PROFILE PAGE OF ANOTHER **************************************************


# *********************************** USER PASSWORD RESET **************************************************
@user_bp.route('/user/reset/')
@login_required
def userresetpwd():
    form = UserPasswordReset()
    return render_template('users/user_password_reset.html', form=form)

# *********************************** USER PASSWORD RESET **************************************************

# *********************************** USER SEARCH **************************************************

@user_bp.route('/user/search/', methods=['GET', 'POST'])
@login_required
def user_search():
    u_id = session.get('isonline')
    try:
        # Fetch current user's project (optional, for context)
        project = db.session.query(Project).filter(Project.user_id == u_id).first()

        if request.method == 'POST':
            search_query = request.form.get('search_query', '').strip()
            logger.info(f"Search query: {search_query}")
            if not search_query:
                flash('Please enter a search term.', 'error')
                return redirect(url_for('user.user_search'))

            # Search for users based on fname, lname, or username
            users = db.session.query(Users)\
                .join(Project, Users.id == Project.user_id, isouter=True)\
                .filter(
                    Users.fname.ilike(f'%{search_query}%') |
                    Users.lname.ilike(f'%{search_query}%') |
                    Users.username.ilike(f'%{search_query}%')
                )\
                .distinct()\
                .all()

            if not users:
                flash('No users found matching your search criteria.', 'info')
                return redirect(url_for('user.user_search'))

            return render_template('users/searchpage.html',
                                  users=users,
                                  search_query=search_query,
                                  current_project=project)

        # Handle GET request
        return render_template('users/searchpage.html',
                              users=[],
                              search_query='',
                              current_project=project)

    except Exception as e:
        logger.error(f"Error in user_search: {str(e)}", exc_info=True)
        flash('An error occurred while searching.', 'error')
        return redirect(url_for('user.user_search'))
# *********************************** USER SEARCH **************************************************

# *********************************** ERROR PAGES **************************************************

@user_bp.errorhandler(404)
def page_not_found(e):
    # Log the error details
    logger.error(f"404 Error: {str(e)}", exc_info=True)
    # Return a custom 404 error page
    return render_template('users/errorpage.html', error404=e), 404

@user_bp.errorhandler(500)
def internal_server_error(e):
    # Log the error details
    logger.error(f"500 Error: {str(e)}", exc_info=True)
    # Return a custom 500 error page
    return render_template('users/errorpage.html', error500=e), 500

@user_bp.errorhandler(403)
def forbidden(e):
    # Log the error details
    logger.error(f"403 Error: {str(e)}", exc_info=True)
    # Return a custom 403 error page
    return render_template('users/errorpage.html', error403=e), 403


# *********************************** ERROR PAGES **************************************************

from sqlalchemy import text  # type: ignore # <-- ADD THIS IMPORT

@user_bp.route('/health')
def health_check():
    try:
        # FIX: Use text() for explicit SQL declaration
        db.session.execute(text('SELECT 1'))  # <-- ADD text() here
        return {
            'status': 'healthy', 
            'database': 'connected',
            'service': 'SeenIT'
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy', 
            'database': 'disconnected', 
            'error': str(e)
        }, 500
    
# *********************************** FILTER BY CATEGORY **************************************************

@user_bp.route('/filter/category/<int:category_id>/', methods=['GET'])
@login_required
def filter_by_category(category_id):
    try:
        # Fetch the category by ID
        category = db.session.query(Category).get_or_404(category_id)
        
        # Fetch all users who have projects in the specified category
        users = db.session.query(Users)\
            .join(Project, Users.id == Project.user_id)\
            .filter(Project.category_id == category.id)\
            .distinct()\
            .all()
        
        if not users:
            flash('No users found in this category.', 'info')
            return redirect(url_for('user.seenITHub'))

        return render_template('users/filter_by_category.html', 
                               users=users, 
                               category=category)

    except Exception as e:
        logger.error(f"Error filtering by category: {str(e)}", exc_info=True)
        flash('An error occurred while filtering by category.', 'error')
        return redirect(url_for('user.seenITHub'))

# *********************************** FILTER BY CATEGORY **************************************************

# *********************************** TIME FUNCTION **************************************************


# @user_bp.template_filter('time_ago')
def time_ago_filter(dt):
    now = datetime.utcnow()
    diff = now - dt
    
    periods = [
        ('year', 365*24*60*60),
        ('month', 30*24*60*60),
        ('day', 24*60*60),
        ('hour', 60*60),
        ('minute', 60)
    ]
    
    for period, seconds in periods:
        value = diff.total_seconds() // seconds
        if value:
            return f"{int(value)} {period}{'s' if value > 1 else ''} ago"
    return "just now"


# <small>Posted {{ project.datereg_project|time_ago }}</small>
# {Example output: "3 hours ago" #}
# *********************************** TIME FUNCTION **************************************************