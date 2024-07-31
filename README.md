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

## 相关命令

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

#### 修改模型

```shell
1. 更改 models.py
2. 运行 python manage.py makemigrations x 为模型的改变生成迁移文件
3. 运行 python manage.py migrate 来应用数据库迁移
```