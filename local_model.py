from config import * 

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch 

class LocalModel(): 
    def __init__(self, ): 

        model_name = LLM_MODEL_NAME
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name,
                                                    device_map="auto",
                                                    trust_remote_code=False,
                                                    revision="main")
        
    def __call__(self, prompt): 
        with torch.no_grad(): 

            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(input_ids=inputs["input_ids"].to("cuda"), max_new_tokens=MAX_NEW_TOKENS)

            return (self.tokenizer.batch_decode(outputs)[0])