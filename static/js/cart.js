// Initialize Alpine store for cart drawer
document.addEventListener("alpine:init", () => {
  Alpine.store("cartDrawer", {
    open: false,
    toggle() {
      this.open = !this.open;
    },
    close() {
      this.open = false;
    },
  });
});
