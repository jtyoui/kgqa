# KGQA

一个问答系统

# 下载模型。下载到relation文件夹下
```
wget https://oss.jtyoui.com/data/wss-model.tar.gz
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

## 需要修改系统配置

```shell
# 最后一行追加
echo vm.max_map_count=655360 >> /etc/sysctl.conf
# 执行命令重新加载
sysctl -p 
```

## 安装环境(dockerUI-elasticsearch-neo4j-kibana-mysql+redis) + 安装后台服务环境(uvicorn-gunicorn-fastapi)

```shell
git clone https://github.com/wusaisa/KGQA.git
cd ./KGQA
docker-compose up -d
```

### 单元测试地址

`http://localhost:11000/docs`

### dockerUi地址:账号admin，密码自己设置

`http://localhost:9000/#/init/admin`

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

### 访问网页初始化Mysql

`http://localhost:11000/wss/createMysql`

### 访问网页初始化ES

`http://localhost:11000/wss/createES`

### 访问网页初始化Redis

`http://localhost:11000/wss/createRedis`

### 注意:如果数据库初始化那么redis也要初始化