@ECHO OFF
cd ./mysql
docker build -t message-mysqlcontainer .
cd ..
cd ./message
docker build -t message-microservice:1.0.0 .
cd ..
cd ./AMQPmessageclient
docker build -t message-client:1.0.0 .
echo Done!
pause
start "" http://esdosmessaging.tk:8000/esdos/login