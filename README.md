# ScoreForge


## first time
````bash
#build
docker-compose up -d --build
# migrate and create superuser
docker-compose exec web python3 manage.py migrate
docker-compose exec web python3 manage.py createsuperuser
````

## start container
````bash
#build
docker-compose up -d --build
````

## stop container
````bash
# stop
docker-compose down
````


## Idea
- Single page application
- user login and get a "dashboard"
- track the progress of score -> specialized for shooting-score

#### dashboard
- shows all the performance-trackers. (scoreTables)
- shows one favourite.
- own widget that shows change in score.

##### styling
- navbar on left (if on wider device).
- else on top.
- blue themed.
- able for both darkmode and whitemode.

#### ScoreTable
- when clicked on a specific ScoreTable:
    - show a loading page
    - page should fetch a JSON to get information about the performance
    - shows a graph, that shows all the perfomances
    - able to see specific information about each "node", or perfomance score logged on a seperate part of the page (fetch on request).