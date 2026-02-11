(function () {
    window.piAjax = window.piAjax || { loadEmailIndicator: function () {} };

    // Match legacy Pardot behavior: links without target open at top window.
    var formAnchors = document.querySelectorAll('#pardot-form a[href]:not([target])');
    formAnchors.forEach(function (a) {
      a.target = "_top";
    });

    // Match legacy submit behavior without inline JS attributes.
    var formEl = document.getElementById("pardot-form");
    if (formEl) {
      formEl.addEventListener("submit", function () {
        var submitBtn = formEl.querySelector('input[type="submit"][name="formSubmit"]');
        if (submitBtn) submitBtn.disabled = true;
      });
    }

    var submitBtnForBlur = document.querySelector('#pardot-form input[type="submit"][name="formSubmit"]');
    if (submitBtnForBlur) {
      submitBtnForBlur.addEventListener("click", function () {
        this.blur();
      });
    }

    var links = document.querySelectorAll('a[href^="#"]');
    links.forEach(function (link) {
      link.addEventListener("click", function (e) {
        var id = this.getAttribute("href");
        if (!id || id === "#") return;
        var target = document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });

    var params = new URLSearchParams(window.location.search);
    var gclid = params.get("gclid") || sessionStorage.getItem("op_gclid");
    if (gclid) {
      sessionStorage.setItem("op_gclid", gclid);
      var gclidInput = document.getElementById("22_660579pi_22_660579");
      if (gclidInput) gclidInput.value = gclid;
    }

    // Remove empty auto-inserted <p> nodes that create extra whitespace.
    var junkParagraphs = document.querySelectorAll(
      '.op-ppc-landing > p, .op-ppc-landing + p, .op-bottom-cta + p, #op-sticky-cta + p'
    );
    junkParagraphs.forEach(function (p) {
      var hasContentNode = p.querySelector('img, video, iframe, form, input, textarea, button, select');
      var text = (p.textContent || "").replace(/\u00a0/g, " ").trim();
      if (!hasContentNode && text === "") {
        p.remove();
      }
    });

    var sticky = document.getElementById("op-sticky-cta");
    if (sticky) {
      sticky.classList.remove("is-hidden");
    }
  })();
