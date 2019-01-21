import sys
import subprocess


def bench(infile, opts, tdelay):
	dictionary = {'infile':infile, 'opts':opts, 'tdelay':tdelay}
	bashCommand = 'python2 src/optimize.py examplefiles/%(infile)s.dot %(opts)s' % dictionary
	try:
		output = subprocess.check_output(bashCommand, shell=True)
	except subprocess.CalledProcessError as e:
		print(bashCommand)
		return 'xxxx'
	# os.system(bashCommand)
	bashCommand = './test/benchmark.sh examplefiles/%(infile)s %(tdelay)s' % dictionary
	# os.system(bashCommand)
	try:
		output = subprocess.check_output(bashCommand, shell=True)
	except subprocess.CalledProcessError as e:
		print(bashCommand)
		return '----'
	# print(output.split())
#	print(output[-2])
	return output.split()[-1]

infiles=[
'opdelay_add',
'tag_6x10G',
'c1mepp',
#'c1mipp'
]
opts=[
#'--eq_1',
#'--bitwidth',
#'--const_merging',
#'--remove_duplicates',
#'--bitwidth --tree_height_red_add --tree_height_red_and --tree_height_red_or',
# '--all',
# '--eq_1 --bitwidth --const_merging --tree_height_red_add --tree_height_red_and --tree_height_red_or '
'--const_merging --eq_1'
]

sys.stdout.write(',')
for infile in infiles:
	sys.stdout.write(infile+',')
sys.stdout.write('\n')
for opt in opts:
	sys.stdout.write(opt+',')
	for infile in infiles:
		imp = bench(infile, opt, 80)
		sys.stdout.write(str(imp)+',')
		# print(opt, infile, imp)
	sys.stdout.write('\n')
