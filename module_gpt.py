from openai import OpenAI
import streamlit as st
import pdf_processor
import time

def exe_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        tiempo_total = (end_time - start_time) / 60 
        print(f"La función {func.__name__} tardó {tiempo_total:.2f} minutos en ejecutarse.")
        return result
    return wrapper

@exe_time
def ask_gpt(contexto,
            question,
            # gpt-4-1106-preview
            model="gpt-4-1106-preview",
            temperature=0):

    client = OpenAI(api_key="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")  

    context = contexto  + question  
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": context}],
        temperature=temperature,
        #max_tokens=100
    )
    return (question, response.choices[0].message.content)

def unir_elementos(tuplas):
    # Unimos el segundo elemento de cada tupla y agregamos un salto de línea
    return ''.join([tupla[1] + '\n\n' for tupla in tuplas])

