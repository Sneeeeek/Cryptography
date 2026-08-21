from openai import OpenAI
client = OpenAI(api_key="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")

with open("book2txt/text.txt", "r", encoding="utf-8") as f:
    text = f.read()

sysprompt = """Following is text copied from a PDF of a book.

Your task:
1. Clean the formatting so it reads smoothly in TTS.
2. Remove repeated page furniture such as headers, footers, page numbers, running heads, and similar artifacts.
3. Replace diagrams, images, tables, charts, and other non-TTS content with short placeholders like "image removed" or "table removed".
4. Preserve the original content exactly. Do not paraphrase, summarize, or change wording.
5. Fix obvious PDF extraction issues only, such as broken line wraps, hyphenation caused by line breaks, and spacing errors.
6. Keep chapter titles, paragraph structure, and punctuation intact where possible.

Output only the cleaned text."""

print("Sending off to openAI")

response = client.responses.create(model="gpt-5.4-mini", input= sysprompt +"\n" + text,)

with open("book2txt/output.txt", "w", encoding="utf-8") as f:
    f.write(response.output_text)

print("Finihsed")