import requests
# this set of tools downlaod file without using google drive api
#https://discuss.streamlit.io/t/how-to-download-large-model-files-to-the-sharing-app/7160
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def download_file_from_google_drive_sharables(id, destination):
    # https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
    '''
    importantly, if you create the link by "Share" or "Get shareable link", the URL doesn't work - you must replace in the URL "open" to "uc". In other words, drive.google.com/open?id= ... to drive.google.com/uc?id= ... –
    Agile Bean
    May 16, 2020 at 13:43

    #note: thomas added r to convert string literals

    :param id:
    :param destination:
    :return:
    '''
    URL = "https://drive.google.com/uc?" + id
    #URL = "https://drive.google.com/uc?" + id
    #URL ="https://drive.google.com/file/d/"+id

    print(URL)
    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)


def download_all_signals(signal_pointer_file, downloaded_data_dir):
    import os
    import pandas as pd
    import streamlit as st
    from pathlib import Path

    try:
        signal_pointer_df = pd.read_csv(signal_pointer_file)
        if signal_pointer_df.empty:
            raise pd.errors.EmptyDataError

        p = Path(downloaded_data_dir)
        p.mkdir(exist_ok=True)

        for idx, row in signal_pointer_df.iterrows():
            # we assume the target is csv but this should change depending on the original file type accordingly
            destination = os.path.join(p,row.signal+'.'+row.file_ext)
            id = row.file_id
            download_file_from_google_drive_sharables(id, destination)
            print(row.signal, row.file_id)
            st.info("download_all_signals:: SIGNAL=" +row.signal+ " DOWNLAODED.")

    except Exception as e:
        print(e)
        pass

def download_signal_pointer_file(id, destination):
    import streamlit as st
    #id = st.secrets['signal_pointer_fileid']
    # make sure your link is set to EDIT
    download_file_from_google_drive_sharables(id, destination)
    return destination


if __name__ == "____":
    #SINAL_POINTER_FILE = "signal_pointer_file.csv"
    #raws =r"1VA-QE48-5S1GABReSsNZ1fyR1nKsqKSB"
    raws='1VA-QE48-5S1GABReSsNZ1fyR1nKsqKSB'
    download_signal_pointer_file(raws,'xyz2.csv')
    #download_all_signals(SINAL_POINTER_FILE,DOWNLOADED_DATA_DIR)