document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const imagePreview = document.getElementById('imagePreview');
    const uploadPrompt = document.querySelector('.upload-prompt');
    const convertBtn = document.getElementById('convertBtn');
    const btnText = convertBtn.querySelector('.btn-text');
    const spinner = convertBtn.querySelector('.spinner');

    const widthSlider = document.getElementById('widthSlider');
    const widthInput = document.getElementById('widthInput');
    const contrastSlider = document.getElementById('contrastSlider');
    const contrastInput = document.getElementById('contrastInput');
    const brightnessSlider = document.getElementById('brightnessSlider');
    const brightnessInput = document.getElementById('brightnessInput');

    const charsetSelect = document.getElementById('charset');
    const invertCheckbox = document.getElementById('invert');
    const autoScaleCheckbox = document.getElementById('autoScale');

    const asciiOutput = document.getElementById('asciiOutput');
    const outputPlaceholder = document.getElementById('outputPlaceholder');
    const outputContainer = document.getElementById('outputContainer');
    const outputMeta = document.getElementById('outputMeta');
    const dimDisplay = document.getElementById('dimDisplay');
    const charSetDisplay = document.getElementById('charSetDisplay');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const toast = document.getElementById('toast');

    let currentFile = null;

    // Sync sliders and number inputs
    function syncInputs(slider, number) {
        slider.addEventListener('input', () => { number.value = slider.value; });
        number.addEventListener('input', () => {
            let val = parseFloat(number.value);
            if (!isNaN(val)) {
                slider.value = val;
            }
        });
    }

    syncInputs(widthSlider, widthInput);
    syncInputs(contrastSlider, contrastInput);
    syncInputs(brightnessSlider, brightnessInput);

    // Drag & drop
    dropZone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'));
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'));
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            showToast('Please select an image file', 'error');
            return;
        }
        currentFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.hidden = false;
            uploadPrompt.hidden = true;
            convertBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Convert
    convertBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        setLoading(true);

        const formData = new FormData();
        formData.append('image', currentFile);
        formData.append('width', widthInput.value);
        formData.append('charset', charsetSelect.value);
        formData.append('contrast', contrastInput.value);
        formData.append('brightness', brightnessInput.value);
        formData.append('invert', invertCheckbox.checked);
        formData.append('auto_scale', autoScaleCheckbox.checked);

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                asciiOutput.textContent = data.ascii_art;
                asciiOutput.hidden = false;
                outputPlaceholder.style.display = 'none';
                outputMeta.hidden = false;
                dimDisplay.textContent = `${data.width} x ${data.height} chars`;
                charSetDisplay.textContent = `Set: ${data.char_set}`;
                copyBtn.disabled = false;
                downloadBtn.disabled = false;

                // Scroll to top of output
                outputContainer.scrollTop = 0;
                showToast('ASCII art generated!', 'success');
            } else {
                showToast(data.error || 'Generation failed', 'error');
            }
        } catch (err) {
            showToast('Network error: ' + err.message, 'error');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(loading) {
        convertBtn.disabled = loading || !currentFile;
        btnText.hidden = loading;
        spinner.hidden = !loading;
    }

    // Copy to clipboard
    copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(asciiOutput.textContent);
            showToast('Copied to clipboard!', 'success');
        } catch {
            showToast('Failed to copy', 'error');
        }
    });

    // Download
    downloadBtn.addEventListener('click', () => {
        const blob = new Blob([asciiOutput.textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ascii-art-${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('Downloaded!', 'success');
    });

    // Toast
    function showToast(message, type = 'success') {
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        toast.hidden = false;

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
