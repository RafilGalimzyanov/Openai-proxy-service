import pandas as pd

from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from starlette.responses import JSONResponse

from service.models import Document, User, ErrorMessage


embeddings = OpenAIEmbeddings()


def create_db(user: User, document: Document):
    df = pd.DataFrame(document.rows)
    loader = DataFrameLoader(df, page_content_column='question')
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    db = FAISS.from_documents(texts, embeddings)
    db.as_retriever()

    db.save_local(f'./service/faiss_index_{user.login}')

    return JSONResponse(content="Vector database created!")


def answer(user: User, prompt_template: str, input_variables: list, question: str):
    try:
        db = FAISS.load_local(f'./service/faiss_index_{user.login}', embeddings=embeddings)
    except (RuntimeError, FileNotFoundError, IsADirectoryError, Exception) as e:
        return ErrorMessage(message=e)

    prompt = PromptTemplate(template=prompt_template, input_variables=input_variables)
    chain = LLMChain(llm=OpenAI(temperature=0, max_tokens=500), prompt=prompt)

    relevants = db.similarity_search(question)
    doc = relevants[0].dict()['metadata']

    return chain.run(doc)
