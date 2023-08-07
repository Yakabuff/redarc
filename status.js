var express = require('express');
var pool = require('./pool');
router = express.Router();

router.get('/', function (req, res) {
   let id = req.query.job_id;
   console.log(id)
   let text = 'SELECT job_id, start_utc, finish_utc, error FROM progress WHERE job_id = $1';

   pool.query(text, [id])
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