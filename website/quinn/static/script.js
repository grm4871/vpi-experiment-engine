const MAG_MIN = 1, LN_MAG_MIN = Math.log(MAG_MIN);
const MAG_MAX = 50, LN_MAG_MAX = Math.log(MAG_MAX);
const HALF_WIDTH = window.innerWidth / 2;
const HALF_HEIGHT = window.innerHeight / 2;
const MIN_CIRCLE_GAP = 10;  // pixels

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
if (document.documentElement.classList.contains('experiment')) {
    addCircles();
}
function addCircles() {
    for (let n = 0; n < 20; n++) {
        const div = document.createElement('div');
        div.className = 'circle';
        if (n == 0) div.classList.add('blinking');
        
        let count = 0;
        do {
            const x = (Math.random()*2 - 1) * HALF_WIDTH;
            const y = (Math.random()*2 - 1) * HALF_HEIGHT;
            const radius = 15 + 0.15*Math.hypot(x, y);
            if (++count > 1000) break;
        } while (isInvalid(x, y, radius));
        // console.log(count);
        
        div.style.left = `${x + HALF_WIDTH}px`;
        div.style.top = `${y + HALF_HEIGHT}px`;
        div.style.width = div.style.height = `${radius*2}px`;
        
        setCircleColor(div, [50, 0, 0]);
        
        div.addEventListener('click', event => {
            if (document.body.classList.contains('stopped')) {
                location.reload();
            }
        });
        
        circles.push({
            div, x, y, radius,
        });
        document.body.appendChild(div);
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

function doFrame(t) {
    for (let circle of blinkingCircles) {
        circle.update(t);
    }
    
    afID = requestAnimationFrame(doFrame);
}

let afID = requestAnimationFrame(doFrame);

document.addEventListener('keyup', event => {
    if (event.code === 'Space') {
        document.body.classList.add('stopped');
        cancelAnimationFrame(afID);
        for (let circle of blinkingCircles) {
            circle.setToGray();
        }
    }
});
