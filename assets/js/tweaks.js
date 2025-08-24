<script>
(function () {
  // --- utils ---------------------------------------------------------------
  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  }

  function isMacPlatform() {
    // максимально терпим к разным UA
    const nav = typeof navigator !== "undefined" ? navigator : null;
    const plat = (nav && (nav.userAgentData && nav.userAgentData.platform)) ||
                 (nav && nav.platform) || "";
    return /Mac|iPhone|iPad|iPod/.test(plat);
  }

  // заменить символ ⌘ на "Ctrl" только в ТЕКСТОВЫХ узлах,
  // не трогая внутренние теги <kbd><span>…</span></kbd>
  function replaceKbdCmd(container, replacementText) {
    const kbds = container.querySelectorAll("kbd");
    kbds.forEach(kbd => {
      kbd.childNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE && node.nodeValue.includes("⌘")) {
          node.nodeValue = node.nodeValue.replace(/⌘/g, replacementText);
        }
      });
    });
  }

  // усилить видимость комментариев в блоках Python Markdown,
  // но НЕ трогать директивы ячеек Quarto, начинающиеся с "#|"
  function emphasizeComments(container) {
    container.querySelectorAll(".pymd span.co").forEach(el => {
      const txt = el.innerText.trimStart();
      if (!txt.startsWith("#|")) {
        el.style.fontWeight = "700"; // 700 обычно достаточно; 1000 может не поддерживаться шрифтом
      }
    });
  }

  // применяем оба преобразования в пределах основного контента
  function applyTweaks(root = document) {
    const scope = root.querySelector("#quarto-content") || root;
    if (!isMacPlatform()) {
      replaceKbdCmd(scope, "Ctrl");
    }
    emphasizeComments(scope);
  }

  // --- run once DOM is ready ----------------------------------------------
  onReady(applyTweaks);

  // На некоторых страницах контент меняется динамически (табы/фолды).
  // Лёгкий наблюдатель: дотюним только добавленные узлы.
  const observer = new MutationObserver(muts => {
    for (const m of muts) {
      if (m.addedNodes && m.addedNodes.length) {
        m.addedNodes.forEach(n => {
          if (n.nodeType === 1) { // ELEMENT_NODE
            applyTweaks(n);
          }
        });
      }
    }
  });
  onReady(() => {
    observer.observe(document.body, { childList: true, subtree: true });
  });
})();
</script>
