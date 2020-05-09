import click
import time
import socket, sys, requests, json, base64
from cryptography.fernet import Fernet

chunk_size = 50

@click.group()
def op():
    #click.echo('Hello World!')
    pass

@op.command()
@click.option('--filename', type=click.File('rb'), help='Path to file to be uploaded', required=True)
# @click.option('--keysfilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved keys. Default is current directory')
@click.option('--keysfilename', type=click.File('wb'), help='File name to store the recieved keys. If the file is not in current directory, include path to the file', required=True)#TODO:change to not required and check for overwiting 
def upload(filename, keysfilename):
    ''' This command is used to upload files to cloud'''

    # Contacting discovery server
    nodeAddr = None
    nodePort = None
    # Get node address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        hostname = '127.0.0.1'
        s.connect((hostname, 8000))
        data = b'\x02'
        print('Formed connection')
        s.sendall(data)
        print('Sent data')
        data = (s.recv(1024)).decode().split('/')
        print('recved addr ', data[2], ' port ', data[4])
        nodeAddr = data[2]
        nodePort = int(data[4])


    # Read file content
    click.echo('Reading file contents...')
    chunks = []
    with filename as f:
        content = f.read(chunk_size)
        while len(content) > 0:
            # print('******** chunk ********')
            # print(content)
            chunks.append(content)
            content = f.read(chunk_size)
    click.echo('Closing file...')

    # Generating key for encryption
    fernet_key = Fernet.generate_key()
    keysfilename.write(fernet_key)
    keysfilename.write(b"\n")

    # nodeAddr = '127.0.0.1'
    # nodePort = 9000

    # Upload to server
    with click.progressbar(chunks, label = 'Uploading to server') as prog_chunks, keysfilename as k:
        for i, chunk in enumerate(prog_chunks):
            # # # # Call api
            key = f"{i}_key"
            data = requests.post(url = f'http://{nodeAddr}:{nodePort+1}', json = {'JSONRPCMethod':'dht_putValue', 'Key':key, 'Value':Fernet(fernet_key).encrypt(chunk).decode()}) # Encrypting with key and sending string to server
            # print(data)
            # print(data.text)
            # print(data.status_code)
            # Write to keysFileName
            k.write(f'{key}\n'.encode()) #TODO: Check for status code

    click.echo('Finished uploading to server! Use this keystore file to retrieve your file contents anytime!')


@op.command()
@click.option('--filename', type=click.File('wb'), help='Name to be used for the retrieved file. Default is current directory, include required path in the name to save it at another location', required=True)
# @click.option('--keysfilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved file. Default is current directory')
@click.option('--keysfilename', type=click.File('rb'), help='File name of the keys file. If the file is not in current directory, include path to the file', required=True)
def retrieve(filename, keysfilename):
    ''' This command is used to retrieve files from cloud using keystore file'''

    # Read keystore
    click.echo('Reading keys...')
    keys = []
    fernet_key = None
    with keysfilename as kf:
        fernet_key = kf.readline().strip()
        print('fkey', fernet_key)
        while True:
            key = kf.readline()
            if not key : break
            keys.append(key.strip().decode())
    click.echo('Closing file...')

    nodeAddr = None
    nodePort = None
    #Get node address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        hostname = '127.0.0.1'
        s.connect((hostname, 8000))
        data = b'\x02'
        print('Formed connection')
        s.sendall(data)
        print('Sent data')
        data = (s.recv(1024)).decode().split('/')
        print('recved addr ', data[2], ' port ', data[4])
        nodeAddr = data[2]
        nodePort = int(data[4])

    # nodeAddr = '127.0.0.1'
    # nodePort = 9000

    # Download from server
    with click.progressbar(keys, label = 'Downloading from server') as p_keys, filename as f:
        for key in p_keys:
            # # # # Call api
            data = requests.post(url = f'http://{nodeAddr}:{nodePort+1}', json = {'JSONRPCMethod':'dht_getValue', 'Key':key, 'Value':''})
            # Write to keysFileName
            chunk = Fernet(fernet_key).decrypt(data.text.encode())
            # print('ret text', chunk)
            f.write(chunk)

    click.echo('Download complete!')


if __name__ == '__main__':
    op()


'''

    To create executable : pyinstaller --hidden-import='pkg_resources.py2_warn' filename
    Add to path temporarily : export PATH=$PATH:</path/to/file>
    Permanantly : Add above line to ~/.bashrc

'''