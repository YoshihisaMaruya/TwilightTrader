
TESTFILE=${TT_HOME}/collect/scripts/pid.txt

i=0
while read line; do
	if [ $i = 0 ]; then
		i=1
    	echo "cmd name is " $line
    else
    	i=0
    	kill -9 $line
    fi
done < $TESTFILE
