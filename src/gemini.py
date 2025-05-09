from dotenv import load_dotenv
import os

load_dotenv()

def gemini_key() -> str:
    if not os.getenv('GEMINI_API_KEY'):
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    return os.getenv('GEMINI_API_KEY')

def gemini_model() -> str:
    """Retrieves the Gemini model name from environment variables or uses a default.

    Args:
        None(None): No parameters are needed.

    Returns:
        str: The name of the Gemini model, either from the environment variable GEMINI_MODEL or the default "gemini-2.0-flash".

    Raises:
        Exception: Any exception raised during environment variable access.
    """
    if not os.getenv('GEMINI_MODEL'):
        return 'gemini-2.0-flash'
    return os.getenv('GEMINI_MODEL')