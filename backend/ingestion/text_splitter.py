"""Text chunking utilities using LangChain's RecursiveCharacterTextSplitter.

This module provides the `TextSplitter` class to validate raw string inputs
and split large bodies of text into smaller, overlapping chunks suitable for
embeddings, retrieval-augmented generation (RAG), or LLM context windows.


"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
    def __init__(self):
     pass 
    
    
    
    
    def __validate__arg(self,text:str)-> bool:
        """
           Validates against empty arguments or not a string text

           Args:
                text -> str

           Returns:
                    True if text is string
                    False if no argument was provided or it wasn't a string representation

         
        """
        if isinstance(text, bool) or not isinstance(text,str):
            return False
        elif not text.strip():
            return False
        return True


    def split_text(self,text:str,chunk_size:int,chunk_overlap:int)->list[str]:
        """
         Using RecursiveCharacterTextSplitter splits the extracted string text into small chunks

         Args:
              text-> str
         
         Returns:
                 list[str] filled with chunked text

         Raises
                ValueError if text is not a string representation or argument is None
                 
        """
        #return an error message if text wasn't provided or variable is empty
        if not self.__validate__arg(text):
            raise ValueError('Data must be passed in string format. No empty argument is acceptable')

        #return an error message if chunk_size / chunk_overlap wasn't provided, they are not integers or they're bools
        if isinstance(chunk_size,bool) or isinstance(chunk_overlap,bool):
            raise TypeError(f'chunk_size or chunk_overlap cannot be booleans: {chunk_size}, {chunk_overlap}')      


        elif not isinstance(chunk_size,int) or not isinstance(chunk_overlap,int):
            raise TypeError(f'chunk_size or chunk_overlap must be integers: {chunk_size}, {chunk_overlap}')

        #raise ValueError if chunk_size / chunk_overlap  are zeros
        if chunk_size <= 0:
            raise ValueError(
                f"chunk_size must be greater than zero (got {chunk_size})"
            )

        if chunk_overlap < 0:
            raise ValueError(
                f"chunk_overlap cannot be negative (got {chunk_overlap})"
            )    

        #raise value error if chunk_overlap is bigger than chunk_size
        if chunk_overlap >= chunk_size:
            raise ValueError(
                f"chunk_overlap ({chunk_overlap}) must be smaller than chunk_size ({chunk_size})"
            )             
                
       
        #define splitter
        splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
         )
        
        #split text
        chunks = splitter.split_text(text)
        #print number of chunks if succeed
        for i, chunk in enumerate(chunks):
         print(f"\nChunk {i+1}:\n{chunk}")
        return chunks



        