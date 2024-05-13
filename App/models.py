from datetime import datetime
# 导入SQLAlchemy模块
from flask import jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# 初始化db
db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    user_id = db.Column(db.String(200), primary_key=True)
    user_name = db.Column(db.String(16))
    password = db.Column(db.String(200))
    user_phone = db.Column(db.String(11))
    user_pic = db.Column(db.String(1000))
    user_question = db.Column(db.String(200))
    user_answer = db.Column(db.String(200))
    user_role = db.Column(db.Integer)
    user_class = db.Column(db.String(200))

    __tablename__ = 'user'

    def __init__(self, u_id, username, password, u_phone, u_pic_url, u_question, u_answer, u_role, u_class):
        self.user_id = u_id
        self.user_name = username
        self.password = password
        self.user_phone = u_phone
        self.user_pic = u_pic_url
        self.user_question = u_question
        self.user_answer = u_answer
        self.user_role = u_role
        self.user_class = u_class

    def save(self):
        db.session.add(self)
        db.session.commit()


class Message(db.Model):
    """消息模型"""
    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    message_content = db.Column(db.String(200))
    message_from = db.Column(db.String(200))
    message_to = db.Column(db.String(200))
    """read 0代表未读 1代表已读"""
    message_read = db.Column(db.String(200))
    message_create_time = db.Column(db.DateTime, default=datetime.now)

    __tablename__ = 'message'

    def __init__(self, m_content, m_from, m_to):
        self.message_content = m_content
        self.message_from = m_from
        self.message_to = m_to
        self.message_read = "0"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Notice(db.Model):
    """通知模型"""
    notice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    notice_title = db.Column(db.String(200))
    notice_content = db.Column(db.String(200))
    notice_author = db.Column(db.String(200))
    notice_type = db.Column(db.Integer)
    notice_read = db.Column(db.String(1000))
    notice_create_time = db.Column(db.DateTime, default=datetime.now)
    notice_class = db.Column(db.String(200))

    __tablename__ = 'notice'

    def __init__(self, n_title, n_content, n_author, n_type, n_class):
        self.notice_title = n_title
        self.notice_content = n_content
        self.notice_author = n_author
        self.notice_type = n_type
        self.notice_read = ""
        self.notice_class = n_class

    def save(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User


class NoticeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notice


class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Message
