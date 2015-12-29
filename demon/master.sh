node ${TT_HOME}/node/investing/exchange.js &
echo "exchange.js" > pid.txt
echo $! >> pid.txt
node ${TT_HOME}/node/investing/commodity.js &
echo "commodity.js" >> pid.txt
echo $! >> pid.txt
echo "master demo is started" 
cat pid.txt