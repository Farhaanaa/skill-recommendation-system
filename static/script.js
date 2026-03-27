/* ══════════════════════════════════════
   SKILLMATCH — global scripts
══════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {
  initScrollTop();
  initSkillBars();
  initScoreRings();
  initFilterChips();
  initDomainDots();
  initCharCounters();
});

/* ──────────────────────────────────────
   1. SCROLL-TO-TOP BUTTON
────────────────────────────────────── */
function initScrollTop() {
  const btn = document.createElement("button");
  btn.id = "scrollTop";
  btn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
  btn.title = "Back to top";
  btn.addEventListener("click", () =>
    window.scrollTo({ top: 0, behavior: "smooth" }),
  );
  document.body.appendChild(btn);

  window.addEventListener(
    "scroll",
    () => {
      btn.classList.toggle("visible", window.scrollY > 300);
    },
    { passive: true },
  );
}

/* ──────────────────────────────────────
   2. ANIMATED SKILL BARS
   Finds .skill-bar-fill[data-width] and
   animates them when they enter viewport.
────────────────────────────────────── */
function initSkillBars() {
  const bars = document.querySelectorAll(".skill-bar-fill[data-width]");
  if (!bars.length) return;

  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.style.width = e.target.dataset.width + "%";
          obs.unobserve(e.target);
        }
      });
    },
    { threshold: 0.3 },
  );

  bars.forEach((b) => obs.observe(b));
}

/* ──────────────────────────────────────
   3. SVG SCORE RINGS
   Draws a circular progress ring for
   any .score-ring[data-score] element.
────────────────────────────────────── */
function initScoreRings() {
  document.querySelectorAll(".score-ring[data-score]").forEach((el) => {
    const score = parseInt(el.dataset.score, 10) || 0;
    const size = 64;
    const stroke = 5;
    const r = (size - stroke) / 2;
    const circ = 2 * Math.PI * r;
    const offset = circ - (score / 100) * circ;

    el.innerHTML = `
      <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
        <circle cx="${size / 2}" cy="${size / 2}" r="${r}"
          fill="none" stroke="rgba(232,160,160,0.2)" stroke-width="${stroke}"/>
        <circle cx="${size / 2}" cy="${size / 2}" r="${r}"
          fill="none" stroke="#8b3a3a" stroke-width="${stroke}"
          stroke-dasharray="${circ}" stroke-dashoffset="${circ}"
          stroke-linecap="round"
          style="transition:stroke-dashoffset 1.4s cubic-bezier(0.4,0,0.2,1);"
          data-offset="${offset}"/>
      </svg>
      <span class="score-ring-text">${score}%</span>
    `;

    // Animate when visible
    const arc = el.querySelector("circle:last-of-type");
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            arc.style.strokeDashoffset = arc.dataset.offset;
            obs.unobserve(el);
          }
        });
      },
      { threshold: 0.5 },
    );
    obs.observe(el);
  });
}

/* ──────────────────────────────────────
   4. DOMAIN COLOR DOTS
   Reads data-domain and applies the
   matching CSS class.
────────────────────────────────────── */
const DOMAIN_CLASS_MAP = {
  "ai/ml": "domain-aiml",
  "web dev": "domain-webdev",
  backend: "domain-backend",
  cybersecurity: "domain-cybersecurity",
  "data science": "domain-datascience",
  mobile: "domain-mobile",
  devops: "domain-devops",
  iot: "domain-iot",
  blockchain: "domain-blockchain",
  general: "domain-general",
  productivity: "domain-productivity",
};

function initDomainDots() {
  document.querySelectorAll(".domain-dot[data-domain]").forEach((dot) => {
    const key = dot.dataset.domain.toLowerCase().trim();
    const cls = DOMAIN_CLASS_MAP[key] || "domain-general";
    dot.classList.add(cls);
  });
}

/* ──────────────────────────────────────
   5. FILTER CHIPS (results page)
   Clicking a chip filters visible cards
   by domain without a page reload.
────────────────────────────────────── */
function initFilterChips() {
  const chips = document.querySelectorAll(".filter-chip[data-filter]");
  const cards = document.querySelectorAll(".project-card[data-domain]");
  if (!chips.length || !cards.length) return;

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      chips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");

      const filter = chip.dataset.filter.toLowerCase();

      cards.forEach((card) => {
        const domain = (card.dataset.domain || "").toLowerCase();
        const show = filter === "all" || domain === filter;
        card.style.display = show ? "" : "none";
      });
    });
  });

  // Activate "All" by default
  const allChip = document.querySelector('.filter-chip[data-filter="all"]');
  if (allChip) allChip.classList.add("active");
}

/* ──────────────────────────────────────
   6. TEXTAREA CHARACTER COUNTERS
   Adds a live counter below any
   textarea[maxlength][data-count].
────────────────────────────────────── */
function initCharCounters() {
  document.querySelectorAll("textarea[data-count]").forEach((ta) => {
    const max = parseInt(ta.getAttribute("maxlength") || "500", 10);
    const counter = document.createElement("div");
    counter.style.cssText =
      "font-size:0.72rem;color:var(--text-soft);text-align:right;margin-top:0.2rem;";
    counter.textContent = `0 / ${max}`;
    ta.parentNode.insertBefore(counter, ta.nextSibling);

    ta.addEventListener("input", () => {
      const len = ta.value.length;
      counter.textContent = `${len} / ${max}`;
      counter.style.color =
        len > max * 0.9 ? "var(--rose)" : "var(--text-soft)";
    });
  });
}

/* ──────────────────────────────────────
   7. COPY TO CLIPBOARD helper
   Call: copyText(text, btn)
────────────────────────────────────── */
function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
    btn.style.color = "#2e7d32";
    setTimeout(() => {
      btn.innerHTML = orig;
      btn.style.color = "";
    }, 2000);
  });
}

/* ──────────────────────────────────────
   8. CONFIRM BEFORE DELETE
   Attach to any form with data-confirm.
────────────────────────────────────── */
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (e) => {
    if (!confirm(form.dataset.confirm)) e.preventDefault();
  });
});
