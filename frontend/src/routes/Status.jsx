import React, { useEffect, useState } from 'react';
import { useParams} from 'react-router';

export default function Status(){
   const [progs, setProgress] = useState([]);
   const params = useParams()
   const subreddit = params.job_id;
   useEffect(() => {
      fetch(import.meta.env.VITE_API_DOMAIN+ "/status?job_id="+subreddit)
      .then ((resp) => resp.json())
      .then((data) => {
         setProgress(data)
      })
      .catch((error) => setProgress([]));
   }, []);

  return (
      <>
      <body style={{minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
      <ul class="breadcrumb">
      <li><a href="/">Index</a> <span class="divider">/</span></li>
      <li><a href="/search">Search</a> <span class="divider">/</span></li>
      </ul>
      <div class="container-fluid">

      <h1>Progress:</h1>
      <br/>

      <table id = "threads" class = "table table-bordered table-condensed">
         <tr>
            <td> Job ID</td>
            <td> Job start</td>
            <td> Job finish </td>
            <td> Status </td>
         </tr>
         {progs.map((p) => {
            return (
               <tr>
                  <td> {p.job_id}</td>
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
