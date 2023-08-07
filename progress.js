var express = require('express');
var pool = require('./pool');
var CONFIG = require('./config.json');

router = express.Router();

router.post('/', function(req, res) {

   if (req.body.password !== CONFIG.ADMIN_PASSWORD) {
      res.sendStatus(401);
      return
   }
   let text = 'SELECT * FROM progress ORDER BY start_utc DESC LIMIT 200';

   pool.query(text)
   .then(result => {
      res.json(result.rows);
   })
   .catch(e => {
		console.error(e.stack);
		res.sendStatus(500);
		return
	})
});

module.exports = router;