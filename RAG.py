
import openai
from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader
from llama_index import Document

openai.api_key = "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"

documents = SimpleDirectoryReader(
    input_files=["./biblia.pdf"]
).load_data()

print(type(documents), "\n")
print(len(documents), "\n")
print(type(documents[0]))
print(documents[0])

document = Document(text="\n\n".join([doc.text for doc in documents]))

llm = OpenAI(model="gpt-4-1106-preview", temperature=0.1)
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
)
index = VectorStoreIndex.from_documents([document],
                                        service_context=service_context)

query_engine = index.as_query_engine()

response = query_engine.query(
    "qué milagros hizo jesús? dame una lista detallada y el fragmento fuente"
) 
print(str(response))