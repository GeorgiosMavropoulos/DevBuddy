"""
Test suite for the `Loaders` ingestion module.

This module validates document loading, file type routing (.pdf, .docx, .txt, .md),
validation logic, and exception handling behavior using `pytest` and `unittest.mock`.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from backend.ingestion.loaders import Loaders
file_path = r"place a file path"

def test_load_documents_success(capsys):
    """
    Verifies the end-to-end `load_documents` happy path. Mocks file system checks and PDF
    parsing (`PdfReader`) to ensure that valid input yields the expected combined text,
    properly formats metadata, and successfully prints the confirmation side-effect ("File loaded!").
    """
    loaders = Loaders()
    
   
    with patch("backend.ingestion.loaders.Path.is_file", return_value=True), \
         patch("backend.ingestion.loaders.PdfReader") as mock_pdf_reader:
        
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Mocked PDF content"
        mock_pdf_reader.return_value.pages = [mock_page]
        
        result = loaders.load_documents(file_path)
        
        captured = capsys.readouterr()
        assert "File loaded!" in captured.out
        assert result == "Mocked PDF content"

def test_load_documents_missing_file():
    """
    Ensures that passing an empty string or null-like path to `load_documents`
    correctly triggers validation checks and raises either a `FileNotFoundError` or `ValueError`.
    """
    loaders = Loaders()
    # Missing file should call __validate_file_path and raise FileNotFoundError or ValueError
    with pytest.raises((FileNotFoundError, ValueError)):
        loaders.load_documents("")

def test_load_documents_invalid_path():
    """
    Tests input sanitization for `load_documents` when given whitespace-only paths,
    verifying that a `ValueError` is raised as expected by the validation rules.
    """
    loaders = Loaders()
    with pytest.raises(ValueError):
        loaders.load_documents("   ")

def test_handle_pdf_file():
    """
    Tests the private PDF loader helper method (`__handle_pdf_file`) in isolation.
    Mocks `PdfReader` page extraction to confirm that page contents are correctly
    mapped into LangChain `Document` objects with matching metadata and source paths.
    """
    with patch("backend.ingestion.loaders.PdfReader") as mock_pdf_reader:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "PDF text"
        mock_pdf_reader.return_value.pages = [mock_page]
        
        docs = Loaders._Loaders__handle_pdf_file(file_path)
        assert len(docs) == 1
        assert docs[0].page_content == "PDF text"
        assert docs[0].metadata["source"] == file_path

def test_handle_pdf_file_failure():
    """
    Validates robust error handling in `__handle_pdf_file` by injecting an exception
    side-effect into `PdfReader`, ensuring errors bubble up correctly with expected messages.
    """
    with patch("backend.ingestion.loaders.PdfReader", side_effect=Exception("PDF read error")):
        with pytest.raises(Exception, match="PDF read error"):
            Loaders._Loaders__handle_pdf_file("corrupt.pdf")

def test_handle_docx_file():
    """
    Tests the `.docx` document parsing handler (`__handle_docx_file`) using a mocked
    `docx2txt.process` call to guarantee proper conversion into LangChain `Document` format.
    """
    file_path = "dummy.docx"
    with patch("backend.ingestion.loaders.Path.is_file", return_value=True), \
         patch("docx2txt.process", return_value="Docx text"):
        docs = Loaders._Loaders__handle_docx_file(file_path)
        assert len(docs) == 1
        assert docs[0].page_content == "Docx text"
        assert docs[0].metadata["source"] == file_path

def test_handle_docx_file_failure():
    """
    Verifies failure propagation during Word document extraction by raising an exception
    via the mocked `docx2txt` processor.
    """
    file_path = "corrupt.docx"
    with patch("backend.ingestion.loaders.Path.is_file", return_value=True), \
         patch("docx2txt.process", side_effect=Exception("Docx error")):
        with pytest.raises(Exception, match="Docx error"):
            Loaders._Loaders__handle_docx_file(file_path)

def test_handle_text_file():
    """
    Tests plain text and markdown file extraction (`__handle_text_file`) by mocking
    `Path.read_text`, ensuring the file content is accurately captured into `Document` structures.
    """
    file_path = "dummy.txt"
    with patch("pathlib.Path.read_text", return_value="Text content"):
        docs = Loaders._Loaders__handle_text_file(file_path)
        assert len(docs) == 1
        assert docs[0].page_content == "Text content"
        assert docs[0].metadata["source"] == file_path

def test_handle_text_file_failure():
    """
    Ensures that missing text files correctly propagate a `FileNotFoundError` when attempting
    to read content from disk.
    """
    file_path = "missing.txt"
    with patch("pathlib.Path.read_text", side_effect=FileNotFoundError("Not found")):
        with pytest.raises(FileNotFoundError):
            Loaders._Loaders__handle_text_file(file_path)

def test_validate_file_path_empty():
    """
    Validates that the file path validator (`__validate_file_path`) correctly intercepts
    empty string inputs and raises a `ValueError` with the designated error message.
    """
    with pytest.raises(ValueError, match="Please insert a correct file path."):
        Loaders._Loaders__validate_file_path("")

def test_validate_file_path_not_found():
    """
    Verifies that `__validate_file_path` catches nonexistent file paths on disk and raises
    an appropriate `FileNotFoundError`.
    """
    with patch("pathlib.Path.is_file", return_value=False):
        with pytest.raises(FileNotFoundError):
            Loaders._Loaders__validate_file_path("nonexistent.pdf")
