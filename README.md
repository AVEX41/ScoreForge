# ScoreForge

## TODO
- add route to login.html

## first time
````bash
#build
docker-compose up -d --build
# migrate and create superuser
docker-compose exec web python3 manage.py makemigrations
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
- use grid for each component
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


#### JSON - ScoreTable
- JSON should be able to be fetched from a URL.

````` json

{
    "name": "name of the score",
    "description": "description of the score",
    "score": [
        {
            "date": "date of the performance",
            "totalScore": "score of the performance",
            "totalInners": "total inners",
        },
        {
            "date": "date of the performance",
            "score": "score of the performance",
            "totalInners": "total inners",
        },
        {
            "date": "date of the performance",
            "score": "score of the performance",
            "totalInners": "total inners",
        }
    ]
}
`````


#### JSON - ShotDetails
- JSON should be able to be fetched from a URL.

````` json
{
    "date": "date of the performance",
    "score": [
        {
            "shotNumber": "the number of the shot",
            "score": "score of the performance",
            "inner": "true/false",
        },
        {
            "shotNumber": "the number of the shot",
            "score": "score of the performance",
            "inner": "true/false",
        },
        {
            "shotNumber": "the number of the shot",
            "score": "score of the performance",
            "inner": "true/false",
        }
    ]
}
`````