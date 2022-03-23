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

if __name__ == "__main__":
    from pathlib import Path

    downloaded_data_dir = "./Downloaded_data"
    p = Path(downloaded_data_dir)
    p.mkdir(exist_ok=True)
    destination= downloaded_data_dir+"/meow.csv"
    id="1tOMgTtlmke7CeCzfnX8LpWCLxK16DqS4"
    # make sure your link is set to EDIT
    download_file_from_google_drive(id, destination)
