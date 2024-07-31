# API server

为device和web提供API服务


## 开发步骤

1. 拉取代码

```shell
git clone 
```

2. 安装python3和创建虚拟环境

```shell
# 进入项目根目录
cd ~/server

# 安装python3和pip
sudo apt-get install python3 python3.10-venv

# 创建虚拟环境
sudo python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

######开发项目

# 运行自测 默认8000端口
cd server/api

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行项目 端口8000
python manage.py runserver


# 退出python虚拟环境
deactivate
```

3. github action (可选操作)

```shell
# 安装依赖
sudo apt install act
# 运行github action
act
```

## 相关使用

### Django

```shell
pip install -r requirements.txt

django-admin startproject serve

python manage.py startapp polls

# 应用到数据库
python manage.py migrate

# 创建迁移文件
python manage.py makemigrations polls

python manage.py sqlmigrate polls 0001

python manage.py createsuperuser

python -m pip install django-debug-toolbar

python manage.py runserver
```

### gunicorn + nginx 部署django

```shell
# 安装依赖
pip install gunicorn nginx

# 在 Django 项目下执行 收集静态文件
python manage.py collectstatic
# python manage.py collectstatic --settings=api.settings.production

# 测试能否运行
gunicorn --workers 3 api.wsgi:application

# 配置systemd
sudo vim /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 配置nginx
sudo vim /etc/nginx/sites-available/api
sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx # sudo nginx -s reload
```

```systemd
# /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=你的用户名
Group=你的用户组
WorkingDirectory=/path/to/your/django/project
ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind unix:/path/to/your/django/project/gunicorn.sock 你的项目名.wsgi:application

[Install]
WantedBy=multi-user.target
```

```nginx
# /etc/nginx/sites-available/api
server {
    listen 80;
    server_name IP_AND_DOMAIN_NAME;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/django/projec/static/;
    }

    location /media/ {
        alias /path/to/your/django/projec/media/;
    }
}
```

#### 修改模型

```shell
1. 更改 models.py
2. 运行 python manage.py makemigrations x 为模型的改变生成迁移文件
3. 运行 python manage.py migrate 来应用数据库迁移
```