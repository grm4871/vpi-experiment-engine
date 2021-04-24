const TIMER = 5;
const MAX_STATES = 10;
const NUM_TRIALS = 1;

var trial = 0;
var timer = TIMER;
var state = 0;
var img = 0;
var counting = true;

// countDown(counting)

function beginExperiment() {
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
    }

    //End of final trial
    if (state == MAX_STATES && TRIAL == NUM_TRIALS) {
        counting = false;
        document.getElementById('test').hidden = false;
        document.getElementById('experiment').hidden = true;
        document.getElementById('cont_button').value = "Submit";
    }

    else if (state == 0) {
        document.getElementById('timer').textContent = `Your experiment will begin in ${timer}.`
    }
    else if(state >= 1) {
        document.getElementById('timer').textContent = `Time left: ${timer}`
    }
    if (counting) {
        window.setTimeout(countDown, 1000);
    }
}

var lastImg = 0;
function displayImage(img) {
    document.getElementById('slideshow'+lastImg).hidden = true;
    document.getElementById('slideshow'+img).hidden = false;
    lastImg = img;
}

function submitForm(images) {
    const form = document.forms['submit_trial'];
    var num_correct = 0;    
    for (var i = 0; i < CORRECT.length; i++) {
        num_correct += (CORRECT[i].filter(x => images.includes(x))).length;
    }
    var num_incorrect = 5 - num_correct;
    form.correct.value = num_correct;
    form.incorrect.value = num_incorrect;
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
    }
    else {
        document.getElementById('warning').hidden = false;
        event.preventDefault();
        alert("Please select no more than 5 images.");
    }
}

const form_ele = document.getElementById('submit_trial');
if (form_ele !== null) {
    form_ele.addEventListener('submit', checkBoxes);
}

const begin_ele = document.getElementById('begin-form');
if (begin_ele !== null) {
    begin_ele.addEventListener('click', beginExperiment);
}




// code for waiting until all the images have loaded
var loadingMsg = document.getElementById('timer');

var lazyImgs = document.querySelectorAll('img[data-src]');
var numLoadedImgs = 0;
var errorred = false;
function registerLazyImg(img) {
    function imgLoaded() {
        console.log('imgLoaded:', img.id);
        img.removeEventListener('load', imgLoaded);
        numLoadedImgs++;
        if (numLoadedImgs === lazyImgs.length) {
            console.log('all loaded!');
            countDown();
        } else if (!errorred) {
            var p = numLoadedImgs / lazyImgs.length;
            loadingMsg.textContent = `(loading images: ${Math.floor(p*100)}%)`;
        }
    }
    function imgError() {
        console.log('imgError:', img.id);
        img.removeEventListener('error', imgError);
        errorred = true;
        loadingMsg.textContent = "(couldn't load all images; try reloading the page)";
    }
    img.addEventListener('load', imgLoaded);
    img.addEventListener('error', imgError);
    img.src = img.getAttribute('data-src');
}
for (let i = 0; i < lazyImgs.length; i++) {
    registerLazyImg(lazyImgs[i]);
}
