// Alma Intel v2: small additions on top of site.js
(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Hero flow: rotate the three examples until the visitor picks one
  document.querySelectorAll('[data-workflow-demo][data-autoplay]').forEach((root) => {
    if (reduced) return;
    const choices = [...root.querySelectorAll('[data-flow-choice]')];
    let i = 0;
    let timer = setInterval(() => {
      i = (i + 1) % choices.length;
      choices[i].click();
    }, 6000);
    const stop = () => { clearInterval(timer); timer = null; };
    choices.forEach((c) => c.addEventListener('pointerdown', stop));
    choices.forEach((c) => c.addEventListener('keydown', stop));
  });

  // Contact: show what the visitor came about (e.g. a lab solution)
  const topic = document.querySelector('[data-booking-topic]');
  if (topic) {
    const key = new URLSearchParams(location.search).get('proceso');
    const topics = {
      'lab-signals': 'You asked about the signal engine from our lab.',
      'lab-assistant': 'You asked about the operations assistant from our lab.',
      'lab-control': 'You asked about the control room from our lab.',
      'lab-opportunities': 'You asked about the opportunity graph from our lab.',
      proyecto: 'You want to discuss a specific project.',
      continuo: 'You want to discuss an ongoing partnership.'
    };
    if (key && key.startsWith('caso-')) topics[key] = 'You came from one of our client cases.';
    if (key && topics[key]) {
      topic.textContent = topics[key] + ' Mention it when you book and we will come prepared.';
      topic.hidden = false;
    }
  }
})();
