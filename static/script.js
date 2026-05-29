let selectedImage = null;
let stream = null;
let currentMode = "file";

<<<<<<< HEAD
=======
// Elements
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
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

<<<<<<< HEAD
=======

// Add message (WhatsApp style)
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
function addMessage(text, type, imageUrl = null) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${type}`;

    if (imageUrl) {
        msgDiv.innerHTML = `
<<<<<<< HEAD
            <img src="${imageUrl}" style="max-width:200px; border-radius:12px; margin-top:8px; display:block;">
=======
            <img src="${imageUrl}" style="max-width:200px; border-radius:12px; margin-top:8px;">
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
            <div>${text}</div>
        `;
    } else {
        msgDiv.innerHTML = text;
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

<<<<<<< HEAD
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    video.srcObject = null;
}

async function initCamera() {
    try {
        stopCamera();

        const constraints = {
            video: {
                facingMode: { ideal: "environment" },
                width: { ideal: 480 },
                height: { ideal: 360 }
            },
            audio: false
        };

        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;

        await video.play();

        cameraPreview.style.display = "flex";
        addMessage("✅ Camera started successfully.", "bot");
    } catch (err) {
        console.error("Camera error:", err);
        addMessage("❌ Camera access failed: " + err.message, "bot");
        setMode("file");
    }
}

function setMode(mode) {
    currentMode = mode;

    document.querySelectorAll(".quick-btn").forEach(btn => {
=======
// File upload
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
    fileInput.click();
});


// Live camera mode
function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll(".quick-btn").forEach((btn) => {
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
        btn.classList.toggle("active", btn.dataset.mode === mode);
    });

    if (mode === "camera") {
        cameraPreview.style.display = "flex";
        initCamera();
    } else {
        cameraPreview.style.display = "none";
<<<<<<< HEAD
        stopCamera();
    }
}

fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;

    selectedImage = file;

    const reader = new FileReader();
    reader.onload = (ev) => {
        addMessage("✅ Photo uploaded", "user", ev.target.result);
    };
    reader.readAsDataURL(file);
});

uploadBtn.addEventListener("click", () => {
    setMode("file");
    fileInput.click();
});

liveBtn.addEventListener("click", () => {
    setMode("camera");
});

captureBtn.addEventListener("click", () => {
    if (!video.videoWidth || !video.videoHeight) {
        addMessage("❌ Camera not ready yet. Please wait a moment.", "bot");
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
        if (!blob) {
            addMessage("❌ Failed to capture image.", "bot");
            return;
        }

        selectedImage = new File([blob], "capture.png", { type: "image/png" });

        const reader = new FileReader();
        reader.onload = (ev) => {
            addMessage("📸 Live photo captured!", "user", ev.target.result);
        };
        reader.readAsDataURL(blob);

        stopCamera();
        cameraPreview.style.display = "none";
    }, "image/png");
});

async function sendImage() {
=======
        if (stream) {
            stopCamera();
        }
    }
}

function initCamera() {
    if (stream) return;
    navigator.mediaDevices
        .getUserMedia({
            video: { width: 480, height: 360, facingMode: "user" },
        })
        .then((s) => {
            stream = s;
            video.srcObject = stream;
        })
        .catch((err) => {
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

    canvas.toBlob(
        (blob) => {
            selectedImage = new File([blob], "capture.png", { type: "image/png" });
            const reader = new FileReader();
            reader.onload = (e) => {
                addMessage("📸 Live photo captured!", "user", e.target.result);
                // Capture के बाद camera और capture बंद हो जाएँ
                stopCamera();
                cameraPreview.style.display = "none";
            };
            reader.readAsDataURL(blob);
        },
        "image/png"
    );
});

// Switch modes
liveBtn.addEventListener("click", () => {
    setMode("camera");
});
uploadBtn.addEventListener("click", () => {
    setMode("file");
});


// Predict / send button (WhatsApp style)
function sendImage() {
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
    if (!selectedImage) {
        addMessage("❌ Pehle photo upload ya capture karo.", "bot");
        return;
    }

    predictBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    predictBtn.disabled = true;
<<<<<<< HEAD

    addMessage("🔬 AI analyzing your image...", "bot");

    try {
        const formData = new FormData();
        formData.append("file", selectedImage);

        const res = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (data.result) {
            const emoji = data.result === "Cancer" ? "⚠️" : "✅";
            const color = data.result === "Cancer" ? "#ff4757" : "#2ed573";
            const msg = `${emoji} <strong>${data.result}</strong> (${data.confidence}%)<br>
                         <small style="color:${color}">Doctor se confirm karna zaroori hai.</small>`;
            addMessage(msg, "bot");
        } else {
            addMessage("❌ Prediction failed: " + (data.error || "Unknown error"), "bot");
        }
    } catch (err) {
        console.error(err);
        addMessage("❌ Server error! Try again.", "bot");
    } finally {
        predictBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
        predictBtn.disabled = false;
        selectedImage = null;
        fileInput.value = "";
    }
=======
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
        .catch((err) => {
            addMessage("❌ Server error! Try again.", "bot");
        })
        .finally(() => {
            predictBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
            predictBtn.disabled = false;
            selectedImage = null;
            fileInput.value = "";
        });
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
}

predictBtn.addEventListener("click", sendImage);

<<<<<<< HEAD
=======

// Info modal (top right 3 dots)
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
infoBtn.addEventListener("click", () => {
    infoModal.style.display = "flex";
});

<<<<<<< HEAD
window.addEventListener("click", (e) => {
    if (e.target === infoModal) {
        infoModal.style.display = "none";
    }
});
=======
window.onclick = (e) => {
    if (e.target === infoModal) {
        infoModal.style.display = "none";
    }
};
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1

function closeInfo() {
    infoModal.style.display = "none";
}