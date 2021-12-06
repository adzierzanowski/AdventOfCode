import Day from './day.js';


class Day1 extends Day {
  constructor() {
    super('01');
  }

  part1() {
    this.loadData().then(data => {
      this.data = this.data.split('\n').map(x => parseInt(x));


      const canvas = document.createElement('canvas');
      canvas.setAttribute('width', 640);
      canvas.setAttribute('height', 480);

      this.mountpoint.appendChild(canvas);

      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#283848';
      ctx.rect(0, 0, 640, 480);
      ctx.fill()

      ctx.fillStyle = '#ff0';
      ctx.strokeStyle = '#ff0';
      ctx.beginPath();
      ctx.ellipse(500, 100, 50, 20, 0, 0, 2* Math.PI);
      ctx.fill();
      ctx.beginPath();
      ctx.rect(480, 70, 40, 20);
      ctx.fill();

      let i = 0;
      let dst = 150;
      let pos = 150;
      setInterval(() => {
        if (pos == dst) {
          dst = this.data[Math.floor(i/20)];
        } else {
          pos < dst ? pos++ : pos--;
        }
        i++;
        ctx.beginPath();
        ctx.moveTo(500, 150+pos/10);
        ctx.lineTo(500, 151+pos/10);
        ctx.stroke();
        const chunk = ctx.getImageData(0, 150, 640, 480-150);
        ctx.putImageData(chunk, -1, 150);
      }, 10);

      console.log(this.data);
    });
  }


  part2() {
    console.log('part2');
  }
}

export default Day1;
