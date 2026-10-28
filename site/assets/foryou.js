// "Built for you" pages: a Spotlight-style prompt, an animated orb while the AI
// chooses pieces, then the page assembles from approved sections with their sources.
(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const wait = (ms) => new Promise((r) => setTimeout(r, reduced ? 0 : ms));

  const LANG = document.documentElement.lang.startsWith('es') ? 'es' : 'en';
  const T = {
    en: {
      locale: 'en-US', contact: '/en/contact/', built: 'Built for you', onPage: 'On this page',
      aiNote: 'The headline and these two lines were written by AI. Everything below is taken word for word from our site, with its source under each part.',
      copy: 'Copy link to this page', copied: 'Link copied', send: 'Send it to a colleague', again: 'Build another page',
      source: 'Source', sources: 'Sources', sourcesLead: 'Everything on this page comes from these pages of our site.', nextEyebrow: 'Your next step',
      nextTitle: 'Talk it through with the people who built these systems.', book: 'Book a 30-minute call',
      mailSubject: 'A page Alma Intel built for us', found: (n) => `Found ${n} parts of our work for you.`,
      reading: 'Reading what you need…', choosing: 'Choosing the parts of our work that fit…', putting: 'Putting your page together…',
      hints: ['Looking at our construction work…', 'Looking at our e-commerce work…', 'Looking at our finance work…',
        'Looking at our CRM work…', 'Looking at our hospitality work…', 'Checking how engagements work…'],
      limitVisitor: 'You have built several pages in the last hour. Try again a little later, or book a call and ask us directly.',
      limitDaily: 'We have reached the limit of pages we build today. Try again tomorrow, or book a call and ask us directly.',
      failed: 'We could not build your page right now. Try again in a moment.'
    },
    es: {
      locale: 'es-ES', contact: '/es/contacto/', built: 'Hecha para ti', onPage: 'En esta página',
      aiNote: 'El titular y estas dos líneas los ha escrito una IA. Todo lo demás está tomado literalmente de nuestra web, con su fuente debajo de cada parte.',
      copy: 'Copiar el enlace a esta página', copied: 'Enlace copiado', send: 'Enviársela a un compañero', again: 'Crear otra página',
      source: 'Fuente', sources: 'Fuentes', sourcesLead: 'Todo lo que hay en esta página sale de estas páginas de nuestra web.', nextEyebrow: 'Tu siguiente paso',
      nextTitle: 'Háblalo con las personas que construyeron estos sistemas.', book: 'Reserva una llamada de 30 minutos',
      mailSubject: 'Una página que Alma Intel ha preparado para nosotros', found: (n) => `Hemos encontrado ${n} partes de nuestro trabajo para ti.`,
      reading: 'Leyendo lo que necesitas…', choosing: 'Eligiendo las partes de nuestro trabajo que encajan…', putting: 'Montando tu página…',
      hints: ['Mirando nuestro trabajo en construcción…', 'Mirando nuestro trabajo en e-commerce…', 'Mirando nuestro trabajo en finanzas…',
        'Mirando nuestro trabajo con CRM…', 'Mirando nuestro trabajo en hostelería…', 'Revisando cómo trabajamos con los clientes…'],
      limitVisitor: 'Has creado varias páginas en la última hora. Vuelve a intentarlo un poco más tarde, o reserva una llamada y pregúntanos directamente.',
      limitDaily: 'Hemos llegado al límite de páginas que creamos hoy. Vuelve a intentarlo mañana, o reserva una llamada y pregúntanos directamente.',
      failed: 'No hemos podido crear tu página ahora mismo. Vuelve a intentarlo en un momento.'
    }
  }[LANG];

  const intro = $('[data-fy-intro]');
  const out = $('[data-fy-out]');
  const overlay = $('[data-fy-overlay]');
  const form = $('[data-fy-form]', overlay);
  const input = $('input', form);
  const status = $('[data-fy-status]', overlay);
  const asked = $('[data-fy-asked]', overlay);
  const errorBox = $('[data-fy-error]', overlay);
  const mic = $('.ask-mic', overlay);
  let lastFocus = null;
  let piecesP = null;
  const pieces = () => (piecesP ||= fetch(`/assets/pieces${LANG === 'es' ? '-es' : ''}.json`).then((r) => r.json()));

  /* ---------------- Spotlight ---------------- */
  function open(prefill = '') {
    lastFocus = document.activeElement;
    overlay.hidden = false;
    overlay.dataset.state = 'ask';
    errorBox.textContent = '';
    void overlay.offsetWidth; // apply the closed state first so the fade-in runs
    overlay.classList.add('is-open');
    input.value = prefill;
    input.focus();
    document.body.style.overflow = 'hidden';
    pieces();
  }
  function close() {
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
    setTimeout(() => { overlay.hidden = true; }, reduced ? 0 : 250);
    lastFocus?.focus();
  }
  document.querySelectorAll('[data-fy-open]').forEach((b) => b.addEventListener('click', () => open(b.dataset.fyOpen || '')));
  $('[data-fy-close]', overlay).addEventListener('click', close);
  overlay.addEventListener('click', (e) => { if (e.target === overlay && overlay.dataset.state === 'ask') close(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !overlay.hidden && overlay.dataset.state === 'ask') close();
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); overlay.hidden ? open() : close(); }
  });
  overlay.querySelectorAll('.fy-examples button').forEach((b) => b.addEventListener('click', () => { input.value = b.textContent; form.requestSubmit(); }));

  /* ---------------- Orb (rotating point sphere with an orbit ring) ---------------- */
  const canvas = $('canvas', overlay);
  const ctx = canvas.getContext('2d');
  let raf = 0;
  function orb() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const size = canvas.clientWidth;
    canvas.width = canvas.height = size * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const N = 900, pts = [];
    for (let i = 0; i < N; i++) {
      const y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), t = i * 2.39996;
      pts.push([Math.cos(t) * r, y, Math.sin(t) * r]);
    }
    const ring = Array.from({ length: 160 }, (_, i) => i / 160 * Math.PI * 2);
    const R = size * 0.3, c = size / 2;
    let a = 0;
    const frame = () => {
      a += 0.012;
      ctx.clearRect(0, 0, size, size);
      const ca = Math.cos(a), sa = Math.sin(a), cb = Math.cos(0.45), sb = Math.sin(0.45);
      for (const [x, y, z] of pts) {
        const wob = 1 + 0.06 * Math.sin(a * 3 + y * 6);
        const x1 = (x * ca - z * sa) * wob, z1 = (x * sa + z * ca) * wob;
        const y1 = y * cb - z1 * sb, z2 = y * sb + z1 * cb;
        const d = (z2 + 1.2) / 2.2;
        ctx.fillStyle = z2 > 0.1 ? `rgba(107,115,238,${0.45 + d * 0.55})` : `rgba(38,34,77,${0.3 + d * 0.6})`;
        const s = 2.4 * d + 0.7;
        ctx.fillRect(c + x1 * R - s / 2, c + y1 * R - s / 2, s, s);
      }
      for (const t of ring) {
        const x = Math.cos(t + a * 1.6) * 1.45, z = Math.sin(t + a * 1.6) * 1.45;
        const y1 = -z * Math.sin(1.15), z2 = z * Math.cos(1.15);
        const d = (z2 + 1.5) / 3;
        ctx.fillStyle = `rgba(107,115,238,${0.3 + d * 0.65})`;
        ctx.fillRect(c + x * R, c + y1 * R * 0.95 + R * 0.05, 2, 2);
      }
      raf = reduced ? 0 : requestAnimationFrame(frame);
    };
    frame();
  }

  /* ---------------- Status messages while building ---------------- */
  const HINTS = [
    /construct|builder|contractor|job site|obra|constru/i,
    /amazon|shopify|ecommerce|e-commerce|orders?|pedidos/i,
    /quickbooks|xero|invoice|accounting|books|finance|factur|contab/i,
    /crm|hubspot|salesforce|monday|contacts?|leads?|contactos/i,
    /hotel|hospitality|booking|rooms?|reservas|hostel/i,
    /cost|price|how much|budget|precio|cuánto|cuesta/i,
  ];
  async function narrate(q, done) {
    const lines = [T.reading];
    HINTS.forEach((re, i) => { if (re.test(q)) lines.push(T.hints[i]); });
    lines.push(T.choosing, T.putting);
    for (const line of lines) {
      if (done()) return;
      status.textContent = line;
      await wait(1100);
    }
  }

  /* ---------------- Build ---------------- */
  async function build(q) {
    overlay.dataset.state = 'building';
    asked.textContent = `“${q}”`;
    orb();
    let finished = false;
    narrate(q, () => finished);
    const started = Date.now();
    let plan;
    try {
      const res = await fetch('/api/page', {
        method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ q, lang: LANG }), signal: AbortSignal.timeout(30000)
      });
      plan = await res.json();
      if (!res.ok) throw plan;
    } catch (err) {
      finished = true;
      cancelAnimationFrame(raf);
      overlay.dataset.state = 'ask';
      errorBox.textContent = err && err.error === 'limit' ? (err.scope === 'visitor' ? T.limitVisitor : T.limitDaily) : T.failed;
      return;
    }
    await wait(Math.max(0, 2400 - (Date.now() - started)));
    finished = true;
    status.textContent = T.found(plan.pieces.length);
    await wait(700);
    cancelAnimationFrame(raf);
    history.pushState(null, '', `?p=${plan.id}`);
    close();
    await render(plan, true);
  }
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (q.length < 3) { input.focus(); return; }
    build(q);
  });

  // Tabs inside a rendered "how we work" piece (site.js only wires the ones present on load)
  function wireStages(root) {
    root.querySelectorAll('[data-stage-explorer]').forEach((ex) => {
      const tabs = [...ex.querySelectorAll('[data-stage-choice]')];
      const panels = [...ex.querySelectorAll('[data-stage-panel]')];
      tabs.forEach((tab, i) => {
        tab.disabled = false;
        tab.addEventListener('click', () => {
          tabs.forEach((t, j) => t.setAttribute('aria-selected', String(j === i)));
          panels.forEach((p, j) => { p.hidden = j !== i; });
        });
      });
    });
  }

  async function render(plan, animate) {
    const lib = await pieces();
    const sources = [];
    // Consecutive notes or lab items share one grid
    const groups = [];
    plan.pieces.forEach((id) => {
      const p = lib[id];
      if (!p) return;
      const last = groups[groups.length - 1];
      if (p.group && last && last.group === p.group) last.items.push([id, p]);
      else groups.push({ group: p.group, items: [[id, p]] });
    });
    const toc = groups.map((g, i) => `<a href="#fy-${i + 1}"><span>${String(i + 1).padStart(2, '0')}</span>${esc(g.items[0][1].label)}</a>`).join('');
    let html = `<section class="fy-head wrap"><p class="eyebrow">${T.built} · ${new Date(plan.created || Date.now()).toLocaleDateString(T.locale, { month: 'long', day: 'numeric', year: 'numeric' })}</p>
      <h1>${esc(plan.headline)}</h1><p class="lead">${esc(plan.intro)}</p>
      <p class="fy-ai-note"><span class="fy-dot" aria-hidden="true"></span>${T.aiNote}</p>
      <nav class="fy-toc" aria-label="${T.onPage}"><b>${T.onPage}</b>${toc}</nav>
      <div class="fy-share"><button type="button" class="button secondary" data-fy-copy>${T.copy}</button>
      <a class="link-arrow" data-fy-mail href="#">${T.send}<span class="arrow" aria-hidden="true">↗</span></a>
      <button type="button" class="link-arrow fy-again" data-fy-open>${T.again}<span class="arrow" aria-hidden="true">↗</span></button></div></section>`;
    groups.forEach((g, i) => {
      const src = [...new Map(g.items.map(([, p]) => [p.url, p])).values()];
      src.forEach((p) => sources.push(p));
      const body = g.group
        ? `<section class="section wrap"><div class="${g.group === 'notes' ? 'note-cards' : 'lab-list'} fy-grid">${g.items.map(([, p]) => p.html).join('')}</div></section>`
        : g.items.map(([, p]) => p.html).join('');
      html += `<div class="fy-piece" id="fy-${i + 1}">${body}<p class="fy-source wrap">${T.source}: ${src.map((p) => `<a href="${p.url}">${esc(p.source)} · almaintel.ai${p.url}</a>`).join(' · ')}</p></div>`;
    });
    const uniq = [...new Map(sources.map((p) => [p.url, p])).values()];
    html += `<section class="fy-sources"><div class="wrap fy-sources-grid"><div><p class="eyebrow">${T.sources}</p><p class="fy-sources-lead">${T.sourcesLead}</p></div>
      <ol>${uniq.map((p, i) => `<li><a href="${p.url}"><span class="n">${String(i + 1).padStart(2, '0')}</span><b>${esc(p.source)}</b><span class="u">almaintel.ai${p.url}</span><span class="arrow" aria-hidden="true">↗</span></a></li>`).join('')}</ol></div></section>
      <section class="closing"><div class="wrap closing-inner"><div><p class="eyebrow">${T.nextEyebrow}</p><h2>${T.nextTitle}</h2></div>
      <a class="button" href="${T.contact}?proceso=foryou-${esc(plan.id)}">${T.book}<span class="arrow" aria-hidden="true">↗</span></a></div></section>`;

    intro.hidden = true;
    out.innerHTML = html;
    out.hidden = false;
    // Each source line sits inside the last section of its part, on the same background
    out.querySelectorAll('.fy-piece').forEach((piece) => {
      const src = piece.querySelector(':scope > .fy-source');
      const host = src && src.previousElementSibling;
      if (!host || host.tagName !== 'SECTION') return;
      if (host.classList.contains('wrap')) src.classList.remove('wrap');
      host.appendChild(src);
    });
    wireStages(out);
    // The EN / ES switch keeps this page
    document.querySelectorAll('.language a').forEach((a) => { a.href = `${new URL(a.href).pathname}?p=${encodeURIComponent(plan.id)}`; });
    window.scrollTo({ top: 0, behavior: 'instant' });
    out.querySelectorAll('[data-fy-open]').forEach((b) => b.addEventListener('click', () => open()));
    const link = location.href;
    $('[data-fy-mail]', out).href = `mailto:?subject=${encodeURIComponent(T.mailSubject)}&body=${encodeURIComponent(plan.headline + '\n\n' + link)}`;
    $('[data-fy-copy]', out).addEventListener('click', async (ev) => {
      try { await navigator.clipboard.writeText(link); ev.target.textContent = T.copied; } catch { ev.target.textContent = link; }
    });
    if (animate && !reduced) {
      const parts = [...out.children];
      parts.forEach((el) => el.classList.add('fy-enter'));
      for (const el of parts) { el.classList.add('is-in'); await wait(260); }
    }
  }

  /* ---------------- Arriving with a shared link or a question from the home page ---------------- */
  const params = new URLSearchParams(location.search);
  const shared = params.get('p');
  const fromHome = params.get('ask');
  if (shared) {
    fetch(`/api/page?id=${encodeURIComponent(shared)}`).then((r) => (r.ok ? r.json() : null)).then((plan) => plan && render(plan, false));
  } else if (fromHome && fromHome.trim().length >= 3) {
    history.replaceState(null, '', location.pathname);
    open(fromHome.trim());
    build(fromHome.trim());
  }
  window.addEventListener('popstate', () => { if (!location.search) location.reload(); });

  /* ---------------- Voice ---------------- */
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (Rec && mic) {
    mic.hidden = false;
    const rec = new Rec();
    rec.lang = LANG === 'es' ? 'es-ES' : 'en-US';
    rec.interimResults = true;
    rec.onresult = (e) => {
      input.value = [...e.results].map((r) => r[0].transcript).join('');
      if (e.results[e.results.length - 1].isFinal) form.requestSubmit();
    };
    rec.onend = () => mic.setAttribute('aria-pressed', 'false');
    mic.addEventListener('click', () => {
      if (mic.getAttribute('aria-pressed') === 'true') { rec.stop(); return; }
      mic.setAttribute('aria-pressed', 'true');
      rec.start();
    });
  }
})();
