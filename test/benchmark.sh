# compares $1 to output.dot
FILE1=output
FILE2=$1

ARGS="--algo simple-timing --target-delay 1000"

if [ -z "$FILE2" ]; then
	echo "usage: ./test/benchmark.sh _filename_"
	exit -1
fi

echo "==== ${FILE1}: ===="
# genreates FILE1_sorted.dot
./test/sort_graph.sh ${FILE1}
./pacopt/pacopt.bin ${ARGS} ${FILE1}_sorted.dot ${FILE1}_sorted_pacopt.dot
echo "\n"

echo "==== ${FILE2}: ===="
# genreates FILE2_sorted.dot
./test/sort_graph.sh ${FILE2}
./pacopt/pacopt.bin ${ARGS} ${FILE2}_sorted.dot ${FILE2}_sorted_pacopt.dot
echo "\n"

echo "created: ${FILE1}_sorted.dot"
echo "created: ${FILE2}_sorted.dot"
echo "created: ${FILE1}_sorted_pacopt.dot"
echo "created: ${FILE2}_sorted_pacopt.dot"