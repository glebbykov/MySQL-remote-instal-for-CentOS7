from fabric import Connection
import json
def load_config():
    with open('config.json') as json_file:
        return json.load(json_file)
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
def create_db_user(c, data):
    temp_password = c.run("sudo grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}'", hide=True).stdout.strip()
    # check if new_user, new_user_password, new_database are in config.json
    if all(k in data for k in ('new_user', 'new_user_password', 'new_database','root_password')):
        c.run("mysql -u root --connect-expired-password -p{} -e 'ALTER USER root@localhost IDENTIFIED BY \"{}\";'".format(temp_password, data['root_password']))
        c.run("mysql -u root --connect-expired-password -p{} -e \"CREATE USER '{}'@'localhost' IDENTIFIED BY '{}';\"".format(data['root_password'], data['new_user'], data['new_user_password']))
        c.run("mysql -u root --connect-expired-password -p{} -e \"CREATE DATABASE {};\"".format(data['root_password'], data['new_database']))
        c.run("mysql -u root --connect-expired-password -p{} -e \"GRANT ALL PRIVILEGES ON {}.* TO '{}'@'localhost';\"".format(data['root_password'], data['new_database'], data['new_user']))
        c.run("mysql -u {} --connect-expired-password -p{} {} -e \"CREATE TABLE dates (date DATE);\"".format(data['new_user'], data['new_user_password'], data['new_database']))
    else:
        print("Could not find new_user, new_user_password, new_database, root_password in config.json.")

def insert_random_dates(c, data):
    # Insert random dates into the table
    import random
    import datetime
    for i in range(10):
        random_date = datetime.date(random.randint(2000, 2030), random.randint(1, 12), random.randint(1, 28))
        c.run("mysql -u {} -p{} {} -e 'INSERT INTO dates (date) VALUES (\"{}\");'".format(data['new_user'], data['new_user_password'], data['new_database'], random_date))

def main():
    data = load_config()
    c = Connection(host=data['remote_host'], user=data['remote_user'], connect_kwargs={"password": data['remote_password']})
    install_mysql(c, data)
    create_db_user(c, data)
    insert_random_dates(c, data)

if __name__ == '__main__':
    main()
