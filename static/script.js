/**
 * JavaScript for Smart Garbage Segregation System
 * Handles file upload, camera capture, API calls, and servo motor simulation
 */

// Global variables
let currentImage = null;
let stream = null;
let currentImageSource = null; // 'file' or 'camera'

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const cameraPreview = document.getElementById('cameraPreview');
const cameraImage = document.getElementById('cameraImage');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startCameraBtn = document.getElementById('startCamera');
const capturePhotoBtn = document.getElementById('capturePhoto');
const stopCameraBtn = document.getElementById('stopCamera');
const predictBtn = document.getElementById('predictBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');

// File Upload Handling
fileInput.addEventListener('change', handleFileSelect);
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('drop', handleDrop);
uploadArea.addEventListener('click', () => fileInput.click());

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        displayImage(file, 'file');
    } else {
        showError('Please select a valid image file.');
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.style.background = '#e9ecef';
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.style.background = '#f8f9fa';
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        displayImage(file, 'file');
    } else {
        showError('Please drop a valid image file.');
    }
}

function displayImage(file, source) {
    currentImageSource = source;
    const reader = new FileReader();
    
    reader.onload = function(e) {
        if (source === 'file') {
            previewImage.src = e.target.result;
            previewContainer.style.display = 'block';
            cameraPreview.style.display = 'none';
        } else {
            cameraImage.src = e.target.result;
            cameraPreview.style.display = 'block';
            previewContainer.style.display = 'none';
        }
        currentImage = file;
        predictBtn.disabled = false;
        hideError();
        hideResults();
    };
    
    reader.readAsDataURL(file);
}

// Camera Handling
startCameraBtn.addEventListener('click', startCamera);
capturePhotoBtn.addEventListener('click', capturePhoto);
stopCameraBtn.addEventListener('click', stopCamera);

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } 
        });
        video.srcObject = stream;
        video.style.display = 'block';
        startCameraBtn.style.display = 'none';
        capturePhotoBtn.style.display = 'inline-block';
        stopCameraBtn.style.display = 'inline-block';
        hideError();
    } catch (err) {
        showError('Could not access camera. Please check permissions.');
        console.error('Camera error:', err);
    }
}

function capturePhoto() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    canvas.toBlob(function(blob) {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        displayImage(file, 'camera');
    }, 'image/jpeg', 0.95);
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    video.srcObject = null;
    video.style.display = 'none';
    startCameraBtn.style.display = 'inline-block';
    capturePhotoBtn.style.display = 'none';
    stopCameraBtn.style.display = 'none';
}

// Prediction
predictBtn.addEventListener('click', makePrediction);

async function makePrediction() {
    if (!currentImage) {
        showError('Please select or capture an image first.');
        return;
    }
    
    // Show loading, hide results
    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';
    hideError();
    predictBtn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', currentImage);
        
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Prediction failed');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (err) {
        showError('Error making prediction: ' + err.message);
        console.error('Prediction error:', err);
    } finally {
        loadingIndicator.style.display = 'none';
        predictBtn.disabled = false;
    }
}

function displayResults(result) {
    // Update result fields
    document.getElementById('predictedClass').textContent = result.predicted_class.toUpperCase();
    document.getElementById('confidence').textContent = (result.confidence * 100).toFixed(2) + '%';
    
    const binTypeElement = document.getElementById('binType');
    binTypeElement.textContent = result.bin;
    binTypeElement.className = 'result-value ' + (result.bin === 'Recyclable' ? 'bin-recyclable' : 'bin-other');
    
    // Update servo simulation
    updateServoSimulation(result.servo_angle, result.bin);
    
    // Show results section
    resultsSection.style.display = 'block';
}

function updateServoSimulation(angle, binType) {
    const servoArm = document.getElementById('servoArm');
    const servoArrow = document.getElementById('servoArrow');
    const servoAngleElement = document.getElementById('servoAngle');
    const servoDirectionElement = document.getElementById('servoDirection');
    
    // Update angle
    servoAngleElement.textContent = angle;
    
    // Update direction text
    servoDirectionElement.textContent = binType === 'Recyclable' ? 'LEFT (Recyclable)' : 'RIGHT (Other)';
    
    // Rotate servo arm
    // 0° = right (Other), 90° = left (Recyclable)
    // We'll rotate from center (45°) to the target angle
    const rotation = angle; // 0 for Other, 90 for Recyclable
    servoArm.style.transform = `rotate(${rotation}deg)`;
    
    // Update arrow direction
    if (angle === 90) {
        servoArrow.textContent = '←';
        servoArrow.style.color = '#28a745';
    } else {
        servoArrow.textContent = '→';
        servoArrow.style.color = '#dc3545';
    }
}

// Utility Functions
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function hideResults() {
    resultsSection.style.display = 'none';
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopCamera();
});

