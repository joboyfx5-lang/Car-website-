// Fetch and render vehicles
let currentBrand = 'All Brands';

async function fetchVehicles() {
    const params = new URLSearchParams();
    if (currentBrand !== 'All Brands') params.append('brand', currentBrand);
    const q = document.getElementById('searchInput')?.value;
    const condition = document.getElementById('conditionFilter')?.value;
    const listing_type = document.getElementById('listingTypeFilter')?.value;
    const body_style = document.getElementById('bodyStyleFilter')?.value;
    const drive_type = document.getElementById('driveTypeFilter')?.value;
    const min_price = document.getElementById('minPrice')?.value;
    const max_price = document.getElementById('maxPrice')?.value;
    if (q) params.append('q', q);
    if (condition) params.append('condition', condition);
    if (listing_type) params.append('listing_type', listing_type);
    if (body_style) params.append('body_style', body_style);
    if (drive_type) params.append('drive_type', drive_type);
    if (min_price) params.append('min_price', min_price);
    if (max_price) params.append('max_price', max_price);

    const res = await fetch(`/api/vehicles?${params}`);
    const vehicles = await res.json();
    const grid = document.getElementById('vehicleGrid');
    grid.innerHTML = '';
    vehicles.forEach(v => {
        const card = document.createElement('div');
        card.className = 'vehicle-card';
        card.innerHTML = `
            <img src="${v.primary_image || ''}" alt="${v.title}">
            <div class="body">
                <h3>${v.title}</h3>
                <div class="specs">${v.year} • ${v.mileage} • ${v.transmission} • ${v.drive_type}</div>
                ${v.customs_verified ? '<span class="badge duty-paid">Duty Paid ✅</span>' : ''}
                <div class="price">₦${v.price.toLocaleString()}</div>
                <a href="/vehicle/${v.id}" class="details-link">View Details</a>
                <a href="https://wa.me/2348183533837?text=${encodeURIComponent(`I'm interested in ${v.title} (${v.year}) priced at ₦${v.price.toLocaleString()}. Listing ID: ${v.id}`)}" target="_blank" class="whatsapp-link" onclick="trackLead(${v.id})">Chat on WhatsApp</a>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Brand filter
document.querySelectorAll('.brand-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.brand-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentBrand = btn.dataset.brand;
        fetchVehicles();
    });
});

// Input listeners
['searchInput','conditionFilter','listingTypeFilter','bodyStyleFilter','driveTypeFilter','minPrice','maxPrice'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', fetchVehicles);
});

// Initial load
if (document.getElementById('vehicleGrid')) fetchVehicles();

// Lead tracking
async function trackLead(vehicleId) {
    try {
        await fetch('/track-lead', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({vehicle_id: vehicleId, source: 'whatsapp'})
        });
    } catch(e) { console.error('Lead tracking failed', e); }
}

// Admin stats
async function loadStats() {
    const res = await fetch('/admin/api/stats');
    const stats = await res.json();
    document.getElementById('statTotal').textContent = stats.total;
    document.getElementById('statSale').textContent = stats.sale;
    document.getElementById('statRent').textContent = stats.rent;
    document.getElementById('statFeatured').textContent = stats.featured;
    document.getElementById('statLeads').textContent = stats.leads;
}
if (document.getElementById('statTotal')) loadStats();

// Admin table
async function loadAdminTable() {
    const res = await fetch('/api/vehicles');
    const vehicles = await res.json();
    const tbody = document.getElementById('adminVehicleTable');
    if (!tbody) return;
    tbody.innerHTML = '';
    vehicles.forEach(v => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${v.title}</td>
            <td>${v.brand}</td>
            <td>₦${v.price.toLocaleString()}</td>
            <td>${v.listing_type}</td>
            <td>
                <a href="/admin/edit/${v.id}">Edit</a>
                <button onclick="deleteVehicle(${v.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}
if (document.getElementById('adminVehicleTable')) loadAdminTable();

async function deleteVehicle(id) {
    if (confirm('Delete this vehicle?')) {
        await fetch(`/admin/delete/${id}`, { method: 'POST' });
        loadAdminTable();
        loadStats();
    }
}

// Loan Calculator
function showCalculator() {
    document.getElementById('calculatorModal').classList.add('active');
}
function hideCalculator() {
    document.getElementById('calculatorModal').classList.remove('active');
}
function calculateLoan(price) {
    const down = parseFloat(document.getElementById('downPayment').value) || 0;
    const rate = parseFloat(document.getElementById('interestRate').value) || 0;
    const term = parseFloat(document.getElementById('loanTerm').value) || 60;
    const principal = price - down;
    const monthlyRate = rate / 100 / 12;
    const monthlyPayment = (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -term));
    document.getElementById('loanResult').innerHTML = `
        <p>Monthly Payment: ₦${monthlyPayment.toFixed(2)}</p>
        <p>Total Payment: ₦${(monthlyPayment * term).toFixed(2)}</p>
    `;
}
