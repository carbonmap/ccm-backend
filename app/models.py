from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(1000))
    org = db.Column(db.String(1000))
    user_type = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.String(100))
    registered_on = db.Column(db.DateTime)
    confirmed = db.Column(db.String(100))
    confirmed_on = db.Column(db.DateTime)

class ReportingEntity(db.Model):
    id = db.Column(db.String(1000), primary_key=True, nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    primary = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String, nullable=False)
    osm_id = db.Column(db.String, nullable=True)
    geohash = db.Column(db.String, nullable=True)

class EntityProperty(db.Model):
    # Composite primary key
    id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)
    entity_property = db.Column(db.String(1000), nullable=False, primary_key=True)
    numeric = db.Column(db.Boolean, nullable=False)
    num_value = db.Column(db.Float, nullable=True)
    str_value = db.Column(db.String, nullable=True)

class EntityToSubentity(db.Model):
    # Composite primary foreign key
    entity_id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)
    subentity_id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)

class UserToEntity(db.Model):
    # Composite primary foreign key
    user_id = db.Column(db.String(1000), db.ForeignKey(User.id), nullable=False, primary_key=True)
    entity_id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)

class SuperUser(db.Model):
    superuser_id = db.Column(db.String(1000), db.ForeignKey(User.id), nullable=False, primary_key=True)