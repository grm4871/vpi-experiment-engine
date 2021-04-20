const TIMER = 3;
const MAX_STATES = 10;
const NUM_TRIALS = 2;

var trial = 0;
var timer = TIMER;
var state = 0;
var img = 0;
var counting = true;

countDown(counting)

function beginExperiment() {
    document.getElementById('instructions').hidden = true;
    document.getElementById('experiment').hidden = false;
    counting = true;
    img = 0;
    state = 0;
    timer = TIMER;
    countDown(counting);
}

// Counts down. Responsible for state rules and displaying images.
function countDown() {
    timer -= 1;
    if (timer == 0) {
            state++;
            displayImage(img);
            timer = TIMER - 1;
            img++;
    }

    //End of first trial
    if(state == MAX_STATES) {
        trial++;
        counting = false;
        document.getElementById('experiment').hidden = true;
        document.getElementById('test').hidden = false;
        document.getElementById('slideshow').src = ``;
    }

    //End of final trial
    if (state == MAX_STATES && trial == NUM_TRIALS) {
        counting = false;
        document.getElementById('instructions').hidden = true;
        document.getElementById('test').hidden = false;
        document.getElementById('cont_button').onclick = 'finish()';
        document.getElementById('cont_button').value = "Submit";
    }

    else if (state == 0) {
        document.getElementById('timer').innerHTML = `Your experiment will begin in ${timer}.`
    }
    else if(state >= 1) {
        document.getElementById('timer').innerHTML = `Time left: ${timer}`
    }
    if (counting) {
        window.setTimeout(countDown, 1000);
    }
}

function displayImage(img) {
    document.getElementById('slideshow').src = `static/images/_/${TRIAL1[img][0]}`;
}

function displayInstructions() {
    document.getElementById('instructions').hidden = false;
    document.getElementById('test').hidden = true;
}
