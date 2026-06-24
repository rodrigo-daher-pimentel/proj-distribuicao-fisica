import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document
doc = Document(r'C:\Users\rodri\Downloads\ENG4560_RelatorioSprint01_Equipe_2_3VA.docx')
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f'P{i}|[{p.style.name}]|{p.text}')
print('---TABLES---')
for ti, t in enumerate(doc.tables):
    print(f'TABLE {ti}: {len(t.rows)} rows x {len(t.columns)} cols')
    for ri, row in enumerate(t.rows[:3]):
        cells = [c.text[:80] for c in row.cells]
        print(f'  R{ri}: {cells}')
