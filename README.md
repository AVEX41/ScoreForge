# ScoreForge

# How to run

## first time

```bash
#build
docker-compose up -d --build
# migrate and create superuser
docker-compose exec web python3 manage.py makemigrations
docker-compose exec web python3 manage.py migrate
docker-compose exec web python3 manage.py createsuperuser
```

## start container

```bash
#build
docker-compose up -d --build
```

## stop container

```bash
# stop
docker-compose down
```

# General Information

## Backend

The backend is powered by Django, a python web framework, and PostgreSQL. This application is designed as a Single Page Application. The backend utilizes Django's models to store data in a PostgreSQL database, and uses Django's http to communicate with the frontend using JSON response. The backend also uses Django's authentication system to authenticate users.

## Frontend

The frontend is powered by HTML, CSS, and JavaScript. It uses bootstrap and adminkit to make the frontend look good and mobile responsive.

# Distinctiveness and Complexity

This project is focused on tracking performance in some kind of score. It does not match the idea of a social network or e-commerce site because; in this application, the user stores information about their performance in a game or sport (or anything other represented in numbers), to store their information for the sole purpose of seeing if they are improving or not. The complexity of this project is greatly increased by the fact that it is a Single Page Application, and relies on a lot of JavaScript interpereting the data from the backend, and displaying it in a way that is easy to understand and use.
