from config import * 

import google.generativeai as genai
from pathlib import Path
from time import sleep

import os 

class GeminiInference():
  def __init__(self,):

    if "GEMINI_API_KEY" in [k for k, v in os.environ.items()]: 
        self.gemini_key = os.environ["GEMINI_API_KEY"]
    else: 
        self.gemini_key = str(input("Write you gemini api there (Or set the 'GEMINI_API_KEY' in enviroment variables):\n")).strip()

    genai.configure(api_key=self.gemini_key)
    generation_config = {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 32,
        "max_output_tokens": 4096,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    self.model = genai.GenerativeModel(model_name=GEMINI_MODEL,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)


  def prompt(self, *args, **kwargs):
    """
    Write there custom way to prompt to model or just return the text
    
    """
    return " ".join([str(arg) for arg in args])

  def extract_target_answer(self, response): 
    """
    Write there custom way to process the model output or just return the text
    
    """
    return response

  def get_response(self, input_text):
    prompt_parts = [
        input_text
    ]
    response = self.model.generate_content(prompt_parts)
    return response.text

  def __call__(self, *args, **kwargs):
    input_text = self.prompt(*args, **kwargs)

    output_text = self.get_response(input_text)
    
    return self.extract_target_answer(output_text)