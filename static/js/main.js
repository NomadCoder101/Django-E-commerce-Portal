// Store management for Alpine.js
document.addEventListener("alpine:init", () => {
  // Cart drawer state
  Alpine.store("cartDrawer", {
    open: false,

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    open() {
      this.open = true;
    },
  });

  // Search modal state
  Alpine.store("searchModal", {
    open: false,
    query: "",
    results: [],
    loading: false,

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
      this.query = "";
      this.results = [];
    },

    async search() {
      if (!this.query) {
        this.results = [];
        return;
      }

      this.loading = true;
      try {
        const response = await fetch(
          `/api/search/?q=${encodeURIComponent(this.query)}`
        );
        const data = await response.json();
        this.results = data.results;
      } catch (error) {
        console.error("Search error:", error);
        this.results = [];
      } finally {
        this.loading = false;
      }
    },
  });
});

// HTMX extensions
htmx.onLoad(function (content) {
  // Reinitialize Alpine components in HTMX-loaded content
  if (window.Alpine) {
    window.Alpine.initTree(content);
  }
});
