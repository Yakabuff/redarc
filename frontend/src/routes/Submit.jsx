import React, { useEffect, useState} from 'react';

export default function Submit(){
   const [errorMessage, setErrorMessage] = React.useState("");
   const handleSubmit = event => {
      event.preventDefault();
      let request = '/submit';
      const url = event.target.url.value;
      const password = event.target.password.value;
      //\S+reddit\.com\/r\/\S+\/comments\/\S+\/\S+\/?$
      //\S+redd\.it\/\S+\/?$
      const regexShort = new RegExp(/\S+redd\.it\/\S+\/?$/);
      const regexLong = new RegExp(/\S+reddit\.com\/r\/\S+\/comments\/\S+\/\S+\/?$/);
      const valid = regexShort.test(url) || regexLong.test(url);
      if (url.split(" ").length > 1 || url.length === 0 || valid === false){
         setErrorMessage("Invalid url: Must be in the format https://redd.it/123asf or https://www.reddit.com/r/foo/comments/asdf123/bar/")
         return;
      }

      fetch(import.meta.env.VITE_API_DOMAIN + request, {
         headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
          },
         method: "POST",
         body: JSON.stringify({'url': url, 'password': password})
      })
      .then (resp => {
         if (resp['status'] === 401) {
            throw new Error("Invalid password")
         } else if (resp['status'] === 501) {
            throw new Error("Ingest disabled")
         } else {
            return resp.json()
         }
      })
      .then((data) => {
         if (data.status === 'success') {
            throw new Error("Thread submitted! Check back in a bit. Job ID: "+  data.id)
         } else {
            throw new Error("Failed to submit thread");
         }
      })
      .catch((error) => {
         console.log(error)
         setErrorMessage(error.message);
      });
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
               <label>Submit thread URL: </label>
               <input id="url" type="text" placeholder="redd.it/asdf213"/>
               <label>Password: Leave blank if no password set</label>
               <input id="password" type="text" placeholder="password"/>
            </fieldset>
            <button type="submit" class="btn btn-primary">Submit</button>
         </form>
         {errorMessage && <div class="alert alert-error"> {errorMessage} </div>}
         </div>
      </body>
      </>
   );
}