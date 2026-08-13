from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

def generate_answer(query,context):
    load_dotenv()
    client = genai.Client()

    system_instruction = (
        "You are a helpful assistant. Answer questions using only the provided context. "
        "Provide a concise answer. If you don't find the info in the context, do not guess—"
        "state that the info is not found in the document."
    )
    prompt = f"""
    Context:
    {context}

    Question:
    {query}
    """
    response = client.interactions.create(
        model="gemini-2.5-flash",
        input=  prompt,
        system_instruction=system_instruction,
        generation_config={
            "temperature": 0
        }
    )
    return response.output_text

if __name__ == '__main__':
    from app.rag.retriever import retrieve_query
    query = input("Please enter your question: ") 
    results = retrieve_query(query)
    chunks = results["documents"][0]
    context = "\n\n".join(chunks)
    answer = generate_answer(query,context)
    print("\n Answer: ")
    print(answer)
