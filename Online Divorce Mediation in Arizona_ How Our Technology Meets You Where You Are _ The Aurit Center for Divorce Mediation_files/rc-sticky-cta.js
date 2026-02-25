(function () {
  function onReady(fn){ if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  onReady(function () {
    var topEl = document.getElementById('rc-sticky-cta-top');
    var botEl = document.getElementById('rc-sticky-cta-bottom');
    if (!topEl) return;

    var cloneSelector = topEl.getAttribute('data-clone-selector') || (window.RCStickyCTA && RCStickyCTA.cloneSelector) || '';
    var passive = { passive:true }, cloned = false;

    function isStickyOrFixed(el){
      if (!el) return false;
      var cs = getComputedStyle(el);
      return cs.position === 'sticky' || cs.position === 'fixed' || /\b(sticky|is-sticky|is-fixed|header-stuck)\b/i.test(el.className||'');
    }
    function padForFixed(){
      document.documentElement.style.setProperty('--rc-cta-top', (topEl.offsetHeight||0) + 'px');
      document.body.classList.add('has-rc-fixed-top');
    }
    function clearPad(){
      document.documentElement.style.removeProperty('--rc-cta-top');
      document.body.classList.remove('has-rc-fixed-top');
    }
    function appendIntoHeader(h){
      if (!h || h.contains(topEl)) return;
      h.appendChild(topEl);
      topEl.classList.add('in-header'); topEl.classList.remove('is-fixed-top');
      clearPad();
      if (botEl) document.body.classList.add('has-rc-fixed-bottom');
    }
    function pinToTop(){
      if (!document.body.contains(topEl)) document.body.appendChild(topEl);
      topEl.classList.add('is-fixed-top'); topEl.classList.remove('in-header');
      padForFixed();
      try { new ResizeObserver(padForFixed).observe(topEl); } catch(e){ window.addEventListener('resize', padForFixed); }
      if (botEl) document.body.classList.add('has-rc-fixed-bottom');
    }
    function tryClone(){
      if (cloned || !cloneSelector) return;
      var t; try { t = document.querySelector(cloneSelector); } catch(e){ t=null; }
      if (!t) return;
      if (t.querySelector('.rc-sticky-cta.rc-sticky-cta--top[data-rc-clone="1"]')) { cloned = true; return; }
      var c = topEl.cloneNode(true);
      c.removeAttribute('id'); c.setAttribute('data-rc-clone','1');
      c.classList.add('in-header'); c.classList.remove('is-fixed-top');
      t.appendChild(c); cloned = true;
      stopWatch();
    }
    function stopWatch(){
      window.removeEventListener('scroll', tryClone, passive);
      window.removeEventListener('resize', tryClone);
      if (mo) mo.disconnect();
    }

    // primary: header target
    var headerEl = document.querySelector('header');
    if (headerEl && isStickyOrFixed(headerEl)) appendIntoHeader(headerEl); else pinToTop();

    // optional clone
    var mo;
    if (cloneSelector){
      tryClone();
      if (!cloned){
        window.addEventListener('scroll', tryClone, passive);
        window.addEventListener('resize', tryClone);
        try { mo = new MutationObserver(tryClone); mo.observe(document.documentElement, {childList:true,subtree:true}); } catch(e){}
      }
    }

    // modal behavior
    document.addEventListener('click', function(e){
      var btn   = e.target.closest && e.target.closest('.rc-sticky-cta__button-form');
      var close = e.target.closest && e.target.closest('[data-rc-close]');
      var modal = document.getElementById('rc-sticky-cta-modal');
     if (btn && modal) {

  // ✅ If this is a LINK (form empty case), allow navigation
  if (btn.tagName === 'A' && btn.getAttribute('href')) {
    return;
  }

  modal.setAttribute('aria-hidden', 'false');
  modal.classList.add('is-open');
  document.body.classList.add('rc-modal-open');
  e.preventDefault();
}
      if(close && modal){ modal.setAttribute('aria-hidden','true'); modal.classList.remove('is-open'); document.body.classList.remove('rc-modal-open'); e.preventDefault(); }
    });
  });
})();
