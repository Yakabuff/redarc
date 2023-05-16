var express = require('express');
var pool = require('./pool');
router = express.Router();

router.get('/', function(req, res){
	if (Object.keys(req.query).length == 0) {
		res.sendStatus(500);
    return;
	}
	let text = 'SELECT * FROM comments where'
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
		values.push(req.query.author)
		text += ` author = \$${count}`
	}
	if (req.query.body) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.body)
		text += ` body = \$${count}`
	}
	if (req.query.subreddit) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.subreddit)
		text += ` subreddit = \$${count}`
	}
	if (req.query.after) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.after)
		text += ` created_utc > TO_TIMESTAMP(\$${count})`
	}
	if (req.query.before) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.before)
		text += ` created_utc < TO_TIMESTAMP(\$${count})`
	} 
	if (req.query.parent_id) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.parent_id)
		text += ` parent_id = \$${count}`
	} 
	if (req.query.link_id) {
		count = count + 1;
		if (values.length != 0) {
      text += ' and';
		}
		values.push(req.query.link_id)
		text += ` link_id = \$${count}`
	} 
	if (req.query.sort) {
		count = count + 1;
		values.push(req.query.sort)
		text += ` ORDER BY created_utc \$${count})`
	} else {
		text += ` ORDER BY created_utc DESC`
	}
	text += ` LIMIT 500`

  pool.query(text, values)
  .then(result => {
		query_results = result.rows;
		if (req.query.unflatten && req.query.link_id) {
      res.send(unflatten(result.rows, req.query.link_id));
			return;
		}
    res.send(result.rows);
  })
  .catch(e => {
		console.error(e.stack);
		res.sendStatus(500);
		return
	})
})
 
function unflatten(data, root) {
  // Turn array of comments into hashmap. Add empty array field replies to comment obj
	// Iterate over keys
	// If comment's parent is root, push to commentTree list. These are top level comments
	// find parent comment in hashmap and append this comment into parent's reply. 
	// Set replies of root to commentTree 

  let lookup = arrayToLookup(data);
	let commentTree = [];
	Object.keys(lookup).forEach(commentID => {
    let comment = lookup[commentID];
		let parentID = comment.parent_id;
		
		if (parentID == root) {
      commentTree.push(comment);
		} else {
			if (lookup[parentID.split('_')[1]] == undefined) {
				commentTree.push({body: comment.body, author: comment.author, id: commentID, replies: [comment], parent_id: root, link_id: root})
			} else {
        		lookup[parentID.split('_')[1]].replies.push(comment);
		  }
		}
  });

	return commentTree;
}
function arrayToLookup(commentList){
	let lookup = {}
  commentList.forEach(comment => {
    comment.replies = [];
		lookup[comment.id] = comment;
  });
	return lookup;
}
module.exports = router;
