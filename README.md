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
# Endpoints
| Method | Endpoint                         | Description                                           | Input Model (Sample JSON)                                                                                                                                                                                                           | Response                                            |
|--------|----------------------------------|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| POST   | /api/openai/chat                 | Send a request to openai                              | {"user": {"login": "Test","password": "123"},"message": {"dialog_contexts": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "How are you?"}],"configs": [{"model": "gpt-3.5-turbo"}]} } | JSONResponse from OpenAI                            |
| POST   | /api/langchain/vector_base       | Create a vector database                              | {"user": {"login": "Test","password": "123"},"document":{"rows":[{"id": 1, "question": "How to recover your password?", "answer": "To recover your password, follow the link 'Forgot your password?' on the login page..."}]}}      | JSONResponse with context "Vector database created! |
| POST   | /api/langchain/vector_base/query | Request with a prompt for the created vector database | {"user": {"login": "Test","password": "123"},"config":{"prompt_template": "...","input_variables": [...],"question": "..."}}                                                                                                        | Text reply                                          |

