TESTFILE=${TT_HOME}/collect/scripts/pid.txt
i=0
while read line; do
    if [ $i = 0 ]; then
        i=1
        echo $line "is "
    else
        i=0
        p=`ps -ef | grep $line | grep -v grep | grep $line | grep -v srvchk | wc -l`
        if [ $p = 1 ]; then
                echo "alive."
        else
                echo "dead."
        fi
    fi
done < $TESTFILE
