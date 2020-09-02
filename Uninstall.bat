@echo off
echo Now deleting, please wait 15 seconds...
start /min cmd.exe /c docker stop message_client
start /min cmd.exe /c docker stop message_microservice
start /min cmd.exe /c docker stop mysql_message

ping -n 15 127.0.0.1 >nul
start /min cmd.exe /c docker system prune -f

start /min cmd.exe /c docker rmi -f message-client:1.0.0
start /min cmd.exe /c docker rmi -f message-microservice:1.0.0
start /min cmd.exe /c docker rmi -f message-mysqlcontainer:latest

pause