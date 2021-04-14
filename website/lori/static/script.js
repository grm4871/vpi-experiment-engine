const isExperimentPage = document.documentElement.classList.contains('experiment');

var timer = 6;
var state = 0;

countDown()
console.log(timer);

function countDown() {
    timer -= 1;
    console.log(timer);
    if (state == 0) {
        document.getElementById('timer').innerHTML = `Your experiment will begin in ${timer}.`
        
        if(timer == 1) {
            state++;
        }
    }
    else if(state == 1) {
    }
    window.setTimeout(countDown, 1000);
}