document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var currentDate = new Date();
  
    // Function to fetch availability data from Flask route
    function fetchAvailabilityData() {
      return fetch('/availability')
        .then((response) => response.json());
    }
  
    // Function to generate the calendar
    function generateCalendar() {
      var calendar = document.createElement('div');
      calendar.classList.add('calendar');
  
      var header = document.createElement('div');
      header.classList.add('calendar-header');
      header.textContent = currentDate.toLocaleString('en-US', { month: 'long', year: 'numeric' });
      calendar.appendChild(header);
  
      var days = document.createElement('div');
      days.classList.add('calendar-days');
  
      var weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      weekdays.forEach(function (day) {
        var dayElement = document.createElement('div');
        dayElement.classList.add('calendar-day');
        dayElement.textContent = day;
        days.appendChild(dayElement);
      });
  
      calendar.appendChild(days);
      calendarEl.appendChild(calendar);
    }
  
    // Function to highlight available dates
    function highlightAvailableDates(availabilityData) {
      var calendarDates = document.getElementsByClassName('calendar-date');
  
      Array.from(calendarDates).forEach(function (dateElement) {
        var date = dateElement.dataset.date;
  
        if (availabilityData.some(function (data) {
          return data.start === date;
        })) {
          dateElement.classList.add('available');
        }
      });
    }
  
    // Function to handle date selection
    function handleDateSelection(event) {
      var selectedDate = event.target.dataset.date;
      console.log('Selected date:', selectedDate);
      // Implement your logic here for handling the selected date
    }
  
    generateCalendar();
    fetchAvailabilityData().then(function (availabilityData) {
      highlightAvailableDates(availabilityData);
    });
    
  calendarEl.addEventListener('click', handleDateSelection);

  function handleDateSelection(event) {
    var selectedDate = event.target.dataset.date;
    console.log('Selected date:', selectedDate);
    // Implement your logic here for handling the selected date
  }
});