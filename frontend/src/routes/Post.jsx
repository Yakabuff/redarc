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
   const permalink = props.permalink;
   const subreddit = props.subreddit;
   const imageURL = url && url.includes('redd.it') ?
      import.meta.env.VITE_API_DOMAIN + "/media?file=" +
      props.url.split('/').at(-1) + "&subreddit=" + subreddit: null;
   const toggleThumbnail = () =>{
      let x = document.getElementById("thumbnail");
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
   }

   const toggleFull = () =>{
      let x = document.getElementById("full");
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
   }

   return(
      <div>
         <h1><a style={{color: 'inherit'}} href={`https://reddit.com${permalink}`}>{title}</a></h1>
         <h4>
            <span class="label label-info">{type}</span>&nbsp;
            <span class="label label-success">Anonymous</span>&nbsp;
            <span class="label label-important">⬆ {score} 🪙 {gilded}</span>&nbsp;
            {date != null && <span class="label label-info">{new Date(parseInt(date) * 1000).toISOString()}</span>}&nbsp;
            <span class="label label-default">{num_comments} comments</span>
         </h4>
         {is_self ? <div class="well"><p style={{overflowWrap: 'break-word'}}>{self_text}</p></div> : <div class="well"><p style={{overflowWrap: 'break-word'}}><small>{url}</small></p></div>}
         <img src={thumbnail} class="img-rounded" id="thumbnail" style={{display: 'none'}}></img>
         <a onClick={toggleThumbnail} type="thumbnail"><small>Thumbnail</small></a>
         <br></br>
         <img src={imageURL} class="img-rounded" id="full" style={{display: 'none'}}></img>
         {imageURL ? <a onClick={toggleFull} type="full"><small>Full Image</small></a> : <br></br>}
         <hr></hr>
      </div>
   )
}

