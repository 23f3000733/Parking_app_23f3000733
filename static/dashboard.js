// Dashboard Modal Logic

document.addEventListener('DOMContentLoaded', function() {
  // DOM elements for booking modal
  const bookingModal = document.getElementById('bookingModal');
  const closeBookingModal = document.getElementById('closeBookingModal');
  const bookingForm = document.getElementById('dashboard-booking-form');
  const spotSelect = document.getElementById('dashboard-spot-select');
  const ratePerHourEl = document.getElementById('dashboard-rate-per-hour');
  const totalPriceEl = document.getElementById('dashboard-total-price');
  const startTimeInput = document.getElementById('dashboard-start-time');
  const endTimeInput = document.getElementById('dashboard-end-time');
  const noSpotsMessage = document.getElementById('no-spots-message');

  // When start or end time changes, fetch available spots for the selected lot and time window
  function fetchAvailableSpots(lot) {
    const startTime = startTimeInput.value;
    const endTime = endTimeInput.value;
    if (!startTime || !endTime) return;
    const formData = new FormData();
    formData.append('query', lot.prime_location_name);
    formData.append('start_time', startTime);
    formData.append('end_time', endTime);
    fetch('/user/search_parking_ajax', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(results => {
      const lotResult = results.find(l => l.id === lot.id);
      spotSelect.innerHTML = '';
      if (!lotResult || lotResult.spots.length === 0) {
        spotSelect.innerHTML = '<option value="">No spots available</option>';
        bookingForm.querySelector('button[type="submit"]').disabled = true;
        noSpotsMessage.style.display = 'block';
      } else {
        lotResult.spots.forEach(spot => {
          spotSelect.innerHTML += `<option value="${spot.id}">Spot #${spot.number}</option>`;
        });
        bookingForm.querySelector('button[type="submit"]').disabled = false;
        noSpotsMessage.style.display = 'none';
      }
      // Keep hidden input in sync
      document.getElementById('dashboard-spot-id').value = lotResult && lotResult.spots.length > 0 ? lotResult.spots[0].id : '';
    });
  }

  // Patch openBookingModal to use AJAX spot fetching
  window.openBookingModal = function(lot, spotId) {
    window.currentLotRate = lot.rate;
    ratePerHourEl.textContent = lot.rate;
    totalPriceEl.textContent = 0;
    startTimeInput.value = '';
    endTimeInput.value = '';
    setMinDate();
    bookingModal.style.display = 'block';
    // Fetch spots when modal opens (if times are already set)
    fetchAvailableSpots(lot);
    // On time change, refetch
    startTimeInput.onchange = endTimeInput.onchange = function() {
      fetchAvailableSpots(lot);
    };
  };

  function setMinDate() {
    const nowISO = new Date().toISOString().slice(0,16);
    startTimeInput.min = nowISO;
    endTimeInput.min = nowISO;
  }

  // Restrict booking to only the next two days from today
  const now = new Date();
  const minDate = now.toISOString().slice(0,16);
  const maxDate = new Date(now.getTime() + 2 * 24 * 60 * 60 * 1000).toISOString().slice(0,16);
  document.getElementById('dashboard-start-time').min = minDate;
  document.getElementById('dashboard-end-time').min = minDate;
  document.getElementById('dashboard-start-time').max = maxDate;
  document.getElementById('dashboard-end-time').max = maxDate;

  // Close modal logic
  if (closeBookingModal) {
    closeBookingModal.onclick = function() {
      bookingModal.style.display = 'none';
    };
  }
  window.onclick = function(event) {
    if (event.target == bookingModal) bookingModal.style.display = 'none';
  };

  // Calculate total price
  function calculateTotal() {
    const spotId = spotSelect.value;
    const rate = window.currentLotRate || 0;
    const start = new Date(startTimeInput.value);
    const end = new Date(endTimeInput.value);
    let hours = (end - start) / (1000 * 60 * 60);
    if (isNaN(hours) || hours <= 0) {
      totalPriceEl.textContent = 0;
      return;
    }
    totalPriceEl.textContent = Math.ceil(hours) * rate;
  }
  [startTimeInput, endTimeInput, spotSelect].forEach(input => {
    input.addEventListener('input', calculateTotal);
  });
  // Keep hidden input in sync with dropdown
  spotSelect.addEventListener('change', function() {
    document.getElementById('dashboard-spot-id').value = this.value;
  });
}); 