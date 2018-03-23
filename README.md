LEGO_Python_Krampus
===================
Python Code to Load LEGO Data - By Team Krampus
-----------------------------------------------

1. Install Docker and provide it with at least 4 gigabytes of memory
2. In a terminal window, execute the following command:
docker run --publish=7474:7474 --publish=7687:7687 lego:neolego
3. Wait until the terminal window displays:
Remote interface available at http://0.0.0.0:7474/
4. In a second terminal window, execute the following command:
docker run --net=“host” andyartz/lego:loadlego
5. Wait for the command to finish executing and display the message:
    Total Loading Time: XXXX
    
Once this is done, the data is loaded and ready for access at http://0.0.0.0:7474/.
**Your username/password is neo4j/admin**
