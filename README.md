# Pricing Service Web site

This is a pricing service website made in Python and Bootstrap 4.

# Digital Ocean Deployments

## Instructions UNIX update and user creation

* `ssh root@${doIP}`
* `adduser apecr` --> create a new user apecr (include name and password after)
* `which adduser`
* `echo $PATH`
* `whoami` --> it returns root yet
* `visudo` --> opens up a file that contains the configuration of administrator users in the server
** Include one line that says:
```
apecr ALL=(ALL:ALL) ALL
```

* `vi /etc/ssh/sshd_config` --> include these changes:
```
PasswordAuthentication yes
PermitRootLogin no
AllowUsers apecr
```

* `service sshd reload` --> if you have not configured correctly the permissions for the new user you can still enter in the machine via the Digital Ocean console in the administrator panel of the project.
* `logout`
* `ssh apecr@${doIP}`
* `sudo apt-get update`

## Install Python

```sh
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install build-essential python3.7-dev python3-pip pyt
```

## Install pipenv

```sh
pip3 install --user pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

## Clone the repo and install dependencies

```sh
git clone https://github.com/apecr/pricing-service.git
cd pricing-service
pipenv install
```

## Install MongoDB in Ubuntu

```sh
sudo apt install mongodb
sudo systemctl status mongodb # check if the process is running
sudo systemctl disable mongodb # to stop the service
sudo systemctl start mongodb # to start mongodb
sudo systemctl stop mongodb # to stop mongodb
mongo # start the client
```

## Get the app and deploy it locally

```sh
sudo mkdir -p /var/www/html/pricing-service
ls -la /var/www/html/pricing-service # we see that the folder is owned by user root
sudo chown apecr:apecr /var/www/html/pricing-service # we give apecr user and group to the folder
cd /var/www/html/pricing-service/
git clone https://github.com/apecr/price-of-chair-deployment .
mkdir log
pipenv install --python=python3.7
pipenv run python app.py
```

## Configuring uWSGI and the system service

* `vi uwsgi.ini`. We introduce the following and save the file:

```uwsgi.ini
[uwsgi]
base = /var/www/html/pricing-service
app = app
module = %(app)
```

* `pipenv --venv`--> get the route to our virtual environment
* Final **uwsgi.ini**

```uwsgi.ini
[uwsgi]
base = /var/www/html/pricing-service
app = app
module = %(app)

home = /home/apecr/.local/share/virtualenvs/pricing-service-inAv0XFt
pythonpath = %(base)

socket = %(base)/socket.sock

chmod-socket = 777

processes = 8
threads = 8

harakiri = 15

callable = app

logto = %(base)/log/%n.log
```

* `sudo vi /etc/systemd/system/uwsgi_pricing_service.service`

```uwsgi_pricing_service.service
[Unit]
Description=uWSGI Pricing Service

[Service]
User=apecr
Group=apecr
WorkingDirectory=/var/www/html/pricing-service
Environment=MONGODB_URI=mongodb://127.0.0.1:27017/fullstack
ExecStart=/home/apecr/.local/bin/pipenv run uwsgi --master --emperor uwsgi.ini --die-on-term --uid apecr --gid apecr --logto log/emperor.log
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

* `touch log/emperor.log` --> it creates the file with the **apecr** user and not the **root** user.
* `sudo systemctl daemon-reload`
* `sudo systemctl start uwsgi_pricing_service` The **log/uwsgi.log** should look like that:

```txt
*** Starting uWSGI 2.0.18 (64bit) on [Fri Apr 10 10:24:37 2020] ***
compiled with version: 7.5.0 on 10 April 2020 10:00:30
os: Linux-4.15.0-66-generic #75-Ubuntu SMP Tue Oct 1 05:24:09 UTC 2019
nodename: deployment-learning-droplet
machine: x86_64
clock source: unix
detected number of CPU cores: 1
current working directory: /var/www/html/pricing-service
detected binary path: /home/apecr/.local/share/virtualenvs/pricing-service-inAv0XFt/bin/uwsgi
!!! no internal routing support, rebuild with pcre support !!!
your processes number limit is 3842
your memory page size is 4096 bytes
 *** WARNING: you have enabled harakiri without post buffering. Slow upload could be rejected on post-unbuffered webservers ***
detected max file descriptor number: 1024
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
uwsgi socket 0 bound to UNIX address /var/www/html/pricing-service/socket.sock fd 3
Python version: 3.7.7 (default, Mar 10 2020, 15:16:38)  [GCC 7.5.0]
PEP 405 virtualenv detected: /home/apecr/.local/share/virtualenvs/pricing-service-inAv0XFt
Set PythonHome to /home/apecr/.local/share/virtualenvs/pricing-service-inAv0XFt
Python main interpreter initialized at 0x560e8e851f60
python threads support enabled
your server socket listen backlog is limited to 100 connections
your mercy for graceful operations on workers is 60 seconds
mapped 1313856 bytes (1283 KB) for 64 cores
*** Operational MODE: preforking+threaded ***
added /var/www/html/pricing-service/ to pythonpath.
WSGI app 0 (mountpoint='') ready in 1 seconds on interpreter 0x560e8e851f60 pid: 22329 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI master process (pid: 22329)
spawned uWSGI worker 1 (pid: 22338, cores: 8)
spawned uWSGI worker 2 (pid: 22339, cores: 8)
spawned uWSGI worker 3 (pid: 22340, cores: 8)
spawned uWSGI worker 4 (pid: 22341, cores: 8)
spawned uWSGI worker 5 (pid: 22342, cores: 8)
spawned uWSGI worker 6 (pid: 22343, cores: 8)
spawned uWSGI worker 7 (pid: 22344, cores: 8)
spawned uWSGI worker 8 (pid: 22387, cores: 8)
```

## Configuring nginx

* `sudo apt install nginx`
* `sudo ufw status` --> Check the firewall (inactive at the moment)
* `sudo ufw allow 'Nginx HTTP'`
* `sudo ufw allow ssh` --> Allow ssh
* `sudo ufw enable`
* `sudo systemctl status nginx`--> se the service active already
* `sudo vi /etc/nginx/sites-available/pricing-service.conf`

```conf
server {
        listen 80;
        real_ip_header X-Forwarded-For;
        set_real_ip_from 127.0.0.1;
        server_name localhost;

        location / {
                include uwsgi_params;
                uwsgi_pass unix:/var/www/html/pricing-service/socket.sock;
        }

        error_page 404 /404.html;
        location = /404.html {
                root /usr/share/nginx/html;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
                root /usr/share/nginx/html;
        }
}
```

* `sudo rm /etc/nginx/sites-enabled/default` --> delete the default
* `sudo ln -s /etc/nginx/sites-available/pricing-service.conf /etc/nginx/sites-enabled/`
* `sudo systemctl reload nginx`
* `sudo systemctl start uwsgi_pricing_service`
* We can now access to our app in the url of the server:
![Pricing Service Home](/pricing-service-home.png?raw=true)

## Creating a cron job in Ubuntu

* `sudo vi /etc/crontab`. Include this line:
`29 *    * * *   apecr   cd /var/www/html/pricing-service && /home/apecr/.local/bin/pipenv run python alert_updater.py`





