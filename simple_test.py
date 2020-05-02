from click.testing import CliRunner
from filestore import op, upload

def test_sync():
    runner = CliRunner()
    result = runner.invoke(op, ['upload', '--filename', './Misc/testfile.txt', '--keysfilename', './Misc/testkeys.txt'])
    # print(result.output)
    assert result.exit_code == 0
    assert 'Finished uploading to server!' in result.output
    print('Upload test succesful!')

    result = runner.invoke(op, ['retrieve', '--filename', './Misc/retestfile.txt', '--keysfilename', './Misc/testkeys.txt'])
    # print(result.output)
    assert result.exit_code == 0
    assert 'Download complete!' in result.output
    print('Retrieve test succesful!')


if __name__ == "__main__":
    test_sync()