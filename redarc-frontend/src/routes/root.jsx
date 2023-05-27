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

      <footer style = {{ marginTop: 'auto', textAlign: 'center', padding: 30+'px 0', borderTop: 1+'px solid #e5e5e5', backgroundColor: '#f5f5f5' }}>
        <div class="container">
          <small>redarc is licensed under the <a href="http://opensource.org/licenses/MIT">MIT License</a></small>
          <br/>
          <ul style = {{display: 'inline', listStyleType: 'none'}}>
            <li style = {{display: 'inline', paddingRight: 10+'px'}}><small><a href="https://github.com/yakabuff/redarc">redarc</a></small></li>
            <li style = {{display: 'inline', paddingRight: 10+'px'}}><small><a href="http://basedbin.org">basedbin.org</a></small></li>
            <li style = {{display: 'inline', paddingRight: 10+'px'}}><small><a href="/about">FAQ</a></small></li>
          </ul>
        </div>
      </footer>
    </body>
  );
}
