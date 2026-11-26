"""
 Using RecursiveCharacterTextSplitter splitting the retrieved text in small chunks 
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
    def __init__(self,text):
        self.text = text

         #validate init arguments
        if not self.__validate_init_arg(text):
            raise ValueError('Data must be passed in string format. No empty argument is acceptable')



    def __validate_init_arg(self,text:str)-> bool:
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