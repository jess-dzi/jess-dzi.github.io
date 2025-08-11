document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll("figure img");
  
    images.forEach(img => {
      img.addEventListener("click", function () {
        const overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.top = 0;
        overlay.style.left = 0;
        overlay.style.width = "100%";
        overlay.style.height = "100%";
        overlay.style.backgroundColor = "rgba(0,0,0,0.8)";
        overlay.style.display = "flex";
        overlay.style.justifyContent = "center";
        overlay.style.alignItems = "center";
        overlay.style.zIndex = 1000;
  
        const bigImage = document.createElement("img");
        bigImage.src = this.src;
        bigImage.style.maxWidth = "90%";
        bigImage.style.maxHeight = "90%";
        bigImage.style.border = "4px solid white";
        bigImage.style.borderRadius = "8px";
  
        overlay.appendChild(bigImage);
        document.body.appendChild(overlay);
  
        overlay.addEventListener("click", function () {
          document.body.removeChild(overlay);
        });
      });
    });
  });
  