import os
import subprocess
import configparser
import mysql.connector # pip install mysql-connector-python
import getpass
import urllib.request
import zipfile
import pwd


def build(domain, database, wordpress):
    config = configparser.ConfigParser()
    config.read("config.ini")

    contentPath = f'/var/www/html/{domain}'
    defaultPath = '/etc/nginx/sites-available/default'
    defaultLinkPath = '/etc/nginx/sites-enabled/default'
    targetPath = f'/etc/nginx/sites-available/{domain}'
    linkPath = f'/etc/nginx/sites-enabled/{domain}'

    # Check to verify if the default virtual host is linked in sites-enabled
    # Comment this out if you are using this.
    if os.path.exists(defaultLinkPath):
        os.unlink(defaultLinkPath)

    

    # Copy the default file from /etc/nginx/sites-available to /etc/nginx/sites-available and name it the domain variable
    os.system(f"cp {defaultPath} {targetPath}")

    # Update the server_name directive in the domain file with the domain variable and add www. to the domain variable and save that as well
    # Update the root directive in the domain file to point to the directory created in /var/www/html
    with open("/etc/nginx/sites-available/" + domain, "r") as f:
        lines = f.readlines()

    root_updated = False
    with open("/etc/nginx/sites-available/" + domain, "w") as f:
        for line in lines:
            if "server_name" in line:
                f.write("    server_name " + domain + " www." + domain + ";\n")
            elif "root" in line and not root_updated:
                f.write("    root /var/www/html/" + domain + ";\n")
                root_updated = True
            else:
                f.write(line)

    # Create a symbolic link from the newly created file in /etc/nginx/sites-available to /etc/nginx/sites-enabled
    if os.path.exists(linkPath):
        os.unlink(linkPath)
        os.symlink(targetPath,linkPath)
    else:
        os.symlink(targetPath,linkPath)

    # Restart Nginx
    result = subprocess.run("systemctl restart nginx", shell=True)
    if result.returncode != 0:
        print('There was an error starting nginx.')

    if database == 'y':
        # Read the password from the configuration file
        user = config.get("database", "user")
        password = config.get("database", "password")
        
        cnx = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password
        )

        dbName = input('What would you like to name the database? ')
        dbUser = input('What would you like username of the database to be? ')
        dbPassword = getpass.getpass("What would you like the password for this user to be? ")

        cursor = cnx.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{dbUser}'@'localhost' IDENTIFIED BY '{dbPassword}';")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {dbName}.* TO '{dbUser}'@'localhost';")
        cnx.close()

        print(f'Database {dbName} was created with username {dbUser} with the provided password.')
        print('Please note that this information is case sensative.')

    if wordpress == 'y':
        urllib.request.urlretrieve("https://wordpress.org/latest.zip", "/var/www/html/latest.zip")
        # Open the ZIP file
        with zipfile.ZipFile("/var/www/html/latest.zip", "r") as zip_ref:
            # Extract the contents of the ZIP file to the current working directory
            zip_ref.extractall("/var/www/html/")
        if os.path.exists(contentPath):
            print(f'A previous verion of this domain exists. Renaming it to {domain}_old')
            os.rename(contentPath, contentPath+'_old')
        os.rename("/var/www/html/wordpress", contentPath)
        os.remove("/var/www/html/latest.zip")
        
        # Set the permissions for the directory to 775
        os.chmod(contentPath, 0o775)
        # Get the UID and GID of the www-data user
        www_data_uid = pwd.getpwnam("www-data").pw_uid
        www_data_gid = pwd.getpwnam("www-data").pw_gid

        # Recursively change the ownership of the directory and its contents
        for root, dirs, files in os.walk(f"/var/www/html/{domain}"):
            for d in dirs:
                os.chown(os.path.join(root, d), www_data_uid, www_data_gid)
            for f in files:
                os.chown(os.path.join(root, f), www_data_uid, www_data_gid)

if __name__ == '__main__':
    if os.geteuid() != 0:
        print("This must be run as root!")
        quit()
    domain = input("Please enter a Fully Qualified Domain Name: ")
    while True:
            database = input("Do you need a database? (y/n) ")
            if not (database.lower() == "y" or database.lower() == "n"):
                    # The user entered an invalid response, so print an error message and continue the loop
                    print("Invalid response. Please enter 'y' or 'n'.")
            else:
                    break
    while True:
            wordpress = input("Does the site require WordPress? (y,n)")
            if not (wordpress.lower() == "y" or wordpress.lower() == "n"):
                    # The user entered an invalid response, so print an error message and continue the loop
                    print("Invalid response. Please enter 'y' or 'n'.")
            else:
                    break
    build(domain, database, wordpress)