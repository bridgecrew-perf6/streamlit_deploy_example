
import webbrowser



def build_page(pdf, ticker, time_series_png_path, stockinfo_df, vcp_property_df, vcp_supplementary_df, factors_df, contractions_df):

    pdf.add_page()
    pdf.set_font("Courier", size=12, style='B')
    pdf.multi_cell(0, 0, ticker.upper(), 0, 'C')
    pdf.ln(2)
    pdf.image(time_series_png_path,link='', type='', w=198, h=100)
    pdf.ln(2)
    pdf = make_table(pdf, vcp_property_df)
    pdf.ln(2)
    pdf = make_table(pdf, stockinfo_df)
    pdf.ln(2)
    pdf = make_table(pdf, factors_df)
    pdf.ln(2)
    pdf = make_table(pdf, vcp_supplementary_df)
    pdf.ln(2)
    pdf = make_table(pdf, contractions_df)

    pdf.set_font("Courier", 'I',size=8)
    pdf.set_text_color(128)
    pdf.multi_cell(0, 5, "page " + str(pdf.page_no()), 0, 'C')
    return pdf

def make_table(pdf, df,size=11):
    pdf.set_text_color(000)

    TABLE_COL_NAMES = df.columns
    TABLE_DATA = df.values

    pdf.set_font("Courier",size=size)
    line_height = pdf.font_size * 1.15
    col_width = pdf.epw / len(df.columns)  # distribute content evenly

    def render_table_header():
        pdf.set_font(style="B")  # enabling bold text
        for col_name in TABLE_COL_NAMES:
            pdf.set_fill_color(251,139,30)
            pdf.cell(col_width, line_height, col_name, border=1,fill=True)
        pdf.ln(line_height)
        pdf.set_font(style="")  # disabling bold text

    render_table_header()
    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header()
        for datum in row:
            pdf.cell(col_width, line_height, str(datum), border=1)
        pdf.ln(line_height)
    return pdf


def setup_titlepage(title = '20000 Leagues Under the Seas'):
    from fpdf import FPDF
    pdf = FPDF(orientation='P', unit='mm', format='letter')
    # pdf.add_page()
    #pdf.set_font("Courier", "B", 16)
    pdf.add_page()
    import datetime

    def make_header(pdf, title):
        # Arial bold 15
        #pdf.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = pdf.get_string_width(title) + 6
        pdf.set_x((210 - w) / 2)
        # Colors of frame, background and text
        # self.set_draw_color(0, 80, 180)
        # self.set_fill_color(230, 230, 0)
        pdf.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        pdf.set_line_width(1)

    def put_middle(pdf,str_input):
        from fpdf.enums import XPos, YPos
        #self.set_text_color(225, 225, 225)
        w = pdf.get_string_width(str_input) + 6
        pdf.set_x((210 - w) / 2)
        #pdf.cell(w, 9, str_input, 0,1, 'C', 0)
        pdf.cell(w, 9, str_input, 0, XPos.CENTER, YPos.NEXT, ln = "DEPRECATED", align = "C",fill = False)

    make_header(pdf, title)
    put_middle(pdf,"VCP scan results")
    put_middle(pdf,"Published Date: " + str(datetime.datetime.today().date()))
    #pdf.set_font('Arial', 'B', 10)
    return pdf