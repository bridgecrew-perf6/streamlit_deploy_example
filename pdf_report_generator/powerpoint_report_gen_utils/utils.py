# only works in local machine with windows installed

def PPTtoPDF(inputFileName, outputFileName, formatType=32):
    import win32com.client

    # https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api
    # >pip install pywin32==225

    powerpoint = win32com.client.DispatchEx("Powerpoint.Application")
    powerpoint.Visible = 1

    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName + ".pdf"
    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, formatType)  # formatType = 32 for ppt to pdf
    deck.Close()
    powerpoint.Quit()
    #return outputFileName

def merge_pdfs(pdfs,output_file_path):
    from PyPDF2 import PdfFileMerger
    #pdfs = ['1_ESEMPIO.pdf', '2_ESEMPIO.pdf', '3_ESEMPIO.pdf']

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    if output_file_path[-3:] != 'pdf':
        outputFileName = output_file_path + ".pdf"
    merger.write(output_file_path)
    merger.close()
    return output_file_path