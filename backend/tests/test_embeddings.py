"""
Test suite for the Embeddings class in backend.ingestion.embeddings.

This module validates constructor argument validation, chunk filtering, batch size
boundary checks, and mock interaction with the Gemini API for successful embedding generation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from ingestion.embeddings import Embeddings


def test_constructor_empty_or_blank_chunks():
    """
    Test that providing an empty list or a list with blank strings to the
    Embeddings constructor raises a ValueError with the expected message.
    """
    # Empty list
    with pytest.raises(ValueError, match="Chunks list cannot be empty or contain blank strings."):
        Embeddings(chunks=[])

    # List containing blank strings
    with pytest.raises(ValueError, match="Chunks list cannot be empty or contain blank strings."):
        Embeddings(chunks=["   ", "valid chunk"])


def test_batch_size_is_boolean():
    """
    Test that passing a boolean value for batch_size raises a ValueError.
    """
    with pytest.raises(ValueError, match="batch_size must be an integer between 1 and 100."):
        Embeddings(chunks=["valid chunk"], batch_size=True)


def test_batch_size_is_not_int():
    """
    Test that passing a non-integer (e.g., float or string) for batch_size
    raises a ValueError.
    """
    # Test with a float value
    with pytest.raises(ValueError, match="batch_size must be an integer between 1 and 100."):
        Embeddings(chunks=["valid chunk"], batch_size=50.5)  # type: ignore

    # Test with a string value
    with pytest.raises(ValueError, match="batch_size must be an integer between 1 and 100."):
        Embeddings(chunks=["valid chunk"], batch_size="50")  # type: ignore


def test_batch_size_out_of_range():
    """
    Test that passing an integer outside the range [1, 100] for batch_size
    raises a ValueError.
    """
    with pytest.raises(ValueError, match="batch_size must be an integer between 1 and 100."):
        Embeddings(chunks=["valid chunk"], batch_size=0)

    with pytest.raises(ValueError, match="batch_size must be an integer between 1 and 100."):
        Embeddings(chunks=["valid chunk"], batch_size=101)


@patch("ingestion.embeddings.genai.Client")
def test_create_embeddings_success(mock_genai_client):
    """
    Test that loading a correct chunk (a string letter * 1000 and batch_size=100)
    successfully calls create_embeddings and returns embeddings without error.
    """
    # Mock the client instance and its embed_content response
    mock_client_instance = MagicMock()
    mock_genai_client.return_value = mock_client_instance

    mock_embedding_obj = MagicMock()
    mock_embedding_obj.values = [0.1, 0.2, 0.3]
    mock_response = MagicMock()
    mock_response.embeddings = [mock_embedding_obj]
    mock_client_instance.models.embed_content.return_value = mock_response

    chunk = "a" * 1000
    embeddings_instance = Embeddings(chunks=[chunk], batch_size=100)

    # Verify that the API was called and embeddings were successfully returned
    mock_client_instance.models.embed_content.assert_called_once()
    assert embeddings_instance.embeddings == [[0.1, 0.2, 0.3]]
