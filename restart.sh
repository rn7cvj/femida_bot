#!/bin/bash

CONTAINER_NAME="femida_bot"
IMAGE_NAME="femida_bot"

# Проверяем, существует ли контейнер
if [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "Остановка и удаление контейнера: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
else
    echo "Контейнер $CONTAINER_NAME не найден."
fi

# Проверяем, существует ли образ, и удаляем его
if [ "$(docker images -q $IMAGE_NAME)" ]; then
    echo "Удаление образа: $IMAGE_NAME"
    docker rmi $IMAGE_NAME
else
    echo "Образ $IMAGE_NAME не найден."
fi

# Сборка нового образа
echo "Сборка образа: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Запуск контейнера
echo "Запуск контейнера: $CONTAINER_NAME"
# Используем --env-file .env, если файл существует, иначе просто запускаем
if [ -f .env ]; then
    docker run -d --name $CONTAINER_NAME --env-file .env $IMAGE_NAME
else
    echo "Файл .env не найден, запускаем без него (убедитесь, что переменные окружения заданы)"
    docker run -d --name $CONTAINER_NAME $IMAGE_NAME
fi
