// In-Browser Audio Recorder for Multilingual Speech Emotion Analysis

class AudioEmotionRecorder {
  constructor(startBtnId, stopBtnId, playerElementId, timerElementId, hiddenBlobInputId) {
    this.startBtn = document.getElementById(startBtnId);
    this.stopBtn = document.getElementById(stopBtnId);
    this.player = document.getElementById(playerElementId);
    this.timer = document.getElementById(timerElementId);
    this.hiddenInput = document.getElementById(hiddenBlobInputId);

    this.mediaRecorder = null;
    this.audioChunks = [];
    this.timerInterval = null;
    this.seconds = 0;

    this.initEvents();
  }

  initEvents() {
    if (this.startBtn) {
      this.startBtn.addEventListener('click', () => this.startRecording());
    }
    if (this.stopBtn) {
      this.stopBtn.addEventListener('click', () => this.stopRecording());
    }
  }

  async startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.audioChunks = [];
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) this.audioChunks.push(e.data);
      };

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        if (this.player) {
          this.player.src = audioUrl;
          this.player.style.display = 'block';
        }
        // Base64 encoding for form transfer
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
          if (this.hiddenInput) {
            this.hiddenInput.value = reader.result;
          }
        };
        showToast("Audio Recorded Successfully. Ready for Analysis.");
      };

      this.mediaRecorder.start();
      this.seconds = 0;
      this.startTimer();

      if (this.startBtn) this.startBtn.disabled = true;
      if (this.stopBtn) this.stopBtn.disabled = false;
      showToast("Recording session audio... speak now.");
    } catch (err) {
      console.warn("Microphone not available, enabling sample audio fallback:", err);
      showToast("Microphone unavailable. You can upload an audio file or test sample voice clip.", "warning");
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
    this.stopTimer();
    if (this.startBtn) this.startBtn.disabled = false;
    if (this.stopBtn) this.stopBtn.disabled = true;
  }

  startTimer() {
    this.timerInterval = setInterval(() => {
      this.seconds++;
      const mins = String(Math.floor(this.seconds / 60)).padStart(2, '0');
      const secs = String(this.seconds % 60).padStart(2, '0');
      if (this.timer) this.timer.innerText = `${mins}:${secs}`;
    }, 1000);
  }

  stopTimer() {
    clearInterval(this.timerInterval);
  }
}

window.AudioEmotionRecorder = AudioEmotionRecorder;
