#naviagte to the folder where you need to create a docker image

#create a docker image
sudo docker build -t my-apache-image .

#run the created apache image
docker run -p 80:80 my-apache-image
