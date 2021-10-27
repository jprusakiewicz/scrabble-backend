# scrabble-backend

#### Python based server for multiplayer gameplay to be used with any API based frontend.

## API

API URL:

    scrabble-backend-dev.capgemini.enl-projects.com

New version is updated after each commit on `main` branch (rolling update on K8S).

## Swagger Documentation

For documentation go to `/docs` address

## Exporting game results

Service exports a _**list**_ of players ids and their points

i.e. `[{'player_id': 'pl4y3rid', "score": 350}]`


