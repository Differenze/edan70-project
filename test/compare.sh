# compares nodes in two graphs
dot -Tplain $1 | sed -ne 's/^node \([^ ]\+\).*$/\1/p' | sort >a1.nodes
dot -Tplain $2 | sed -ne 's/^node \([^ ]\+\).*$/\1/p' | sort >a2.nodes
diff a1.nodes a2.nodes
rm a1.nodes
rm a2.nodes