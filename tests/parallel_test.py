from click.testing import CliRunner
import lorem, sys
import multiprocessing

sys.path.insert(1, "..")
from filestore import op

num_workers = 1
runner = None

def init_runner():
    global runner
    if not runner:
        runner = CliRunner()

def test_sync(i):

    f = open(f'../Misc/testfile_{i}.txt', 'w')
    f.write(lorem.paragraph())
    f.close()

    global runner
    result = runner.invoke(op, ['upload', '--filename', f'../Misc/testfile_{i}.txt', '--keysfilename', f'../Misc/testkeys_{i}.txt'])
    # print(result.output)
    assert result.exit_code == 0
    assert 'Finished uploading to server!' in result.output
    print('Upload test succesful!')

    result = runner.invoke(op, ['retrieve', '--filename', f'../Misc/retestfile_{i}.txt', '--keysfilename', f'../Misc/testkeys_{i}.txt'])
    # print(result.output)
    assert result.exit_code == 0
    assert 'Download complete!' in result.output
    print('Retrieve test succesful!')

    f1 = open(f'../Misc/testfile_{i}.txt', 'rb')
    f2 = open(f'../Misc/retestfile_{i}.txt', 'rb')
    if f1.read() == f2.read():
        print('Got same data')
    else:
        print('Got different data')
    f1.close()
    f2.close()


if __name__ == "__main__":
    with multiprocessing.Pool(initializer=init_runner) as pool:
        pool.map(test_sync, range(num_workers))