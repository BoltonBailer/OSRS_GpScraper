
# **Reflection Report**

## **Name and Explanation of the Document**
This python script gets the info for a gold selling website and saves it at a .txt, then the second python scripts reads in the .txt file and update the chat prompt so it can give out current pricing info on gold.

---
## **How the Program Works**
I asked the AI to give me a simple explanation of how the program works. It responded:

### **1. Load the Document**
- The program starts by loading the document selected by the user. 
- If the document is a webpage, the program scrapes the content using BeautifulSoup. 
- The text is cleaned and saved into a file named `Selected_Document.txt`.

### **2. Process and Split the Document**
- The document is read from `Selected_Document.txt` and split into smaller, manageable chunks. 
- These chunks are separated by double newline characters (`\n\n`) to ensure each chunk represents a logical segment of the text.

### **3. Generate Embeddings**
- Using the `SentenceTransformers` library, each text chunk is converted into a numerical representation called an **embedding**. 
- These embeddings are stored in a dictionary, where each chunk is linked to its corresponding vector representation. 
- Embeddings allow the program to calculate the similarity between text segments efficiently.

### **4. Query the System**
- When the user enters a query, it is also converted into an embedding using the same `SentenceTransformers` model. 
- The program compares this query embedding to all the document embeddings using **cosine similarity**, which measures how closely two vectors are aligned. 
- The top three most similar chunks are retrieved.

### **5. Generate a Response**
- The retrieved chunks are combined into a single prompt and passed to a HuggingFace model (e.g., `flan-t5-small`). 
- This model generates a response that combines the user query and the context provided by the retrieved chunks. 
- The response is displayed as the final output.

### **6. Test and Analyze**
- The program can be tested with multiple queries, and its output is analyzed for relevance and accuracy. 

---

 1: What is the role of embeddings in this program, and why are they necessary?
💡 Why ask this?
Embeddings are at the core of your program’s ability to compare text meaningfully.

Answer:
Embeddings are numerical representations of text that capture semantic meaning rather than just word similarity. In this program, embeddings allow us to compare text chunks and queries in a mathematical space, making it possible to retrieve the most relevant responses.

 2: How does cosine similarity help find the most relevant text chunks?
💡 Why ask this?
Understanding cosine similarity is essential to knowing how your program ranks and retrieves relevant information.

Answer:
Cosine similarity measures the angle between two vectors (embeddings), which helps determine how similar two pieces of text are. A similarity score closer to 1 means the texts are very similar, while a score near 0 means they are not related.

Example:

Query: "What is the OSRS gold price?"
Stored text chunk: "OSRS gold currently costs $0.2028 per million."
Cosine similarity helps determine that this chunk is relevant.
3: What does sentence-transformers do in this program, and why was it chosen?
💡 Why ask this?
Understanding the role of sentence-transformers helps in optimizing and modifying the system.

Answer:
The sentence-transformers library is used to generate high-quality text embeddings. The model "all-MiniLM-L6-v2" is chosen because it is lightweight, fast, and effective for capturing semantic meaning in short text chunks. This makes it ideal for information retrieval tasks.

4: How does the "google/flan-t5-small" model generate responses from retrieved text?
💡 Why ask this?
Knowing how flan-t5-small works will help in understanding how final answers are generated.

Answer:
The "google/flan-t5-small" model is a fine-tuned T5 language model that generates text based on input prompts. In this program:

The user enters a query.
The most relevant text chunks are retrieved using cosine similarity.
The retrieved chunks + query are passed to flan-t5-small.
The model generates a coherent response.
Example Flow:

Query: "What is the OSRS gold price?"
Retrieved Chunk: "The current OSRS gold price is $0.2028 per M."
Model Response: "As of now, OSRS gold is selling for $0.2028 per million."

5: How does the program store and retrieve embeddings efficiently?
💡 Why ask this?
Efficient storage and retrieval impact speed and scalability.

Answer:
Instead of recomputing embeddings every time, they are stored in a dictionary (JSON or database) where:

Keys = Text Chunks
Values = Precomputed Embeddings
When a query is made:

Its embedding is computed.
Cosine similarity is applied to compare it against stored embeddings.
The top-3 most similar chunks are retrieved.
This approach dramatically speeds up retrieval, making the system scalable.

🔹 Bonus Question (For Advanced Understanding)
How could this system be improved for larger datasets or better accuracy?
💡 Why ask this?
Scaling AI-powered retrieval is a real-world challenge.

Possible Answer:

Use FAISS (Facebook AI Similarity Search) for faster nearest-neighbor searches.
Use a larger embedding model like "all-mpnet-base-v2" for better accuracy.
Implement hybrid search (combine embeddings + keyword matching).
Store embeddings in a vector database like Pinecone or Weaviate.


---

## **Performance Analysis**
I had to check it from beautoful soup to Selenoium because the webpage was coded using java.
### **Retrieval Quality**  
the program retrieves the gold and the cost of them and it compiles it to a list I can use to check prices 

### **Response Quality**  
The generated answers were accurate and contextually grounded. They demonstrated a clear understanding of the information from the retrieved content.

### **Possible Improvements**  
1. **Fine-tuning the Model:** Using a domain-specific dataset to fine-tune the HuggingFace model could improve the quality of the generated responses.  
2. **Expanding Retrieval Mechanism:** Incorporating more advanced vector storage solutions, such as Pinecone or FAISS, might improve the retrieval speed and accuracy for larger datasets.  
3. **User Interface:** Adding a simple graphical user interface would make the system more accessible to non-technical users.

---

## **Example Queries and Outputs**

### **Query 1:**  
Q; What is the current OSRS gold price?
A; As of now, OSRS gold is selling for approximately **$0.2028 per million**. Prices may fluctuate based on seller availability.

### **Query 2:**  
Q; Which seller has the best price for OSRS gold?
A;The best price for OSRS gold is currently **$0.2028 per M**, offered by **Searchy**. Other sellers include:
- **RPGStash** - $0.203 per M
- **Rhynogames** - $0.209 per M
Prices may change, so check back for updates.

### **Query 3:**  
Q;How much stock does Searchy have?
A;Seller **Searchy** currently has **8,770 M OSRS gold in stock**. Minimum purchase requirement is **200 M**.


---


