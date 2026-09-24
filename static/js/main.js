// Main JavaScript for UI Interactions, Sample Loaders & Tab Navigation

document.addEventListener('DOMContentLoaded', function () {
  // Tab switching logic
  const tabButtons = document.querySelectorAll('.tab-pill-btn');
  const tabContents = document.querySelectorAll('.tab-content-panel');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      const targetId = this.getAttribute('data-tab');
      
      tabButtons.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.style.display = 'none');
      
      this.classList.add('active');
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.style.display = 'block';
      }
    });
  });

  // Image upload preview
  const imageInput = document.getElementById('imageFileInput');
  const imagePreview = document.getElementById('imagePreview');
  const imagePreviewContainer = document.getElementById('imagePreviewContainer');

  if (imageInput && imagePreview) {
    imageInput.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          imagePreview.src = e.target.result;
          if (imagePreviewContainer) imagePreviewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Audio file input preview
  const audioInput = document.getElementById('audioFileInput');
  const audioPreview = document.getElementById('audioPlayer');
  if (audioInput && audioPreview) {
    audioInput.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        audioPreview.src = URL.createObjectURL(file);
        audioPreview.style.display = 'block';
      }
    });
  }

  // Sample prompt loader for Multilingual Text
  window.loadSamplePrompt = function (lang, index) {
    fetch('/static/sample_data/sample_prompts.json')
      .then(res => res.json())
      .then(data => {
        const langData = data.multilingual_text[lang];
        if (langData && langData[index]) {
          const sample = langData[index];
          const textArea = document.getElementById('counsellingTextInput');
          const langSelect = document.getElementById('languageSelect');
          if (textArea) {
            textArea.value = sample.text;
            textArea.focus();
          }
          if (langSelect) {
            langSelect.value = lang === 'malayalam' ? 'ml' : (lang === 'hindi' ? 'hi' : 'en');
          }
          showToast(`Loaded ${lang.toUpperCase()} sample for [${sample.label.toUpperCase()}]`);
        }
      })
      .catch(err => console.error('Error loading sample prompt:', err));
  };

  // Sample Portrait Image Loader
  window.loadSampleImage = function (emotion) {
    const hiddenHint = document.getElementById('filenameHintInput');
    const imagePreview = document.getElementById('imagePreview');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const sampleInputNotice = document.getElementById('sampleInputNotice');

    const sampleUrl = `/static/sample_data/${emotion}.svg`;
    if (imagePreview) {
      imagePreview.src = sampleUrl;
      if (imagePreviewContainer) imagePreviewContainer.style.display = 'block';
    }
    if (hiddenHint) {
      hiddenHint.value = `sample_${emotion}.svg`;
    }
    if (sampleInputNotice) {
      sampleInputNotice.innerText = `Selected preset portrait: ${emotion.toUpperCase()}`;
      sampleInputNotice.style.display = 'block';
    }
    showToast(`Loaded sample portrait for: ${emotion.toUpperCase()}`);
  };

  // Toast Notification helper
  window.showToast = function (message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
      document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = 'glass-card';
    toast.style.cssText = 'padding:12px 20px;color:#fff;background:rgba(30,41,59,0.95);border-left:4px solid #4f46e5;font-size:0.9rem;border-radius:8px;box-shadow:0 8px 20px rgba(0,0,0,0.3);';
    toast.innerText = message;
    
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.4s ease';
      setTimeout(() => toast.remove(), 400);
    }, 3000);
  };
});
