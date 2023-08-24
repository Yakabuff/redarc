var express = require('express');
var cors = require('cors');
var app = express();
var submissionRoutes = require('./submissions');
var commentRoutes = require('./comments');
var subredditRoutes = require('./subreddits');
var searchRoutes = require('./search');
var progressRoutes = require('./progress');
var statusRoutes = require('./status');

app.use(cors());
app.use(express.json())
app.use('/search/comments', commentRoutes);
app.use('/search/submissions', submissionRoutes);
app.use('/search/subreddits', subredditRoutes);
app.use('/search', searchRoutes);
app.use('/progress', progressRoutes);
app.use('/status', statusRoutes);

app.listen(3000);
