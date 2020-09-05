from flask_login import UserMixin
from . import db

# TODO: change to table type?
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

ReportingEntity = db.Table('reporting_entity',
    id = db.Column(db.String(1000), primary_key=True, nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    primary = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String, nullable=False)
    osm_id = db.Column(db.String, nullable=True)
    geohash = db.Column(db.String, nullable=True)
)

EntityProperty = db.Table('entity_property',
    # Composite primary key
    id = db.Column(db.String(1000), db.ForeignKey('reporting_entity.id'), nullable=False, primary_key=True)
    entity_property = db.Column(db.String(1000), nullable=False, primary_key=True)
    numeric = db.Column(db.Boolean, nullable=False)
    num_value = db.Column(db.Float, nullable=True)
    str_value = db.Column(db.String, nullable=True)
)

EntityToSubentity = db.Table('entity_to_subentity',
    # Composite primary foreign key
    entity_id = db.Column(db.String(1000), db.ForeignKey('reporting_entity.id'), nullable=False, primary_key=True)
    subentity_id = db.Column(db.String(1000), db.ForeignKey('reporting_entity.id'), nullable=False, primary_key=True)
)

UserToEntity = db.Table('user_to_entity',
    # Composite primary foreign key
    user_id = db.Column(db.String(1000), db.ForeignKey(User.id), nullable=False, primary_key=True)
    entity_id = db.Column(db.String(1000), db.ForeignKey('reporting_entity.id'), nullable=False, primary_key=True)
)

SuperUser = db.Table('superuser',
    superuser_id = db.Column(db.String(1000), db.ForeignKey(User.id), nullable=False, primary_key=True)
)