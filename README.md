# LEGO_Python_Krampus.
# Python Code to Load LEGO Data - By Team Krampus.
Install neo4j (One time activity).
Install python in your computer (One time activity).
Open command prompt in administrator mode and navigate to the python installation folder (if python directory is not set to windows environment variable).
Install py2neo library by running the following command (One time activity):
		pip install py2neo
Copy the .py files to your local directory.
Open the file(s) in text editor and set the file path to your .csv file path.
Update your neo4j DB password (The Graph URI should be same though).
In the neo4j config file comment the line "dbms.directories.import=import".
In the command prompt run the python file.
Make sure your neo4j DB is running when you run the python program.
This will load the parts to neo4j database.
