"""This module contains the embedding class which is responsible to transform the chunked text into an embeddings representation"""
from google import genai
from google.genai import errors
import time
from dotenv import load_dotenv
load_dotenv()
class Embeddings:
    def __init__(self,chunks,batch_size = 100):
               
        
        """
            Initialization if Embeddings constructor. 
            Once an object is being created the method: create_embeddings is being called
            Args:
                chunks -> list[str]
                batch_size: Maximum number of chunks to send per API request (1 to 100).
                   
            Raises:
                   TypeError if chunks is not a valid list[str] or is boolean
                   ValueError if chunks list is empty
        """
        #raise errors if chunks are missing or they're not string

        if not isinstance(chunks, list) or not all(isinstance(c, str) for c in chunks):
            raise TypeError(f"Chunks must be a valid list of strings, got: {type(chunks).__name__}")
        
        if not chunks or any(not c.strip() for c in chunks):
            raise ValueError("Chunks list cannot be empty or contain blank strings.")
        
        if isinstance(batch_size, bool) or not isinstance(batch_size, int) or not (1 <= batch_size <= 100):
            raise ValueError("batch_size must be an integer between 1 and 100.")

        self.chunks = chunks
        self.client = genai.Client()
        self.batch_size = batch_size
        #call create embeddings method to transform the string
        self.embeddings = self.create_embeddings(self.chunks)


    def create_embeddings(self, chunks: list[str]) -> list[list[float]]:
        """Create embedding vectors from a list of text chunks using Gemini.

        Args:
            chunks: A list of text strings to embed.

        Returns:
            A list of embedding vectors (each vector is a list of floats).

        Raises:
            RuntimeError: If a temporary server error (500, 503, 504) occurs.
            errors.APIError: For non-retryable Gemini API errors (e.g., 400, 401, 429).
                 
        """

        #create an empty list to store the embeddings
        all_emb = []

        #use a for loop to iterate through chunks
        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i : i + self.batch_size]

        try:
            
            result = self.client.models.embed_content(
                model="gemini-embedding-2",
                contents=batch
            )

            #add the embeddings into the list
            all_emb.extend(embedding.values for embedding in result.embeddings)
        
        except errors.APIError as e:
             if e.code in (500, 503, 504):
                 return f"Temporary error {e.code} ({e.status})"
             
        except ValueError as e:
            return f"Invalid input data: {e}"

        #brief pause between batches to avoid 429 rate limits on free/low tiers
        if i + self.batch_size < len(chunks):
            time.sleep(0.1)


        return all_emb


                


    