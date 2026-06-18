import os

base = r'd:\cc.claude\ADHD'
raw = os.path.join(base, 'research_raw')

# Count sizes
prd_path = os.path.join(base, 'extracted_text.txt')
md_path = os.path.join(base, 'FocusReset_US_Market_Research_Report.md')
html_path = os.path.join(base, 'FocusReset_US_Market_Research_Report.html')
pdf_path = os.path.join(base, 'FocusReset_US_Market_Research_Report.pdf')
script_path = os.path.join(base, 'md2pdf.py')

sizes = {}
if os.path.exists(prd_path): sizes['PRD extracted text (input)'] = os.path.getsize(prd_path)
if os.path.exists(raw):
    total = 0
    for f in os.listdir(raw):
        fp = os.path.join(raw, f)
        if os.path.isfile(fp): total += os.path.getsize(fp)
    sizes['Research raw files (input)'] = total
    # count files
    html_count = len([f for f in os.listdir(raw) if f.endswith('.html')])
    txt_count = len([f for f in os.listdir(raw) if f.endswith('.txt')])
    sizes['  - HTML files'] = html_count
    sizes['  - TXT files'] = txt_count

if os.path.exists(md_path): sizes['MD report (output)'] = os.path.getsize(md_path)
if os.path.exists(html_path): sizes['HTML report (output)'] = os.path.getsize(html_path)
if os.path.exists(pdf_path): sizes['PDF report (output)'] = os.path.getsize(pdf_path)
if os.path.exists(script_path): sizes['md2pdf script (output)'] = os.path.getsize(script_path)

print('=' * 55)
for label, val in sizes.items():
    if isinstance(val, int) and val < 1000:
        print(f'{label:<40} {val:>4} files')
    else:
        print(f'{label:<40} {val:>6,} B  ({val/1024:.1f} KB)')

print('=' * 55)

# Count characters in key text files
total_chars = 0

if os.path.exists(prd_path):
    with open(prd_path, 'r', encoding='utf-8') as f:
        c = len(f.read())
        total_chars += c
        print(f'PRD chars: {c:,}')

if os.path.exists(raw):
    for f in os.listdir(raw):
        if f.endswith('.txt'):
            with open(os.path.join(raw, f), 'r', encoding='utf-8') as fh:
                total_chars += len(fh.read())
    print(f'Raw text chars (after deduction): included')

if os.path.exists(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        c = len(f.read())
        total_chars += c
        print(f'Report MD chars: {c:,}')

if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        c = len(f.read())
        total_chars += c
        print(f'Report HTML chars: {c:,}')

print()
print(f'Total text chars (input+output): {total_chars:,}')

# Token estimation: Mixed CN/EN ~2.5 chars per token
est_io_tokens = total_chars / 2.5
# Add: system prompts, conversation turns, tool call JSON, function defs
# Typically overhead is 1.5-3x of raw content tokens in a long conversation
est_total_low = est_io_tokens * 2.0
est_total_high = est_io_tokens * 3.0

print(f'Estimated I/O tokens: ~{est_io_tokens:,.0f}')
print(f'Estimated TOTAL tokens: ~{est_total_low:,.0f} to ~{est_total_high:,.0f}')
print()
print('This includes:')
print('  - PRD document analysis (137 paragraphs)')
print('  - 16 web pages fetched + text extracted')
print('  - 6 parallel agent launches (all failed with API error)')
print('  - ~10 conversation turns')
print('  - MD/HTML/PDF report generation')
print('  - System prompts and tool definitions')
print()
print('Note: Estimate only. Actual API token usage not accessible.')
