# Coin Keeper

A club payment/tracking website created by Cindy Hua, Mikayla Morrison, Vanja Dorovic, Subha Tasnim, and Katrina Mei.
- [Coin Keeper](#coin-keeper)
  - [Setup](#setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Install virtualenv in python by typing the commands in your terminal](#2-install-virtualenv-in-python-by-typing-the-commands-in-your-terminal)
    - [3. While in your branch, create your virtual environment by typing in](#3-while-in-your-branch-create-your-virtual-environment-by-typing-in)
    - [4. Activate your virtual environment](#4-activate-your-virtual-environment)
      - [macOS/Linux:](#macoslinux)
      - [Windows:](#windows)
    - [5. Install the requirements](#5-install-the-requirements)
    - [6. Ensure database is migrated](#6-ensure-database-is-migrated)
    - [7. Run the application](#7-run-the-application)
  - [Common Errors and Fixes](#common-errors-and-fixes)
    - [Database errors](#database-errors)
    - [Address already in use. Port 5000 is in use by another program error](#address-already-in-use-port-5000-is-in-use-by-another-program-error)
    - [ModuleNotFoundError when running flask application](#modulenotfounderror-when-running-flask-application)
  - [Sample Accounts](#sample-accounts)
    - [Admin](#admin)
    - [Treasurer](#treasurer)
    - [Coach](#coach)
    - [Users(0-9)](#users0-9)

## Setup 

### 1. Clone the repository
`git clone https://github.com/mikaylamorrison/treasurer-website.git`
### 2. Install virtualenv in python by typing the commands in your terminal 
`pip install virtualenv`
### 3. While in your branch, create your virtual environment by typing in 
`python -m venv env`
### 4. Activate your virtual environment
#### macOS/Linux:
`source env/bin/activate`
#### Windows:
`env\Scripts\activate`
### 5. Install the requirements
`pip install -r requirements.txt`
### 6. Ensure database is migrated
`python manage.py`
### 7. Run the application
`flask run`

## Common Errors and Fixes
### Database errors
Run `python manage.py` to ensure most updated database
### Address already in use. Port 5000 is in use by another program error
Run `flask run --port=8000` instead of `flask run`
### ModuleNotFoundError when running flask application
Ensure all requirements are installed in proper path. Try to manually install the module in question by using `pip install module` where module is the missing module.

## Sample Accounts
These accounts are pregenerated for testing purposes.
### Admin
username: admin  
password: admin123

### Treasurer
username: treasurer  
password: treasurer123

### Coach
username: coach  
password: coach123

### Users(0-9)
username: user(0-9)  
password: user(0-9)pwd  
For exammple: user0 would be the username and user0pwd is the password.
