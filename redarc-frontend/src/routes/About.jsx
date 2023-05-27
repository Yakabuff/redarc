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
         <footer style = {{ textAlign: 'center', padding: 30+'px 0', marginTop: 'auto', borderTop: 1+'px solid #e5e5e5', backgroundColor: '#f5f5f5' }}>
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
      </>
   );
}