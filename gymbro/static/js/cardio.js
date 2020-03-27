$(document).ready(function(){
    document.getElementById("start").onclick = function add(){
        var h1 = document.getElementsByTagName('footer')[0],
            start = document.getElementById('start'),
            stop = document.getElementById('stop'),
            clear = document.getElementById('clear'),
            seconds = 0, minutes = 0,
            t;
        function add() {
            seconds++;
            if (seconds >= 60) {
                seconds = 0;
                minutes++;
            }
            h1.textContent =(minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);
            timer();
        }
        function timer() {
            t = setTimeout(add, 1000);
        }
        timer();


        /* Start button */
        start.onclick = timer;

        /* Stop button */
        stop.onclick = function() {
            clearTimeout(t);
        }

        /* Clear button */
        clear.onclick = function() {
            h1.textContent = "00:00";
            seconds = 0; minutes = 0;
        }
};
});