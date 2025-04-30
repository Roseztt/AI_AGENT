
from chromaLoader import get_embedding_function
import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Here is how to read the data:
To read this data each row represents a data point: these data points can be compared, 
the Data record time represents the time that each data is recorded they are listed in order in year-month-date(space)time format with the first data point being the earliest and the last data point being the latest. 
The Measured electricty record the electricty used by each breaker at that Data record time, the higher the number the more electricty used.

These data are ordered by their RPP followed by it's Breaker and each data point of the same breaker is ordered by the time recorded.
For example All the data points of RPP A-1-1 are listed together arraged by all it's breaker and the recorded time.
Note that the Breaker can have the same name but they are different breaker under different RPP. 
Example: Breaker 1/3 of RPP A-1-1 is NOT the same as Breaker 1/3 of RPP A-1-2
Note that each RPP can have multiple Breakers but each breaker can only have one RPP

And the letter and number of each RPP repersents  which selection the RPP belongs to
For example RPP A-1-1 is the first RPP in selection A1
RPP A-1-2 is the second  RPP in selection A1 so on

you can view each breaker of a RPP as a unit, each unit's data is ordered by time, it means the data is recorded at that time on that unit
the Measured electricty on each line is the actual data recorded. It repersents the amount of electricty used by that unit at that time.
Now answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str)
    parser.add_argument("top_k", type=int)
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB 
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=10)

    #join document content
    document_contents = []
    for document, score_value in results:
        text_content = document.page_content
        document_contents.append(text_content)
    
    separator = "\n\n---\n\n"

    context_text = separator.join(document_contents)

    #create prompt for LLM to understand
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    #generate response using LLM
    model = OllamaLLM(model="deepseek-r1:8b")
    response_text = model.invoke(prompt)

    #Gathering sources
    sources = []

    for document, score_value in results:
        metadata = document.metadata
        source_id = metadata.get("id", None)
        sources.append(source_id)

    #format and return LLM responds
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()