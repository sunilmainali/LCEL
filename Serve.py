from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("groqapikey")
print("Using Groq API Key:", groq_api_key)
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

language = "French"
text = "I Love Programming in Python"

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser=StrOutputParser()

##create chain

chain = prompt_template | model | parser




## App definition
app=FastAPI(title="Langchain Server",
            description="A simple API server using Langchain runnable interfaces")

## Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)





# To run the server, use the command:
# python Serve.py
# You can then access the API at http://localhost:8000/translate
# To test the API, you can use a tool like Postman or curl with a POST request to http://localhost:8000/translate
# with a JSON body like:
# {
#     "language": "French",
#     "text": "I Love Programming in Python"
# }
# The response will be the translated text in French.
# Note: Make sure to set the environment variable `groqapikey` with your Groq API key before running the server.
# You can set it in a .env file or directly in your environment.
# Example .env file content:
# groqapikey=your_groq_api_key_here
# This code demonstrates how to use LCEL (LangChain Expression Language) to chain together components
# such as prompts, models, and output parsers to create a simple translation service using Gro
#q's Gemma2-9b-It model.
# The application is built using FastAPI, allowing for easy deployment and interaction via HTTP requests.
# The server can be run locally, and it provides an endpoint to translate text into a specified language.
