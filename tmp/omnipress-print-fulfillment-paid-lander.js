(function () {
  window.piAjax = window.piAjax || { loadEmailIndicator: function () {} };

  // Match legacy Pardot behavior: links without target open at top window.
  var formAnchors = document.querySelectorAll('#pardot-form a[href]:not([target])');
  formAnchors.forEach(function (a) {
    a.target = '_top';
  });

  var links = document.querySelectorAll('a[href^="#"]');
  links.forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  var params = new URLSearchParams(window.location.search);
  var gclid = params.get('gclid') || sessionStorage.getItem('op_gclid');
  if (gclid) {
    sessionStorage.setItem('op_gclid', gclid);
    var gclidInput = document.getElementById('22_661234pi_22_661234');
    if (gclidInput) gclidInput.value = gclid;
  }

  var sticky = document.getElementById('op-sticky-cta');
  var quoteForm = document.getElementById('request-quote');
  if (sticky && quoteForm && 'IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          sticky.classList.add('is-hidden');
        } else {
          sticky.classList.remove('is-hidden');
        }
      });
    }, { threshold: 0.28 });
    obs.observe(quoteForm);
  }
})();
