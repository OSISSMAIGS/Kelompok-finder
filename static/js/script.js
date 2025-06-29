document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nama = document.getElementById('namaInput').value.trim();
    const loadingEl = document.getElementById('loading');
    const hasilEl = document.getElementById('hasil');
    const searchBtn = document.getElementById('searchBtn');
    
    if (!nama) {
        hasilEl.innerHTML = '<div class="error">❌ Nama tidak boleh kosong!</div>';
        return;
    }
    
    // Show loading
    loadingEl.style.display = 'block';
    hasilEl.innerHTML = '';
    searchBtn.disabled = true;
    searchBtn.textContent = 'Mencari...';
    
    // Simulate form data
    const formData = new FormData();
    formData.append('nama', nama);
    
    fetch('/cari', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingEl.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.textContent = 'Cari';
        
        if (data.error) {
            hasilEl.innerHTML = `<div class="error">❌ ${data.error}</div>`;
        } else {
            displayResults(data.hasil);
        }
    })
    .catch(error => {
        loadingEl.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.textContent = 'Cari';
        hasilEl.innerHTML = '<div class="error">❌ Terjadi kesalahan saat mencari data.</div>';
        console.error('Error:', error);
    });
});

function displayResults(hasil) {
    const hasilEl = document.getElementById('hasil');
    let html = '';
    
    if (hasil.length > 1) {
        html += '<div class="multiple-results">📋 Ditemukan beberapa hasil yang cocok, diurutkan berdasarkan kecocokan terbaik:</div>';
    }
    
    html += '<div class="success">';
    
    hasil.forEach((item, index) => {
        html += `
            <div class="result-item">
                <div class="nama-lengkap">👤 ${item.nama_lengkap}</div>
                <div class="kelompok-info">📚 ${item.kelompok}</div>
                <div class="pembina-info">👨‍🏫 Kakak Pembina: ${item.kakak_pembina}</div>
            </div>
        `;
    });
    
    html += '</div>';
    hasilEl.innerHTML = html;
}

// Auto focus on input
document.getElementById('namaInput').focus();

// Enter key support
document.getElementById('namaInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('searchForm').dispatchEvent(new Event('submit'));
    }
});