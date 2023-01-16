# Soko

![Soko Log](/web_app/customer_app/static/images/site/logo-big.svg)

## About

Soko is an e-commerce platform project. It offers some of the best features of online shopping, aiming to better customer experience through

1. Real-time customer-seller interactions.
2. Easier cart accessibility
3. Quick checkouts
4. Simplified order placement and tracking
5. In-app and email notification

## Installation

### Step 1:

Clone the repository:

```
$ git clone https://github.com/ngugimuchangi/Soko.git
```

### Step 2:

The application works uses `MySQL` database and requires several python libraries and plugins. You can install the requirements one by one or run the [installation.sh](installation.sh) script for automatic installation

### _*Option A*_

Run installation script with sudo priveleges

```
$ sudo installation.sh
```

### _Option B_

Step by step installation of requirements
Install MySQl

```
$ sudo apt update
$ sudo apt install mysql-server
$ sudo systemctl start mysql.service
```

Set up MySQl database:

```
$ cat db_setup.sql | sudo mysql
```

Install python libraries and plugins:

```
$ pip install -r requirements.txt
```

## Configuration

Configuration file contains a list of variables, including

1. Ports
2. Hosts
3. Secret keys

Sample configuration file:

```
# Database development settings
SOKO_ENV="production"
SOKO_MYSQL_USER="databse_user"
SOKO_MYSQL_HOST="host"
SOKO_MYSQL_PWD="mysecretpassword"
SOKO_MYSQL_DB="production_db"

# File storage settings
PRODUCT_IMAGES="/absolute/path/to/product/images"
CHAT_FILES="/absolute/path/to/chat/files"

# Host settings
HOST_DOMAIN="host domain"

# Soko customer_app setting
SOKO_CUSTOMER_APP_HOST="localhost"
SOKO_CUSTOMER_APP_PORT="5000"
SOKO_CUSTOMER_APP_SECRET_KEY="shh!donttellanyoneaboutthis"

# Soko seller_app setting
SOKO_SELLER_APP_HOST="localhost"
SOKO_SELLER_APP_PORT="5001"
SOKO_SELLER_APP_SECRET_KEY="shh!donttellanyoneaboutthis"

# Soko admin_app setting
SOKO_ADMIN_APP_HOST="localhost"
SOKO_ADMIN_APP_PORT="5002"
SOKO_ADMIN_APP_SECRET_KEY="shh!donttellanyoneaboutthis"

# API origins
ORIGINS="*"

# Buyer api setting
BUYER_API_HOST="0.0.0.0"
BUYER_API_PORT="5003"

# Seller api setting
SELLER_API_HOST="0.0.0.0"
SELLER_API_PORT="5004"

# Notification api setting
NOTIFICATION_API_HOST="0.0.0.0"
NOTIFICATION_API_PORT="5005"

# Products api setting
PRODUCT_API_HOST="0.0.0.0"
PRODUCT_API_PORT="5006"

# Orders api setting
ORDER_API_HOST="0.0.0.0"
ORDER_API_PORT="5007"

# Chat api setting
CHAT_API_SECRET_KEY="shh!donttellanyoneaboutthis"
CHAT_API_HOST="0.0.0.0"
CHAT_API_PORT="5008"
```

## Requirements

1. flasgger==0.9.5
2. flask-cors==3.0.10
3. flask-login==0.6.2
4. flask-mail==0.9.1
5. flask-socketio==5.3.2
6. mysql-client==0.0.1
7. pip-chill==1.0.1
8. python-dotenv==0.21.0
9. requests==2.28.1
10. sqlalchemy==1.4.45

## Usage

1. Set up the config a config file [`.env`](.env). as shown in the configuration example.

2. Run the startup script [`startup.sh`](startup.sh).

```
$ startup.sh
```
