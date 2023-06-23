import React, { useEffect, useState } from 'react';
import { useSearchParams } from "react-router-dom";

export default function Results(){
   const [results, setResults] = useState([]);
   const [searchParams, setSearchParams] = useSearchParams();
   const [errorMessage, setErrorMessage] = React.useState("");

   const next = ()=>{
      let table = document.getElementById('results')
      let date = table.rows[ table.rows.length - 1 ].cells[0].id;
      let query = searchParams.get("search");
      let subreddit = searchParams.get("subreddit");
      const type = searchParams.get("type");
      fetch(import.meta.env.VITE_API_DOMAIN + "/search?subreddit="+subreddit+"&before="+date+"&search="+query+"&type="+type)
      .then ((resp) => resp.json())
      .then((data) => {
         let x = data['hits']['hits']
         // console.log(x)
         setResults(x)
      })
      .catch((error) => setResults([]));
    }
    const prev = ()=>{
      let table = document.getElementById('results')
      let date = table.rows[ 0 ].cells[0].id;
      let query = searchParams.get("search");
      let subreddit = searchParams.get("subreddit");
      const type = searchParams.get("type");
      fetch(import.meta.env.VITE_API_DOMAIN + "/search?subreddit="+subreddit+"&after="+date+"&search="+query+"&type="+type+"&sort=asc")
      .then ((resp) => resp.json())
      .then((data) => {
         let x = data['hits']['hits']
         x.reverse()
         setResults(x)
      })
      .catch((error) => setResults([]));
    }

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
         // console.log(data)
         let x = data['hits']['hits']
         document.title = 'Redarc - Results for ' + searchParams.get("search");
         setResults(x)
      })
      .catch((error) => {
         // console.log(error)
         setResults([])
         setErrorMessage("Error 500. Something went wrong or searching is disabled")
      });
   }, [])

   if (searchParams.get("type") === "submission") {
      return (
         <>
         <ul class="breadcrumb">
            <li><a href="/">Index</a> <span class="divider">/</span></li>
            <li><a href="/search">Search</a> <span class="divider">/</span></li>
         </ul>
         <div class="container-fluid">
            <h1>Submission results for: </h1>
            <code>{searchParams.get("search")}</code> in <code>{searchParams.get("subreddit")}</code>
            <br/>
            <button onClick={prev} class = "btn btn-link">Prev</button>
            <button onClick={next} class = "btn btn-link">Next</button>
            <br/>
            <table style={{border: "1px solid"}} id = "results" class="table">
               {results.map((result) => {
                  return (
                  <tr>
                     <td id={result['_source']['created_utc']}>{result['_source']['datestring']}</td>
                     <td> <a href = {"/r/"+searchParams.get("subreddit")+"/comments/"+result._id}>{result['_source']['title']} </a></td>
                     <td> {result._source.self_text} </td>
                  </tr>
                  );
               })}
            </table>
               <button onClick={prev} class = "btn btn-link">Prev</button>
               <button onClick={next} class = "btn btn-link">Next</button>
            <br/>
         </div>
         {errorMessage && <div class="alert alert-error"> {errorMessage} </div>}
          </>
      )
   } else if (searchParams.get("type") === "comment") {
      return (
         <>
         <ul class="breadcrumb">
            <li><a href="/">Index</a> <span class="divider">/</span></li>
            <li><a href="/search">Search</a> <span class="divider">/</span></li>
        </ul>
         <div class="container-fluid">
            <h1>Comment results for: </h1>
            <code>{searchParams.get("search")}</code> in <code>{searchParams.get("subreddit")}</code>
            <br/>
            <button onClick={prev} class = "btn btn-link">Prev</button>
            <button onClick={next} class = "btn btn-link">Next</button>
            <br/>
            <table style={{border: "1px solid"}} id = "results" class="table">
               {results.map((result) => {
                  return (
                  <tr>
                     <td id={result['_source']['created_utc']}>{result['_source']['datestring']}</td>
                     <td> <a href = {"/r/"+searchParams.get("subreddit")+"/comments/"+result._source.link_id}>{result['_source']['body']} </a></td>
                  </tr>
                  );
               })}
            </table>
               <button onClick={prev} class = "btn btn-link">Prev</button>
               <button onClick={next} class = "btn btn-link">Next</button>
            <br/>
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