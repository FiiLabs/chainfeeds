# return to uploaded file hash
def add_to_ipfs(filepath, host="127.0.0.1", port="5001"):
    from pathlib import Path
    import requests

    # rb means open in binary. read binary
    with Path(filepath).open("rb") as fp:
        image_binary=fp.read()

    # we need to make post request to this endpoint.
    ipfs_url = "http://{host}:{port}/api/v0/add"

    # we need to send a file so we use multipart/form-data
    files = {'file': image_binary}

    # make the request and get response
    r = requests.post(ipfs_url, files=files)

    # get json data from response object
    ipfs_hash = r.json()['Hash']

    return ipfs_hash


def download_from_ipfs(ipfs_hash, save_path, host="127.0.0.1", port="8080"):
    import requests
    # Define the gateway host and port
    gateway_host = host
    gateway_port = port

    # Define the file hash and path
    file_hash = ipfs_hash
    file_path = "/ipfs/" + file_hash

    # Construct the gateway URL
    gateway_url = "http://" + gateway_host + ":" + gateway_port + file_path

    # Make a GET request to the gateway URL
    response = requests.get(gateway_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content as output.txt
        with open(save_path, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully")
    else:
        # Print an error message
        print("File download failed: ", response.reason)
