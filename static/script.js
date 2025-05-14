document.addEventListener('DOMContentLoaded', () => {
  const themeSwitch = document.getElementById('theme-toggle');
  const compressForm = document.querySelector("form[action='/compress']");
  const decompressForm = document.querySelector("form[action='/decompress']");

  // Apply stored theme
  if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light');
    themeSwitch.checked = true;
  }

  // Theme toggle handler
  themeSwitch.addEventListener('change', () => {
    document.body.classList.toggle('light');
    if (document.body.classList.contains('light')) {
      localStorage.setItem('theme', 'light');
    } else {
      localStorage.removeItem('theme');
    }
  });

  // Show success message if "message" query param is present
  const urlParams = new URLSearchParams(window.location.search);
  const message = urlParams.get('message');

  if (message) {
    const status = document.getElementById('status');
    const messageText = document.getElementById('message-text');
    status.style.display = 'block';
    messageText.textContent = message;

    setTimeout(() => {
      status.style.opacity = 0;
      setTimeout(() => {
        status.style.display = 'none';
        status.style.opacity = 1;
      }, 500);
    }, 3000);
  }

  // Handle compression
  compressForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Compressing your file. Please wait...");

    const fileInput = compressForm.querySelector("input[type='file']");
    if (!fileInput.files.length) {
      alert("Please select a file to compress.");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/compress", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Compression failed.");
        return response.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileInput.files[0].name + ".zlib";
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch((err) => alert("Error: " + err.message));
  });

  // Handle decompression
  decompressForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Decompressing your file. Please wait...");

    const fileInput = decompressForm.querySelector("input[type='file']");
    if (!fileInput.files.length) {
      alert("Please select a file to decompress.");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/decompress", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Decompression failed.");
        return response.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileInput.files[0].name.replace(".zlib", "") || "decompressed_file";
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch((err) => alert("Error: " + err.message));
  });
});