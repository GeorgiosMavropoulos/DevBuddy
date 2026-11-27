
"""
Test suite for the `TextSplitter` module.

This module validates text argument validation, error handling for chunk configuration parameters,
and recursive text splitting behavior using `pytest`.
"""


import pytest
from backend.ingestion.text_splitter import TextSplitter

def test_validate_arg_no_argument():
    """
    Validates that `__validate__arg` returns False when `None` (representing a missing argument) is provided.
    """
    splitter = TextSplitter()
   
    assert splitter._TextSplitter__validate__arg(None) is False

def test_validate_arg_bool():
    """
    Validates that `__validate__arg` returns False when boolean values are provided as arguments.
    """
    splitter = TextSplitter()
    # b. validate it returns false if add a bool argument.
    assert splitter._TextSplitter__validate__arg(True) is False
    assert splitter._TextSplitter__validate__arg(False) is False

def test_validate_arg_whitespace():
    """
    Validates that `__validate__arg` returns False when whitespace or empty strings are provided.
    """
    splitter = TextSplitter()
    # c. assert it returns false if string is a whitespace
    assert splitter._TextSplitter__validate__arg("   ") is False
    assert splitter._TextSplitter__validate__arg("\n\t") is False

def test_validate_arg_valid_string():
    """
    Validates that `__validate__arg` returns True when a valid non-empty string is provided.
    """
    splitter = TextSplitter()
    # d. validate that returns true if it contains a string for argument
    assert splitter._TextSplitter__validate__arg("Hello world") is True

def test_split_text_value_and_type_errors():
    """
    Tests that `split_text` correctly raises all expected `ValueError` and `TypeError` exceptions
    for invalid text inputs, invalid parameter types, non-positive chunk sizes, negative overlaps,
    and overlaps greater than or equal to chunk sizes.
    """
    splitter = TextSplitter()
    # a. test that the method returns all the expected ValueErrors/TypeErrors
    
    # 1. Invalid text (None / empty / bool)
    with pytest.raises(ValueError):
        splitter.split_text(None, 100, 20)
    with pytest.raises(ValueError):
        splitter.split_text("", 100, 20)
        
    # 2. Invalid chunk_size / chunk_overlap types (bool or non-int)
    with pytest.raises(TypeError):
        splitter.split_text("Valid text", True, 20)
    with pytest.raises(TypeError):
        splitter.split_text("Valid text", 100, False)
    with pytest.raises(TypeError):
        splitter.split_text("Valid text", "100", 20)
    with pytest.raises(TypeError):
        splitter.split_text("Valid text", 100, "20")
        
    # 3. chunk_size <= 0
    with pytest.raises(ValueError):
        splitter.split_text("Valid text", 0, 10)
    with pytest.raises(ValueError):
        splitter.split_text("Valid text", -50, 10)
        
    # 4. chunk_overlap < 0
    with pytest.raises(ValueError):
        splitter.split_text("Valid text", 100, -1)
        
    # 5. chunk_overlap >= chunk_size
    with pytest.raises(ValueError):
        splitter.split_text("Valid text", 100, 100)
    with pytest.raises(ValueError):
        splitter.split_text("Valid text", 100, 150)

def test_split_text_reaches_print_state(capsys):
    """
    Creates a 1000-character text and asserts that `split_text` successfully splits it into chunks,
    reaching the print state and outputting the expected chunk headers (e.g., 'Chunk 1:').
    """
    splitter = TextSplitter()
    # b. create an 1000 char text and assert it will reach this state: print(f"\nChunk {i+1}:\n{chunk}")
    long_text = "A" * 1000
    chunks = splitter.split_text(long_text, chunk_size=300, chunk_overlap=50)
    
    captured = capsys.readouterr()
    assert len(chunks) > 0
    assert "Chunk 1:" in captured.out
    for i, chunk in enumerate(chunks):
        assert f"Chunk {i+1}:" in captured.out
    assert splitter._TextSplitter__validate__arg(None) is False
