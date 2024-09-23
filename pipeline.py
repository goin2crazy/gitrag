from config import * 
from parsegit import save_user_repos, move_readme_files

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

# load fine-tuned model from hub
# from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch 

# load tokenizer

class get_a_context():
    def __init__(self, documents, top_k=1): 
            # store docs into vector DB
        index = VectorStoreIndex.from_documents(documents, )

        # configure retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=top_k,
        )
        # assemble query engine
        self.query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.3)],

        )
        self.top_k = top_k

    def __call__(self, query): 
        response = self.query_engine.query(query)
        # reformat response
        context = "Context:\n"
        for i in range(self.top_k):
            context = context + response.source_nodes[i].text + "\n\n"

        print(context)
        return context

class Main(): 
    def __init__(self, username, model='gemini'): 
        # Parse the user repositories 
        save_user_repos('repositories', username)
        move_readme_files('repositories', STATIC_FILES_DIR)

        # import any embedding model on HF hub (https://huggingface.co/spaces/mteb/leaderboard)
        Settings.embed_model = HuggingFaceEmbedding(model_name=RETRIEVER_MODEL_NAME)
        # Settings.embed_model = HuggingFaceEmbedding(model_name="thenlper/gte-large") # alternative model

        Settings.llm = None
        Settings.chunk_size = CHUNK_SIZE
        Settings.chunk_overlap = CHUNK_OVERLAP

        statis_dir = STATIC_FILES_DIR
        # articles available here: {add GitHub repo}
        documents = SimpleDirectoryReader(statis_dir).load_data()
        self.get_context = get_a_context(documents)
        
        if model == 'gemini': 
            from gemini_model import GeminiInference
            self.model = GeminiInference() 
        elif model=='local': 
            from local_model import LocalModel
            self.model= LocalModel()
        else: 
            print('undefined type of model')

    

    def __call__(self, query): 
        
        context = self.get_context(query)
        # prompt (with context)
        prompt_template_w_context = lambda context, comment: f"""[INST]
        You are GitGPT Which helps people to know information about user activity in github 

        {context}

        And there is your question or task: 
        '{comment}'
        [/INST]
        """
        prompt = prompt_template_w_context(context, query)
        return self.model(prompt)
        