# converts a file into png and export to the same directory of source
def html2png(src_path):
    from pathlib import Path
    import os
    from html2image import Html2Image
    hti = Html2Image()

    assert os.path.isfile(src_path) ," input needs to be a abs path"

    export_filename = Path(src_path).stem+'.png'
    with open(src_path, "r") as f:
        hti.screenshot(f.read(), save_as=export_filename)
    return export_filename

def export_plotly_2_png(fig, html_export_path, png_export_dir):
    import os
    import plotly
    # step 1 export the plotly plot into html
    html_export_path = os.path.join(png_export_dir,html_export_path)
    plotly.offline.plot(fig, filename = html_export_path, auto_open=False)

    # step 2 convert the exported html into png
    from pdf_report_generator.report_utils.graph_conversion import html2png
    png_filename = html2png(html_export_path)
    from pathlib import Path

    import os
    import shutil
    abs_export_path = os.path.join(png_export_dir,png_filename)
    shutil.move(png_filename,abs_export_path)

    from PIL import Image

    image = Image.open(abs_export_path)
    imageBox = image.getbbox()
    cropped = image.crop(imageBox)
    cropped.save(abs_export_path)
    return abs_export_path