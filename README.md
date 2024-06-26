# docker-projects
I have completed a 4 simple projects on docker. That helped me to learn more about docker and their usages.
In this i have added those 4 projects handled with.
Also I have given the installation guide for docker installation in ubuntu

## project1_Setting-Up-ssh-connection-between-2-ubuntu-containers
- Pulled the ubunutu image from the docker hub to my local system
- created two ubuntu containers named container1 and container2
- In container1 installed openssh-server and configured it
- started the ssh service in container1 and got the ip address of the container1
- In container2 installed openssh-client and started the ssh service
- connected the server(container1) from client(container2) using ssh

## project2_Dockerizing-apache-web-server
- Dockerized the apache web server running in ubuntu
-  Using dockerfile i have pulled the ubuntu image
- in that os i have installed my apache server
- configured the port to 80
- and entered command to run the apache server
- Build a docker image and run the image

## project3_Dockerizing-the-nginx-server
- Dockerized the webpage running in the nginx server
- From the ubuntu image
- i have installed the nginx server into it
- Copied my html file in my local machine to the ubuntu image
- exposed the port to 8000
- build the docker image for the docker file

## project_4_Dockerizing_movie_library_flask_app
- Dockerized a Movie Library a flask based app
- from the docker file, installed the python
- changed the working directory
- made the requirements file and copied it
- run the virtual environment
- installed the requirements
- copied the files in the current directory
- created a script to verify the virtula environment
- initialized database and run the application
