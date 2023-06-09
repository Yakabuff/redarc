var express = require('express');
var pool = require('./pool');
router = express.Router();

var types = require('pg').types;
var timestampOID = 1114;
types.setTypeParser(1114, function(stringValue) {
  return stringValue;
})

router.get('/', function(req, res){
	if (Object.keys(req.query).length == 0) {
		res.sendStatus(500);
    	return;
	}
	let text = 'SELECT * FROM submissions where'
	let values = [];
	let count = 0;
	if (req.query.id) {
		count = count + 1;
		values.push(req.query.id)
		text += ` id = \$${count}`
	}
	if (req.query.author) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.author.toLowerCase())
		text += ` author = \$${count}`
	}
	if (req.query.title) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.title)
		text += ` title = \$${count}`
	}
	if (req.query.subreddit) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.subreddit.toLowerCase())
		text += ` subreddit = \$${count}`
	}
	if (req.query.after) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.after)
		text += ` created_utc > \$${count}`
	}
	if (req.query.before) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.before)
		text += ` created_utc < \$${count}`
	} 
	if (req.query.sort === 'ASC') {
		text += ` ORDER BY created_utc ASC`
	} else {
		text += ` ORDER BY created_utc DESC`
	}
	text += ` LIMIT 100`
	pool.query(text, values)
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
