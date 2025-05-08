gsap.registerPlugin(ScrollTrigger);

gsap.to(".box-lid", {
  y: "-100%",
  scrollTrigger: {
    trigger: ".unbox-container",
    start: "top center",
    end: "bottom center",
    scrub: true
  }
});

gsap.to(".console", {
  opacity: 1,
  scrollTrigger: {
    trigger: ".unbox-container",
    start: "top center",
    end: "bottom center",
    scrub: true
  }
});