document.addEventListener('DOMContentLoaded', function() {
  const swiperServices = new Swiper('.services-carousel', {
    loop: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
    slidesPerView: 3,
    spaceBetween: 30,
    navigation: {
      nextEl: '.services .swiper-button-next',
      prevEl: '.services .swiper-button-prev',
    },
    pagination: {
      el: '.services .swiper-pagination',
      clickable: true,
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 30,
      }
    }
  });

  const swiperWhy = new Swiper('.why-carousel', {
    loop: true,
    autoplay: {
      delay: 3500,
      disableOnInteraction: false,
    },
    slidesPerView: 3,
    spaceBetween: 30,
    navigation: {
      nextEl: '.why-choose-us .swiper-button-next',
      prevEl: '.why-choose-us .swiper-button-prev',
    },
    pagination: {
      el: '.why-choose-us .swiper-pagination',
      clickable: true,
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 30,
      }
    }
  });
});
