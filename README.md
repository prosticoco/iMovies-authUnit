# Abstract

_Imovies_ keeps a MySQL database of its employees, containing personal information and credentials. The company's CA webserver needs information from this database to authenticate its employees before issuing certificates. For security reasons, the company chose to store the database on a separate host from the webserver. However the web server still needs some access to this information. This repository contains server intended to run on top of the MySQL database to be only accessible from the companys webserver and provide the information needed from the database.  

# VM Instructions 

## (No installation required)

1. Download the VM at : https://polybox.ethz.ch/index.php/apps/files/?dir=/Shared/ApplSecLab/VMs/VM_auth_unit&fileid=1679151160

2. When logged in as user _Master_, open a terminal and type :

   ```console
   sudo su bob
   ```

   If you have any trouble logging in to bob, his password can be found on the Github repo in the folder _secrets_ 

3. Then navigate to the _iMovies-authUnit_ folder

4. Run the server : 

   ```console
   ./run 
   ```

   You can choose the ip/port of the server as well as other options

   ```console
   ./run -h
   usage: auth_unit.py [-h] [--port PORT] [--ip IP] [--user USER] [--host HOST]
                       [--db DB] [--pwd PWD] [--cert CERT] [--sk SK]
   
   optional arguments:
     -h, --help   show this help message and exit
     --port PORT  server port
     --ip IP      server ip
     --user USER  database username
     --host HOST  db username host ip
     --db DB      database name
     --pwd PWD    db user password
     --cert CERT  server certificate path
     --sk SK      server private key path
   ```

   **Important Note :** To ensure the server works, these options should not be specified as the defaults work :

   - __pwd__ : already set to __toor__ in the database which is already installed on the machine
   - __db__ : already set to __imovies__ in the database
   - __user__ : already set to __root__ in the database

   Additionnaly, the server is already loaded with a certificate and private key which can be found in the _keys_ folder. These can be regenerated by navigating into this folder and calling the following script : 

   ```console
   ./genkeyscert.sh
   ```

# Installation (Automatic)


## Use install only script (need sudo rights)

```console
sudo ./install_only.sh <MySQL Password> <Path to dumpfile>
```

## Use install and run (unsafe)

```console
sudo ./install_and_run.sh <MySQL Password> <Path to dumpfile>
```
This will run the server as root and should not be used.


## Notes

Dump files can be found in the db/ folder. There are two dump files :

1. containing only the user table
2. containing user table + admin table

The database _imovies_ can be reset at any time with a new dumpfile by running:

```console
sh scripts/setup_mysql.sh <MySQL Password> <Path to dumpfile>
```

# Installation (Manual)

## Install Database

1. install MySQL :

```console
sudo apt-get install mysql-server
```
you will need to specify a password for the root account. 

2. Create __imovies__ database :

```console
echo 'create database imovies' | mysql -uroot -p<yourpassword>
```

3. Load __users__ table :

```console
mysql -uroot -p<yourpassword> imovies < imovies_users.dump
```

## Install Python Dependencies 



### Creating a new environment

If needed, create a virtual environment for python :

```console
python3 -m venv <env_name>
```

### Activating environment

Activate the environment :

```console
source <env_name>/bin/activate
```

### Install all dependencies

Pip should be installed with the newly created environment.

```console
pip install -r requirements.txt
```

# Usage

## Run the server 

By Default :

```console
./run
```

*By Default*

- The server will run on ip __127.0.0.1__ and port __5001__ 
- The server tries to connect the database with name __imovies__ using username __root__ with password __toor__ and hostname __localhost__


These options can be changed, to list options :

```console
./run -h
```

## Run the Client

A client can be used to test the server and analyse its behaviour :


```console
python3 auth_client.py
```

# Server Interaction

This section explains what kind of data the server expects from any querier.

## Routes

### Credential checking

Send a *POST* request to the given address :

*POST* <http://<server_ip>:<server_port>/check_user> 

Containing a JSON of the following format :

```json
{
	"uid" : "exampleUID",
	"pwd" : "aPassword"
}
```

and get back an answer with status code 200 containing a JSON of the following format : 

```json
{
	"valid" : false,
	"type" : 1,
	"description" : "Wrong Password" 
}
```

The type field is just an response type identifier.

### Get Personal information from a user :

Send a *POST* request to the given address :

*POST* <http://<server_ip>:<server_port>/get_info> 

containing a JSON of the following format :

```json
{
	"uid" : "exampleUID"
}
```

and get back an answer with status code 200 containing a JSON of the following format : 

```json
{
	"found" : true,
	"info" : {
		"uid" : "pr",
		"lastname" : "prost",
		"firstname" : "adrien",
		"email" : "prostategmail.com",
		"pwd" : "e27a5b2abab6e9fb6b36b95db5deda8cb1796d93"
	}

}
```

or 

```json
{
	"found" : false,
	"info" : {}

}
```

### Change information 

Send a *POST* request to the given address :

*POST* <http://<server_ip>:<server_port>/update_info> 

containing a JSON of the following format :

```json
{
	"uid" : "uid affected by changes",
	"updates" : {
		"uid" : "pr",
		"lastname" : "prost",
		"firstname" : "adrien",
		"email" : "prostategmail.com",
		"pwd" : "strongpassword:)"
	}

}
```

The updates field can contain any subset of the fields __uid__,__lastname__,__firstname__,__email__ and __pwd__. Hence the changes will only affect the specified fields. 


*Important:* The password should not be hashed when sent to the server. 

The server will send back a JSON of the following format :

```json
{
	"updated" : true,
	"type" : 0,
	"description" : "Information updated with Success" 
}
```

## Additionnal Information 


The server will send back response with status code 400 whenever : 

- The client does not send a valid request
- the request does not contain a valid JSON
- The JSON does not contain valid fields





