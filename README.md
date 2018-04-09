# NoZuoNoDie

## 启动相关服务
```
redis-serve
# 启动celery
celery -B -A tasks worker --loglevel=info 
# 启动主任务进程
python main.py 
# 启动flask 进程
python app.py  
```

## 项目需求
> python2/3

### 外部库
```
pymysql  
lxml  
celery  
redis  
flask  
tldextract  
DBUtils  
```
