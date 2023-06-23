var express = require('express');
var pool = require('./pool');
var CONFIG = require('./config.json');
const es_client = require('./es');

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

   if (!CONFIG.ES_ENABLED) {
      simpleSearch(req, res)
   }else {
      elasticSearch(req, res)
   }

});
function elasticSearch(req, res) {
   // title/body if submission
   // comment body if comment

   if (req.query.type === SUBMISSION) {
      let q = {
         size: 100,
         index: 'redarc',
         sort :[
            {"created_utc": 
               {
                  "order" : req.query.sort
               }
            }
         ],
         query: {
            bool: {
               must: [
                  {
                     match: {
                        "type": 'submission'
                     },
                  },
                  {
                     match: {
                        "subreddit": req.query.subreddit
                     }
                  },
                  {
                     bool: {
                        should: [
                           {
                              match_phrase_prefix: {
                                 "self_text": req.query.search, 
                              }
                           },
                           {
                              match_phrase_prefix: {
                                 "title": req.query.search, 
                              },
                           },
                        ]
                     }
                  }
               ], 

            }
         }
      }

      if (req.query.after && !req.query.before) {
         let x = {
            'range': {
               'created_utc': {
                  gt: req.query.after,
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)

      } else if(!req.query.after && req.query.before) {
         let x = {
            'range': {
               'created_utc': {
                  lt: req.query.before,
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)

      } else if (req.query.after && req.query.before) {
         let x = {
            'range': {
               'created_utc': {
                  gt: req.query.after,
                  lt: req.query.before
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      }else {

      }
      // console.log(JSON.stringify(q))
      es_client.search(q).then((result) => {
         let x = result['hits']['hits']
         x.forEach(element => {
            // 2019-07-11 22:14:51
            let date = new Date(element['_source']['created_utc'] * 1000);

            let dateString = date.toISOString().replace(/T/, ' ').replace(/\..+/, '');

            element['_source']['datestring'] = dateString;
         })
         res.json(result);
      }).catch((error)=> {
         res.sendStatus(500);
         // console.log(error)
         return;
      })
   } else {
      let q = {
         size: 100,
         index: 'redarc_comments',
         sort :[
            {"created_utc": 
               {
                  "order" : req.query.sort
               }
            }
         ],
         query: {
            bool: {
               must: [
                  {
                     match_phrase_prefix: {
                        "body": req.query.search, 
                     },
                  },
                  {
                     match: {
                        "type": 'comment',
                     }
                  }, 
                  {
                     match: {
                        "subreddit": req.query.subreddit
                     }
                  }
               ],
            }
         }
      }

      if (req.query.after && !req.query.before) {
         let x = {
            'range': {
               'created_utc': {
                  'gte': req.query.after
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      } else if(!req.query.after && req.query.before) {
         let x = {
            'range': {
               'created_utc': {
                  'lte': req.query.before
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      } else if (req.query.after && req.query.before) {
         let x = {
            'range': {
               'created_utc': {
                  'lte': req.query.beforeDate,
                  'gte': req.query.afterDate
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      }else {

      }
      // console.log(JSON.stringify(q))
      es_client.search(q).then((result) => {
         let x = result['hits']['hits']
         x.forEach(element => {
            // 2019-07-11 22:14:51
            let date = new Date(element['_source']['created_utc'] * 1000);
            let dateString = date.toISOString().replace(/T/, ' ').replace(/\..+/, '');
            element['_source']['datestring'] = dateString;
         })
         res.json(result);
      }).catch((error)=> {
         res.sendStatus(500);
         // console.log(error)
         return;
      })
   }
}

function simpleSearch(req, res) {
	let text = ''

   if (req.query.type === SUBMISSION) {
      text = 'SELECT id, created_utc, score, self_text, subreddit, title FROM submissions where'
   } else {
      text = 'SELECT id, link_id, created_utc, score, body, subreddit FROM comments where'
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
      let zulu = new Date(req.query.after*1000).toISOString();
		values.push(zulu)
		text += ` and created_utc > \$${count}`
	}
	if (req.query.before) {
		count = count + 1;
      let zulu = new Date(req.query.before*1000).toISOString();
		values.push(zulu)
		text += ` and created_utc < \$${count}`
	} 

   if (req.query.type === SUBMISSION) {
      count = count + 1;

      values.push('%'+req.query.search+'%')
      text += ` and (title LIKE \$${count}`
   
      count = count + 1;

      values.push('%'+req.query.search+'%')
      text += ` or self_text LIKE \$${count})`
      
   } else {
      count = count + 1;

      values.push('%'+req.query.search+'%')
      text += ` and body LIKE \$${count}`
   }

	if (req.query.sort === 'asc') {
		text += ` ORDER BY created_utc ASC`
	} else {
		text += ` ORDER BY created_utc DESC`
	}
   
   text += ` LIMIT 100`
   pool.query(text, values)
	.then(result => {
      data = {}
      data['hits'] = {} 
      data['hits']['hits'] = []
      result.rows.forEach(element => {
         let d = element['created_utc'].split(" ");
         d = d[0] + "T" + d[1] + "Z"
         element['datestring'] = element['created_utc'];
         element['created_utc'] = new Date(d).valueOf()/1000;
         if (req.query.type === SUBMISSION) {
            data['hits']['hits'].push({'_source': element, '_id': element.id})
         } else {
            data['hits']['hits'].push({'_source': element, '_id': element.link_id})
         }
      })
		res.json(data);
	})
	.catch(e => {
			// console.error(e.stack);
			return [];
	})
}

module.exports = router;
