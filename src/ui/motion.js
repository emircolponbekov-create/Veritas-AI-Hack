/* Trusted local UI runtime. No polling, network calls, Streamlit events or timers. */
(() => {
  const state = window.__waterLab || { seen: new Set(), values: new Map() };
  state.cleanup?.();
  window.__waterLab = state;
  const abort = new AbortController();
  const opts = { signal: abort.signal };
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const reduced = () => reduce.matches || document.documentElement.classList.contains('lab-motion-off');
  const mouse = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 761px)');
  let hero = null, inView = false, frame = 0, pending = [0, 0];
  const sync = () => {
    if (!hero) return;
    const active = inView && !document.hidden && !reduced();
    hero.classList.toggle('scene-paused', !active);
    hero.dataset.motion = active ? 'running' : 'paused';
    if (!active) {
      cancelAnimationFrame(frame); frame = 0;
      hero.style.setProperty('--px', '0px'); hero.style.setProperty('--py', '0px');
    }
  };
  const visibility = new IntersectionObserver(entries => {
    for (const e of entries) if (e.target === hero) { inView = e.isIntersecting; sync(); }
  }, { threshold: .01 });
  const reveal = new IntersectionObserver(entries => {
    for (const e of entries) if (e.isIntersecting) {
      e.target.classList.add('is-revealed');
      state.seen.add(e.target.dataset.revealKey);
      reveal.unobserve(e.target);
    }
  }, { threshold: .08 });
  const move = e => {
    if (!mouse.matches || reduced() || !inView || document.hidden) return;
    const b = hero.getBoundingClientRect();
    pending = [((e.clientX - b.left) / b.width - .5) * 8, ((e.clientY - b.top) / b.height - .5) * 5];
    if (!frame) frame = requestAnimationFrame(() => {
      hero.style.setProperty('--px', pending[0] + 'px');
      hero.style.setProperty('--py', pending[1] + 'px'); frame = 0;
    });
  };
  const reset = () => {
    cancelAnimationFrame(frame); frame = 0;
    hero?.style.setProperty('--px', '0px'); hero?.style.setProperty('--py', '0px');
  };
  const visited = new WeakSet();
  const bind = () => {
    const next = document.querySelector('.lab-hero');
    if (next && next !== hero) {
      if (hero) visibility.unobserve(hero);
      hero = next; visibility.observe(hero);
      hero.addEventListener('pointermove', move, opts);
      hero.addEventListener('pointerleave', reset, opts);
    }
    const vector = hero?.querySelector('.scene-vector[data-vector]');
    if (vector && !vector.firstElementChild) {
      const svg = new DOMParser().parseFromString(atob(vector.dataset.vector), 'image/svg+xml').documentElement;
      if (svg.localName === 'svg') vector.appendChild(document.importNode(svg, true));
    }
    const nodes = document.querySelectorAll('[data-testid="stMetric"], .lab-note, .section-heading, [data-testid="stVegaLiteChart"]');
    nodes.forEach((node, i) => {
      const label = node.querySelector('[data-testid="stMetricLabel"]')?.textContent;
      if (label) {
        const value = node.querySelector('[data-testid="stMetricValue"]')?.textContent;
        if (state.values.has(label) && state.values.get(label) !== value) {
          node.classList.add('month-updated');
          node.addEventListener('animationend', () => node.classList.remove('month-updated'), { once: true, ...opts });
        }
        state.values.set(label, value);
        node.dataset.temperature = /Intake/.test(label) ? 'intake' : /Discharge/.test(label) ? 'discharge' : 'other';
      }
      if (visited.has(node)) return;
      visited.add(node);
      const key = label || node.id || `${node.dataset.testid || node.className}-${i}`;
      node.dataset.revealKey = key;
      if (state.seen.has(key) || reduced()) node.classList.add('is-revealed');
      else { node.classList.add('reveal-ready'); reveal.observe(node); }
    });
    sync();
  };
  // React may hydrate later. Observe added nodes without changing their content.
  const mutation = new MutationObserver(records => {
    if (records.some(r => r.type === 'childList')) bind();
  });
  mutation.observe(document.querySelector('[data-testid="stAppViewContainer"]') || document.body,
                   { childList: true, subtree: true });
  document.addEventListener('visibilitychange', sync, opts);
  reduce.addEventListener('change', () => { reset(); bind(); sync(); }, opts);
  mouse.addEventListener('change', reset, opts);
  state.cleanup = () => { abort.abort(); mutation.disconnect(); visibility.disconnect(); reveal.disconnect(); cancelAnimationFrame(frame); };
  bind();
})();
