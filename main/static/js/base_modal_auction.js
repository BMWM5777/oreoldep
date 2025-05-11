document.addEventListener("DOMContentLoaded", function() {
  var auctionTrigger = document.getElementById("auctionModalTrigger");
  var authModal = document.getElementById("authAuctionModal");
  var closeModal = authModal ? authModal.querySelector(".close-modal") : null;

  if (auctionTrigger && authModal) {
    auctionTrigger.addEventListener("click", function(e) {
      e.preventDefault();
      authModal.style.display = "flex";
    });
  }

  if (closeModal) {
    closeModal.addEventListener("click", function() {
      authModal.style.display = "none";
    });
  }

  window.addEventListener("click", function(e) {
    if (e.target === authModal) {
      authModal.style.display = "none";
    }
  });
});
