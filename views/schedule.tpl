<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Jotari op {{time}}</title>


<style>
  #klein
  {
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:33%;
    border-collapse:collapse;
  }
  #klein td, #klein th 
  {
    font-size:1.2em;
    border:1px solid #347638;
    padding:3px 7px 2px 7px;
  }
  #klein th 
  {
    font-size:1.4em;
    text-align:left;
    padding-top:5px;
    padding-bottom:4px;
    background-color:#347638;
    color:#fff;
  }
  #klein tr.alt td 
  {
    color:#000;
    background-color:#347638;
  }
</style>

<style>
  #groot
  {
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:33%;
    border-collapse:collapse;
  }
  #groot td, #groot th 
  {
    font-size:1.2em;
    border:1px solid #DFCAAB;
    padding:3px 7px 2px 7px;
  }
  #groot th 
  {
    font-size:1.4em;
    text-align:left;
    padding-top:5px;
    padding-bottom:4px;
    background-color:#DFCAAB;
    color:#fff;
  }
  #groot tr.alt td 
  {
    color:#000;
    background-color:#DFCAAB;
  }
</style>

<style>
  #leiding
  {
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:33%;
    border-collapse:collapse;
  }
  #leiding td, #leiding th
  {
    font-size:1.2em;
    border:1px solid #DE2A4D;
    padding:3px 7px 2px 7px;
  }
  #leiding th
  {
    font-size:1.4em;
    text-align:left;
    padding-top:5px;
    padding-bottom:4px;
    background-color:#DE2A4D;
    color:#fff;
  }
  #leiding tr.alt td
  {
    color:#000;
    background-color:#DE2A4D;
  }
</style>

  </head>
  <body>
    <div style="float: left;">
      <table id='klein'>
        <tr><th>Klein</th><th>Programma</th></tr>
         % for group, activity in klein.iteritems():
            <tr>
              <td>{{group}}</td><td>{{activity}}</td>
            </tr>
          % end
      </table>
    </div>
    <div style="float: left;">
      <table id='groot'>
        <tr><th>Groot</th><th>Programma</th></tr>
         % for group, activity in groot.iteritems():
            <tr>
              <td>{{group}}</td><td>{{activity}}</td>
            </tr>
          % end
      </table>
    </div>
  </body>
</html>
