const batonMenuReady = () => {
  if (window.location.pathname === "/admin/") return;
  const link = document.querySelector(
    ".sidebar-menu a[href='" +
      window.location.pathname +
      window.location.search +
      "']",
  );
  if (link) {
    for (let item of document.querySelectorAll(".sidebar-menu li.active")) {
      item.classList.remove("active");
    }
    link.parentElement.classList.add("active");
  }
};

const batonOnReady = () => {
  initCodingCollapseToggle();
};

const initCodingCollapseToggle = () => {
  document
    .querySelectorAll(".dynamic-itemcoding_set > h3")
    .forEach((el) =>
      el.addEventListener("click", (/* event */) =>
        el.parentElement.toggleAttribute("expanded")),
    );
  document
    .querySelectorAll(".dynamic-itemcoding_set > h3 span.delete")
    .forEach((el) => el.addEventListener("click", (e) => e.stopPropagation()));
};
