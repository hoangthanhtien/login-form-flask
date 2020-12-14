from enum import unique
import uuid
from app import db
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


def default_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
    # id = db.Column(String(), primary_key=True)
    user_name = db.Column(String(), nullable=False, unique=True, index=True)
    user_email = db.Column(String(), nullable=False, unique=True)
    user_password = db.Column(String(), nullable=False)
    user_phone = db.Column(String(), nullable=True, unique=True)
    user_address = db.Column(String(), nullable=True)
    is_admin = db.Column(Boolean(), default=False)
