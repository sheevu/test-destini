(function () {
  function runWhenIdle(task) {
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(task, { timeout: 1200 });
    } else {
      window.setTimeout(task, 120);
    }
  }

  const navToggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      const expanded = nav.classList.contains("open");
      navToggle.setAttribute("aria-expanded", String(expanded));
    });
  }

  const currentPage = document.body.getAttribute("data-page");
  if (currentPage) {
    const currentLink = document.querySelector(`.site-nav a[data-nav='${currentPage}']`);
    if (currentLink) {
      currentLink.classList.add("active");
    }
  }

  const faqButtons = document.querySelectorAll(".faq-question");
  faqButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const wrapper = button.closest(".faq-item");
      if (!wrapper) return;
      wrapper.classList.toggle("open");
      const expanded = wrapper.classList.contains("open");
      button.setAttribute("aria-expanded", String(expanded));
      const symbol = button.querySelector(".faq-symbol");
      if (symbol) {
        symbol.textContent = expanded ? "-" : "+";
      }
    });
  });

  runWhenIdle(function () {
    const revealElements = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && revealElements.length) {
      const observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("show");
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.16 }
      );

      revealElements.forEach(function (element) {
        observer.observe(element);
      });
    } else {
      revealElements.forEach(function (element) {
        element.classList.add("show");
      });
    }
  });

  const contactForm = document.getElementById("contact-form");
  if (contactForm) {
    const contactFormNote = document.getElementById("contact-form-note");

    function setContactNote(text, isError) {
      if (!contactFormNote) return;
      contactFormNote.textContent = text;
      contactFormNote.style.color = isError ? "#b42318" : "";
    }

    function openMailFallback(name, phone, email, topic, message) {
      const rawBody = [
        "Name: " + name,
        "Phone: " + phone,
        "Email: " + email,
        "Topic: " + topic,
        "",
        "Message:",
        message
      ].join("\n");

      const subject = encodeURIComponent("Destini Numbers Inquiry - " + topic);
      const body = encodeURIComponent(rawBody);
      window.location.href = "mailto:destininumbers37@gmail.com?subject=" + subject + "&body=" + body;
    }

    contactForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const name = document.getElementById("name").value.trim();
      const phone = document.getElementById("phone").value.trim();
      const email = document.getElementById("email").value.trim();
      const topic = document.getElementById("topic").value;
      const message = document.getElementById("message").value.trim();
      const submitButton = contactForm.querySelector("button[type='submit']");
      const serviceIdField = document.getElementById("service-id");

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Submitting...";
      }

      const payload = {
        name: name,
        phone: phone,
        email: email,
        topic: topic,
        message: message
      };

      if (serviceIdField && serviceIdField.value) {
        const numericServiceId = Number(serviceIdField.value);
        if (!Number.isNaN(numericServiceId) && numericServiceId > 0) {
          payload.service_id = numericServiceId;
        }
      }

      try {
        const response = await fetch("api/submit-contact.php", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.error || "Unable to submit inquiry.");
        }

        contactForm.reset();
        setContactNote("Your inquiry has been submitted successfully. Our team will contact you shortly.", false);
      } catch (error) {
        setContactNote("Server setup is incomplete, so your email app is opening as fallback.", true);
        openMailFallback(name, phone, email, topic, message);
      } finally {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = "Submit Inquiry";
        }
      }
    });
  }

  runWhenIdle(function () {
    const hero = document.querySelector(".home-hero");
    if (hero && window.matchMedia("(min-width: 981px)").matches) {
      const parallaxTargets = hero.querySelectorAll("[data-parallax]");
      hero.addEventListener("mousemove", function (event) {
        const rect = hero.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        parallaxTargets.forEach(function (target) {
          const depth = Number(target.getAttribute("data-parallax")) || 8;
          target.style.transform = "translate(" + x * depth + "px," + y * depth + "px)";
        });
      });
    }
  });

  runWhenIdle(function () {
    const chatbotWidget = document.getElementById("chatbot-widget");
    if (!chatbotWidget) return;
    const toggle = document.getElementById("chatbot-toggle");
    const panel = document.getElementById("chatbot-panel");
    const close = document.getElementById("chatbot-close");
    const quickButtons = chatbotWidget.querySelectorAll("[data-chatbot-intent]");
    const replyNode = document.getElementById("chatbot-reply");
    const openWhatsApp = document.getElementById("chatbot-open-whatsapp");
    const formLink = "https://forms.gle/34orCT2JitYgCnbM9";

    function respond(intent) {
      if (!replyNode) return;
      let message = "I can help with services, store items, report interpretation, and bookings.";
      if (intent === "services") {
        message = "For services: Career Alignment, Business Numerology, Personal Destiny Reading, and premium packages are available.";
      } else if (intent === "store") {
        message = "For store: crystals, gemstones, rudraksha (1-14 Mukhi), and puja kits are available with guidance.";
      } else if (intent === "reports") {
        message = "For reports: share your generated Life Path, Compatibility, or House Number result and get personalized guidance.";
      } else if (intent === "booking") {
        message = "For booking: you can connect on WhatsApp directly and select the best consultation format.";
      }

      replyNode.innerHTML =
        message +
        " For callback support, please fill this form: " +
        '<a class="chatbot-form-link" href="' +
        formLink +
        '" target="_blank" rel="noopener">Callback Form</a>.';

      if (openWhatsApp) {
        const text = encodeURIComponent(message + " I have also submitted the callback form.");
        openWhatsApp.href = "https://wa.me/917269031175?text=" + text;
      }
    }

    if (toggle && panel) {
      toggle.addEventListener("click", function () {
        const isHidden = panel.hasAttribute("hidden");
        if (isHidden) {
          panel.removeAttribute("hidden");
          toggle.setAttribute("aria-expanded", "true");
          respond("services");
        } else {
          panel.setAttribute("hidden", "");
          toggle.setAttribute("aria-expanded", "false");
        }
      });
    }

    if (close && panel && toggle) {
      close.addEventListener("click", function () {
        panel.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", "false");
      });
    }

    quickButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const intent = button.getAttribute("data-chatbot-intent");
        respond(intent);
      });
    });
  });

  function scrollSlider(targetId, direction) {
    const track = document.getElementById(targetId);
    if (!track) return;
    const firstCard = track.querySelector(".slider-card");
    const step = firstCard ? firstCard.getBoundingClientRect().width + 14 : 300;
    track.scrollBy({ left: direction * step, behavior: "smooth" });
  }

  runWhenIdle(function () {
    const sliderPrevButtons = document.querySelectorAll("[data-slider-prev]");
    const sliderNextButtons = document.querySelectorAll("[data-slider-next]");

    sliderPrevButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const targetId = button.getAttribute("data-slider-prev");
        scrollSlider(targetId, -1);
      });
    });

    sliderNextButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const targetId = button.getAttribute("data-slider-next");
        scrollSlider(targetId, 1);
      });
    });

    const sliderTracks = document.querySelectorAll("[data-slider-track]");
    sliderTracks.forEach(function (track) {
      track.addEventListener("keydown", function (event) {
        if (event.key === "ArrowRight") {
          event.preventDefault();
          track.scrollBy({ left: 280, behavior: "smooth" });
        } else if (event.key === "ArrowLeft") {
          event.preventDefault();
          track.scrollBy({ left: -280, behavior: "smooth" });
        }
      });
    });
  });

  // ── Scroll to Top Button functionality ──
  runWhenIdle(function () {
    const scrollTop = document.createElement("button");
    scrollTop.className = "scroll-top";
    scrollTop.setAttribute("aria-label", "Scroll to top");
    scrollTop.innerHTML = "↑";
    document.body.appendChild(scrollTop);

    window.addEventListener("scroll", function () {
      if (window.scrollY > 400) {
        scrollTop.classList.add("visible");
      } else {
        scrollTop.classList.remove("visible");
      }
    });

    scrollTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // ── Image Load State Helper for Product Cards ──
  window.initProductImageLoaders = function () {
    document.querySelectorAll('.product-card .img-box img').forEach(img => {
      const handleLoad = () => {
        img.classList.add('loaded');
        const ph = img.closest('.img-box').querySelector('.img-placeholder');
        if (ph && img.classList.contains('main-img')) {
          ph.style.opacity = '0';
          setTimeout(() => ph.style.display = 'none', 300);
        }
      };

      if (img.complete) {
        handleLoad();
      } else {
        img.addEventListener('load', handleLoad);
        img.addEventListener('error', function() {
          img.style.display = 'none';
        });
      }
    });
  };
  runWhenIdle(initProductImageLoaders);

  // ── Cosmic Background Particle Canvas System ──
  runWhenIdle(function () {
    const canvases = document.querySelectorAll(".cosmic-canvas");
    canvases.forEach(function (canvas) {
      const ctx = canvas.getContext("2d");
      let animationFrameId;
      let width = (canvas.width = canvas.parentElement.offsetWidth);
      let height = (canvas.height = canvas.parentElement.offsetHeight);

      // Handle resize
      window.addEventListener("resize", function () {
        if (!canvas.parentElement) return;
        width = canvas.width = canvas.parentElement.offsetWidth;
        height = canvas.height = canvas.parentElement.offsetHeight;
      });

      const stars = [];
      const count = Math.min(80, Math.floor((width * height) / 8000));

      for (let i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * width,
          y: Math.random() * height,
          r: Math.random() * 1.5 + 0.5,
          speed: Math.random() * 0.05 + 0.01,
          opacity: Math.random(),
          factor: Math.random() > 0.5 ? 1 : -1
        });
      }

      function draw() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "rgba(255, 203, 94, 0.4)";
        stars.forEach(function (s) {
          s.opacity += s.speed * s.factor;
          if (s.opacity > 1) {
            s.opacity = 1;
            s.factor = -1;
          } else if (s.opacity < 0) {
            s.opacity = 0;
            s.factor = 1;
            s.x = Math.random() * width;
            s.y = Math.random() * height;
          }
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r * (s.opacity * 0.5 + 0.5), 0, Math.PI * 2);
          ctx.fillStyle = "rgba(255, 203, 94, " + s.opacity * 0.4 + ")";
          ctx.fill();
        });
        animationFrameId = requestAnimationFrame(draw);
      }
      draw();
    });
  });

  // ── Magnetic Button Effect ──
  runWhenIdle(function () {
    const magneticBtns = document.querySelectorAll(".btn-primary, .btn-secondary, .nav-cta, .btn-cosmic");
    magneticBtns.forEach(function (btn) {
      if (window.matchMedia("(min-width: 981px)").matches) {
        btn.addEventListener("mousemove", function (e) {
          const rect = btn.getBoundingClientRect();
          const x = e.clientX - rect.left - rect.width / 2;
          const y = e.clientY - rect.top - rect.height / 2;
          btn.style.transform = "translate(" + x * 0.2 + "px, " + y * 0.2 + "px)";
        });
        btn.addEventListener("mouseleave", function () {
          btn.style.transform = "translate(0px, 0px)";
        });
      }
    });
  });

  // ── Interactive Footer Geometry mousemove glow effect ──
  runWhenIdle(function () {
    const footer = document.querySelector(".footer");
    const graphic = document.querySelector(".footer-graphic");
    if (footer && graphic) {
      footer.addEventListener("mousemove", function (e) {
        const rect = footer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const width = rect.width;
        const height = rect.height;
        const rotate = (x / width - 0.5) * 15;
        const scale = 1 + (y / height - 0.5) * 0.05;
        graphic.style.transform = "rotate(" + rotate + "deg) scale(" + scale + ")";
      });
    }
  });
})();
