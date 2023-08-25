import React, { useEffect, useState } from 'react';

export default function Progress(){
   const [progs, setProgress] = useState([]);
   const handleSubmit = event => {
      event.preventDefault();
      const password = event.target.password.value;
      fetch(import.meta.env.VITE_API_DOMAIN+ "/progress", {
         headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
          },
         method: "POST",
         body: JSON.stringify({'password': password})
      })
      .then ((resp) => {
         if (resp['status'] === 401) {
            throw new Error("Invalid password")
         } else {
            return resp.json()
         }
      })
      .then((data) => {
         setProgress(data)
      })
      .catch((error) => setProgress([]));
   }

  return (
      <>
      <body style={{minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
      <ul class="breadcrumb">
      <li><a href="/">Index</a> <span class="divider">/</span></li>
      <li><a href="/search">Search</a> <span class="divider">/</span></li>
      </ul>
      <div class="container-fluid">
      <form onSubmit={handleSubmit}>
         <fieldset>
            <label>Password:</label>
            <input id="password" type="text" placeholder="password"/>
         </fieldset>
         <button type="submit" class="btn btn-primary">Submit</button>
      </form>
      <h1>Progress:</h1>
      <br/>

      <table id = "threads" class = "table table-bordered table-condensed">
         <tr>
            <td> Job ID</td>
            <td> URL </td>
            <td> Job start</td>
            <td> Job finish </td>
            <td> Status </td>
         </tr>
         {progs.map((p) => {
            return (
               <tr>
                  <td> {p.job_id}</td>
                  <td> {p.url}</td>
                  <td> {new Date(p.start_utc * 1000).toISOString()}</td>
                  <td> {new Date(p.finish_utc * 1000).toISOString()} </td>
                  <td> {p.error ? <span class="label label-important">Error</span> : <span class="label label-success">Success</span>}</td>
               </tr>
            );
            })}

      </table>
      </div>
      </body>
      </>
   );  
}
