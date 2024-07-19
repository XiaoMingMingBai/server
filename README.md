# 命令

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

## 修改模型

```shell
1. 更改 models.py
2. 运行 python manage.py makemigrations x 为模型的改变生成迁移文件
3. 运行 python manage.py migrate 来应用数据库迁移
```