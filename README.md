<a href="https://onlinesoko.pythonanywhere.com/" target="_blank">
<p align="center"><img src="/web_app/customer_app/static/images/site/favicon-big.svg" 
alt="soko logo" width="59" height="66" >
</p>
<p align="center"><img src="/web_app/customer_app/static/images/site/logo-small.svg" 
alt="soko text" width="200" height="51" style="margin: 0 auto; display: block;" ></p>
</a>

## Table of Contents

- [About](#About)
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [Usage](#Usage)
- [Demo](#Demo)

## About

Soko is an e-commerce platform project. It offers some of the best features of online shopping, aiming to better customer experience through

1. Real-time customer-seller interactions.
2. Easier cart accessibility
3. Quick checkouts
4. Simplified order placement and tracking
5. In-app and email notifications

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

## Installation

### Step 1:

Clone the repository:

```
$ git clone https://github.com/ngugimuchangi/Soko.git
```

### Step 2:

The application works uses `MySQL` database and requires several python libraries and plugins. You can install the requirements one by one or run the [`installation.sh`](installation.sh) script for automatic installation

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

An environment configuration file contains a list of variables, including

1. Ports
2. Hosts
3. Secret keys

This allows changing the above secret keys if compromised or changing ports to avoid conflicts when the application is configured to run on port already in use.

A sample environment configuration file:

```
# Database settings
SOKO_ENV="production"
SOKO_MYSQL_USER="databse_user"
SOKO_MYSQL_HOST="host"
SOKO_MYSQL_PWD="mysecretpassword"
SOKO_MYSQL_DB="production_db"

# File storage settings
PRODUCT_IMAGES="/absolute/path/to/product/images/folder"
CHAT_FILES="/absolute/path/to/chat/files/folder"

# Host settings
HOST_DOMAIN="host domain"

# Soko customer_app settings
SOKO_CUSTOMER_APP_HOST="localhost"
SOKO_CUSTOMER_APP_PORT="5000"
SOKO_CUSTOMER_APP_SECRET_KEY="shh!donttellanyoneaboutthis"

# Soko seller_app settings
SOKO_SELLER_APP_HOST="localhost"
SOKO_SELLER_APP_PORT="5001"
SOKO_SELLER_APP_SECRET_KEY="shh!donttellanyoneaboutthis"

# Soko admin_app settings
SOKO_ADMIN_APP_HOST="localhost"
SOKO_ADMIN_APP_PORT="5002"
SOKO_ADMIN_APP_SECRET_KEY="shh!donttellanyoneaboutthis"

# API origins
ORIGINS="*"

# Buyer api settings
BUYER_API_HOST="0.0.0.0"
BUYER_API_PORT="5003"

# Seller api settings
SELLER_API_HOST="0.0.0.0"
SELLER_API_PORT="5004"

# Notification api settings
NOTIFICATION_API_HOST="0.0.0.0"
NOTIFICATION_API_PORT="5005"

# Products api settings
PRODUCT_API_HOST="0.0.0.0"
PRODUCT_API_PORT="5006"

# Orders api settings
ORDER_API_HOST="0.0.0.0"
ORDER_API_PORT="5007"

# Chat api settings
CHAT_API_SECRET_KEY="shh!donttellanyoneaboutthis"
CHAT_API_HOST="0.0.0.0"
CHAT_API_PORT="5008"
```

## Usage

1. Set up the config a config file [`.env`](.env). as shown in the configuration example.

2. Run the startup script [`startup.sh`](startup.sh).

```
$ cd Soko
$ startup.sh
```

## Demo

**Deployment link**: https://onlinesoko.pythonanywhere.com/

**Screenshots**:

![Home Page](/web_app/customer_app/static/images/landing_page/landing-page-carousel.png)

![Notifications](/web_app/customer_app/static/images/landing_page/notifications.png/)

![Cart](/web_app/customer_app/static/images/landing_page/cart.png/)

![Products](/web_app/customer_app/static/images/landing_page/landing-page-products.png/)

![Chat List](/web_app/customer_app/static/images/landing_page/messenger-chat-list.png)

![Messages](/web_app/customer_app/static/images/landing_page/messenger-messages.png)
