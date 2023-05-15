import React, { useEffect, useState } from 'react';
import { useParams} from 'react-router';
export default function Subreddit(){
  const [threads, setThreads] = useState([]);
  const params = useParams()
  const subreddit = params.subreddit;
  const [pos, setPos] = useState(1);
  useEffect(() => {
      fetch("http://localhost:3000/search/submissions?subreddit="+subreddit)
      .then ((resp) => resp.json())
      .then((data) => {
          setThreads(data)
      })
      .catch((error) => setThreads([]));
  }, []);

  const next = (direction)=>{
    var date = document.getElementById('threads').rows[ table.rows.length - 1 ].cells[3];
  }
  const prev = (direction)=>{
    var date = document.getElementById('threads').rows[ table.rows.length - 1 ].cells[3];
  }

  return (
    <>
    <h1>/r/{subreddit}</h1>
    <button onClick={prev}>Prev</button>
    <code> {pos} </code>
    <button onClick={next}>Next</button>
    <br/>
    <table style={{border: "1px solid"}} id = "threads">

          {threads.map((thread) => {
            return (
              <tr>
                <td style={{border: "1px solid"}}> <a href = {`/r/${subreddit}/comments/${thread.id}`}>{thread.title}</a></td>
                <td style={{border: "1px solid"}}> {thread.subreddit}</td>
                <td style={{border: "1px solid"}}> {thread.author}</td>
                <td style={{border: "1px solid"}}> 📅{thread.created_utc}</td>
                <td style={{border: "1px solid"}}> ⬆{thread.score}</td>
                <td style={{border: "1px solid"}}> 🥇{thread.gilded}</td>
                <td style={{border: "1px solid"}}> 💬{thread.num_comments}</td>
              </tr>
            );
          })}

    </table>
    <button onClick={prev}>Prev</button>
    <code> {pos} </code>
    <button onClick={next}>Next</button>
    <br/>
   </>
  );  
}
