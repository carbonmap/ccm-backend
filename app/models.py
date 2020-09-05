from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

class ReportingEntity(UserMixin, db.Model):
    id = db.Column(db.String(1000), primary_key=True, nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    primary = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String, nullable=False)
    osm_id = db.Column(db.String, nullable=True)
    geohash = db.Column(db.String, nullable=True)

class EntityProperty(UserMixin, db.Model):
    # Composite primary key
    id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)
    entity_property = db.Column(db.String(1000), nullable=False, primary_key=True)
    numeric = db.Column(db.Boolean, nullable=False)
    num_value = db.Column(db.Float, nullable=True)
    str_value = db.Column(db.String, nullable=True)

class EntityToSubentity(UserMixin, db.Model):
    # Composite primary foreign key
    entity_id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)
    subentity_id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)

class UserToEntity(UserMixin, db.Model):
    # Composite primary foreign key
    user_id = db.Column(db.String(1000), db.ForeignKey(User.id), nullable=False, primary_key=True)
    entity_id = db.Column(db.String(1000), db.ForeignKey(ReportingEntity.id), nullable=False, primary_key=True)

class SuperUser(UserMixin, db.Model):
    superuser_id = db.Column(db.String(1000), db.ForeignKey(User.id), nullable=False, primary_key=True)