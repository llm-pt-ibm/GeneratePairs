import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MUTATION_MODEL = os.environ.get("MUTATION_MODEL", "gpt-4o")