import React, { useEffect, useState } from 'react';
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
   const thumbnail = props.thumbnail;
   const gilded = props.gilded;

   const toggle = () =>{
      let x = document.getElementById("thumbnail");
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }

   return(
      <div>
         <h1>{title}</h1>
         <h4>
            <span class="label label-info">{type}</span>&nbsp;
            <span class="label label-success">Anonymous</span>&nbsp;
            <span class="label label-important">⬆ {score} 🪙 {gilded}</span>&nbsp;
            {date != null && <span class="label label-info">{new Date(parseInt(date) * 1000).toISOString()}</span>}&nbsp;
            <span class="label label-default">{num_comments} comments</span>
         </h4>
         {is_self ? <div class="well"><p style={{overflowWrap: 'break-word'}}>{self_text}</p></div> : <div class="well"><p style={{overflowWrap: 'break-word'}}><small>{url}</small></p></div>}
         <img src={thumbnail} class="img-rounded" id="thumbnail"></img>
         <a onClick={toggle}><small>Toggle thumbnail</small></a>
         <hr></hr>
      </div>
   )
}

