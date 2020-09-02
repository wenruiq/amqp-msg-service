@echo off
set /p userid="What is your SMU user id? e.g. qxpang.2018 "
start /min cmd.exe /c docker run -d --name mysql_message -p 3310:3306 -v mysql_data:/var/lib/mysql message-mysqlcontainer
ping -n 5 127.0.0.1 >nul
start /min cmd.exe /c docker run -d --name message_microservice -p 5001:5001 -e dbURL=mysql+mysqlconnector://user:message@host.docker.internal:3310/message message-microservice:1.0.0

for /F "tokens=2 delims=:" %%i in ('"ipconfig | findstr IP | findstr 192."') do SET LOCAL_IP=%%i
set ipAddress=%LOCAL_IP: =%
echo %ipAddress%
start /min cmd.exe /c docker run -d --name message_client -p 5672:5762 -e dbURL=mysql+mysqlconnector://user:message@host.docker.internal:3310/message -e username=%userid% -e ipAddress=%ipAddress% message-client:1.0.0

pause
start "" http://noisy-quill.surge.sh