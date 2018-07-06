# Telebot and 

A [Telegram](https://telegram.org/) Bot written in Python (Work-In-Progress)

## Mô hình:

- Một server cài devstack
    
    + OS: ubuntu16
    + IP: 192.168.100.114
    + Ram: 4GB Vcpu: 4 

- Một server cài telegram_bot

    + OS: ubuntu16
    + IP: 192.168.30.200
    + Ram: 1GB Vcpu: 2

## Cài đặt devstack 

- Tạo user stack 

`sudo useradd -s /bin/bash -d /opt/stack -m stack`

- Add stack có quyền sudo và khi chạy không hỏi pass

```sh
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo su - stack
```

- Clone devstack từ git 

```
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
git checkout stable/pike
```
- Tạo một file `local.conf`

```sh
[[local|localrc]]
SERVICE_TOKEN=hocchudong
ADMIN_PASSWORD=hocchudong
DATABASE_PASSWORD=hocchudong
RABBIT_PASSWORD=hocchudong
SERVICE_PASSWORD=hocchudong
LOGFILE=$DEST/logs/stack.sh.log
LOGDAYS=2
#OFFLINE=True

##########################

# Enable normally
disable_service tempest
disable_service c-api
disable_service c-vol
disable_service c-sch

# Enable Heat

# Enable Neutron
enable_service neutron
enable_service q-svc
enable_service q-agt
enable_service q-l3,q-meta,q-dhcp
```

- Chạy script cài đặt 

`./stack.sh`

## Cài đặt BOT

- Yêu cầu: 

    + Python3
    + Đã tạo được bot trong telegram và lấy token 

1. Tải repo và cài đặt requirements:

```
git https://github.com/vietstacker/teleops.git
cd teleops
sudo pip3 install -r requirements.txt
```
2. Khai báo thông tin devstack server 

```sh
cd teleops
vim telebot/plugins/config.py

IP = '192.168.100.114'
USERNAME = 'admin'
PASSWORD = 'hocchudong'
PROJECT_NAME = 'admin'
AUTH_URL = 'http://{}/identity/v3'.format(IP)
```

3. Run Setup

```
sudo python3 setup.py install
```

4. Sửa tele.conf file và chuyển nó tới /etc/telegram/

```
cd etc/
sed -i "s/TETO/Your token/g" tele.conf
sudo mkdir /etc/telebot
sudo mv tele.conf /etc/telebot/
```

5. Cài đặt supervisor

```
sudo apt install -y supervisor
sudo cp bot_mdt.conf /etc/supervisor/conf.d/
```

6. Start BOT

```
sudo supervisorctl update
sudo supervisorctl start bot_mdt
```

====================================

## Running with Docker

1. Chuẩn bị môi trường

- Install docker on Ubuntu or CentOS

```
curl -fsSL https://get.docker.com | sh
```

2. Build image từ Dockerfile

```
cd bot_mdt
build -t bot_image .
```

Work-in-process
