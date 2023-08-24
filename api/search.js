var express = require('express');
var db = require('./pool');
var CONFIG = require('./config.json');

router = express.Router();

const COMMENT = "comment"
const SUBMISSION = "submission"

router.get('/', function(req, res){
   // comment or submission
   let type = ""
   if (req.query.type === COMMENT) {
      type = "comment"
   } else if (req.query.type === SUBMISSION) {
      type = "submission"
   } else {
      res.sendStatus(500);
      return
   }

   if (!req.query.subreddit) {
      res.sendStatus(500);
      return
   }

   if (!req.query.sort) {
      req.query.sort = "desc"
   }

   if (!req.query.search) {
      res.sendStatus(500);
      return
   }

   if (req.query.before && isNaN(req.query.before)) {
      res.sendStatus(500);
      return
   }

   if (req.query.after && isNaN(req.query.after)) {
      res.sendStatus(500);
      return
   }

   search(req, res)

});

function search(req, res) {
	let text = ''

   if (req.query.type === SUBMISSION) {
      text = 'SELECT * FROM submissions where'
   } else {
      text = 'SELECT * FROM comments where'
   }
	let values = [];
	let count = 0;
   if (req.query.subreddit) {
		count = count + 1;
		values.push(req.query.subreddit.toLowerCase())
		text += ` subreddit = \$${count}`
	}
   if (req.query.after) {
		count = count + 1;
		values.push(req.query.after)
		text += ` and created_utc > \$${count}`
	}
	if (req.query.before) {
		count = count + 1;
		values.push(req.query.before)
		text += ` and created_utc < \$${count}`
	} 

   if (req.query.search) {
      count = count + 1;

      values.push(req.query.search)
      text += ` and ts @@ phraseto_tsquery(\$${count})`
      
   } else {
      res.sendStatus(500);
      return
   }

	if (req.query.sort === 'asc') {
		text += ` ORDER BY created_utc ASC`
	} else {
		text += ` ORDER BY created_utc DESC`
	}
   
   text += ` LIMIT 100`
   db.ftspool.query(text, values)
	.then(result => {
      res.json(result.rows);
	})
	.catch(e => {
			console.error(e.stack);
			return [];
	})
}

module.exports = router;
