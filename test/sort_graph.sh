# compares nodes in two graphs
# $1 input

echo "digraph packetarc {" > $1_sorted.dot
echo "node [shape=record];" >> $1_sorted.dot
# find everything that is not a vertex
SPECIAL="packetarc {\|^}$\|^$\|node"
grep "\->" $1.dot --line-buffer -v | grep "$SPECIAL" -v | sort >> $1_sorted.dot
# find everything that is a vertex
grep "\->" $1.dot --line-buffer | grep "$SPECIAL" -v | sort >> $1_sorted.dot

echo "}" >> $1_sorted.dot