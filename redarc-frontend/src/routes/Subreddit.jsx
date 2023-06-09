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
    let  date = table.rows[ table.rows.length - 1 ].cells[2].innerHTML;

    fetch(import.meta.env.VITE_API_DOMAIN + "/search/submissions?subreddit="+subreddit+"&before="+date)
    .then ((resp) => resp.json())
    .then((data) => {
        setThreads(data)
    })
    .catch((error) => setThreads([]));
  }
  const prev = ()=>{
    let table = document.getElementById('threads');
    let date = table.rows[ 0 ].cells[2].innerHTML;


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
    </ul>
    <div class="container">

    <h1>/r/{subreddit}</h1>

    <select name="year" id="year" onChange={jump}>
      <option value="2023-01-01T00:00:00.000Z">2023</option>
      <option value="2022-01-01T00:00:00.000Z">2022</option>
      <option value="2021-01-01T00:00:00.000Z">2021</option>
      <option value="2020-01-01T00:00:00.000Z">2020</option>
      <option value="2019-01-01T00:00:00.000Z">2019</option>
      <option value="2018-01-01T00:00:00.000Z">2018</option>
      <option value="2017-01-01T00:00:00.000Z">2017</option>
      <option value="2016-01-01T00:00:00.000Z">2016</option>
      <option value="2015-01-01T00:00:00.000Z">2015</option>
      <option value="2014-01-01T00:00:00.000Z">2014</option>
      <option value="2013-01-01T00:00:00.000Z">2013</option>
      <option value="2012-01-01T00:00:00.000Z">2012</option>
      <option value="2011-01-01T00:00:00.000Z">2011</option>
      <option value="2010-01-01T00:00:00.000Z">2010</option>
      <option value="2009-01-01T00:00:00.000Z">2009</option>
      <option value="2008-01-01T00:00:00.000Z">2008</option>
      <option value="2007-01-01T00:00:00.000Z">2007</option>
      <option value="2006-01-01T00:00:00.000Z">2006</option>
      <option value="2005-01-01T00:00:00.000Z">2005</option>
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
                <td> {thread.created_utc} </td>
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
