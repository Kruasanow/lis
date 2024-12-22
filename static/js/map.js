let listcoord = {};

function addMap() {
    const map = L.map('map').setView({lon: 0, lat: 0}, 2);
    let selectedCoordinates = null;

    // Получаем элементы формы
    const latInput = document.querySelector('input[name="latitude"]');
    const lonInput = document.querySelector('input[name="longitude"]');
    const form = document.getElementById('sendevent');

    let currentMarker = null;

    // Функция для отображения выбранных координат в форме
    function updateForm(lat, lon) {
        latInput.value = lat;
        lonInput.value = lon;
    }

    // Функция для подтверждения выбранных координат
    function confirmCoordinates(lat, lon) {
        // Добавляем или обновляем координаты в объекте
        listcoord['latitude'] = lat;
        listcoord['longitude'] = lon;
        console.log("Confirmed coordinates:", listcoord);
    }

    // Обработчик клика по карте
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;

        if (currentMarker !== null) {
            map.removeLayer(currentMarker);
        };

        function addlistmarkers() {
            currentMarker = L.marker([lat, lon]).bindPopup('pizda').addTo(map);
        }
        addlistmarkers();

        // Отображаем координаты в форме
        updateForm(lat, lon);

        // Подтверждаем координаты после клика
        confirmCoordinates(lat, lon);
    });

    // Логика отправки формы
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Добавляем координаты в данные
        // jsonData['latitude'] = listcoord.latitude;
        // jsonData['longitude'] = listcoord.longitude;

        $(document).ready(function() {
          $('#sendevent').on('submit', function(event) {
              event.preventDefault();  // Предотвращаем стандартное поведение формы

              var formData = new FormData();  // Создаем объект FormData

              // Получаем данные из формы
              formData.append('latitude', $('input[name="latitude"]').val());
              formData.append('longitude', $('input[name="longitude"]').val());
              formData.append('description', $('textarea[name="description"]').val());
              formData.append('short', $('input[name="short"]').val());
              formData.append('story', $('textarea[name="story"]').val());
              formData.append('privates', $('input[name="privates"]').val());

              // Получаем файл изображения
              var imgFile = $('input[name="img"]')[0].files[0];
              if (imgFile) {
                  formData.append('img', imgFile);
              }

              // Отправляем данные на сервер с помощью AJAX
              $.ajax({
                  url: '/upload',  // Путь на сервере, который будет обрабатывать данные
                  type: 'POST',
                  data: formData,
                  contentType: false,  // Чтобы jQuery не устанавливала contentType автоматически
                  processData: false,  // Чтобы jQuery не пыталась преобразовать данные
                  success: function(response) {
                      $('#message').html('<p>Форма успешно отправлена!</p>');
                  },
                  error: function(xhr, status, error) {
                      $('#message').html('<p>Ошибка: ' + error + '</p>');
                  }
              });
          });
      });

    });

    // Добавляем карту с OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: 'OpenStreetMap'
    }).addTo(map);

    // Добавляем масштаб
    L.control.scale().addTo(map);
}

addMap();