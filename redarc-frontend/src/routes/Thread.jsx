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
  useEffect(() => {
      fetch("http://localhost:3000/search/comments?link_id=t3_"+threadID + "&unflatten=true")
      .then ((resp) => resp.json())
      .then((data) => {
          setComments(data)
      })
      .catch((error) => setComments([]));

      fetch("http://localhost:3000/search/submissions?id="+threadID)
      .then ((resp) => resp.json())
      .then((data) => {
          setPost(data[0])
      })
      .catch((error) => setPost({}));
  }, []);

  return (
      <>
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
            // <>
            // <h2>{comment.author}</h2>
            // <h2>{comment.body}</h2>
            // </>
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

   </>
  );  
}
