# Scrabble game server

#### Python based server for multiplayer gameplay to be used with any API based frontend.

## API

API URL:

    scrabble-backend-dev.capgemini.enl-projects.com

New version is updated after each commit on `main` branch (rolling update on K8S).

## Swagger Documentation

For documentation go to `/docs` address

## Exporting game results

[comment]: <> (Service exports a _**list**_ of players _ids_ in descending order &#40;Player who won has index 0&#41;)

[comment]: <> (i.e. `[17,64,9,24]`)

Address for export must be provided as docker variable (not implemented yet)
