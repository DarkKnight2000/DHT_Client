import click

@click.group()
def op():
    #click.echo('Hello World!')
    pass

@op.command()
@click.option('--filename', type=click.File('r'), help='File path to be uploaded', required=True)
@click.option('--keysFilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved keys. Default is current directory')
@click.option('--keysFileName', type=click.File('w'), help='File name to store the recieved keys', required=True)#TODO:change to not required and check for overwiting 
def upload(filename, keysFilepath, keysFileName):
    ''' This command is used to upload files to cloud'''
    # Read file content
    click.echo(filename.read())
    # Call api

    # Write to keysFileName

@op.command()
@click.option('--filename', type=click.File('w'), help='File name to be used', required=True)
@click.option('--keysFilepath', default='.', type=click.Path(exists=True, resolve_path=True), help='Path to store the recieved file. Default is current directory')
@click.option('--keysFileName', type=click.File('w'), help='File name of the keys file', required=True)
def retrieve(filename, keysFilepath, keysFileName):
    ''' This command is used to retrieve files from cloud using keys'''
    # Read keys
    click.echo(keysFileName.read())
    # Call api

    # Write to filename


if __name__ == '__main__':
    op()


'''

    To create executable : pyinstaller --hidden-import='pkg_resources.py2_warn' filename
    Add to path temporarily : export PATH=$PATH:</path/to/file>
    Permanantly : Add above line to ~/.bashrc

'''