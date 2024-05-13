**本项目为大学课程设计作业，仅供参考**

- 第一步，根据提示下载必要的库。

- 第二步，设置本地 MySql 链接。

   ```py
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/class'
   ```

- 第三步，运行 app.py 后调用 `user/create_db/`接口创建数据库即可。



客户端（Android）地址：https://github.com/Yuyi-Chen/MyClass

