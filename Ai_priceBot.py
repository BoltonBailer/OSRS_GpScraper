import json
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import T5Tokenizer, T5ForConditionalGeneration

# ------------------------------ STEP 1: LOAD & PROCESS TEXT ------------------------------ #

def process_text_file(file_path):
    """Reads the content of a file, splits it into chunks based on double newlines (\n\n)."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Split content into chunks
    chunks = content.split("\n\n")
    
    # Remove empty chunks
    return [chunk.strip() for chunk in chunks if chunk.strip()]

# ------------------------------ STEP 2: GENERATE EMBEDDINGS ------------------------------ #

def generate_embeddings(chunks, model):
    """Generates embeddings for a list of text chunks using SentenceTransformers."""
    return {chunk: model.encode(chunk).tolist() for chunk in chunks}

# ------------------------------ STEP 3: SAVE & LOAD EMBEDDINGS ------------------------------ #

def save_embeddings(embeddings_dict, file_path="embeddings.json"):
    """Saves embeddings dictionary to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(embeddings_dict, file, indent=4)

def load_embeddings(file_path="embeddings.json"):
    """Loads embeddings dictionary from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# ------------------------------ STEP 4: RETRIEVE MOST SIMILAR TEXT ------------------------------ #

def retrieve_top_chunks(query, embeddings_dict, model, top_n=3):
    """Finds the most similar text chunks to the query using cosine similarity."""
    text_chunks = list(embeddings_dict.keys())
    embeddings = np.array(list(embeddings_dict.values()))

    query_embedding = model.encode(query).reshape(1, -1)
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # Get indices of top N most similar text chunks
    top_indices = np.argsort(similarities)[-top_n:][::-1]

    # Retrieve top text chunks
    return [text_chunks[idx] for idx in top_indices]

# ------------------------------ STEP 5: GENERATE RESPONSE WITH FLAN-T5 ------------------------------ #

def generate_response(query, retrieved_chunks, t5_model, tokenizer):
    """Generates a response using the google/flan-t5-small model."""
    prompt = f"Context: {' '.join(retrieved_chunks)} \n\n Query: {query} \n Answer:"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    with torch.no_grad():
        output_ids = t5_model.generate(input_ids, max_length=100)

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# ------------------------------ MAIN EXECUTION ------------------------------ #

def main():
    # Load models
    print("Loading models...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
    t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

    # Process and generate embeddings (only if embeddings file doesn't exist)
    try:
        print("Loading existing embeddings...")
        embeddings_dict = load_embeddings()
    except FileNotFoundError:
        print("Generating embeddings from text file...")
        text_chunks = process_text_file("Selected_Document.txt")
        embeddings_dict = generate_embeddings(text_chunks, embedding_model)
        save_embeddings(embeddings_dict)
        print("Embeddings saved successfully.")

    # Main query loop
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break

        # Retrieve top similar text chunks
        top_chunks = retrieve_top_chunks(query, embeddings_dict, embedding_model)

        # Generate a response using the FLAN-T5 model
        response = generate_response(query, top_chunks, t5_model, tokenizer)

        # Print the response
        print("\nResponse:\n", response)

# Run the program
if __name__ == "__main__":
    main()
