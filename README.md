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
3Store `admins.json` in the root directory (to view logs)

Example of `admins.json`
```json
{
  "login_1": "password_1",
  "login_2": "password_2"
}
```
## Endpoints
| Method | Endpoint                                 | Description                                           | Input Model (Sample JSON)                                                                                                    | Response                                                                                     |
|--------|------------------------------------------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| POST   | /api/{login}:{password}/embeddings       | Create embeddings                                     | [EmbeddingRequest model](https://github.com/RafilGalimzyanov/Openai-proxy-service/blob/only-proxy/service/models.py#L10)     | [JSONResponse from OpenAI](https://platform.openai.com/docs/api-reference/embeddings/create) |
| POST   | /api/{login}:{password}/chat/completions | Create chat completion                                | [ChatCompletionRequest](https://github.com/RafilGalimzyanov/Openai-proxy-service/blob/only-proxy/service/models.py#L19)      | [JSONResponse from OpenAI](https://platform.openai.com/docs/api-reference/chat/create)       |

## Usage example
### OpenAI:
```jupyter
import os

from openai import OpenAI


os.environ['OPENAI_BASE_URL'] = "https://openai-proxy-bla-bla.com/api/LOGIN:PASSWORD"
os.environ['OPENAI_API_KEY'] = "blank-key"

client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))

message = [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
response = client.chat.completions.create(model="gpt-3.5-turbo", messages=message, max_tokens=10)
print(response)
```
### LangChain (OpenAI llm)
```jupyter
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter


os.environ['OPENAI_BASE_URL'] = "https://openai-proxy-ecn8.onrender.com/api/LOGIN:PASSWORD"
os.environ['OPENAI_API_KEY'] = "interns"

model = "gpt-3.5-turbo"
question = "How to install the program?"
loader = TextLoader(f"testing_text.txt")

index = VectorstoreIndexCreator(text_splitter=CharacterTextSplitter(chunk_size=2000)).from_loaders([loader])
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model=model),
    retriever=index.vectorstore.as_retriever(
        search_kwargs={'k': 1}
    )
)
result = chain({'question': question, 'chat_history': []})
print(result["answer"])
```
