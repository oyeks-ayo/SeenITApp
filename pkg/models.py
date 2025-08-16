from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    admin_pwd = db.Column(db.String(200), nullable=False)
    datereg_signup = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('Users', backref='admin', uselist=False)
    profile = db.relationship('Profile', backref='admin', uselist=False)

    def __repr__(self):
        return f"<SignUp {self.username}>"


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    mname = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    user_pwd = db.Column(db.String(200), nullable=False)
    terms = db.Column(db.String(20), default=False)
    datereg_signup = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))


    profile = db.relationship('Profile', backref='user', uselist=False)

    def __repr__(self):
        return f"<SignUp {self.username}>"


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False, server_default='Male')
    address1 = db.Column(db.String(100), nullable=False)
    address2 = db.Column(db.String(100))
    profile_pix = db.Column(db.String(500))
    cover_pix = db.Column(db.String(500))
    slogan = db.Column(db.String(500))
    bio = db.Column(db.Text)
    social_media = db.Column(db.String(200))
    blog = db.Column(db.String(500))
    datereg_profile = db.Column(db.DateTime, default=datetime.utcnow)

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


    # My One-to-Many Relationships
    projects = db.relationship('Project', backref='owner')
    category = db.relationship('Category', backref='profiles')

    # My Association Table Relationships (ProfileSkill and ProfileService)
    profile_skills = db.relationship('ProfileSkill', backref='profile')
    profile_services = db.relationship('ProfileService', backref='profile')

    def __repr__(self):
        return f"<Profile of {self.user.username}>"



class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    datereg_project = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    # RELATIONSHIP BETWEEN PROJECTS AND USERS

    user = db.relationship('Users', backref=db.backref('projects', lazy=True))
    media = db.relationship("ProjectMedia", backref="projects", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Project '{self.title}'>"

class ProjectMedia(db.Model):
    __tablename__ = 'project_media'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    file_type = db.Column(db.String(10))  # 'image' or 'video'
    filename = db.Column(db.String(255))



class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    profiles = db.relationship('ProfileSkill', backref='skill')

    def __repr__(self):
        return f"<Skill {self.name}>"

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    profiles = db.relationship('ProfileService', backref='service')

    def __repr__(self):
        return f"<Service {self.name}>"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    profiles = db.relationship('Profile', backref='state')

    def __repr__(self):
        return f"<State {self.name}>"



class ProfileSkill(db.Model):
    __tablename__ = 'profile_skills'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))

    def __repr__(self):
        return f"<ProfileSkill profile={self.profile_id} skill={self.skill_id}>"

class ProfileService(db.Model):
    __tablename__ = 'profile_services'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    def __repr__(self):
        return f"<ProfileService profile={self.profile_id} service={self.service_id}>"


class ContactSeenIT(db.Model):
    __tablename__ = 'contact_seenit'
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    datereg_contact = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Contact from {self.email}>"



