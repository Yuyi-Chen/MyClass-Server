from datetime import datetime

import pybase64

from flask import Blueprint, request, session, jsonify
from sqlalchemy import extract
from sqlalchemy import or_, and_
from App.models import db, User, Notice, Message, UserSchema, NoticeSchema, MessageSchema

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/create_db/')
def create_db():
    """
    创建数据库
    """
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    """
    删除数据库
    """
    db.drop_all()
    return '删除成功'


# 角色规定 0：班主任 1.班长 2.副班长 3.团支部书记 4.文体委员 5.学习委员 6.普通学生
@user_blueprint.route('/add_student/', methods=['GET', 'POST'])
def add_student():
    """
    添加学生
    """

    if request.method == 'POST':
        # 获取用户填写的信息
        u_id = request.form.get('user_id')
        username = request.form.get('user_name')
        u_phone = request.form.get('user_phone')
        u_class = request.form.get('class_id')
        flag = True
        if not all([u_id, username, u_phone]):
            msg, flag = '请填写完整信息', False
        # 判断用户名是长度是否大于16
        if len(username) > 16:
            msg, flag = '用户名太长', False
        if len(u_phone) != 11:
            msg, flag = '手机号码输入错误', False
        # 如果上面的检查有任意一项没有通过就返回注册页面,并提示响应的信息
        if not flag:
            return jsonify(code=100, msg=msg)

        # 核对输入的用户是否已经被注册了
        # u = User.query.filter(User.user_id == u_id).first()
        # 判断用户名是否已经存在
        # if u:
        #    msg = '用户名已经存在'
        #    return jsonify(code=100, msg=msg)
        # 上面的验证全部通过后就开始创建新用户
        user = User(u_id=u_id, username=username, password=u_id, u_phone=u_phone, u_pic_url="",
                    u_question=" ",
                    u_answer=" ",
                    u_class=u_class,
                    u_role=6)
        # 保存注册的用户
        user.save()
        # 跳转到登录页面
        return jsonify(code=200, msg="添加成功")


@user_blueprint.route('/add_teacher/', methods=['GET', 'POST'])
def add_teacher():
    """
    添加老师
    """

    if request.method == 'POST':
        # 获取用户填写的信息
        u_id = request.form.get('user_id')
        username = request.form.get('user_name')
        u_phone = request.form.get('user_phone')
        flag = True
        if not all([u_id, username, u_phone]):
            msg, flag = '请填写完整信息', False
        # 判断用户名是长度是否大于16
        if len(username) > 16:
            msg, flag = '用户名太长', False
        if len(u_phone) != 11:
            msg, flag = '手机号码输入错误', False
        # 如果上面的检查有任意一项没有通过就返回注册页面,并提示响应的信息
        if not flag:
            return jsonify(code=100, msg=msg)

        # 核对输入的用户是否已经被注册了
        # u = User.query.filter(User.user_id == u_id).first()
        # 判断用户名是否已经存在
        # if u:
        #    msg = '用户名已经存在'
        #    return jsonify(code=100, msg=msg)
        # 上面的验证全部通过后就开始创建新用户
        user = User(u_id=u_id, username=username, password=u_id, u_phone=u_phone, u_pic_url="",
                    u_question=" ",
                    u_answer=" ",
                    u_class=u_id,
                    u_role=0)
        # 保存注册的用户
        user.save()
        # 跳转到登录页面
        return jsonify(code=200, msg="添加成功")


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录
    """
    if request.method == 'POST':
        u_id = request.form.get('user_id')
        password = request.form.get('password')
        # 核对用户名和密码是否一致
        user = User.query.filter_by(user_id=u_id, password=password).first()
        # 如果用户名和密码一致
        if user:
            return jsonify(code=200, msg="登录成功")
        # 如果用户名和密码不一致返回登录页面,并给提示信息
        else:
            msg = '用户名或者密码不一致'
            return jsonify(code=100, msg=msg)


@user_blueprint.route('/userlist/', methods=['GET', 'POST'])
def user_list():
    """用户信息列表"""
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        users = User.query.filter(User.user_class == class_id).all()
        user_schema = UserSchema(many=True)
        user_data = user_schema.dump(users)
        return jsonify(user_data)


@user_blueprint.route('/get_user/', methods=['GET', 'POST'])
def get_user():
    """获取用户信息"""
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        users = User.query.filter(User.user_id == user_id).first()
        user_schema = UserSchema(many=False)
        user_data = user_schema.dump(users)
        return jsonify(user_data)


@user_blueprint.route('/substu/', methods=['GET', 'POST'])
def sub_stu():
    """删除学生"""

    if request.method == 'POST':
        s_id = request.form.get('user_id')
        stu = User.query.filter(User.user_id == s_id).first()
        if stu:
            db.session.delete(stu)
            db.session.commit()
            return jsonify(code=200, msg="删除学生成功")
        msg = '学生学号不存在'
        return jsonify(code=200, msg=msg)


@user_blueprint.route('/changerole/', methods=['GET', 'POST'])
def change_role():
    """更改角色"""

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_role = request.form.get('user_role')
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            user.user_role = user_role
            user.save()
            return jsonify(code=200, msg="更改角色成功")
        else:
            return jsonify(code=100, msg="用户不存在")


@user_blueprint.route('/changepwd/', methods=['GET', 'POST'])
def change_password():
    """修改用户密码"""
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            if pwd1 == user.password:
                user.password = pwd2
                user.save()
                msg = '更改成功'
                return jsonify(code=200, msg=msg)
            else:
                msg = '请输入正确的旧密码'
                return jsonify(code=100, msg=msg)
        else:
            msg = '用户不存在'
            return jsonify(code=100, msg=msg)


@user_blueprint.route('/notice/', methods=['GET', 'POST'])
def notice():
    """
    发布通知
    """
    if request.method == 'POST':
        type = request.form.get('type')
        author = request.form.get('author')
        n_title = request.form.get('notice_title')
        n_content = request.form.get('notice_content')
        user = User.query.filter(User.user_id == author).first()
        notice = Notice(n_title=n_title, n_content=n_content, n_author=author, n_type=type, n_class=user.user_class)
        notice.save()
        return jsonify(code=200, msg="添加通知成功")


@user_blueprint.route('/noticelist_today/', methods=['GET', 'POST'])
def notice_list():
    """当日通知列表"""
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        # 查询某年某月某日数据
        notices = db.session.query(Notice).filter(
            extract('day', Notice.notice_create_time) == datetime.now().day,
            extract('year', Notice.notice_create_time) == datetime.now().year,
            extract('month', Notice.notice_create_time) == datetime.now().month,
            Notice.notice_class == class_id
        ).all()

        notice_schema = NoticeSchema(many=True)
        notice_data = notice_schema.dump(notices)
        return jsonify(code=200, msg='查询成功', notice_data=notice_data)


@user_blueprint.route('/getnotice/', methods=['GET', 'POST'])
def get_notice():
    if request.method == 'POST':
        year = request.form.get('year')
        month = request.form.get('month')
        day = request.form.get('day')
        class_id = request.form.get('class_id')
        # 查询某年某月某日数据
        notices = db.session.query(Notice).filter(
            extract('day', Notice.notice_create_time) == day,
            extract('year', Notice.notice_create_time) == year,
            extract('month', Notice.notice_create_time) == month,
            Notice.notice_class == class_id).all()

        notice_schema = NoticeSchema(many=True)
        notice_data = notice_schema.dump(notices)

        return jsonify(code=200, msg='查询成功', notice_data=notice_data)


@user_blueprint.route('/readnotice/', methods=['GET', 'POST'])
def read_notice():
    if request.method == 'POST':
        notice_id = request.form.get('notice_id')
        user_id = request.form.get('user_id')
        notice = Notice.query.filter(Notice.notice_id == notice_id).first()
        if notice.notice_read == "":
            notice.notice_read = notice.notice_read + user_id
        else:
            notice.notice_read = notice.notice_read + ',' + user_id
        notice.save()
        return jsonify(code=200, msg='操作成功')


@user_blueprint.route('/message/', methods=['GET', 'POST'])
def message():
    """
    发消息
    """
    if request.method == 'POST':
        message_from = request.form.get('message_from')
        message_to = request.form.get('message_to')
        message_content = request.form.get('message_content')
        message = Message(m_content=message_content, m_from=message_from, m_to=message_to)
        message.save()
        return jsonify(code=200, msg="发送成功")


@user_blueprint.route('/meslist_tome/', methods=['GET', 'POST'])
def mes_list():
    """发送给我的消息列表"""
    if request.method == 'POST':
        u_id = request.form.get('user_id')
        mess = Message.query.filter(Message.message_to == u_id).all()
        mes_schema = MessageSchema(many=True)
        mes_data = mes_schema.dump(mess)
        return jsonify(mes_data)


@user_blueprint.route('/meslist_notread/', methods=['GET', 'POST'])
def mes_not_read():
    if request.method == 'POST':
        u_id = request.form.get('user_id')
        mess = Message.query.filter(Message.message_to == u_id, Message.message_read == "0").all()
        mes_schema = MessageSchema(many=True)
        mes_data = mes_schema.dump(mess)
        return jsonify(mes_data)


@user_blueprint.route('/readmessage/', methods=['GET', 'POST'])
def read_message():
    if request.method == 'POST':
        message_id = request.form.get('message_id')
        mess = Message.query.filter(Message.message_id == message_id).first()
        mess.message_read = "1"
        mess.save()
        return jsonify(code=200, msg='操作成功')


@user_blueprint.route('/messagelist/', methods=['GET', 'POST'])
def message_list():
    """两人的消息列表"""
    if request.method == 'POST':
        u_id1 = request.form.get('uid_1')
        u_id2 = request.form.get('uid_2')
        message = Message.query.filter(or_(
            and_(
                Message.message_from == u_id1,
                Message.message_to == u_id2
            ),
            and_(
                Message.message_from == u_id2,
                Message.message_to == u_id1
            )
        )
        ).all()
        message_schema = MessageSchema(many=True)
        message_data = message_schema.dump(message)
        return jsonify(message_data)


@user_blueprint.route('/get_mes_out/', methods=['GET', 'POST'])
def message_out():
    """两人的消息列表"""
    if request.method == 'POST':
        user_id1 = request.form.get('user_from')
        user_id2 = request.form.get('user_to')
        message = Message.query.filter(or_(
            and_(
                Message.message_from == user_id1,
                Message.message_to == user_id2
            ),
            and_(
                Message.message_from == user_id2,
                Message.message_to == user_id1
            )
        )
        ).all()
        num = 0
        content = ""
        time = ""
        for mes in message:
            if mes.message_read == "0" and mes.message_to == user_id2:
                num = num + 1
            content = mes.message_content
            time = mes.message_create_time
        user = User.query.filter(User.user_id == user_id1).first()
        return jsonify(from_name=user.user_name, from_id=user.user_id, from_role=user.user_role, time=time,
                       message=content, no_read=num)


@user_blueprint.route('/getquestion/', methods=['GET', 'POST'])
def get_question():
    if request.method == 'POST':
        u_id = request.form.get('user_id')
        users = User.query.filter(User.user_id == u_id).all()
        user_schema = UserSchema()
        user_data = user_schema.dumps(users)

        return jsonify(code=200, msg='查询成功', user_question=user_data[0])


@user_blueprint.route('/setquestion/', methods=['GET', 'POST'])
def set_question():
    if request.method == 'POST':
        # 设置密保问题
        u_id = request.form.get('user_id')
        u_question = request.form.get('user_question')
        u_answer = request.form.get('user_answer')
        user = User.query.filter(User.user_id == u_id).first()
        user.user_question = u_question
        user.user_answer = u_answer
        user.save()
        return jsonify(code=200, msg="设置问题成功")


@user_blueprint.route('/setpassword/', methods=['GET', 'POST'])
def set_password():
    if request.method == 'POST':
        # 重新设置密码
        u_id = session.get('use_id')
        password = request.form.get('password')
        user = User.query.filter(User.use_id == u_id).first()
        user.password = password
        user.save()
        return jsonify(code=200, msg="重新设置密码成功")


@user_blueprint.route('/forgetpwd/', methods=['GET', 'POST'])
def forget_pwd():
    """
    忘记密码
    """
    if request.method == 'POST':
        u_answer = request.form.get('user_answer')
        u_question = request.form.get('user_question')
        # 核对用户名和密码是否一致
        user = User.query.filter(User.user_question == u_question, User.user_answer == u_answer).first()
        # 问题和答案一致
        if user:
            msg = '正确'
            return jsonify(code=200, msg=msg)
        else:
            msg = '错误'
            return jsonify(code=200, msg=msg)
