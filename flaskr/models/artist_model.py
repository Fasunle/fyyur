from flaskr.models import db


class Artist(db.Model):
    """
    Artist model inherit from a base class and thus, we can manipulate the class using  
    Args:
        db (BaseModel): BaseModel is an SQLAlchemy base class 

        you could check this: 

        https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/#model-class
    """
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(120), nullable=False)
    show = db.relationship("Show", cascade="all, delete-orphan")
