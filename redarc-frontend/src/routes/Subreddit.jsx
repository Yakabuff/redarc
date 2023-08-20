import React, { useEffect, useState } from 'react';
import { useParams} from 'react-router';

export default function Subreddit(){
  const [threads, setThreads] = useState([]);
  const params = useParams()
  const subreddit = params.subreddit;

  useEffect(() => {
      fetch(import.meta.env.VITE_API_DOMAIN+ "/search/submissions?subreddit="+subreddit)
      .then ((resp) => resp.json())
      .then((data) => {
          setThreads(data)
      })
      .catch((error) => setThreads([]));
  }, []);

  const next = ()=>{
    let table = document.getElementById('threads')
    let  date = table.rows[ table.rows.length - 1 ].cells[2].id;

    fetch(import.meta.env.VITE_API_DOMAIN + "/search/submissions?subreddit="+subreddit+"&before="+date)
    .then ((resp) => resp.json())
    .then((data) => {
        setThreads(data)
    })
    .catch((error) => setThreads([]));
  }
  const prev = ()=>{
    let table = document.getElementById('threads');
    let date = table.rows[ 0 ].cells[2].id;


    fetch(import.meta.env.VITE_API_DOMAIN + "/search/submissions?subreddit="+subreddit+"&after="+date+"&sort=ASC")
    .then ((resp) => resp.json())
    .then((data) => {
        data.reverse()
        setThreads(data)
    })
    .catch((error) => setThreads([]));
  }

  const jump = () => {
    var e = document.getElementById("year");
    var value = e.value;
    fetch(import.meta.env.VITE_API_DOMAIN + "/search/submissions?subreddit="+subreddit+"&after="+value+"&sort=ASC")
    .then ((resp) => resp.json())
    .then((data) => {
        setThreads(data)
    })
    .catch((error) => setThreads([]));
  }

  return (
    <>
    <body style={{minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
    <ul class="breadcrumb">
      <li><a href="/">Index</a> <span class="divider">/</span></li>
      <li><a href="/search">Search</a> <span class="divider">/</span></li>
    </ul>
    <div class="container">

    <h1>/r/{subreddit}</h1>

    <select name="year" id="year" onChange={jump}>
      <option value="1672531200">2023</option>
      <option value="1640995200">2022</option>
      <option value="1609459200">2021</option>
      <option value="1577836800">2020</option>
      <option value="1546300800">2019</option>
      <option value="1514764800">2018</option>
      <option value="1483228800">2017</option>
      <option value="1451606400">2016</option>
      <option value="1420070400">2015</option>
      <option value="1388534400">2014</option>
      <option value="1356998400">2013</option>
      <option value="1325376000">2012</option>
      <option value="1293840000">2011</option>
      <option value="1262304000">2010</option>
      <option value="1230768000">2009</option>
      <option value="1199145600">2008</option>
      <option value="1167609600">2007</option>
      <option value="1136073600">2006</option>
      <option value="1104537600">2005</option>
    </select>
    <br/>
    <button onClick={prev} class = "btn btn-link">Prev</button>
    <button onClick={next} class = "btn btn-link">Next</button>
    <br/>
    <br/>
    <table id = "threads" class = "table table-bordered table-condensed">

          {threads.map((thread) => {
            return (
              <tr>
                <td> <span class="label label-info">{thread.is_self ? "self" : "link"}</span></td>
                <td> <a href = {`/r/${subreddit}/comments/${thread.id}`}>{thread.title}</a></td>
                <td id={thread.created_utc}> {new Date(thread.created_utc * 1000).toISOString()} </td>
                <td> ⬆ {thread.score}</td>
                <td>🥇 {thread.gilded} </td>
                <td> 💬 {thread.num_comments}</td>
              </tr>
            );
          })}

    </table>
    <button onClick={prev} class = "btn btn-link">Prev</button>
    <button onClick={next} class = "btn btn-link">Next</button>
    </div>
    <br/>
    </body>
    </>
  );  
}
