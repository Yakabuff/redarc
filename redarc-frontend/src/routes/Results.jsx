import React, { useEffect, useState } from 'react';
import { useSearchParams } from "react-router-dom";

export default function Results(){
   const [results, setResults] = useState([]);
   const [searchParams, setSearchParams] = useSearchParams();
   const [errorMessage, setErrorMessage] = React.useState("");
   useEffect(() => {
      let q = import.meta.env.VITE_API_DOMAIN 
      + "/search?type="+searchParams.get("type")
      + "&search=" + searchParams.get("search")
      + '&subreddit=' + searchParams.get("subreddit");

      if (searchParams.get("before")) {
         q += "&before=" + searchParams.get("before")
      }

      if (searchParams.get("after")) {
         q += "&after=" + searchParams.get("after")
      }

      fetch(q)
      .then ((resp) => resp.json())
      .then((data) => {
         // console.log(data['hits']['hits'])
         let x = data['hits']['hits']
         x.map(z => {
            z['_source']['created_utc'] = new Date(z['_source']['created_utc']*1000).toLocaleDateString("en-US"); 
         })
         document.title = 'Redarc - Results for ' + searchParams.get("search");
         setResults(x)
      })
      .catch((error) => {
         setResults([])
         setErrorMessage("Error 500. Something went wrong or searching is disabled")
      });
   }, [])

   if (searchParams.get("type") === "submission") {
      return (
         <>
         <div class="container-fluid">
            <h3>Submission results for: <code>{searchParams.get("search")}</code></h3>
            <table style={{border: "1px solid"}} id = "threads" class="table">
               {results.map((result) => {
                  return (
                  <tr>
                     <td> {result['_source']['created_utc']} </td>
                     <td> <a href = {"/r/"+searchParams.get("subreddit")+"/comments/"+result._id}>{result['_source']['title']} </a></td>
                     <td> {result._source.self_text} </td>
                  </tr>
                  );
               })}
            </table>
          </div>
          {errorMessage && <div class="alert alert-error"> {errorMessage} </div>}
          </>
      )
   } else if (searchParams.get("type") === "comment") {
      return (
         <>
         <div class="container-fluid">
            <h1>Comment results for: <code>{searchParams.get("search")}</code></h1>
            <table style={{border: "1px solid"}} id = "comments" class="table">
               {results.map((result) => {
                  return (
                  <tr>
                     <td> {result['_source']['created_utc']} </td>
                     <td> <a href = {"/r/"+searchParams.get("subreddit")+"/comments/"+result._source.link_id}>{result['_source']['body']} </a></td>
                  </tr>
                  );
               })}
            </table>
         </div>
         {errorMessage && <div class="alert alert-error"> {errorMessage} </div>}
         </>
      )
   } else {
      return (
         <div class="alert alert-error"> Invalid document type! </div>
      )
   }

}