const TIMER = 2;
const MAX_STATES = 5;
const NUM_TRIALS = 1;

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
    if(state == MAX_STATES && TRIAL == NUM_TRIALS - 1) {
        trial++;
        counting = false;
        document.getElementById('experiment').hidden = true;
        document.getElementById('test').hidden = false;
        document.getElementById('slideshow').src = ``;
    }

    //End of final trial
    if (state == MAX_STATES && TRIAL == NUM_TRIALS) {
        counting = false;
        document.getElementById('instructions').hidden = true;
        document.getElementById('test').hidden = false;
        document.getElementById('experiment').hidden = true;
        document.getElementsByClassName('img').src = `static/images/m/{{TRIAL2[i][TRIAL]}`;
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

function submitForm(images) {
    const form = document.forms['submit_trial'];
    var num_correct = 0;    
    for (var i = 0; i < images.length; i++) {
        num_correct += (CORRECT[i].filter(x => images.includes(x))).length;
    }
    var num_incorrect = 5 - num_correct;
    form.correct.value = num_correct;
    form.incorrect.value = num_incorrect;
    form.rate.value = num_incorrect / num_correct;
}

function checkBoxes(event) {
    var inputs = document.getElementsByTagName("input");
    var selectedImages = [];
    var count = 0;
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type == "checkbox" && inputs[i].checked == true) {
            count++;
        }
    }
    console.log(count);
    if (count <= 5) {
        document.getElementById('warning').hidden = true;
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].type == "checkbox" && inputs[i].checked == true) {
                selectedImages.push(inputs[i].id);
            }
        }
        submitForm(selectedImages);
        displayInstructions();
    }
    else {
        document.getElementById('warning').hidden = false;
        event.preventDefault();
    }
}

const form_ele = document.getElementById('submit_trial');
form_ele.addEventListener('submit', checkBoxes);
const begin_ele = document.getElementById('begin_button');
begin_ele.addEventListener('click', beginExperiment);