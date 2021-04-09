var scale = 50;
var rand = scale * (Math.random()*2 - 1)
var lab = Math.random() < 0.5 ?
    [50, rand, 0.0] :
    [50, 0.0, rand];

// var rgb = [194, 79, 121];
// lab = rgb2lab(rgb);
// lab[1] *= -1;

var MAG_MIN = 1, LN_MAG_MIN = Math.log(MAG_MIN);
var MAG_MAX = 50, LN_MAG_MAX = Math.log(MAG_MAX);
var HALF_WIDTH = window.innerWidth / 2;
var HALF_HEIGHT = window.innerHeight / 2;
var MIN_CIRCLE_GAP = 10;  // pixels

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
    for (var c of circles) {
        var d = Math.hypot(x - c.x, y - c.y);
        if (d < radius + c.radius + MIN_CIRCLE_GAP) {
            return true;
        }
    }
    return false;
}

var circles = [];
for (var n = 0; n < 20; n++) {
    var div = document.createElement('div');
    div.className = 'circle';
    
    var count = 0;
    do {
        var x = (Math.random()*2 - 1) * HALF_WIDTH;
        var y = (Math.random()*2 - 1) * HALF_HEIGHT;
        var radius = 15 + 0.15*Math.hypot(x, y);
        if (++count > 1000) break;
    } while (isInvalid(x, y, radius));
    console.log(count);
    
    div.style.left = `${x + HALF_WIDTH}px`;
    div.style.top = `${y + HALF_HEIGHT}px`;
    div.style.width = div.style.height = `${radius*2}px`;
    
    var index = Math.floor(Math.random()*3);
    var mag = Math.exp(Math.random()*(LN_MAG_MAX-LN_MAG_MIN) + LN_MAG_MIN);
    if (Math.random() < 0.5) mag = -mag;
    
    setCircleColor([50, 0, 0], div);
    
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

var circle = document.querySelector('.circle');
var index = Math.floor(Math.random()*3);
var mag = Math.exp(Math.random()*(LN_MAG_MAX-LN_MAG_MIN) + LN_MAG_MIN);
if (Math.random() < 0.5) mag = -mag;
console.log(mag);

function setCircleColor(lab, div=circle) {
    div.style.backgroundColor = `rgb(${lab2rgb(lab).join(',')})`;
}

var DELAY = 0;//1000 + 5000*Math.random();
function doFrame(t) {
    var at = Math.max(t, DELAY) - DELAY
    
    var lab = [50, 0, 0];
    lab[index] += mag*Math.sin(2*Math.PI * at/1000 / 0.8);
    setCircleColor(lab);
    
    afID = requestAnimationFrame(doFrame);
}

var afID = requestAnimationFrame(doFrame);

document.addEventListener('keyup', event => {
    if (event.code === 'Space') {
        document.body.classList.add('stopped');
        cancelAnimationFrame(afID);
        setCircleColor([50, 0, 0]);
    }
});
