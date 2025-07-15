





from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore



class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'mistral'})



vn.connect_to_sqlite('medical.db')


from vanna.flask import VannaFlaskApp
app = VannaFlaskApp(vn,allow_llm_to_see_data=True)
app.run()






