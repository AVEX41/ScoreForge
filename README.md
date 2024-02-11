# ScoreForge

# Distinctiveness and Complexity

This project is focused on tracking performance in some kind of score. It does not match the idea of a social network or e-commerce site because; in this application, the user stores information about their performance in a game or sport (or anything other represented in numbers), to store their information for the sole purpose of seeing if they are improving or not. The complexity of this project is greatly increased by the fact that it is a Single Page Application, and relies on a lot of JavaScript interpereting the data from the backend, and displaying it in a way that is easy to understand and use.

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

The frontend is powered by HTML, CSS, and JavaScript. It uses bootstrap and adminkit to make the frontend look good and mobile responsive. The frontend uses JavaScript to communicate with the backend using Django's http, and to display the data in a way that is easy to understand and use.

## The develoment process

I started by building a minimal demo with basic features such as user authentication, The layout, and moving between pages. By then, the only model created was User, for the user authentication, so i continued by creating the rest of the models and their views.  
After that the backend was mostly done, so i started working on the frontend. I wanted a modern looking and responsive design and got inspired by the modern dashboard design and found adminkit which was an exstension of bootstrap. I started by creating the manage page and all the subpages. Then I created the design of the comp-page with the graph and table which shows all the datapoints for a perfomance indicator. After that i added the profile page and the user edit page. after that i added the dashboard and user favourite feature.

# Files and Directories

This section will explain the purpose of the files and directories in the project. It will exclude the files and directories that are created and managed by Django such as the migrations directory, apps.py.

## Configuration files

#### github_actions

The .github/workflows directory contains the github actions workflow file. This file is configured to test the backend every time a push or pull request is made in the repository.

#### Dockerfile and docker-compose.yml

The Dockerfile is used to configure how to build and run the backend in a docker container. and the docker-compose.yml is used to configure how to build the database and how they communicate with each other.

#### .prettierrc

The .prettierrc file is used to configure the prettier extension for the HTML files, to make the code consistent and easier to read.

## Backend

#### Admin.py

The admin.py file is used to register the models so it can be viewed and edited in the django admin interface.

#### models.py

The models.py file is used to define the models: User, PerformanceIndicator and DataPoint, and their fields. Models defined in this file are managed by Django's ORM and are used to store data in the database.

#### tests.py

The tests.py file is used to write unit tests for the backend, to make sure that the backend is working as expected.

#### urls.py

The urls.py is used to define what view (inside views.py) should be called when a certain url is visited.

#### views.py

The views.py is the most important file of the backend and contains the logic for the whole backend.

## Frontend

### templates

#### layout.html

The layout.html is the base template and contains the sidebar, navbar.

#### index.html

The index.html is the main page of the application and contains all the "pages" such as dashboard and manage.

#### login.html

The login.html is the login page of the application.

#### register.html

The register.html is the register page of the application.

### static

#### /favicon_io/\*

Contains the favicon for the application. In other words: the icon that is displayed in the browser tab.

#### /adminKit/\*

Contains the compiled adminkit css and js files.

#### comp-new.js

The comp-new.js file is used to handle the logic for page containing the form for adding, or editing, a datapoint. It also contains the logic to show the page in either add or edit mode.

#### comp-view.js

The comp-new.js file is used to define the logic for the comp-new page, the page where one can view the datapoins in a table and graph.

#### index.js

The index.js file is used to handle the logic of fetching and displaying the data for the dashboard, inside the graph.

#### manage.js

The manage.js file is used to handle the logic for the manage page, the page where one can view and edit the performance indicators. And also the logic for fetching and displaying all performance indicators for each user.

#### messages.js

The messages.js file is used to handle the logic for the messages that are displayed when some error happens or a form submission is returned.

#### new.js

The new.js file handles the logic for submitting the form that either edits or adds a performance indicator.

#### pages.js

The pages.js is managing the entire logic for switching between pages.

#### profile.js

The profile.js is used to handle the logic for the profile page, the page where one can view and edit the user information.
