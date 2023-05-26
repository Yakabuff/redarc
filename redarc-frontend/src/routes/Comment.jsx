export default function Comment(props){
   const date = props.date;
   const score = props.score;
   const author = props.author;
   const gilded = props.gilded;
   const body = props.body;
   const id = props.id;
   const replies = props.replies;
   const depth = props.depth;
   return(
      <>
      <div>
         <h4> <span class="label label-success">Anonymous</span> <span class="label label-important">⬆ {score}</span>  <span class="label label-info">{date}</span>  <span class="label label-default">{replies.length} replies</span></h4>
         <div class="well">{<p>{body}</p>}</div>
      </div>

      {replies.map((comment) => {
         return(
            <div style = {{marginLeft: 50, borderLeftStyle: "dotted", borderWidth: 0.5, paddingLeft: 15}}>
               <Comment 
                  id = {comment.id}
                  body = {comment.body}
                  author = {comment.author}
                  score = {comment.score}
                  gilded = {comment.gilded}
                  date = {comment.created_utc}
                  replies = {comment.replies}
                  depth = {depth+1} />
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