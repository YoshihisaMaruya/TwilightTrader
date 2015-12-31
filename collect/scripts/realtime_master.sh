node ${TT_HOME}/collect/investing/investing_websocket.js &
echo "investing_websocket.js" > ${TT_HOME}/collect/scripts/pid.txt
echo $! >> ${TT_HOME}/collect/scripts/pid.txt
cat ${TT_HOME}/collect/scripts/pid.txt
