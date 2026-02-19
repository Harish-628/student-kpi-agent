import PyPDF2
import sys

path = r'C:\Users\batman\Downloads\Student Performance AI Agent.pdf'
reader = PyPDF2.PdfReader(path)
for i, page in enumerate(reader.pages):
    sys.stdout.buffer.write(f"--- Page {i+1} ---\n".encode('utf-8'))
    text = page.extract_text() or ''
    sys.stdout.buffer.write(text.encode('utf-8', errors='ignore'))
    sys.stdout.buffer.write(b"\n")
