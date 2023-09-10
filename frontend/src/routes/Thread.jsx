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
        fetch(import.meta.env.VITE_API_DOMAIN + "/search/comments?link_id="+ threadID + "&unflatten=true")
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
            <li><a href="/search">Search</a> <span class="divider">/</span></li>
        </ul>
        <div class="container-fluid">
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
                thumbnail = {post.thumbnail}
                permalink = {post.permalink}
                subreddit = {post.subreddit}
            />

            {comments.map((comment) => {
                return(
                <Comment 
                    id = {comment.id}
                    body = {comment.body}
                    author = {comment.author}
                    score = {comment.score}
                    gilded = {comment.gilded}
                    date = {new Date(parseInt(comment.created_utc * 1000)).toISOString()}
                    replies = {comment.replies}
                    depth = {0} />
                )
            })}
        </div>
    </body>
    </>
    );  
}
