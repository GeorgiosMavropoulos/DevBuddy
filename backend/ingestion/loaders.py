"""
This module contains the class with the method to ingest documents using simple python code.
 It contains the load_document function which is responsible to extract document's content
The program allows for PDF, DOCX and .md files

"""

from langchain_core.documents import Document
from pypdf import PdfReader
from pathlib import Path
import docx2txt

class Loaders:
    def __init__(self):
     """Initialize GEMINI embedding model"""
     self.path_file = "./data"  
     self.content = [] #store document's content   
 

    def load_documents(self,document:str)->list[Document]:
       """
       Function to read the document and parse its content
       Validates document type and acts properly

       Args:

            document: str (filepath)

       Returns: 
               document content: list[document]

       Raises:
                     ValueError if the provided file path is wrong or not supported
       """

       #return an error message if file path is empty
       self.__validate_file_path(document)
      
       #get the suffix of files
       ext = Path(document).suffix.lower()

       if ext == ".pdf": # if file is pdf use pdf handler
         docs = self.__handle_pdf_file(document)
                          
       elif ext == ".docx": # if file is word document use word handler
         docs = self.__handle_docx_file(document)

       elif ext in {".txt", ".md"}: # if file is txt or md use text file handler
         docs = self.__handle_text_file(document)
       else:
            raise ValueError(f"Unsupported document format: {ext}")


       
       #convert the document to a full string
       full_text = "\n".join(doc.page_content for doc in docs)
       self.content.append(full_text)
       print('File loaded!')
       return full_text



    @staticmethod
    def __handle_text_file(file: str) -> list[Document]:
      """Extract content from .txt and .md files."""
      text = Path(file).read_text(encoding="utf-8")
      return [Document(page_content=text, metadata={"source": file})]


    @staticmethod
    def __handle_docx_file(file:str) -> list[Document]:
        """Extract content from .docx file"""
        #return an error message if file path is empty
        Loaders.__handle_empty_file_argument(file)
        
        text = docx2txt.process(file)
        return [Document(page_content=text, metadata={"source": file})]
        
         

    @staticmethod
    def __handle_pdf_file(file: str) -> list[Document]:
        """Extract content from PDF files page by page."""
        reader = PdfReader(file)
        return [
            Document(
                page_content=page.extract_text() or "",
                metadata={"source": file, "page": i},
            )
            for i, page in enumerate(reader.pages)
        ]


    @staticmethod
    def __validate_file_path(file: str) -> None:
        """Validates that the file path is not empty and the file exists.
        Raises:
               ValueError if file path is wrong,
               FileNotFoundError if file does wasn't available
        """
        if not file or not file.strip():
            raise ValueError("Please insert a correct file path.")
        if not Path(file).is_file():
            raise FileNotFoundError(f"File not found: {file}")


<<<<<<< HEAD
=======


>>>>>>> 2872555 (removedtest call)
       
       



     

     