#!/bin/sh
cd ${PWD}/crystallake/frontend
npm install
docker exec -it crystal_lake_app sh -c 'cd /app/frontend && npm run watch'