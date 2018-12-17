# compares $1 to output.dot
FILE1=output
FILE2=$1

ARGS="--algo simple-timing --target-delay 80"

if [ -z "$FILE2" ]; then
	echo "usage: ./test/benchmark.sh _filename_"
	exit -1
fi

echo "==== ${FILE1}: ===="
# genreates FILE1_sorted.dot
./test/sort_graph.sh ${FILE1}
OUTPUT1="$(./pacopt/pacopt.bin ${ARGS} ${FILE1}_sorted.dot ${FILE1}_sorted_pacopt.dot)"
echo "$OUTPUT1"
echo "\n"
AREA1=$(echo "$OUTPUT1" | grep area | sed 's/[^0-9]*//g')


echo "==== ${FILE2}: ===="
# genreates FILE2_sorted.dot
./test/sort_graph.sh ${FILE2}
OUTPUT2="$(./pacopt/pacopt.bin ${ARGS} ${FILE2}_sorted.dot ${FILE2}_sorted_pacopt.dot)"
echo "$OUTPUT2"
echo "\n"
AREA2=$(echo "$OUTPUT2" | grep area | sed 's/[^0-9]*//g')

echo "created: ${FILE1}_sorted.dot"
echo "created: ${FILE2}_sorted.dot"
echo "created: ${FILE1}_sorted_pacopt.dot"
echo "created: ${FILE2}_sorted_pacopt.dot"

echo "DELTA:"
DIF=$(($AREA2-$AREA1))
echo $DIF
#bc -l <<< "($AREA2-$AREA1)/$AREA2"
echo "($AREA2-$AREA1)/$AREA2" | bc -l