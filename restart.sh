#!/bin/bash

CONTAINER_NAME="femida_bot"
IMAGE_NAME="femida_bot"

if [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Остановка и удаление контейнера: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
else
    echo "Контейнер $CONTAINER_NAME не найден."
fi

if [ "$(docker images -q $IMAGE_NAME)" ]; then
    echo "Удаление образа: $IMAGE_NAME"
    docker rmi $IMAGE_NAME
else
    echo "Образ $IMAGE_NAME не найден."
fi

echo "Сборка образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .


echo "Запуск контейнера: $CONTAINER_NAME"
docker run -d --name $CONTAINER_NAME $IMAGE_NAME
