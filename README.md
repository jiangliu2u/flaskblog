# 个人博客
[网址](https://www.xfz1224.com/)
## 功能：
1. 用户注册/登录
2. 发表 删除微博，可带图片 点赞功能
3. 写博客
4. 后台管理

## 服务器部署步骤
部署到服务器采用的是nginx和uwsgi，nginx配置时可加https，此处略过，我的服务器版本为ubuntu16.04
### 1. uwsgi配置文件为flaskblog_uwsgi.ini，放在flaskblog目录下,如下:
<pre>
[uwsgi]
socket = 127.0.0.1:5051 //项目运行的本地地址端口
pythonpath = /**/**/flaskblog //项目的目录
module = manage //运行项目的模块，此处为manage.py
wsgi-file = /**/**/flaskblog/manage.py  //运行项目的文件
callable = flaskapp //启动应用的application，是manage.py里的app
processes = 4
threads = 2
daemonize = /root/src/flaskblog/server.log //日志文件</pre>

### 2. nginx配置文件nginx_flask.conf如下：
<pre>
server{
    listen 80;
    server_name 你的域名;
    location / {
        include uwsgi_params; 
        uwsgi_pass 127.0.0.1:5051;   //与uwsgi配置相同
        uwsgi_param UWSGI_CHDIR /root/src/flaskblog;  //项目目录
        uwsgi_param UWSGI_SCRIPT manage:flaskapp; //项目启动脚本和app
    }
}
</pre>
配置好好执行下列命令使nginx_flask.conf配置生效：

移除默认配置
<pre>sudo rm /etc/nginx/sites-enabled/default</pre>

将Nginx 配置文件用软链接链接到 Nginx 配置文件夹中

<pre>sudo ln -s /yourpath/flaskblog/nginx_flask.conf /etc/nginx/conf.d/</pre>
重新启动Nginx
<pre>sudo /etc/init.d/nginx restart</pre>
最后运行
<pre>sudo uwsgi --ini flask_uwsgi.ini</pre>
即可运行flask项目，nginx_flask.conf中设置的域名即可访问该项目

## 预览如下
![登录](https://i.imgur.com/sPVCJ1i.png)
![](https://i.imgur.com/negU7vE.png)
![](https://i.imgur.com/SNdnjGu.png)
![](https://i.imgur.com/SNV8v0C.png)
![](https://i.imgur.com/tQ3gsjE.png)
![](https://i.imgur.com/D4Gr92S.png)
![](https://i.imgur.com/c7AcUeO.png)
![](https://i.imgur.com/jUtfU6X.png)
![](https://i.imgur.com/N9NatW4.png)
![](https://i.imgur.com/gXVUoXd.png)
