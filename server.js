var express = require('express');
var app = express();

var submissionRoutes = require('./submissions');
var commentRoutes = require('./comments');
app.use('/search/comments', commentRoutes);
app.use('/search/submissions', submissionRoutes);

app.listen(3000);
