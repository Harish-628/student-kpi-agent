import PyPDF2
path = r'C:\Users\batman\Downloads\Student Performance AI Agent.pdf'
reader = PyPDF2.PdfReader(path)
for i, page in enumerate(reader.pages):
    print(f"--- Page {i+1} ---")
    print(page.extract_text())
