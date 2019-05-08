# TODO write test that ensures graph is unchanged when no optimizations are applied
import subprocess
# import optimize

paths = [
    'opdelay_add',
    'tag_6x10G',
    'c1mepp',
    'c1mipp',
    'opdelay_add_opt',
    'tag_6x10G_opt',
    'c1mepp_opt',
    'c1mipp_opt',
    ]

def compare(inFile):
    dictionary = {'inFile':inFile}
    bashCommand = 'python2 src/optimize.py examplefiles/{inFile}.dot'.format(**dictionary)
    print(bashCommand)
    output = subprocess.check_output(bashCommand, shell=True)

    bashCommand = 'sort examplefiles/{inFile}.dot>a.dot'.format(**dictionary)
    output = subprocess.check_output(bashCommand, shell=True)

    bashCommand = 'sort output.dot>b.dot'.format(**dictionary)
    output = subprocess.check_output(bashCommand, shell=True)

    bashCommand = 'icdiff -U 0 a.dot b.dot'
    output = subprocess.check_output(bashCommand, shell=True)

    print(output)


for path in paths:
    compare(path)