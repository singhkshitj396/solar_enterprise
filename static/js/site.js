(() => {
  const menu = document.querySelector("#main-menu");
  const toggle = document.querySelector(".nav-toggle");

  if (menu && toggle) {
    toggle.addEventListener("click", () => {
      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      toggle.setAttribute("aria-label", isOpen ? "Open navigation menu" : "Close navigation menu");
      menu.classList.toggle("is-open", !isOpen);
    });

    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation menu");
        menu.classList.remove("is-open");
      });
    });
  }

  const revealElements = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries, activeObserver) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            activeObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 },
    );
    revealElements.forEach((element) => observer.observe(element));
  } else {
    revealElements.forEach((element) => element.classList.add("is-visible"));
  }

  const filterButtons = document.querySelectorAll(".filter-chip");
  const projectCards = document.querySelectorAll(".project-entry");
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const filter = button.dataset.filter;
      filterButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      projectCards.forEach((card) => {
        const categories = (card.dataset.category || "").split(" ");
        card.classList.toggle("is-hidden", filter !== "all" && !categories.includes(filter));
      });
    });
  });

  const visitDate = document.querySelector("#id_preferred_visit");
  if (visitDate) {
    const now = new Date();
    const nextMinute = new Date(
      now.getTime() + 60_000 - now.getSeconds() * 1000 - now.getMilliseconds(),
    );
    const localNow = new Date(nextMinute.getTime() - nextMinute.getTimezoneOffset() * 60_000);
    visitDate.min = localNow.toISOString().slice(0, 16);
  }

  if (document.querySelector(".form-error-summary")) {
    document.querySelector("#contact")?.scrollIntoView({ block: "start" });
  }
})();
