## 官网

https://gofrp.org

## 服务端

> 下载地址：https://github.com/fatedier/frp/releases

### 安装

步骤1：创建安装目录

```shell
mkdir -p /data/frp
```

步骤2：下载安装包

```shell
wget -P /data/frp https://ghgo.xyz/https://github.com/fatedier/frp/releases/download/v0.61.1/frp_0.61.1_linux_amd64.tar.gz
```

步骤3：解压文件

```shell
tar -zxvf /data/frp/frp_0.61.1_linux_amd64.tar.gz && cd /data/frp/frp_0.61.1_linux_amd64
```

### 配置

编辑配置 frps.toml

```shell
vi /data/frp/frp_0.61.1_linux_amd64/frps.toml
```

修改配置

```toml
# 客户端与服务连接端口
bindPort = 7001

# 客户端连接服务端时认证的密码
auth.token = "woodwhales_token"

# http协议监听端口
vhostHTTPPort = 28081

# web界面配置
webServer.addr = "0.0.0.0"
webServer.port = 7501
webServer.user = "woodwhales_admin"
webServer.password = "woodwhales_password"

# 日志保存设定, 保存位置、保存时长
log.to = "./frps.log"
log.level = "info"
log.maxDays = 7
```

### 创建 frps.service 服务

在 /etc/systemd/system 目录下创建一个`frps.service`文件，用于配置 frps 服务。

```shell
vim /etc/systemd/system/frps.service
```

写入配置
```ini
[Unit]
# 服务名称
Description = frp server
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
# 启动frps的命令，需修改为您的frps的安装路径
ExecStart = /data/frp/frp_0.61.1_linux_amd64/frps -c /data/frp/frp_0.61.1_linux_amd64/frps.toml

[Install]
WantedBy = multi-user.target
```

使用 systemd 命令管理 frps 服务

```shell
# 启动frp
sudo systemctl start frps
# 停止frp
sudo systemctl stop frps
# 重启frp
sudo systemctl restart frps
# 查看frp状态
sudo systemctl status frps
```

开启 frps 开机自启动

```shell
sudo systemctl enable frps
```

停止 frps 开机自启动

```shell
sudo systemctl disable frps
```

## 客户端