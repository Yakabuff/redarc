export default function Footer(){
   return (
      <footer style = {{ textAlign: 'center', padding: 10+'px 0', marginTop: 'auto', borderTop: 1+'px solid #e5e5e5', backgroundColor: '#f5f5f5' }}>
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
   );
}