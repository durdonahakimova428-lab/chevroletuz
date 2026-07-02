// Hero slayder uchun oddiy logika
document.addEventListener("DOMContentLoaded", function () {
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".hero-dots span");
  let current = 0;

  function showSlide(index) {
    slides.forEach((s, i) => s.style.display = i === index ? "flex" : "none");
    dots.forEach((d, i) => d.classList.toggle("active", i === index));
    current = index;
  }

  if (slides.length > 1) {
    document.querySelectorAll(".hero-arrow.right").forEach(btn => {
      btn.addEventListener("click", () => showSlide((current + 1) % slides.length));
    });
    document.querySelectorAll(".hero-arrow.left").forEach(btn => {
      btn.addEventListener("click", () => showSlide((current - 1 + slides.length) % slides.length));
    });
    dots.forEach((d, i) => d.addEventListener("click", () => showSlide(i)));
    setInterval(() => showSlide((current + 1) % slides.length), 6000);
  }
  if (slides.length) showSlide(0);
});
