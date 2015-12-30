var SockJS = require('sockjs-client');
var env = process.env
var fs = require("fs");
require('date-utils');

// load config
load_config = function(){
	var config = require(env["TT_HOME"] + '/config/investing.json');
	return config;
}

// get time
function getUTCTime(timestamp, timezoneOffset) {
	var dt = new Date((timestamp + timezoneOffset) * 1000);
	var formatted = dt.toFormat("YYYYMMDD");
	return formatted;
}

// get time
function getCurrentDate() {
	var dt = new Date();
	var formatted = dt.toFormat("YYYYMMDDHH24MISS");
	return formatted;
}

function getCurrentHour() {
	var dt = new Date();
	// for test : MI
	var formatted = dt.toFormat("HH24");
	return formatted;
}

function ensureDirectoryExistence(dirname) {
  if (fs.existsSync(dirname)) {
    return true;
  }
  fs.mkdirSync(dirname);
  logger("mkdir: " + dirname);
}

// log function
logger = function(text) {
  fs.appendFile(env["TT_HOME"] + "/log/investing.log", getCurrentDate() + ":investing:"+ text + "\n");
}


var sock = null;
var hour = getCurrentHour();
new_conn = function() {
	logger("new connection started.")
	config = load_config();
	logger(JSON.stringify(config));
	
	var options = {
		protocols_whitelist: ['websocket', 'xdr-streaming', 'xhr-streaming', 'iframe-eventsource', 'xdr-polling', 'xhr-polling'],
		debug: true,
		jsessionid: false,
		server_heartbeat_interval: 4000,
		heartbeatTimeout: 2000
	};
	
	var url = config["url"];
	var TimeZoneID = config["TimeZoneID"];
	var contents = config["contents"];
	sock = new SockJS(url, null, options);
	var heartbeat;

	// all users announce their info to the server and start a heartbeat
	var setHeartbeat = function() {
		logger("heartbeat.");
		clearTimeout(heartbeat);
		heartbeat = setTimeout(function() {
			sock.send(JSON.stringify({
				_event: "heartbeat",
				data: 'h'
		}));
		}, 2000);
	};

	sock.onopen = function() {
		logger("socket onopen.");
		setHeartbeat();
		for (var pid in contents)
		{
			params = contents[pid]["param"];
			for(var id in params){
				logger(params[id]);
				sock.send(JSON.stringify({
					_event: "subscribe",
					"tzID": TimeZoneID,
					"message": params[id]
				}));
			}
		}
	};

	// On receive message from server
	sock.onmessage = function(e) {
		// Get the content
		logger(e.data);
		try {
			var data = JSON.parse(e.data);
			var result = data.message.split('::');
			var pid_obj = JSON.parse(result[1]);
			var date = getUTCTime(pid_obj["timestamp"],32400);
			
			csv = pid_obj["timestamp"]+","+pid_obj["bid"]+","+ pid_obj["ask"];
			var dirname = env["TT_HOME"] + "/db/" + date;

			var filename =  dirname + "/" + contents[pid_obj["pid"]]["name"] + ".csv";
			ensureDirectoryExistence(dirname);
 			fs.appendFile(filename, csv + "\n");
 			
 			logger(filename);
 			logger(csv);
			setHeartbeat();
		} catch (err) {
			try{
				// heartbeat
				data["_event"];
				setHeartbeat();
			}
			catch(d){
				//console.log('CATCH ERR ' + err.message + e.data);
				logger(err.message)
				sock.close();
			}
		}
		prev_hour = hour;
		hour = getCurrentHour();
		if(prev_hour != hour){
			logger("collection changed time.")
			sock.close();
		}
	};
	// On receive message from server END

	// On connection close
	sock.onclose = function() {
			logger('socket on close');
			setTimeout(function() {
				new_conn();
			}, 300);
		}
		// On connection close END
	setHeartbeat();
}

new_conn();
