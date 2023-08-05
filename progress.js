var express = require('express');
var pool = require('./pool');
router = express.Router();

router.get('/', function(req, res){

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