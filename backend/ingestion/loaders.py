"""
This module contains the class with the method to ingest documents using simple python code.
 It contains the load_document function which is responsible to extract document's content
The program allows for PDF, DOCX and .md files

"""

from langchain_community.document_loaders import(PyPDFLoader, TextLoader, Docx2txtLoader)
class Loaders:
    def __init__(self):
     """Initialize GEMINI embedding model"""
     self.path_file = "./data"  
     self.content = [] #store document's content   
 

    def load_documents(self,document:str)->str:
       """
       Function to read the document and parse its content
       Validates document type and acts properly

       Args:

            document: str (filepath)

       Returns: 
               document's content: str
       """

    #return an error message if file path is empty
       Loaders.__handle_empty_file_argument(document)

       if document.endswith('.pdf'):
          """
          if document ends with pdf use the pdf reader
          """
          doc = Loaders.__handle_pdf_file(document)
          

       elif document.endswith('.txt'):
          """handle txt"""
          doc = Loaders.__handle_txt_file(document)
          
       elif document.endswith('.docx'):
           """handle docx files"""
           doc = Loaders.__handle_docx_file(document)
           

       elif document.endswith('.md'):
          """Handle .md files"""
          doc = Loaders.__handle_md_file(document)
          

       else:
          return 'Unsupported document format'

       
       #convert the document to a full string
       full_text = "\n".join(doc.page_content for doc in doc)
       self.content.append(full_text)
       return full_text



    @staticmethod
    def __handle_md_file(file:str)-> list:
     """Extract content from .md files"""
     # 2. Load a .md file as plain text
     md_loader = TextLoader(file, encoding="utf-8")
     md_docs = md_loader.load()
     return md_docs


    @staticmethod
    def __handle_docx_file(file:str)-> list:
        """Extract content from .docx file"""
        #return an error message if file path is empty
        Loaders.__handle_empty_file_argument(file)
        
        docx_loader = Docx2txtLoader(file)
        docx_docs = docx_loader.load()
        return docx_docs 
        
    @staticmethod
    def __handle_txt_file(file:str)-> list:
       """Extract content from txt file"""

       #return an error message if file path is empty
       Loaders.__handle_empty_file_argument(file)

       
       txt_loader = TextLoader(file, encoding="utf-8")
       txt_docs = txt_loader.load()
       return txt_docs

          

    @staticmethod
    def __handle_pdf_file(file:str)-> list:
       """
        Private method to handle PDF files
       """

       #return an error message if file path is empty
       Loaders.__handle_empty_file_argument(file)

       loader = PyPDFLoader(file)
       pages = loader.load()

       return pages 


    @staticmethod
    def __handle_empty_file_argument(file:str)->None:
        """return false if file is empty"""
        if not file or not file.strip():
            return 'Please insert a correct file path'

       
       



     

     