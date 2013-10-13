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
    width:100%;
    border-collapse:collapse;
  }
  #klein td, #klein th 
  {
    font-size:1.2em;
    border:1px solid #98bf21;
    padding:3px 7px 2px 7px;
  }
  #klein th 
  {
    font-size:1.4em;
    text-align:left;
    padding-top:5px;
    padding-bottom:4px;
    background-color:#A7C942;
    color:#fff;
  }
  #klein tr.alt td 
  {
    color:#000;
    background-color:#EAF2D3;
  }
</style>

<style>
  #groot
  {
    font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
    width:100%;
    border-collapse:collapse;
  }
  #groot td, #groot th 
  {
    font-size:1.2em;
    border:1px solid #C92424;
    padding:3px 7px 2px 7px;
  }
  #groot th 
  {
    font-size:1.4em;
    text-align:left;
    padding-top:5px;
    padding-bottom:4px;
    background-color:#C92424;
    color:#fff;
  }
  #groot tr.alt td 
  {
    color:#000;
    background-color:#C92424;
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

    <div style="float: right;">
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