from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openAI_key = os.getenv("API_KEY")

client = OpenAI(api_key=openAI_key)

with open("book2txt/text.txt", "r", encoding="utf-8") as f:
    text = f.read()

sysprompt = """Following is text copied from a PDF of a book.

Your task:
1. Clean the formatting so it reads smoothly in TTS.
2. Remove repeated page furniture such as headers, footers, page numbers, running heads, and similar artifacts.
3. Replace diagrams, images, tables, charts, and other non-TTS content with short placeholders like "image removed" or "table removed".
4. Preserve the original content exactly. Do not paraphrase, summarize, or change wording.
5. Fix obvious PDF extraction issues only, such as broken line wraps, hyphenation caused by line breaks, and spacing errors.
6. Keep chapter titles, paragraph structure, and punctuation intact where possible. Since its copied from a pdf, lines are likely to be split. Fix that. Do not keep page numbers and simialar

Output only the cleaned text."""

print("Sending off to openAI")

response = client.responses.create(model="gpt-5.4", input= sysprompt +"\n" + text,)

with open("book2txt/output.txt", "w", encoding="utf-8") as f:
    f.write(response.output_text)

print("Finihsed")