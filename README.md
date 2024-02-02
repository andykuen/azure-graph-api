# azure-graph-api

## How to run on your local?

1. Install docker on your local
2. copy sample docker compose yml file to docker-compose.yml
   ```bash
   $ cp docker-compose.example.yml docker-compose.yml
   ```
3. modify env at docker-compose.yml
4. build docker images via makefile

   ```bash
   $ make dev
   ```

5. Access docker container

   ```bash
   $ make exec

   > python app.py
   ```
