from fabric import Connection
import json

def install_mysql():
    with open('config.json') as json_file:
        data = json.load(json_file)
        remote_host = data['remote_host']
        remote_user = data['remote_user']
        remote_password = data['remote_password']
    c = Connection(host=remote_host, user=remote_user, connect_kwargs={"password": remote_password})
    c.run('sudo curl -sSLOS https://dev.mysql.com/get/mysql80-community-release-el7-7.noarch.rpm')
    c.run('sudo rpm -ivh mysql80-community-release-el7-7.noarch.rpm')
    c.run('sudo yum -y install mysql-server')
    c.run('sudo systemctl start mysqld')
    c.run('sudo systemctl enable mysqld')
install_mysql()
