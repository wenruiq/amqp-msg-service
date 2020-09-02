1) Open this folder in terminal.
2) docker build -t <dockerid>/message:1.0.0 .
4) Before running, make sure mysql container is running.
3) To run, docker run -p 5001:5001 -e dbURL=mysql+mysqlconnector://user:password@host.docker.internal:3306/message <dockerid>/message:1.0.0