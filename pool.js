const { Pool } = require('pg')
var types = require('pg').types;
var CONFIG = require('./config.json');
const pool = new Pool({
	host: CONFIG.host, 
	port: CONFIG.port,
	database: CONFIG.database,
	user: CONFIG.user,
	password: CONFIG.password
})

const ftspool = new Pool({
	host: CONFIG.ftshost, 
	port: CONFIG.ftsport,
	database: CONFIG.ftsdatabase,
	user: CONFIG.ftsuser,
	password: CONFIG.ftspassword
})

// var timestampOID = 1114;
// types.setTypeParser(1114, function(stringValue) {
//   return stringValue;
// })
module.exports = {pool, ftspool};
