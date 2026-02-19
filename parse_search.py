import PyPDF2

path = r'C:\Users\batman\Downloads\Student Performance AI Agent.pdf'
reader = PyPDF2.PdfReader(path)
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ''
    if 'Day' in text:
        print('--- Page',i+1,'---')
        for line in text.splitlines():
            if 'Day' in line:
                print(line)
