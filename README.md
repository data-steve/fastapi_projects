
# Start poetry env
```bash
poetry shell
```


# Start docker if not already
```bash
open /Applications/Docker.app
```


# Run postgres via docker
```bash
docker compose up -d
```




# PGAdmin : 
1. open http://localhost:8080
2.  login : 
    - usr: admin@example.com
    - pwd : admin
3. Add new server
    - Host: db
    - Port: 5432
    usr/pwd: postgres 

# Created FASTAPI table



# COnnecting to table in fastapi app
- host=localhost 
- dbname=fastapi 
- user=postgres 
- password=postgres

# Start FastAPI
```bash
uvicorn app.main:app --reload
```