import React, { useEffect, useState } from 'react';
import { useParams} from 'react-router';
import Post from "./Post";
import Comment from "./Comment";

export default function Thread(){
  const [comments, setComments] = useState([]);
  const [post, setPost] = useState({});
  const params = useParams()
  const subreddit = params.subreddit;
  const threadID = params.threadID;
  const formal_threadID = threadID.split('_').length > 1 ? threadID : 't3' + '_' + threadID;

  useEffect(() => {
      fetch(import.meta.env.VITE_API_DOMAIN + "/search/comments?link_id="+ formal_threadID + "&unflatten=true")
      .then ((resp) => resp.json())
      .then((data) => {
          setComments(data)
      })
      .catch((error) => setComments([]));

      fetch(import.meta.env.VITE_API_DOMAIN + "/search/submissions?id="+threadID)
      .then ((resp) => resp.json())
      .then((data) => {
          setPost(data[0])
          document.title = 'Redarc - ' + data[0].title;
      })
      .catch((error) => setPost({}));
  }, []);

  return (
    <>
    <body style={{minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
        <ul class="breadcrumb">
            <li><a href="/">Index</a> <span class="divider">/</span></li>
            <li><a href={`/r/${subreddit}`}>{subreddit}</a> <span class="divider">/</span></li>
        </ul>
        <div class="container">
        <Post 
            title = {post.title}
            author = {post.author}
            is_self = {post.is_self}
            date = {post.created_utc}
            body = {post.self_text}
            url = {post.url}
            gilded = {post.gilded}
            score = {post.score}
            num_comments = {post.num_comments}
        />

        {comments.map((comment) => {
            return(
            <Comment 
                id = {comment.id}
                body = {comment.body}
                author = {comment.author}
                score = {comment.score}
                gilded = {comment.gilded}
                date = {comment.created_utc}
                replies = {comment.replies}
                depth = {0} />
            )
        })}
        </div>
        <footer style = {{ textAlign: 'center', padding: 30+'px 0', marginTop: 'auto', borderTop: 1+'px solid #e5e5e5', backgroundColor: '#f5f5f5' }}>
            <div class="container">
            <small>redarc is licensed under the <a href="http://opensource.org/licenses/MIT">MIT License</a></small>
            <br/>
            <ul style = {{display: 'inline', listStyleType: 'none'}}>
                <li style = {{display: 'inline', paddingRight: 10+'px'}}><small><a href="https://github.com/yakabuff/redarc">redarc</a></small></li>
                <li style = {{display: 'inline', paddingRight: 10+'px'}}><small><a href="http://basedbin.org">basedbin.org</a></small></li>
                <li style = {{display: 'inline', paddingRight: 10+'px'}}><small><a href="/about">FAQ</a></small></li>
            </ul>
            </div>
        </footer>
    </body>
    </>
  );  
}
