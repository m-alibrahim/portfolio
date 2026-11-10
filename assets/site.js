(function () {
  var root = document.documentElement;

  // Theme toggle (remembered per browser when storage is available)
  var btn = document.querySelector(".theme");
  if (btn) btn.addEventListener("click", function () {
    var next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
  });

  // Highlight the current section in the side navigation
  var links = [].slice.call(document.querySelectorAll(".intro nav a"));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
  if (links[0]) links[0].classList.add("active");
  if ("IntersectionObserver" in window && links.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove("active"); });
        var a = byId[en.target.id];
        if (a) a.classList.add("active");
      });
    }, { rootMargin: "-35% 0px -55% 0px" });
    document.querySelectorAll("main section[id]").forEach(function (s) { io.observe(s); });
  }

  // Soft light that follows the pointer (desktop pointers only, off for reduced motion)
  var glow = document.querySelector(".glow");
  var fine = window.matchMedia("(pointer: fine)").matches;
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (glow && fine && !calm) {
    var raf = null;
    window.addEventListener("pointermove", function (ev) {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        glow.style.setProperty("--mx", ev.clientX + "px");
        glow.style.setProperty("--my", ev.clientY + "px");
        glow.classList.add("on");
        raf = null;
      });
    }, { passive: true });
  }
})();
