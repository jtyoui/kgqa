echo vm.max_map_count=655360 >> /etc/sysctl.conf
sysctl -p

# 下载模型
if [ ! -d $PWD/model ];then
  echo "未找到模型，正在下载模型中...."
  curl -O https://github.com/jtyoui/KGQA/releases/download/v1.0/model.tar.gz
  echo "解压模型中...."
  tar -zxvf wss-model.tar.gz -C $PWD
  rm -rf wss-model.tar.gz
fi

# 启动
docker-compose up -d