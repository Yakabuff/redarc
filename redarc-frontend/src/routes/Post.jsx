import { useParams} from 'react-router';
export default function Post(props){
   const title = props.title
   const author = props.author
   const score = props.score;
   const date = props.date;
   const is_self = props.is_self;
   const type = props.is_self ? "self" : "link";
   const num_comments = props.num_comments;
   const self_text = props.body;
   const url = props.url;
   return(
      <div>
         <h1>{title}</h1>
         <h4>{type} | {author} | ⬆ {score} | 📅 {date} | {num_comments} comments</h4>
         {is_self ? <code>{self_text}</code> : <code>{url}</code>}
         <hr></hr>
      </div>
   )
}