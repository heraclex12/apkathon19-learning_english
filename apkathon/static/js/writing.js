var bool = 1;
function show() {
    var disp = document.getElementById("test");
    var disp2 = document.getElementById("answer");
    if (bool == 1) {
        disp.style.display = "block";
        bool=0;
        disp2.innerHTML='Ẩn lời giải';
    }
    else
    {
        disp.style.display = "none";
        disp2.innerHTML='Xem lời giải';
        bool=1;
    }



}