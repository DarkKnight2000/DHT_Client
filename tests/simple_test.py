from click.testing import CliRunner
import lorem, sys

sys.path.insert(1, "..")
from filestore import op

def test_sync():

    f = open(f'../Misc/testfile.txt', 'w')
    f.write(lorem.paragraph())
    f.close()

    runner = CliRunner()
    result = runner.invoke(op, ['upload', '--filename', '../Misc/testfile.txt', '--keysfilename', '../Misc/testkeys.txt'])
    # print(result.output)
    assert result.exit_code == 0
    assert 'Finished uploading to server!' in result.output
    print('Upload test succesful!')

    result = runner.invoke(op, ['retrieve', '--filename', '../Misc/retestfile.txt', '--keysfilename', '../Misc/testkeys.txt'])
    # print(result.output)
    assert result.exit_code == 0
    assert 'Download complete!' in result.output
    print('Retrieve test succesful!')

    f1 = open('../Misc/testfile.txt', 'rb')
    f2 = open('../Misc/retestfile.txt', 'rb')
    if f1.read() == f2.read():
        print('Got same data')
    else:
        print('Got different data')


if __name__ == "__main__":
    test_sync()