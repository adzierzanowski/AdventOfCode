import Day1 from './day1.js';

const days = [new Day1()];

const loadDay = (day) => {
  const content = document.querySelector('#content');
  days[day].mount(content);
};

const initMenu = () => {
  const menu = document.querySelector('#menu');

  for (let i = 0; i < 25; i++) {
    const link = document.createElement('a');
    link.innerText = `Day ${i+1}`;
    link.addEventListener('click', e => {loadDay(i)});
    menu.appendChild(link);
  }
};

initMenu();
