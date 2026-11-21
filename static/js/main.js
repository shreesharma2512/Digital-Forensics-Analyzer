document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('input[type="file"]').forEach((input) => {
    input.addEventListener("change", () => {
      const file = input.files && input.files[0];
      if (file && file.size > 25 * 1024 * 1024) {
        alert("Selected file exceeds the 25 MB upload limit.");
        input.value = "";
      }
    });
  });
});
