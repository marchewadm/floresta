const lazyLoadInstance = new LazyLoad({
  callback_loaded: (el) => {
    el.style.setProperty("filter", "none");
  }
});