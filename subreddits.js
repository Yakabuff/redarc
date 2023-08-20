var express = require('express');
var db = require('./pool');
router = express.Router();

router.get('/', function(req, res){

	let text = 'SELECT * FROM subreddits'

  db.pool.query(text)
  .then(result => {
      let subreddits = result.rows.filter(sub => 
        sub['unlisted'] === false
      )
      res.json(subreddits);
  })
  .catch(e => {
		console.error(e.stack);
		res.sendStatus(500);
		return
	})
});

module.exports = router;
