class Day {
  constructor(day) {
    this.day = day;
    this.data = null;
    this.mountpoint = null;
  }

  loadData(real=true) {
    return new Promise((resolve, reject) => {
      fetch(`/data/${real ? 'real' : 'test'}/day${this.day}.txt`).then(res => {
        if (res.status === 200) {
          res.text().then(text => {
            this.data = text;
            resolve(this.data);
          });
        }
      });
    });
  }

  mount(el) {
    const self = this;
    this.mountpoint = el;

    el.innerHTML = '';
    const header = document.createElement('h1');
    header.innerText = `Day ${this.day}`;
    el.appendChild(header);

    const menu = document.createElement('div');
    menu.setAttribute('class', 'menu');
    const part1Button = document.createElement('button');
    part1Button.innerText = 'Part 1';
    part1Button.addEventListener('click', e => self.part1());
    const part2Button = document.createElement('button');
    part2Button.innerText = 'Part 2';
    part2Button.addEventListener('click', e => self.part2());
    menu.appendChild(part1Button);
    menu.appendChild(part2Button);
    el.appendChild(menu);
  }
}

export default Day;
