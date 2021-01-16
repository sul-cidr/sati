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

const batonOnTabsReady = () => {
  initCodingCollapseToggle();
  initImagePopOut();
  const observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach((mutation) => {
      initCodingCollapseToggle(mutation.target);
    });
  });

  observer.observe(document.querySelector("#inline-itemcoding"), {
    childList: true,
    subtree: true,
  });
};

const initCodingCollapseToggle = (root = document) => {
  root
    .querySelectorAll(".dynamic-itemcoding_set > h3")
    .forEach((el) =>
      el.addEventListener("click", (/* event */) =>
        el.parentElement.toggleAttribute("expanded")),
    );
  root
    .querySelectorAll(".dynamic-itemcoding_set > h3 span.delete")
    .forEach((el) => el.addEventListener("click", (e) => e.stopPropagation()));
};

const initImagePopOut = () => {
  /* copied from baton/static/baton/app/src/core/ChangeForm.js,
     rewritten without jQuery, and with the image onClick handler added */
  document.querySelectorAll(".file-upload").forEach((p) => {
    const cur = p.querySelector("a");
    if (cur) {
      const url = cur.href;
      const ext = url.split(".").pop();
      if (
        ["jpg", "jpeg", "png", "bmp", "svg", "gif", "tif"].indexOf(ext) !== -1
      ) {
        const spinner = document.createElement("o");
        spinner.className = "fa fa-spinner fa-spin fa-2x fa-fw";
        spinner.style.color = "#aaa";

        const preview = document.createElement("div");
        preview.className = "py-2";
        preview.append(spinner);
        p.prepend(preview);

        const image = new Image();
        image.className = "baton-image-preview";
        image.onload = () => preview.replaceChild(image, spinner);
        image.onerror = () => preview.remove();
        image.addEventListener("click", () =>
          window.open(url, cur.innerText, "width=500, height=450"),
        );
        image.src = url;
      }
    }
  });
};
