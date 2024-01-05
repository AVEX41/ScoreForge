# ScoreForge

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

## Idea

-   Single page application
-   user login and get a "admin dashboard"

#### dashboard

-   shows the favourite performance-tracker. (scoreTables)
-   own widget that shows change in score of favourite from last time.
-   button to manage the favourited scoreTable's data.
-   navigation bar button to manage scoreTables.

#### manage scoreTables

-   shows all the scoreTables in a table.
    -   each row is a scoreTable.
    -   each row has a button to manage the specific scoreTable's data.

##### styling

-   navbar on left (if on wider device).
-   else on top.
-   blue themed.

#### ScoreTable data

-   when clicked on a specific ScoreTable:
    -   show a loading page.
    -   page should fetch a JSON to get information about the performance.
    -   shows a graph, that shows all the perfomances.
