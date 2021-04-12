const MAG_MIN = 1, LN_MAG_MIN = Math.log(MAG_MIN);
const MAG_MAX = 50, LN_MAG_MAX = Math.log(MAG_MAX);
const ASPECT_RATIO = 4/3;  // width/height of the experimentContainer
const HALF_WIDTH = 0.5 * ASPECT_RATIO;
const HALF_HEIGHT = 0.5;
const MIN_CIRCLE_GAP = 0.0105;  // proportion of experimentContainer height
const SPACE_DEBOUNCE_DELAY = 500;  // ms
const AUTO_STOP_TIMEOUT = 10*1000;  // ms

const isExperimentPage = document.documentElement.classList.contains('experiment');

function isInvalid(x, y, radius) {
    // don't be too close to the edge of the screen
    // TODO: just change the inital random bounds
    if (x - radius < -(HALF_WIDTH-MIN_CIRCLE_GAP) ||
        x + radius > +(HALF_WIDTH-MIN_CIRCLE_GAP) ||
        y - radius < -(HALF_HEIGHT-MIN_CIRCLE_GAP) ||
        y + radius > +(HALF_HEIGHT-MIN_CIRCLE_GAP)) {
        return true;
    }
    
    // don't be too close to other circles
    for (const c of circles) {
        const d = Math.hypot(x - c.x, y - c.y);
        if (d < radius + c.radius + MIN_CIRCLE_GAP) {
            return true;
        }
    }
    return false;
}

let circles = [];
const experimentContainer = document.getElementById('experiment-container');
if (isExperimentPage) {
    addCircles();
}
function addCircles() {
    for (let n = 0; n < 20; n++) {
        const div = document.createElement('div');
        div.className = 'circle';
        if (n == 0) div.classList.add('blinking');
        
        let count = 0;
        let x, y, radius;
        do {
            x = (Math.random()*2 - 1) * HALF_WIDTH;
            y = (Math.random()*2 - 1) * HALF_HEIGHT;
            radius = 0.016 + 0.15*Math.hypot(x, y);
            if (++count > 1000) break;
        } while (isInvalid(x, y, radius));
        // console.log(count);
        
        div.style.left = `${(x/ASPECT_RATIO + 0.5)*100}%`;
        div.style.top = `${(y + 0.5)*100}%`;
        div.style.width = `${radius*2/ASPECT_RATIO*100}%`;
        div.style.height = `${radius*2*100}%`;
        
        setCircleColor(div, [50, 0, 0]);
        
        div.addEventListener('click', event => {
            const isStopped = document.body.classList.contains('stopped');
            const isSubmitting = document.body.classList.contains('submitting');
            if (isStopped && !isSubmitting) {
                document.body.classList.add('submitting');
                const form = document.forms['submit-form'];
                form.was_correct.value = n == 0;
                form.blink_index.value = blinkingCircles[0].index;
                form.blink_mag.value = Math.abs(blinkingCircles[0].mag);
                form.correct_x.value = circles[0].x;
                form.correct_y.value = circles[0].y;
                form.picked_x.value = x;
                form.picked_y.value = y;
                form.submit();
            }
        });
        
        circles.push({
            div, x, y, radius,
        });
        experimentContainer.appendChild(div);
    }
}


class BlinkingCircle {
    constructor(div) {
        this.div = div;
        
        if (div.hasAttribute('data-index')) {
            this.index = parseInt(div.getAttribute('data-index'));
        } else {
            this.index = Math.floor(Math.random()*3);
        }
        
        if (div.hasAttribute('data-magnitude')) {
            this.mag = parseFloat(div.getAttribute('data-magnitude'));
        } else {
            this.mag = Math.exp(Math.random()*(LN_MAG_MAX-LN_MAG_MIN) + LN_MAG_MIN);
            if (Math.random() < 0.5) this.mag = -this.mag;
        }
    }
    
    update(t) {
        let lab = [50, 0, 0];
        lab[this.index] += this.mag * Math.sin(2*Math.PI * t/1000 / 0.8);
        setCircleColor(this.div, lab);
    }
    
    setToGray() {
        setCircleColor(this.div, [50, 0, 0]);
    }
}

const blinkingCircles = Array.from(
    document.querySelectorAll('.circle.blinking')
).map(div => new BlinkingCircle(div));

function setCircleColor(div, lab) {
    div.style.backgroundColor = `rgb(${lab2rgb(lab).join(',')})`;
}

let afID;
function doFrame(t) {
    for (let circle of blinkingCircles) {
        circle.update(t);
    }
    
    requestFrame();
}
function requestFrame() {
    afID = requestAnimationFrame(doFrame);
}

function start() {
    document.body.classList.remove('intro');
    requestFrame();
    setTimeout(stop, AUTO_STOP_TIMEOUT);
}
function stop() {
    document.body.classList.add('stopped');
    cancelAnimationFrame(afID);
    for (let circle of blinkingCircles) {
        circle.setToGray();
    }
}

function onSpacePressed() {
    if (document.body.classList.contains('intro')) {
        start();
    } else {
        stop();
    }
}

if (isExperimentPage) {
    let lastSpaceSpess = Date.now();
    document.addEventListener('keyup', event => {
        const now = Date.now();
        if (event.code === 'Space' && now > lastSpaceSpess + SPACE_DEBOUNCE_DELAY) {
            lastSpaceSpess = now;
            onSpacePressed();
        }
    });
}
