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
        card.className = 'bg-white/5 border border-white/10 rounded-xl overflow-hidden';
        card.innerHTML = `
            <div class="relative h-48 bg-gray-800">
                <img src="${v.primary_image || ''}" class="w-full h-full object-cover">
                ${v.featured ? '<span class="absolute top-2 left-2 bg-gold text-black px-2 py-1 rounded-full text-xs font-bold">Featured</span>' : ''}
            </div>
            <div class="p-4">
                <h3 class="font-bold">${v.title}</h3>
                <div class="text-sm text-gray-400">${v.year} • ${v.mileage} • ${v.transmission} • ${v.drive_type}</div>
                <div class="text-gold font-bold text-lg mt-2">₦${v.price.toLocaleString()}</div>
                <a href="https://wa.me/2348183533837?text=${encodeURIComponent(`I'm interested in ${v.title} (${v.year}) priced at ₦${v.price.toLocaleString()}`)}" target="_blank" class="mt-3 block text-center bg-gold text-black py-2 rounded-lg font-semibold">WhatsApp</a>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Brand filter
document.querySelectorAll('.brand-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.brand-btn').forEach(b => b.classList.remove('bg-gold/20','text-gold','border-gold/30'));
        btn.classList.add('bg-gold/20','text-gold','border-gold/30');
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

// Admin stats
async function loadStats() {
    const res = await fetch('/admin/api/stats');
    const stats = await res.json();
    document.getElementById('statTotal').textContent = stats.total;
    document.getElementById('statSale').textContent = stats.sale;
    document.getElementById('statRent').textContent = stats.rent;
    document.getElementById('statFeatured').textContent = stats.featured;
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
        row.className = 'border-b border-white/10';
        row.innerHTML = `
            <td class="px-4 py-3">${v.title}</td>
            <td class="px-4 py-3">${v.brand}</td>
            <td class="px-4 py-3">₦${v.price.toLocaleString()}</td>
            <td class="px-4 py-3">${v.listing_type}</td>
            <td class="px-4 py-3">
                <a href="/admin/edit/${v.id}" class="text-blue-400 mr-2">Edit</a>
                <button onclick="deleteVehicle(${v.id})" class="text-red-400">Delete</button>
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
