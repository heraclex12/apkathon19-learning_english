function abcf()
{
    var checkbox=document.getElementById("change-pass");
    var disp=document.getElementById("test");
    if(checkbox.checked==true)
    {
        disp.style.display="block";
    }
    else {
        disp.style.display = "none";
      }
}