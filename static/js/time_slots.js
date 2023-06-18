
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Selected table change event handler
function handleTableChange() {
  var tableId = document.getElementById('table_number').value;
  console.log('Selected tableId:', tableId);
  var csrftoken = getCookie('csrftoken');

  fetch('/get_time_slots/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({ table_id: tableId })
  })
    .then(response => response.json())
    .then(data => {
      // Handling the response from the view get_time_slots
      if (data && data.time_slots && data.time_slots.length > 0) {
        var timeSlotsContainer = document.getElementById('time_slots_container');
        var reservationTimeSelect = document.getElementById('reservation_time');
        reservationTimeSelect.innerHTML = '';
        for (var i = 0; i < data.time_slots.length; i++) {
          var option = document.createElement('option');
          option.value = data.time_slots[i];
          option.text = data.time_slots[i];
          reservationTimeSelect.appendChild(option);
        }
        reservationTimeSelect.disabled = false;
      } else {
        var reservationTimeSelect = document.getElementById('reservation_time');
        reservationTimeSelect.innerHTML = '';
        var option = document.createElement('option');
        option.disabled = true;
        option.text = 'No time slots available';
        reservationTimeSelect.appendChild(option);
        reservationTimeSelect.disabled = true;
      }
    })
    .catch(error => {
      console.error('Request failed:', error);
    });
}

// Assigning an event handler for the selected table change event
document.getElementById('table_number').addEventListener('change', handleTableChange);
