# VHA (Virtual Host Adder)

## Purpose
The purpose of this document is to provide standard and technical guidance on how to
use the VHA program. It will cover all of the requirements needed to successfully use the
program, including installation instructions, system requirements, and user permissions. This
document will serve as a reference manual for users of the VHA program, helping them to
understand the program's capabilities and limitations, as well as the steps they need to follow in
order to use it effectively. Additionally, this document will provide troubleshooting guidance to
help users resolve any issues they may encounter while using the VHA program.
Overall, the goal of this document is to help users of the VHA program to add new
virtual hosts to their Ubuntu Nginx web server.

## Requirements
It is assumed that the following requirements are already met.
  1. Linux Server running Ubuntu
    a. Currently tested on 20.04.
  2. MySQL Database is locally installed on Ubuntu server
  3. Nginx is installed on Ubuntu server
  4. Python3 is installed on Ubuntu server
  5. Git is installed on Ubuntu server

These requirements may need to be approved and performed before moving forward.
  1. Login as root or run all of the commands as sudo
  2. Install mysql-connector-python
    a. sudo pip3 install mysql-connector-python
  3. Complete the config.ini file
    a. See below

## Download and Configure VHA from Github
The following steps will get you started with VHA. If you already have the most recent copy downloaded
then you can skip to ‘Run VHA’
  1. Log into the server you wish to download and run VHA using git
    a. git clone https://github.com/millalgo/vha.git
    b. Move into the vha directory
      i. cd vha
    c. Using your text editor of choice update config.ini with the root username and password for your database.
      i. nano config.ini
      ii. For Example user = root password=Password#1

## Run VHA
Before running the main script first run test.py to verify the required packages are installed.
python3 test.py

If everything is working as expected then you will get a prompt that states ‘Test Completed and Passed’.
If you get a different error then it is because something was not installed properly. Review the error and attempt the troubleshoot. See the troubleshooting section for more information.

Once you’ve been able to verify your ready then run the vha.py file
python3 vha.py

NOTE: What you type in is what you input. This program is case sensitive.

Please enter a Fully Qualified Domain Name
Do you need a database?
Does the site require Wordpress?

## Actions Performed
This script was developed using an AWS Ubuntu 20.04 virtual machine. Once completed the following
actions have been performed on your server.
  1. Nginx Virtual Host sites-available was created using the Default as a template
  2. Nginx Virtual Host sites-enabled link was established with sites-available
  3. If database option was selected then Database table, username, and password were generated
  4. If the WordPress option was selected then the latest version of Wordpress was downloaded and placed in /var/www/html/ with the domain name you selected.
