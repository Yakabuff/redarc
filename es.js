const { Client } = require('@elastic/elasticsearch')
var CONFIG = require('./config.json');
const es_client = new Client({
   node: CONFIG.ES_HOST,
   auth: {
      username: 'elastic',
      password: CONFIG.ES_PASSWORD
   }
})

module.exports = es_client;