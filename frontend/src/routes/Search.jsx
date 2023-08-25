import React, { useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';

export default function Search(){
   const [errorMessage, setErrorMessage] = React.useState("");
   const navigate = useNavigate();
   const handleSubmit = event => {
      event.preventDefault();
      let query_string = '/query?';
      const subreddit = event.target.subreddit.value;
      if (subreddit.split(" ").length > 1 || subreddit.length === 0){
         setErrorMessage("Invalid subreddit name")
         return;
      }
      query_string = query_string + 'subreddit=' + subreddit
      const type = event.target.type.value;
      if (type !== "comment" && type !== "submission"){
         setErrorMessage("Invalid type")
         return;
      }
      query_string = query_string + '&type=' + type
      const before = event.target.before.value;
      if (before) {
         if (before.split("-").length > 3 || before.split("-").length < 3) {
            setErrorMessage("Invalid before date")
            return;
         }
         let unix_before = new Date(before).valueOf()/1000
         query_string = query_string + '&before=' + unix_before;
      }
      const after = event.target.after.value;
      if (after) {
         if (after.split("-").length > 3 || after.split("-").length < 3) {
            setErrorMessage("Invalid after date")
            return;
         }
         let unix_after = new Date(after).valueOf()/1000
         query_string = query_string + '&after=' + unix_after;
      }
      const search = event.target.search.value;

      if (search.length > 100 || search.length === 0){
         setErrorMessage("Invalid search query")
         return;
      }

      query_string = query_string + '&search=' + search;
      
      // const score = event.target.score.value;
      // if (score) {
      //    query_string = query_string + '&score=' + score; 
      // }
      navigate(query_string);
    };
   return (
      <>
      <body style={{minHeight: 100+'vh', display: 'flex', flexDirection: 'column'}}>
         <ul class="breadcrumb">
            <li><a href="/">Index</a> <span class="divider">/</span></li>
            <li><a href="/search">Search</a> <span class="divider">/</span></li>
         </ul>
         <div class="container">
         <h1>Search:</h1>
         <form onSubmit={handleSubmit}>
            <fieldset>
            <label>Search for</label>
               <select id = "type">
                  <option value="submission">Submission</option>
                  <option value="comment">Comment</option>
               </select>
               <label>Subreddit</label>
               <input id = "subreddit" type="text" placeholder="Subreddit"/>

               <label>Before Date: </label>
               <input id="before" type="text" placeholder="2010-01-01"/>
               <label>After Date: </label>
               <input id="after" type="text" placeholder="2010-01-01"/>
               {/* <label>Score filter</label>
               <input id="score" type="text" placeholder="Score filter eg: >100"/> */}
               <label>Search term</label>
               <input id="search" type="text"/>
            </fieldset>
            <button type="submit" class="btn btn-primary">Submit</button>
         </form>
         {errorMessage && <div class="alert alert-error"> {errorMessage} </div>}
         </div>
      </body>
      </>
   );
}