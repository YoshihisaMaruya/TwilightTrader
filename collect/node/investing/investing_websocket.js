var SockJS = require('sockjs-client');
require('date-utils');

// Create a connection to http://localhost:9999/echo
var stream = "stream20.forexpros.com"
var TimeZoneID = 29;

console.log('stream: ' + stream);
var sock = null;
new_conn = function(pid_to_name, pid_arr, insert, logger) {
	var options = {
		protocols_whitelist: ['websocket', 'xdr-streaming', 'xhr-streaming', 'iframe-eventsource', 'xdr-polling', 'xhr-polling'],
		debug: true,
		jsessionid: false,
		server_heartbeat_interval: 4000,
		heartbeatTimeout: 2000
	};
	var url = 'http://' + stream + ':80/echo'
	sock = new SockJS(url, null, options);
	logger(url)

	var heartbeat;

	// all users announce their info to the server and start a heartbeat
	var setHeartbeat = function() {
		clearTimeout(heartbeat);
		heartbeat = setTimeout(function() {
			sock.send(JSON.stringify({
				_event: "heartbeat",
				data: 'h'
		}));
		}, 2000);
	};

	sock.onopen = function() {
		setHeartbeat();
		for (i=0; i<pid_arr.length; i++)
		{
			sock.send(JSON.stringify({
				_event: "subscribe",
				"tzID": TimeZoneID,
				"message": pid_arr[i]
			}));
		}
	};
	// Open the connection END

	function getUTCTime(timestamp, timezoneOffset) {
		var dt = new Date((timestamp + timezoneOffset) * 1000);
		var formatted = dt.toFormat("YYYYMMDD");
		return formatted;
	}

	// On receive message from server
	sock.onmessage = function(e) {
		// Get the content
		var data = ""
		logger(e.data)
		try {
			//console.log(e.data);
			data = JSON.parse(e.data);
			var result = data.message.split('::');
			var pid_obj = JSON.parse(result[1]);
			date = getUTCTime(pid_obj["timestamp"],32400);
			insert(date,pid_obj);
		} catch (err) {
			try{
				// heartbeat
				data["_event"];
			}
			catch(d){
				//console.log('CATCH ERR ' + err.message + e.data);
				logger(err.message)
				sock.close();
				new_conn();
			}
		}
		setHeartbeat();
	};
	// On receive message from server END

	// On connection close
	sock.onclose = function() {
			logger('close-fx');
			setTimeout(function() {
				new_conn();
			}, 300);

		}
		// On connection close END

	setHeartbeat();
}
