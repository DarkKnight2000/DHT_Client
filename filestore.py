import click
import time
# 1010 for 1mb chunk size
chunk_size = 50

@click.group()
def op():
    #click.echo('Hello World!')
    pass

@op.command()
@click.option('--filename', type=click.File('r'), help='Path to file to be uploaded', required=True)
# @click.option('--keysfilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved keys. Default is current directory')
@click.option('--keysfilename', type=click.File('w'), help='File name to store the recieved keys. If the file is not in current directory, include path to the file', required=True)#TODO:change to not required and check for overwiting 
def upload(filename, keysfilename):
    ''' This command is used to upload files to cloud'''

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

    # Upload to server
    with click.progressbar(chunks, label = 'Uploading to server') as prog_chunks, keysfilename as k:
        for chunk in prog_chunks:
            # Call api
            time.sleep(.1)
            # Write to keysFileName
            key = 'abc'
            k.write(f'{key}\n')

    click.echo('Finished uploading to server! Use this keystore file to retrieve your file contents anytime!')


@op.command()
@click.option('--filename', type=click.File('w'), help='Name to be used for the retrieved file. Default is current directory, include required path in the name to save it at another location', required=True)
# @click.option('--keysfilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved file. Default is current directory')
@click.option('--keysfilename', type=click.File('r'), help='File name of the keys file. If the file is not in current directory, include path to the file', required=True)
def retrieve(filename, keysfilename):
    ''' This command is used to retrieve files from cloud using keystore file'''

    # Read keystore
    click.echo('Reading keys...')
    keys = []
    with keysfilename as kf:
        for key in kf: keys.append(key.strip())
    click.echo('Closing file...')

    # Download from server
    with click.progressbar(keys, label = 'Downloading from server') as p_keys, filename as f:
        for key in p_keys:
            # Call api
            time.sleep(.1)
            # Write to keysFileName
            chunk = 'abc'
            f.write(f'{chunk}\n')

    click.echo('Download complete!')


if __name__ == '__main__':
    op()


'''

    To create executable : pyinstaller --hidden-import='pkg_resources.py2_warn' filename
    Add to path temporarily : export PATH=$PATH:</path/to/file>
    Permanantly : Add above line to ~/.bashrc

'''