var iw = require('./investing_websocket.js');
var fs = require("fs");

var sqlite3 = require("sqlite3").verbose();
var env = process.env
var db = new sqlite3.Database(env["TT_HOME"] + "/db/commodity.db");

// log function
logger=function(text) {
  fs.appendFile(env["TT_HOME"] + "/log/commodity.log", "commodity_demon: " + text + "\n");
}

var pid_to_name = {
	'8849': "oil"
};

var pid_arr = Array(
	"pid-8849:","isOpenPair-8849:"   //原油
);

function insert(date,data) {
			function ensureDirectoryExistence(dirname) {
			  if (fs.existsSync(dirname)) {
			    return true;
			  }
			  fs.mkdirSync(dirname);
			  logger("mkdir: " + dirname);
			var name = pid_to_name[data["pid"]];
			csv = data["timestamp"]+","+data["bid"]+","+ data["ask"];
			var dirname = env["TT_HOME"] + "/db/" + date
			var filename =  dirname + "/" + name + ".csv"

			ensureDirectoryExistence(dirname)
 			fs.appendFile(filename, csv + "\n");

 			logger("csv: " + csv)
			/*db.serialize(function() {
				sql_cmd = "INSERT INTO " + exchange_name + " (timestamp,bid,ask) VALUES ("+data["timestamp"]+","+data["bid"]+","+ data["ask"]+")";
				logger(sql_cmd)
				var stmt = db.prepare(sql_cmd);
				stmt.run();
				stmt.finalize();
			});*/
		}
}


new_conn(pid_to_name, pid_arr, insert, logger);