var express = require('express');
var CONFIG = require('./config.json');
const es_client = require('./es');

router = express.Router();

router.get('/', function(req, res){
   if (!CONFIG.ES_ENABLED) {
      res.sendStatus(500);
      return
   }
   const COMMENT = "comment"
   const SUBMISSION = "submission"
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
   const subreddit = req.query.subreddit
   // date range optional
   const after = req.query.after;
   const before = req.query.before;

   const search = req.query.search;
   // title/body if submission
   // comment body if comment

   if (type === SUBMISSION) {
      // TODO: filter date range + filter subreddit
      let q = {
         size: 100,
         index: 'redarc',
         sort :[
            {"created_utc": 
               {
                  "order" : "desc"
               }
            }
         ],
         query: {
            bool: {
               must: [
                  {
                     multi_match: {
                        "query": search, 
                        "fields": [ "self_text", "title" ],
                     },
                  },
                  {
                     match: {
                        "type": 'submission'
                     },
                  },
                  {
                     match: {
                        "subreddit": subreddit
                     }
                  }
               ]
            }
         }
      }

      if (after && !before) {
         let x = {
            'range': {
               'created_utc': {
                  gte: after,
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)

      } else if(!after && before) {
         let x = {
            'range': {
               'created_utc': {
                  lte: before,
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)

      } else if (after && before) {
         let x = {
               'range': {
                  'created_utc': {
                     gte: after,
                     lte: before
                  }
               }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      }else {
         console.log('no dates')
      }
   
      es_client.search(q).then((result) => {
         res.json(result);
      }).catch((error)=> {
         res.sendStatus(500);
         console.log(error)
         return;
      })
   } else {
      let q = {
         size: 100,
         index: 'redarc_comments',
         sort :[
            {"created_utc": 
               {
                  "order" : "desc"
               }
            }
         ],
         query: {
            bool: {
               must: [
                  {
                     match: {
                        "body": search, 
                     },
                  },
                  {
                     match: {
                        "type": 'comment',
                     }
                  }, 
                  {
                     match: {
                        "subreddit": subreddit
                     }
                  }
               ],
            }
         }
      }

      if (after && !before) {
         let x = {
            'range': {
               'created_utc': {
                  'gte': after
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      } else if(!after && before) {
         let x = {
            'range': {
               'created_utc': {
                  'lte': before
               }
            }
         }
         q['query']['bool']['filter'].push(x)
      } else if (after && before) {
         let x = {
            'range': {
               'created_utc': {
                  'lte': before,
                  'gte': after
               }
            }
         }
         q['query']['bool']['filter'] = []
         q['query']['bool']['filter'].push(x)
      }else {

      }

      es_client.search(q).then((result) => {
         res.json(result);
      }).catch((error)=> {
         res.sendStatus(500);
         console.log(error)
         return;
      })
   }
});

module.exports = router;
