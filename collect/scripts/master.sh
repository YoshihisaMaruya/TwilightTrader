node ${TT_HOME}/collect/node/investing/investing_websocket.js &
echo "investing_websocket.js" > pid.txt
echo $! >> pid.txt
cat pid.txt
