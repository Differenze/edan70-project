import sys
import subprocess
import regex as re
import datetime

def bench(infile, tdelay, mergefactor):
    # print(infile, tdelay)
    dictionary = {'file':infile, 'tdelay':tdelay, 'mergefactor':mergefactor}
    bashCommand = './pacopt/pacopt.bin --algo simple-timing --target-delay {tdelay} {file}.dot pacopt_output.dot'.format(**dictionary)
    try:
        print('running pacopt')
        output = subprocess.check_output(bashCommand, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        return {'error': 'pacopt',
                'filename': infile,
                'target_delay': tdelay,
                'command': bashCommand}
    bashCommand = 'python src/optimize.py pacopt_output.dot --remff --nodemerging --target_delay {tdelay} --mergefactor {mergefactor}'.format(**dictionary)
    try:
        print('running optimize')
        output = subprocess.check_output(bashCommand, stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError as e:
        return {'error': 'optimize',
                'command': bashCommand}
    rgx = r"Unchanged graph costs (\d+) flipflops\nModified graph costs (\d+) flipflops"
    match = re.search(rgx, output)

    unchanged = int(match.group(1))
    modified = int(match.group(2))
    if unchanged == 0:
        if modified == 0:
            factor = 0
        else:
            factor = 'inf'
    else:
        factor = float(modified) / float(unchanged)
    return {
        'filename':infile,
        'target_delay': int(tdelay),
        'unchanged': unchanged,
        'modified': modified,
        'factor': factor,
        'mergefactor': mergefactor,
        }


    # bashCommand = 'python2 src/optimize.py examplefiles/{infile}.dot {opts}'.format(dictionary)
#         return 'xxxx'
#     # os.system(bashCommand)
#     bashCommand = './test/benchmark.sh examplefiles/%(infile)s %(tdelay)s' % dictionary
#     # os.system(bashCommand)
#     try:
#         output = subprocess.check_output(bashCommand, shell=True)
#     except subprocess.CalledProcessError as e:
#         print(bashCommand)
#         return '----'
#     # print(output.split())
# #    print(output[-2])
#     return output.split()[-1]

in_files=[
# 'opdelay_add',
# 'tag_6x10G',
'c1mepp',
'c1mipp'
]

delays = [
    # 20,
    # 40,
    # 80,
    # 160,
    # 320,
    640,
    # 1280
]

mergefactors = [
    0,
    # 0.2,
    0.4,
    # 0.6,
    # 0.8,
    1,
]

csv =       r'{filename:>40}, {target_delay:>15},{mergefactor:>10}, {unchanged:>10}, {modified:>10}, {factor:>5}'
csv_err =   r'{filename:>40}, {target_delay:>15}, error occured in {error},'
latex =     r'{filename} & {target_delay} & {unchanged} & {modified} \\'
latex_err = r'{filename} & {target_delay} & error occured in {error} &  \\'

describ_dict = {
    'filename'      : 'filename',
    'target_delay'  : 'target_delay',
    'unchanged'     : 'unchanged',
    'modified'      : 'modified',
    'factor'        : 'improvement',
    'mergefactor'   : 'mergefactor',
}
formatstring = csv
formatstring_err = csv_err

res_file = open('benchresults.csv', 'a')
res_file.write(str(datetime.datetime.now())+'\n')
print(formatstring.format(**describ_dict))
res_file.write(formatstring.format(**describ_dict)+'\n')
for infile in in_files:
    for delay in delays:
        for mergefactor in mergefactors:
            res_dict = bench('./examplefiles/'+infile, delay, mergefactor)
            if 'error' in res_dict:
                print(formatstring_err.format(**res_dict))
                res_file.write(formatstring_err.format(**res_dict)+'\n')
            else:
                print(formatstring.format(**res_dict))
                res_file.write(formatstring.format(**res_dict)+'\n')
