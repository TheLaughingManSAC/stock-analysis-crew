from groq import Groq

# Initialize Groq Client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

llm = Groq(api_key=groq_api_key)  # Initialize the Groq instance
