import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# create the chat model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192"),
    temperature=0.1,
    max_tokens=4096
)

# track usage
total_calls = 0
total_tokens = 0


def call_llm(prompt, system_prompt="You are a helpful assistant"):
    # send prompt to groq and get text back
    
    global total_calls, total_tokens
    
    messages = [
        ("system", system_prompt),
        ("human", prompt)
    ]
    
    result = llm.invoke(messages)
    
    # update counts
    total_calls += 1
    tokens = result.response_metadata.get("token_usage", {}).get("total_tokens", 0)
    total_tokens += tokens
    
    return result.content


def get_usage():
    # return current usage stats
    
    return {
        "total_calls": total_calls,
        "total_tokens": total_tokens
    }


def reset_usage():
    # reset counters
    
    global total_calls, total_tokens
    total_calls = 0
    total_tokens = 0