# KGQA

一个问答系统

# 下载模型。下载到relation文件夹下
```
wget 
# 解压到数据放在relation/model

-- data
-- relation
--    model
--      bert
--      ERNIE
--    service
```

# 一键安装(忽略下面的文档)
```shell
sh start.sh
```

### 访问网页初始化Mysql

`http://localhost:11000/wss/createMysql`

### 访问网页初始化ES

`http://localhost:11000/wss/createES`

### 访问网页初始化Redis

`http://localhost:11000/wss/createRedis`

### 注意:如果数据库初始化那么redis也要初始化


### 测试文档

`http://localhost:11000/docs`

### kibana地址

`http://localhost:5601/app/kibana`

### neo4j地址：账号/密码都是neo4j

`http://localhost:7474/browser/`

### mysql的配置

```python
HOST = 'mysql'
USER = 'root'
PASSWORD = 'password'
CHARSET = 'utf8mb4'
DB = 'wss'
```