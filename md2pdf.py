import re, os
from fpdf import FPDF

FONT_PATH = 'C:/Windows/Fonts/NotoSansSC-VF.ttf'

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('CJK', '', FONT_PATH, uni=True)
        self.add_font('CJK', 'B', FONT_PATH, uni=True)

    def header(self):
        if self.page_no() == 1:
            self.set_font('CJK', 'B', 8)
            self.set_text_color(120,120,120)
            self.cell(0, 5, 'FocusReset US Market Research Report  |  June 2026  |  Confidential', align='C')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('CJK', '', 7)
        self.set_text_color(150,150,150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def write_h1(self, text):
        if self.get_y() > 240:
            self.add_page()
        self.set_font('CJK', 'B', 16)
        self.set_text_color(26, 58, 92)
        self.cell(0, 11, text, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(46, 117, 182)
        self.set_line_width(0.6)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(5)

    def write_h2(self, text):
        self.set_font('CJK', 'B', 12)
        self.set_text_color(46, 117, 182)
        self.cell(0, 7, text, new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(200,200,200)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(4)

    def write_h3(self, text):
        self.set_font('CJK', 'B', 10)
        self.set_text_color(50,50,50)
        self.cell(0, 6, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def write_para(self, text):
        self.set_font('CJK', '', 9)
        self.set_text_color(34,34,34)
        self.multi_cell(0, 5, text, align='L')
        self.ln(1)

    def write_blockquote(self, text):
        self.set_font('CJK', '', 8.5)
        self.set_text_color(80,80,80)
        x0 = self.l_margin + 6
        self.set_x(x0)
        self.set_draw_color(46, 117, 182)
        self.set_line_width(0.4)
        y0 = self.get_y()
        self.line(self.l_margin + 1, y0, self.l_margin + 1, y0 + 5)
        self.multi_cell(self.w - 2*self.l_margin - 12, 5, text)
        self.ln(2)

    def write_bullet(self, text):
        self.set_font('CJK', '', 9)
        self.set_text_color(34,34,34)
        indent = 6
        self.cell(indent, 5, chr(0x2022))
        self.multi_cell(self.w - 2*self.l_margin - indent, 5, text)
        self.ln(0.5)

    def write_table(self, rows, col_weights=None):
        if not rows:
            return
        ncols = max(len(r) for r in rows)
        if col_weights is None:
            col_weights = [1.0] * ncols

        total_w = self.w - 2 * self.l_margin
        col_w = [total_w * w / sum(col_weights) for w in col_weights[:ncols]]
        line_h = 5.5

        for ri, row in enumerate(rows):
            if self.get_y() > 250:
                self.add_page()

            # Calculate wrapped text for each cell
            cell_texts = []
            max_lines = 1
            for ci in range(ncols):
                txt = str(row[ci]) if ci < len(row) else ''
                words = txt.split(' ')
                lines_in_cell = []
                current_line = ''
                for word in words:
                    test = (current_line + ' ' + word).strip()
                    if self.get_string_width(test) < col_w[ci] - 2:
                        current_line = test
                    else:
                        if current_line:
                            lines_in_cell.append(current_line)
                        current_line = word
                if current_line:
                    lines_in_cell.append(current_line)
                if not lines_in_cell:
                    lines_in_cell = ['']
                cell_texts.append(lines_in_cell)
                max_lines = max(max_lines, len(lines_in_cell))

            cell_h = line_h * max_lines

            # Header style
            if ri == 0:
                self.set_fill_color(46, 117, 182)
                self.set_text_color(255, 255, 255)
            else:
                if ri % 2 == 0:
                    self.set_fill_color(245, 248, 252)
                else:
                    self.set_fill_color(255, 255, 255)
                self.set_text_color(34, 34, 34)

            y_before = self.get_y()
            x_start = self.l_margin

            for ci in range(ncols):
                x_pos = x_start + sum(col_w[:ci])
                self.set_xy(x_pos, y_before)
                self.set_draw_color(200, 200, 200)
                self.set_line_width(0.1)
                self.rect(x_pos, y_before, col_w[ci], cell_h, style='DF')

                for li, line_text in enumerate(cell_texts[ci]):
                    self.set_xy(x_pos + 1, y_before + li * line_h)
                    self.set_font('CJK', 'B' if ri == 0 else '', 7.5)
                    if ri == 0:
                        self.set_text_color(255, 255, 255)
                    else:
                        self.set_text_color(34, 34, 34)
                    self.cell(col_w[ci] - 2, line_h, line_text, align='L')

            self.set_xy(self.l_margin, y_before + cell_h)
        self.ln(3)


def process_markdown(filepath, pdf):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    in_table = False
    table_rows = []
    in_code = False

    while i < len(lines):
        line = lines[i].rstrip()

        # Code blocks
        if line.strip().startswith('```'):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            i += 1
            continue

        # Table detection
        is_table_line = '|' in line and line.strip().startswith('|')
        if is_table_line:
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in line.strip().split('|')][1:-1]
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table and table_rows:
                pdf.write_table(table_rows)
                table_rows = []
                pdf.ln(3)
            in_table = False

        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            pdf.write_h1(line[2:])
        elif line.startswith('## '):
            pdf.write_h2(line[3:])
        elif line.startswith('### '):
            pdf.write_h3(line[4:])
        elif line.startswith('> '):
            pdf.write_blockquote(line[2:])
        elif line.startswith('- ') or line.startswith('* '):
            pdf.write_bullet(line[2:])
        elif line.strip() == '':
            pdf.ln(1.5)
        elif line.startswith('---'):
            pdf.set_draw_color(180,180,180)
            pdf.set_line_width(0.3)
            y = pdf.get_y()
            pdf.line(pdf.l_margin + 100, y, pdf.w - pdf.r_margin - 100, y)
            pdf.ln(4)
        else:
            text = line.strip()
            if text and not text.startswith('|') and not text.startswith('!['):
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                text = re.sub(r'\*(.+?)\*', r'\1', text)
                text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
                text = re.sub(r'`(.+?)`', r'\1', text)
                pdf.write_para(text)

        i += 1

    if in_table and table_rows:
        pdf.write_table(table_rows)


# Main
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

report_path = r'd:\cc.claude\ADHD\FocusReset_US_Market_Research_Report.md'
process_markdown(report_path, pdf)

output_path = r'd:\cc.claude\ADHD\FocusReset_US_Market_Research_Report.pdf'
pdf.output(output_path)
print(f'PDF written to: {output_path}')
print(f'Pages: {pdf.page_no()}')
