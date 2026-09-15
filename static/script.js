let selectedImage = null;
let stream = null;
const fileInput =
    document.getElementById("fileInput");
const uploadBtn =
    document.getElementById("uploadBtn");
const liveBtn =
    document.getElementById("liveBtn");
const predictBtn =
    document.getElementById("predictBtn");
const chatBox =
    document.getElementById("chatBox");
const cameraBox =
    document.getElementById("cameraBox");
const cameraPreview =
    document.getElementById("cameraPreview");
const captureBtn =
    document.getElementById("captureBtn");
const closeCameraBtn =
    document.getElementById("closeCameraBtn");
// =================================
// AUTO SCROLL
// =================================
function scrollToLatest() {
    setTimeout(() => {
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: "smooth"
        });
    }, 100);
}
// =================================
// UPLOAD
// =================================
uploadBtn.addEventListener(
    "click",
    () => {
        fileInput.click();
    }
);
// =================================
// FILE SELECT
// =================================
fileInput.addEventListener(
    "change",
    (event) => {
        const file =
            event.target.files[0];
        if (!file) {
            return;
        }
        selectedImage = file;
        showImage(file);
    }
);
// =================================
// SHOW USER IMAGE
// =================================
function showImage(file) {
    const imageURL =
        URL.createObjectURL(file);
    const row =
        document.createElement("div");
    row.className =
        "user-row";
    row.innerHTML = `
        <div class="user-bubble">
            <img
                src="${imageURL}"
                class="preview-image"
            >
            <div class="selected-text">
                📷 Skin image uploaded
            </div>
        </div>
    `;
    chatBox.appendChild(row);
    scrollToLatest();
}
// =================================
// LIVE CAMERA
// =================================
liveBtn.addEventListener(
    "click",
    async () => {
        try {
            stream =
                await navigator
                    .mediaDevices
                    .getUserMedia({
                        video: {
                            facingMode:
                                "environment"
                        },
                        audio: false
                    });
            cameraPreview.srcObject =
                stream;
            cameraBox.classList.add(
                "active"
            );
        }
        catch (error) {
            alert(
                "Camera permission denied."
            );
        }
    }
);
// =================================
// CAPTURE
// =================================
captureBtn.addEventListener(
    "click",
    () => {
        if (!stream) {
            return;
        }
        const canvas =
            document.createElement(
                "canvas"
            );
        canvas.width =
            cameraPreview.videoWidth;
        canvas.height =
            cameraPreview.videoHeight;
        const context =
            canvas.getContext("2d");
        context.drawImage(
            cameraPreview,
            0,
            0,
            canvas.width,
            canvas.height
        );
        canvas.toBlob(
            (blob) => {
                selectedImage =
                    new File(
                        [blob],
                        "camera-image.jpg",
                        {
                            type:
                                "image/jpeg"
                        }
                    );
                showImage(
                    selectedImage
                );
                stopCamera();
            },
            "image/jpeg"
        );
    }
);
// =================================
// STOP CAMERA
// =================================
closeCameraBtn.addEventListener(
    "click",
    stopCamera
);
function stopCamera() {
    if (stream) {
        stream
            .getTracks()
            .forEach(
                track =>
                    track.stop()
            );
        stream = null;
    }
    cameraPreview.srcObject =
        null;
    cameraBox.classList.remove(
        "active"
    );
}
// =================================
// PREDICT
// =================================
predictBtn.addEventListener(
    "click",
    async () => {
        if (!selectedImage) {
            addBotMessage(
                "Please upload or capture a skin image first."
            );
            return;
        }
        // -----------------------------
        // ANALYZING MESSAGE
        // -----------------------------
        addAnalyzingMessage();
        const formData =
            new FormData();
        formData.append(
            "image",
            selectedImage
        );
        try {
            const response =
                await fetch(
                    "/predict",
                    {
                        method: "POST",
                        body: formData
                    }
                );
            const data =
                await response.json();
            if (!data.success) {
                addBotMessage(
                    "❌ " +
                    data.error
                );
                return;
            }
            // -----------------------------
            // SHOW RESULT
            // -----------------------------
            showResult(data);
        }
        catch (error) {
            console.error(error);
            addBotMessage(
                "❌ Unable to connect to the AI server."
            );
        }
    }
);
// =================================
// ANALYZING MESSAGE
// =================================
function addAnalyzingMessage() {
    const row =
        document.createElement("div");
    row.className =
        "result-row";
    row.innerHTML = `
        <div class="bot-icon">
            🤖
        </div>
        <div class="result-bubble">
            <div class="result-title">
                🔬 AI Assistant
            </div>
            <div class="analyzing">
                AI is analyzing your image
                <span class="dots">...</span>
            </div>
        </div>
    `;
    chatBox.appendChild(row);
    scrollToLatest();
    // Animated dots
    let count = 0;
    const dots =
        row.querySelector(".dots");
    const interval =
        setInterval(() => {
            count++;
            if (count > 3) {
                count = 1;
            }
            dots.textContent =
                ".".repeat(count);
        }, 400);
    // Stop animation later
    setTimeout(() => {
        clearInterval(interval);
    }, 10000);
}
// =================================
// BOT MESSAGE
// =================================
function addBotMessage(text) {
    const row =
        document.createElement("div");
    row.className =
        "result-row";
    row.innerHTML = `
        <div class="bot-icon">
            🤖
        </div>
        <div class="result-bubble">
            <div class="result-title">
                AI Assistant
            </div>
            <div class="normal-message">
                ${text}
            </div>
        </div>
    `;
    chatBox.appendChild(row);
    scrollToLatest();
}
// =================================
// RESULT
// =================================
function showResult(data) {
    const cancer =
        data.cancer_score;
    const nonCancer =
        data.non_cancer_confidence;
    const row =
        document.createElement("div");
    row.className =
        "result-row";
    row.innerHTML = `
        <div class="bot-icon">
            🤖
        </div>
        <div class="result-bubble result-card">
            <div class="result-title">
                🧠 AI Analysis Complete
            </div>
            <!-- CANCER -->
            <div class="score-block">
                <div class="score-header">
                    <span>
                        Cancer
                    </span>
                    <strong>
                        ${cancer}%
                    </strong>
                </div>
                <div class="progress">
                    <div
                        class="progress-fill cancer-fill"
                        style="
                            width:${cancer}%;
                        "
                    ></div>
                </div>
                <div class="score-label">
                    Score
                </div>
            </div>
            <!-- NON CANCER -->
            <div class="score-block">
                <div class="score-header">
                    <span>
                        Non-Cancer
                    </span>
                    <strong>
                        ${nonCancer}%
                    </strong>
                </div>
                <div class="progress">
                    <div
                        class="progress-fill non-cancer-fill"
                        style="
                            width:${nonCancer}%;
                        "
                    ></div>
                </div>
                <div class="score-label">
                    Confidence
                </div>
            </div>
            <!-- DOCTOR -->
            <div class="doctor-warning">
                ⚠️ Please confirm the result
                with a qualified doctor.
            </div>
        </div>
    `;
    chatBox.appendChild(row);
    scrollToLatest();
}
/* =========================================
   RESET BUTTON
========================================= */
const resetBtn =
    document.getElementById("resetBtn");
resetBtn.addEventListener(
    "click",
    () => {
        resetApplication();
    }
);
/* =========================================
   RESET APPLICATION
========================================= */
function resetApplication() {
    /*
       Stop camera if running
    */
    stopCamera();
    /*
       Remove all chat messages
    */
    chatBox.classList.add(
        "resetting"
    );
    setTimeout(() => {
        chatBox.innerHTML = `
            <div class="bot-row">
                <div class="bot-icon">
                    🤖
                </div>
                <div class="bot-bubble">
                    <div class="hello">
                        Hello!
                    </div>
                    <div class="main-text">
                        Send your skin image to get
                        an AI-based prediction.
                    </div>
                    <div class="notice">
                        Results are only for screening,
                        consult a doctor.
                    </div>
                </div>
            </div>
        `;
        /*
           Remove selected image
        */
        selectedImage = null;
        /*
           Reset file input
        */
        fileInput.value = "";
        /*
           Remove animation
        */
        chatBox.classList.remove(
            "resetting"
        );
        /*
           Go to top
        */
        chatBox.scrollTo({
            top: 0,
            behavior: "instant"
        });
    }, 150);
}
