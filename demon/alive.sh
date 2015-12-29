
TESTFILE=./pid.txt

i=0
while read line; do
	if [ $i = 0 ]; then
		i=1
    	echo $line "is "
    else
    	i=0
    	p=`ps -ax | grep $line | grep -v grep`
    	if [ $p = ""]; then
    		echo "dead."
    	else
    		echo "alive."
    	fi
    fi
done < $TESTFILE