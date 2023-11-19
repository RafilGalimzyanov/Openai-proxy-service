# OpenAI - proxy 
build docker-containers 
```angular2html
docker-compose build
```
run docker-containers
```angular2html
docker-compose up
```
## Requirements
1. Store `.env` file.

Example of `.env`:
```angular2html
OPENAI_API_KEY = 'your_openai_key'
OPENAI_BASE_URL = 'https://your_proxy_bla.bla'

DB__USER=postgres
DB__PASSWORD=postgres
DB__HOST=postgres
DB__PORT=5432
DB__NAME=postgres
```
2. Store `secrets.json` in the root directory

Example of `secrets.json`
```json
{
  "login_1": "password_1",
  "login_2": "password_2"
}
```