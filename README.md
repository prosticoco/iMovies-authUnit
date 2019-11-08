# Abstract

_Imovies_ keeps a MySQL database of its employees, containing personal information and credentials. The company's CA webserver needs information from this database to authenticate its employees before issuing certificates. For security reasons, the company chose to store the database on a separate host from the webserver. However the web server still needs some access to this information. This repository contains server intended to run on top of the MySQL database to be only accessible from the companys webserver and provide the information needed from the database.  

# Installation (Manual)

## Install MySQL Database

## Install Python Dependencies 

For your convenience, create a virtual environment for python and then install the dependencies with :

```console
pip install -r requirements.txt
```




# Run the server




