from flask_wtf import FlaskForm   # type: ignore
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,EmailField,DateField,FileField,RadioField,SelectField,SelectMultipleField,MultipleFileField # type: ignore
from wtforms.validators import DataRequired,data_required, Email,length  # type: ignore
from flask_wtf.file import FileAllowed # type: ignore

class ContactUs(FlaskForm):
    fname = StringField('First Name ', validators=[DataRequired(message='Your first name is required')])
    lname = StringField('Last Name ', validators=[DataRequired(message='Your last name is required')])
    email = EmailField('Email Address ', validators=[DataRequired('email field required!'),Email(message='Your first name is required')])
    subject = StringField('Subject ', validators=[DataRequired(message='Subject required')])
    message = TextAreaField('Message ', validators=[DataRequired(message='Message cannot be empty!')])
    submit = SubmitField('Send Message')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class SignUpF(FlaskForm):
    fname = StringField('First Name* ', 
                    validators=[data_required(message='Your first name is required')])
    lname = StringField('Last Name* ', 
                    validators=[data_required(message='Your last name is required')])
    mname = StringField('Middle Name ')
    username = StringField('Username* ', 
                    validators=[data_required(message='Your username is required')])
    email = EmailField('Email Address* ',
                    validators=[data_required(message='Your email is required'),
                    Email(message=f'Input a valid email address {fname}')])
    phone = StringField('Phone Number* ', 
                    validators=[data_required(message='Your phone number is required')])
    password = PasswordField('Password*', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    cpassword = PasswordField('Confirm Password*', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    terms = BooleanField('I agree to the Terms of Service and Privacy Policy', 
                    validators=[data_required('Kindly agree to t&c')], default=False)
    submit = SubmitField('Create Account')
    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class ProfileForm(FlaskForm):
    # ************************************* BASIC INFO ***************************************************

    fname = StringField('First Name ', 
                    validators=[data_required(message='Your first name is required')])
    lname = StringField('Last Name ', 
                    validators=[data_required(message='Your last name is required')])
    mname = StringField('Middle Name ')
    username = StringField('Username ', 
                    validators=[data_required(message='Your username is required')])
    profile_pix = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    cover_pix = FileField('Upload Cover Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    dob = DateField('Date of birth', 
                    validators=[data_required(message='Your date of birth is rquired')])
    gender = RadioField('Gender',
                    validators=[data_required('Your Gender is required')],
                    choices=[('male', 'male'),('female','female')])
    tagline = StringField('Your slogan')
    about_me = TextAreaField('Bio/About me')

    # ************************************* CONTACT & LOCATION ***************************************************

    phone = StringField('Phone Number ', 
                    validators=[data_required(message='Your phone number is required')])
    email = EmailField('Email Address ', 
                    validators=[data_required(message='Your email is required'),
                    Email(message=f'Input a valid email address {fname}')])
    address1 = StringField('Your home address')
    address2 = StringField('Additional address')
    state = StringField('State')
    web_blog = StringField('Website/Blog URL')
    social_m = StringField('Social media link')
    
    # ************************************* WORK/SERVICES ***************************************************

    category = SelectField(validators=[data_required('You need to select a category')], choices=[
        ('', 'Select Work Category'),
        ('fashion', 'Fashion & Tailoring'),
        ('beauty', 'Hair & Beauty'),
        ('graphics', 'Graphics & Branding'),
        ('photography', 'Photography'),
        ('furniture', 'Furniture Making'),
        ('catering', 'Catering & Baking'),
        ('renovation', 'Home Renovation'),
        ('tech', 'Tech & Software'),
        ('events', 'Events & Decoration'),
        ('craft', 'Art & Craft'),
        ('others', 'others')
    ])

    category_others = StringField('Supply your category here if unlisted' )

    service_type = SelectMultipleField('Type of Service Offered',validators=[data_required('You need to select a service')], choices=[
    ('personal', 'Personal Service'),
    ('freelance', 'Freelance / Contract Work'),
    ('onsite', 'Onsite Service'),
    ('remote', 'Remote / Online Work'),
    ('training', 'Training / Mentorship'),
    ('sales', 'Product Sales'),
    ('rental', 'Equipment Rental'),
    ('custom_order', 'Custom Orders'),
    ('group_service', 'Group Services'),
    ('event_coverage', 'Event Coverage'),
    ('others', 'others')
    ])

    service_others = StringField('Supply your service here if unlisted' )

    skill_set = SelectMultipleField(
        'Skill Set',
        validators=[data_required('You need to select a skill')],
        choices=[
            ('', 'Select a skill'),
            ('sewing', 'Sewing'),
            ('embroidery', 'Embroidery'),
            ('tailoring', 'Tailoring'),
            ('fashion_illustration', 'Fashion Illustration'),
            ('beading', 'Beading'),

            ('mobile_app_development', 'Mobile App Development'),
            ('ui_ux_design', 'UI/UX Design'),
            ('web_development', 'Web Development'),
            ('data_analysis', 'Data Analysis'),
            ('graphic_design', 'Graphic Design'),

            ('makeup_artistry', 'Makeup Artistry'),
            ('braiding', 'Braiding'),
            ('hair_styling', 'Hair Styling'),
            ('skincare', 'Skincare'),
            ('nail_art', 'Nail Art'),

            ('photography', 'Photography'),
            ('videography', 'Videography'),
            ('logo_design', 'Logo Design'),
            ('content_creation', 'Content Creation'),
            ('storyboarding', 'Storyboarding'),

            ('plumbing', 'Plumbing'),
            ('electrical_repairs', 'Electrical Repairs'),
            ('carpentry', 'Carpentry'),
            ('cleaning_services', 'Cleaning Services'),
            ('interior_design', 'Interior Design'),

            ('catering', 'Catering'),
            ('cake_baking', 'Cake Baking'),
            ('small_chops', 'Small Chops'),
            ('pastry_making', 'Pastry Making'),
            ('drink_mixing', 'Drink Mixing'),

            ('shoe_making', 'Shoe Making'),
            ('bag_making', 'Bag Making'),
            ('handmade_crafts', 'Handmade Crafts'),
            ('leather_works', 'Leather Works'),
            ('accessories_design', 'Accessories Design'),

            ('tutoring', 'Tutoring'),
            ('language_coaching', 'Language Coaching'),
            ('coding_lessons', 'Coding Lessons'),
            ('mentorship', 'Mentorship'),
            ('skill_training', 'Skill Training'),

            ('event_planning', 'Event Planning'),
            ('decoration', 'Decoration'),
            ('mcing', 'MCing'),
            ('djing', 'DJing'),
            ('sound_management', 'Sound Management'),

            ('fitness_coaching', 'Fitness Coaching'),
            ('massage_therapy', 'Massage Therapy'),
            ('nutrition_consulting', 'Nutrition Consulting'),
            ('yoga_instruction', 'Yoga Instruction'),
            ('personal_training', 'Personal Training'),
            ('others','others')
    ])

    skill_others = StringField('Supply your skill here if unlisted' )

    update = SubmitField('Update Profile')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class UserLogin(FlaskForm):
    uname = StringField('Username/Phone Number/Email ', validators=[data_required()])
    password = PasswordField('Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    login = SubmitField('Login')
    remember = BooleanField('Remember me')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2


class SeenITHubUpload(FlaskForm):
    title = StringField('Your Project Title ', validators=[data_required(message='Your project title')])
    description = TextAreaField('Description')
    projects = MultipleFileField('Projects')
    upload = SubmitField('Share it')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class AdminLogin(FlaskForm):
    uname = StringField('Username/Phone Number/Email ', validators=[data_required()])
    password = PasswordField('Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=1, message='Password must must not be less than 1 characters and must be a mix of alphanumeric and special characters')])
    login = SubmitField('Login')
    remember = BooleanField('Remember me')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class AdminRegister(FlaskForm):
    uname = StringField('Username/Phone Number/Email ', validators=[data_required()])
    password1 = PasswordField('Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    
    password2 = PasswordField('Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    login = SubmitField('Login')
    remember = BooleanField('Remember me')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class UserPasswordReset(FlaskForm):
    uname = StringField('Phone Number/Email used in opening this account', validators=[data_required()])
    newpwd = PasswordField('New Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    cnewpwd = PasswordField('Confirm New Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    reset = SubmitField('Reset Password')
    remember = BooleanField('Remember me')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2

class AdminPasswordReset(FlaskForm):
    uname = StringField('Phone Number/Email used in opening this account', validators=[data_required()])
    newpwd = PasswordField('New Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    cnewpwd = PasswordField('Confirm New Password', 
                    validators=[data_required(message='Your password is required'),
                    length(min=7, message='Password must must not be less than 7 characters and must be a mix of alphanumeric and special characters')])
    reset = SubmitField('Reset Password')
    remember = BooleanField('Remember me')

    class Meta:
        csrf = True
        csrf_time_limit = 3600*2