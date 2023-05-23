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
         <h4> Anonymous | ⬆ {score} | 📅 {date} | {replies.length} replies</h4>
         {<code>{body}</code>}
      </div>

      {replies.map((comment) => {
         return(
            // <>
            // <h2>{comment.author}</h2>
            // <h2>{comment.body}</h2>
            // </>
            <div style = {{marginLeft: 50, borderLeftStyle: "solid", borderWidth: 1, paddingLeft: 15}}>
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