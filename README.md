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




