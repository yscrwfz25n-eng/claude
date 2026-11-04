/* Aurum Skin · movimiento de las secciones "Aurum": estrella que baja con el scroll, apariciones,
   productos que salen del marco, selector de promos y carrusel. Sin librerías externas. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- Selector de promos ---------- */
  function initPacks(root) {
    $$('[data-au-packs]', root).forEach(box => {
      if (box.dataset.ready) return; box.dataset.ready = '1';
      const btns = $$('[data-pack]', box);
      const q = sel => box.querySelector(sel);
      const set = b => {
        btns.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
        const d = b.dataset;
        q('[data-au-price]').textContent = d.price;
        q('[data-au-old]').innerHTML = d.compare ? `<s>${d.compare}</s> <span class="au-off">-${d.off}%</span>` : '';
        q('[data-au-unit]').textContent = d.unit ? `${d.unit} por unidad` : '';
        q('[data-au-ship]').textContent = d.ship || '';
        const tag = q('[data-au-tag]'); tag.hidden = !d.tag; tag.textContent = d.tag || '';
        const gift = q('[data-au-gift]'); gift.hidden = !d.gift; gift.textContent = d.gift || '';
        q('[data-au-qty]').value = d.qty;
        q('[data-au-cta]').textContent = d.cta;
        /* imagen 1:1 de la promo: en la sección Promos, o en la foto principal de la página de producto */
        const target = q('[data-au-packimg]') || box.closest('.au-pdp')?.querySelector('[data-au-main]');
        if (target && d.img && target.getAttribute('src') !== d.img) {
          target.src = d.img;
          if (!reduce) target.animate([{opacity: .3, transform: 'scale(.97)'}, {opacity: 1, transform: 'none'}], {duration: 450, easing: 'cubic-bezier(.22,.8,.2,1)'});
        }
      };
      btns.forEach(b => b.addEventListener('click', () => set(b)));
      set(btns.find(b => b.dataset.default === 'true') || btns[0]);
    });
  }

  /* ---------- Carrusel: flechas y arrastre ---------- */
  function initRails(root) {
    $$('[data-au-rail]', root).forEach(rail => {
      if (rail.dataset.ready) return; rail.dataset.ready = '1';
      const wrap = rail.closest('.au-sec');
      const step = () => (rail.firstElementChild?.offsetWidth || 240) + 16;
      wrap?.querySelector('[data-au-prev]')?.addEventListener('click', () => rail.scrollBy({left: -step(), behavior: 'smooth'}));
      wrap?.querySelector('[data-au-next]')?.addEventListener('click', () => rail.scrollBy({left: step(), behavior: 'smooth'}));
      if (!matchMedia('(pointer: fine)').matches) return;
      let down = false, sx = 0, sl = 0, moved = false;
      rail.addEventListener('pointerdown', e => { if (e.target.closest('button, input')) return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
      addEventListener('pointerup', () => { down = false; });
      rail.addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true; rail.scrollLeft = sl - dx; });
      rail.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    });
  }

  /* ---------- Apariciones suaves ---------- */
  let io;
  function initReveal(root) {
    if (reduce || !('IntersectionObserver' in window)) return;
    io = io || new IntersectionObserver(entries => entries.forEach(en => {
      en.target.classList.toggle('is-below', !en.isIntersecting && en.boundingClientRect.top > 0);
    }), {rootMargin: '0px 0px -8% 0px'});
    $$('.au-reveal', root).forEach(el => io.observe(el));
  }

  /* ---------- Productos que salen del marco: se mueven con el scroll ---------- */
  function popLoop() {
    const pops = $$('.au-pop');
    if (reduce || !pops.length) return;
    const tick = () => {
      pops.forEach(p => {
        const r = p.parentElement.getBoundingClientRect();
        const k = Math.max(-1, Math.min(1, (innerHeight / 2 - (r.top + r.height / 2)) / innerHeight));
        const base = +(p.dataset.rotate || 0);
        p.style.transform = `translateY(${k * 40}px) rotate(${base + k * 10}deg)`;
      });
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ---------- Estrella de 4 puntas ---------- */
  function starLoop() {
    const star = document.querySelector('.au-star');
    if (!star || reduce) return;
    const svg = star.innerHTML.replace(/id="au-sg"/g, 'id="au-sg2"').replace(/url\(#au-sg\)/g, 'url(#au-sg2)');
    const pool = Array.from({length: 16}, () => { const d = document.createElement('div'); d.className = 'au-spark'; d.setAttribute('aria-hidden', 'true'); d.innerHTML = svg; document.body.appendChild(d); return d; });
    let pi = 0, cur = 0, last = 0, spin = 0, lastSpark = 0;
    const tick = now => {
      const max = document.documentElement.scrollHeight - innerHeight;
      const target = max > 0 ? scrollY / max : 0;
      cur += (target - cur) * .08;
      const vel = cur - last; last = cur;
      const amp = Math.max(40, Math.min(innerWidth / 2 - 50, 380));
      const x = innerWidth / 2 + Math.sin(cur * Math.PI * 7 - Math.PI / 2) * amp;
      const y = innerHeight * (.1 + cur * .8);
      spin += .4 + Math.abs(vel) * 2600;
      const sc = 1 + Math.min(Math.abs(vel) * 60, .6);
      star.style.transform = `translate(${x}px, ${y}px) rotate(${spin}deg) scale(${sc})`;
      if (Math.abs(vel) > .0004 && now - lastSpark > 45) {
        lastSpark = now;
        const sp = pool[pi++ % pool.length];
        const sx = x + (Math.random() - .5) * 16, sy = y + (Math.random() - .5) * 16, s0 = .5 + Math.random() * .7, rot = Math.random() * 90;
        sp.animate([
          {transform: `translate(${sx}px, ${sy}px) rotate(${rot}deg) scale(${s0})`, opacity: 1},
          {transform: `translate(${sx}px, ${sy - 10 - Math.random() * 20}px) rotate(${rot}deg) scale(.1)`, opacity: 0}
        ], {duration: 900 + Math.random() * 500, easing: 'cubic-bezier(.2,.8,.2,1)'});
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ---------- Galería de producto: miniaturas ---------- */
  function initGallery(root) {
    $$('[data-au-gallery]', root).forEach(g => {
      if (g.dataset.ready) return; g.dataset.ready = '1';
      const main = g.querySelector('[data-au-main]');
      $$('.au-pdp__thumb', g).forEach(t => t.addEventListener('click', () => {
        if (main) main.src = t.dataset.src;
        $$('.au-pdp__thumb', g).forEach(x => x.removeAttribute('aria-current')); t.setAttribute('aria-current', 'true');
      }));
    });
  }

  function init(root = document) { initPacks(root); initRails(root); initReveal(root); initGallery(root); }
  document.addEventListener('DOMContentLoaded', () => { init(); popLoop(); starLoop(); });
  /* En el editor de temas, las secciones se recargan solas: se vuelven a iniciar */
  document.addEventListener('shopify:section:load', e => init(e.target));
})();
