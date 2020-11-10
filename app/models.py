from dataclasses import dataclass
from flask_login import UserMixin
from datetime import datetime
from . import db


@dataclass
class User(UserMixin, db.Model):
    id: str
    name: str
    org: str
    user_type: str
    email: str
    password: str
    admin: str
    registered_on: datetime
    confirmed: str
    confirmed_on: datetime

    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(100))
    org = db.Column(db.String(500))
    user_type = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.String(100))
    registered_on = db.Column(db.DateTime)
    confirmed = db.Column(db.String(100))
    confirmed_on = db.Column(db.DateTime)


@dataclass
class ReportingEntity(db.Model):
    id: str
    name: str
    primary_display: bool
    status: str
    osm_id: str
    centerpoint: str

    id = db.Column(db.String(256), primary_key=True, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    primary_display = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    osm_id = db.Column(db.String(100), nullable=True)
    centerpoint = db.Column(db.String(20), nullable=True)


@dataclass
class EntityProperty(db.Model):
    id: str
    property: str
    is_numeric: bool
    numb_value: float
    str_value: str

    # Composite primary key
    id = db.Column(
        db.String(256),
        db.ForeignKey(ReportingEntity.id),
        nullable=False,
        primary_key=True,
    )
    property = db.Column(db.String(50), nullable=False, primary_key=True)
    is_numeric = db.Column(db.Boolean, nullable=False)
    numb_value = db.Column(db.Float, nullable=True)
    str_value = db.Column(db.String(500), nullable=True)


@dataclass
class EntityToSubentity(db.Model):
    entity_id: str
    subentity_id: str
    # Composite primary foreign key
    entity_id = db.Column(
        db.String(256),
        db.ForeignKey(ReportingEntity.id),
        nullable=False,
        primary_key=True,
    )
    subentity_id = db.Column(
        db.String(256),
        db.ForeignKey(ReportingEntity.id),
        nullable=False,
        primary_key=True,
    )


@dataclass
class UserToEntity(db.Model):
    user_id: str
    entity_id: str
    role: str
    # Composite primary foreign key
    user_id = db.Column(
        db.String(40), db.ForeignKey(User.id), nullable=False, primary_key=True
    )
    entity_id = db.Column(
        db.String(256),
        db.ForeignKey(ReportingEntity.id),
        nullable=False,
        primary_key=True,
    )
    role = db.Column(db.String(500), nullable=False)


@dataclass
class SuperUser(db.Model):
    superuser_id: str
    superuser_id = db.Column(
        db.String(40), db.ForeignKey(User.id), nullable=False, primary_key=True
    )
