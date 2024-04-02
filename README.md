## Run the commands in the following order
```bash
    1- git clone https://github.com/Haniefz2000/MiniProject_02.git
    2- cd MiniProject_02
    3- docker compose -f ./docker-compose.yml up -d
    4- docker exec -it kafka-broker bash
    5- cd /codes/
    6- sh script.sh
```
then press ```bash  ctrl + p + q``` to read escape sequence from contianer kafka-broker.
Now go to http://localhost:9100/ , you can see the topics and configuration properties of kafka.


