from groq import Groq
import getpass
import os


if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Openai: ")

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Qual a capital do Brasil?"}],
    model = "openai/gpt-oss-120b",  
)

print(chat_completion.choices[0].message.content)
