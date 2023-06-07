import React, { useEffect, useState } from 'react';
export default function Root() {

  const [subreddits, setSubreddits] = useState([]);
  useEffect(() => {
    fetch(import.meta.env.VITE_API_DOMAIN+ "/search/subreddits")
    .then ((resp) => resp.json())
    .then((data) => {
        setSubreddits(data)
    })
    .catch((error) => setThreads([]));
  }, []);
  return(
    <body style={{minHeight: 100+'vh', display: 'flex', flexDirection: 'column'}}>
      <div class="container">
        <div style={{position: "absolute", right: "0px"}}>
          <a href="https://github.com/yakabuff/redarc"><img decoding="async" loading="lazy" width="149" height="149" src="https://github.blog/wp-content/uploads/2008/12/forkme_right_red_aa0000.png?resize=149%2C149" class="attachment-full size-full" alt="Fork me on GitHub" data-recalc-dims="1"/></a>
        </div>
        <h1> Redarc </h1>

        <table style={{border: "1px solid"}} id = "threads" class="table">
        {subreddits.map((subreddit) => {
              return (
                <tr>
                  <td style={{border: "1px solid"}}> <a href = {`/r/${subreddit.name}`}>/r/{subreddit.name}</a></td>
                  <td style={{border: "1px solid"}}> {subreddit.num_submissions} Submissions</td>
                  <td style={{border: "1px solid"}}> {subreddit.num_comments} Comments</td>
                </tr>
              );
            })}
        </table>
      </div>
    </body>
  );
}
