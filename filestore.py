import click

chunk_size = 20

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
    with filename as f:
        content = f.read(chunk_size)
        while len(content) > 0:
            print('******** chunk ********')
            print(content)
            content = f.read(chunk_size)
    # Call api

    # Write to keysFileName
    keysfilename.write('abc')


@op.command()
@click.option('--filename', type=click.File('a'), help='Name to be used for the retrieved file. Default is current directory, include required path in the name to save it at another location', required=True)
# @click.option('--keysfilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved file. Default is current directory')
@click.option('--keysfilename', type=click.File('r'), help='File name of the keys file. If the file is not in current directory, include path to the file', required=True)
def retrieve(filename, keysfilename):
    ''' This command is used to retrieve files from cloud using keystore file'''
    # Read keys
    click.echo(keysfilename.read())
    # Call api

    # Write to filename
    filename.write('abc')


if __name__ == '__main__':
    op()


'''

    To create executable : pyinstaller --hidden-import='pkg_resources.py2_warn' filename
    Add to path temporarily : export PATH=$PATH:</path/to/file>
    Permanantly : Add above line to ~/.bashrc

'''