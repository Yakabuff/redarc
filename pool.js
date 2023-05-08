const { Pool } = require('pg')
var CONFIG = require('./config.json');
const pool = new Pool({
	host: CONFIG.host, 
	port: CONFIG.port,
	database: CONFIG.database,
	user: CONFIG.user,
	password: CONFIG.password
})

module.exports = pool;
