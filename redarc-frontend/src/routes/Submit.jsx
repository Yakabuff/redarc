import React, { useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';

export default function Submit(){
   const [errorMessage, setErrorMessage] = React.useState("");
   const navigate = useNavigate();
   const handleSubmit = event => {
      event.preventDefault();
      let request = '/submit?';
      const url = event.target.url.value;
      //\S+reddit\.com\/r\/\S+\/comments\/\S+\/\S+\/?$
      //\S+redd\.it\/\S+\/?$
      const regexShort = new RegExp(/\S+redd\.it\/\S+\/?$/);
      const regexLong = new RegExp(/\S+reddit\.com\/r\/\S+\/comments\/\S+\/\S+\/?$/);
      const valid = regexShort.test(url) || regexLong.test(url);
      if (url.split(" ").length > 1 || url.length === 0 || valid === false){
         setErrorMessage("Invalid url: Must be in the format https://redd.it/123asf or https://www.reddit.com/r/foo/comments/asdf123/bar/")
         return;
      }
      request = request + 'url=' + url;
      fetch(import.meta.env.VITE_SUBMIT_DOMAIN + request)
      .then (resp => resp.json())
      .then((data) => {
         if (data.status === 'success') {
            setErrorMessage("Thread submitted! Check back in a bit.")
         } else {
            setErrorMessage("Failed to submit thread");
         }
      })
      .catch((error) => {setErrorMessage("Failed to submit thread");});
    };
   return (
      <>
      <body style={{minHeight: 100+'vh', display: 'flex', flexDirection: 'column'}}>
         <ul class="breadcrumb">
            <li><a href="/">Index</a> <span class="divider">/</span></li>
            <li><a href="/search">Search</a> <span class="divider">/</span></li>
         </ul>
         <div class="container">
         <h1>Submit:</h1>
         <form onSubmit={handleSubmit}>
            <fieldset>
            <label>Search for: </label>
               <input id="url" type="text" placeholder="redd.it/asdf213"/>
            </fieldset>
            <button type="submit" class="btn btn-primary">Submit</button>
         </form>
         {errorMessage && <div class="alert alert-error"> {errorMessage} </div>}
         </div>
      </body>
      </>
   );
}