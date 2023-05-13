# Import the required modules from the llama_index library
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, GPTListIndex

# Function to perform a search query on the documents
def search(query):
    # Load the documents from the 'data' directory
    documents = SimpleDirectoryReader('data').load_data()
    
    # Create an index using the GPTVectorStoreIndex from the loaded documents
    index = GPTVectorStoreIndex.from_documents(documents)
    
    # Create a query engine using the index
    query_engine = index.as_query_engine()
    
    # Perform the search query on the query engine
    response = query_engine.query(query)
    
    # Return the response
    return response
