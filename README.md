# mySQL-remote-instal-for-CentOS7

This is a Python script that uses the Fabric library to install, configure and populate a MySQL database on a remote server. The script does the following tasks:

1. Loads the configuration information from a JSON file called config.json.
2. Installs the MySQL server on the remote server by running the necessary shell commands.
3. Creates a new database, a new user and grants the user all privileges on the database.
4. Inserts 10 random dates into the table of the newly created database.

The script uses the Connection object from the Fabric library to establish an SSH connection to the remote server and run shell commands.

To run the script, the config.json file should contain the following information:

+ remote_host: the hostname or IP address of the remote server
+ remote_user: the username to use for SSH authentication
+ remote_password: the password to use for SSH authentication
+ new_user: the username for the new database user
+ new_user_password: the password for the new database user
+ new_database: the name of the new database
+ root_password: the password for the root user in the database.
