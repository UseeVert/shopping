document.addEventListener("DOMContentLoaded", function () {
  const addItemForm = document.getElementById("add-item-form");
  const showListButton = document.getElementById("show-list-button");
  const listModal = document.getElementById("list-modal");
  const closeModal = document.querySelector(".close");
  const paymentForm = document.getElementById("payment-form");

  // Menampilkan notifikasi setelah menambahkan item
  addItemForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch("/add", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        alert(data);
        addItemForm.reset();
        window.location.reload();
      });
  });

  // Menampilkan daftar belanjaan
  showListButton.addEventListener("click", function () {
    listModal.style.display = "block";
  });

  // Menutup modal
  closeModal.addEventListener("click", function () {
    listModal.style.display = "none";
  });

  // Menutup modal jika klik di luar modal
  window.onclick = function (event) {
    if (event.target == listModal) {
      listModal.style.display = "none";
    }
  };

  // Menangani pembayaran dan mereset daftar belanjaan
  paymentForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch("/pay", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        alert(data);
        window.location.href = "/manage";
      });
  });
});
