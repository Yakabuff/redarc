export default function About(){
   return (
      <>
      <body style={{minHeight: 100+'vh', display: 'flex', flexDirection: 'column'}}>
         <ul class="breadcrumb">
            <li><a href="/">Index</a> <span class="divider">/</span></li>
            <li><a href="/about">About</a> <span class="divider">/</span></li>
         </ul>
         <div class="container">
         <h1>FAQ:</h1>
         <ul>
            <li><b>What is this site?</b> An archive that displays Reddit comments and threads over the years.  Depends which dumps the operator has added</li>
            <li><b>Where is this data from?</b> <a href="https://pushshift.io">Pushshift</a> data dumps</li>
            <li><b>Can I get a comment removed?</b> Contact the operator of this redarc instance</li>
         </ul>
         </div>
      </body>
      </>
   );
}