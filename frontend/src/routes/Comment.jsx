export default function Comment(props){
   const date = props.date;
   const score = props.score;
   const author = props.author;
   const gilded = props.gilded;
   const body = props.body;
   const id = props.id;
   const replies = props.replies;
   const depth = props.depth;
   const threadPermalink = props.threadPermalink;
   const commentPermalink = props.threadPermalink + id;
   return(
      <>
      <div>
         <h4> 
            <span class="label label-success">Anonymous</span>&nbsp;
            <span class="label label-important">⬆ {score} 🪙 {gilded}</span>&nbsp;
            <span class="label label-info"><a style={{color: 'inherit'}} href={`https://reddit.com${commentPermalink}`}>{date}</a></span>&nbsp;
            <span class="label label-default">{replies.length} replies</span>
         </h4>
         <div class="well">{<p>{body}</p>}</div>
      </div>

      {replies.map((comment) => {
         return(
            <div style = {{marginLeft: 50, borderLeftStyle: "dotted", borderWidth: 0.5, paddingLeft: 15}}>
               {comment.created_utc != null && <Comment 
                  id = {comment.id}
                  body = {comment.body}
                  author = {comment.author}
                  score = {comment.score}
                  gilded = {comment.gilded}
                  date = {new Date(parseInt(comment.created_utc * 1000)).toISOString()}
                  replies = {comment.replies}
                  threadPermalink = {threadPermalink}
                  commentPermalink = {threadPermalink + comment.id}
                  depth = {depth+1} />
               }
            </div>
         )
      })}
      </>
   )
}
// jan 1 2021 - 11 upvotes - authorname - gilded 
// asdfasdf
// ------------------------
// |jan 1 2021 - 11 upvotes - authorname - gilded 
// | asdfasdf
// ------------------------
//   |jan 1 2021 - 11 upvotes - authorname - gilded 
//   | asdfasdf
// ------------------------
//   |jan 1 2021 - 11 upvotes - authorname - gilded 
//   | asdfasdf
// Each Comment component renders its child 
// Comment gets its margin size from its parent