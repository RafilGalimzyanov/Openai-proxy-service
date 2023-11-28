from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter


def retrieve(user, config):
    model = config.pop("model", "gpt-3.5-turbo")
    question = config.pop("question", "")

    if db_name := config.pop("db_name", None):
        loader = TextLoader(f"db/db_{db_name}")
    else:
        loader = TextLoader(f"db/db_{user.login}")

    index = VectorstoreIndexCreator(text_splitter=CharacterTextSplitter(**config)).from_loaders([loader])
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=model),
        retriever=index.vectorstore.as_retriever(
            search_kwargs={'k': 1}
        )
    )
    result = chain({'question': question, 'chat_history': []})
    return result["answer"]
