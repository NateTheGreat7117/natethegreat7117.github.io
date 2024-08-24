const canvas = document.getElementById("circle");
const ctx = canvas.getContext("2d");

width = canvas.width;
height = canvas.height;

let stopped = false;
let hover = false;

canvas.addEventListener('click', function() {
    if (stopped) {
        stopped = false;
    }else {
        stopped = true;
    }
});

canvas.addEventListener('mouseover', function() {
    if (!stopped) {
        hover = true;
    }
});

canvas.addEventListener('mouseout', function() {
    hover = false;
})

function smoothSamples(samples, windowSize = 5) {
    const smoothed = [];
    for (let i = 0; i < samples.length; i++) {
        let sum = 0;
        let count = 0;
        for (let j = -windowSize; j <= windowSize; j++) {
            if (i + j >= 0 && i + j < samples.length) {
                sum += samples[i + j];
                count++;
            }
        }
        smoothed.push(sum / count);
    }
    return smoothed;
}

function logScale(value, base = 10) {
    // Apply logarithmic scaling to amplify louder noises and reduce quieter ones
    return Math.log(value + 1) / Math.log(base);
}

function drawSlash() {
    ctx.beginPath();
    ctx.moveTo(0.1*width, 0.1*height);
    ctx.lineTo(0.9*width, 0.9*height);

    ctx.stroke();
}

function plotWaveCircle(samples) {
    let gradient = ctx.createLinearGradient(0, 0, width, height);
    if (stopped) {
        gradient.addColorStop(0, 'blue');
        gradient.addColorStop(1, 'purple');
        drawSlash();
    } else {
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(centerX, centerY) - 10;

        // Clear the canvas
        ctx.clearRect(0, 0, width, height);

        if (hover) {
            gradient.addColorStop(0, 'rgba(0, 0, 255, 0.5)');
            gradient.addColorStop(1, 'rgba(128, 0, 128, 0.5)');
            drawSlash();
        } else {
            gradient.addColorStop(0, 'blue');
            gradient.addColorStop(1, 'purple');
        }

        ctx.lineJoin = 'round';

        // Draw the circle graph
        ctx.beginPath();
        samples.forEach((sample, index) => {
            // Apply logarithmic scaling
            sample = logScale(Math.abs(sample), base=2);

            // Calculate the angle for each sample
            const angle = (index / samples.length) * 2 * Math.PI;
            
            // Map the sample value to the circle radius
            const r = radius * (1 + sample * 8); // Scale and offset the sample

            // Calculate the x and y coordinates
            const x = centerX + r * Math.cos(angle);
            const y = centerY + r * Math.sin(angle);

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.closePath();

        // Stroke the circle graph
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 1;
        ctx.stroke();
    }
}

function draw() {
    wav = smoothSamples(wav);
    plotWaveCircle(wav);
    requestAnimationFrame(draw);
}

draw();