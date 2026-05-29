let selectedImage = null;
let stream = null;
let currentMode = "file";

const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const liveBtn = document.getElementById("liveBtn");
const predictBtn = document.getElementById("predictBtn");
const chatBox = document.getElementById("chatBox");
const cameraPreview = document.getElementById("cameraPreview");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("captureBtn");
const infoBtn = document.getElementById("infoBtn");
const infoModal = document.getElementById("infoModal");

function addMessage(text, type, imageUrl = null) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${type}`;
    if (imageUrl) {
        msgDiv.innerHTML = `
            <img src="${imageUrl}" style="max-width:200px; border-radius:12px; margin-top:8px;">
            <div>${text}</div>
        `;
    } else {
        msgDiv.innerHTML = text;
    }
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        selectedImage = file;
        addMessage("✅ Photo uploaded", "user", e.target.result);
    };
    reader.readAsDataURL(file);
});

uploadBtn.addEventListener("click", () => {
    setMode("file");
    fileInput.click();
});

function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll(".quick-btn").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.mode === mode);
    });
    if (mode === "camera") {
        cameraPreview.style.display = "flex";
        initCamera();
    } else {
        cameraPreview.style.display = "none";
        if (stream) stopCamera();
    }
}

function initCamera() {
    if (stream) return;
    navigator.mediaDevices
        .getUserMedia({ video: { width: 480, height: 360, facingMode: "user" } })
        .then((s) => {
            stream = s;
            video.srcObject = stream;
        })
        .catch(() => {
            addMessage("❌ Camera access denied or not available.", "bot");
            setMode("file");
        });
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        stream = null;
    }
}

captureBtn.addEventListener("click", () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);
    canvas.toBlob((blob) => {
        selectedImage = new File([blob], "capture.png", { type: "image/png" });
        const reader = new FileReader();
        reader.onload = (e) => {
            addMessage("📸 Live photo captured!", "user", e.target.result);
            stopCamera();
            cameraPreview.style.display = "none";
        };
        reader.readAsDataURL(blob);
    }, "image/png");
});

liveBtn.addEventListener("click", () => {
    setMode("camera");
});

function sendImage() {
    if (!selectedImage) {
        addMessage("❌ Pehle photo upload ya capture karo.", "bot");
        return;
    }
    predictBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    predictBtn.disabled = true;
    addMessage("🔬 AI analyzing your image...", "bot");

    const formData = new FormData();
    formData.append("file", selectedImage);

    fetch("/predict", {
        method: "POST",
        body: formData,
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.result) {
                const emoji = data.result === "Cancer" ? "⚠️" : "✅";
                const color = data.result === "Cancer" ? "#ff4757" : "#2ed573";
                const msg = `${emoji} <strong>${data.result}</strong> (${data.confidence}%)<br>
                            <small style="color:${color}">Doctor se confirm karna zaroori hai.</small>`;
                addMessage(msg, "bot");
            } else {
                addMessage("❌ Prediction failed: " + (data.error || "Unknown error"), "bot");
            }
        })
        .catch(() => {
            addMessage("❌ Server error! Try again.", "bot");
        })
        .finally(() => {
            predictBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
            predictBtn.disabled = false;
            selectedImage = null;
            fileInput.value = "";
        });
}

predictBtn.addEventListener("click", sendImage);

infoBtn.addEventListener("click", () => {
    infoModal.style.display = "flex";
});

window.onclick = (e) => {
    if (e.target === infoModal) {
        infoModal.style.display = "none";
    }
};

function closeInfo() {
    infoModal.style.display = "none";
}