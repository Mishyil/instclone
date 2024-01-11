// Функция для запроса количества непрочитанных уведомлений
function updateNotificationCount() {
	const url = '/notifications/unread-count/';
	fetch(url)
	  .then(response => {
		if (!response.ok) {
		  throw new Error(`HTTP error! status: ${response.status}`);
		}
		return response.json();
	  })
	  .then(data => {
		const counterElement = document.getElementById('notificationCounter');
		if (counterElement) {
		  if (data.unread_count > 0) {
			counterElement.textContent = data.unread_count;
			counterElement.style.display = 'inline'; // Показываем счетчик, если есть уведомления
		  } else {
			// Если уведомлений нет, не отображаем счетчик и не устанавливаем текст "0"
			counterElement.style.display = 'none';
		  }
		}
	  })
	  .catch(error => {
		console.error('Error fetching the notification count:', error);
	  });
  }
  


var host = window.location.host;
var protocol = window.location.protocol === "https:" ? "wss" : "ws";
var socketUrl = protocol + '://' + host + '/ws/notifications/';
var socket = new WebSocket(socketUrl);

socket.onopen = function(e) {
console.log('WebSocket connection established');
};

// Обновление счетчика через вебсокет
socket.onmessage = function(event) {
	var data = JSON.parse(event.data);
	console.log('Message from server:', data); 

	if(data.type === 'new_notification') {
		updateNotificationCount();
	}

};

// Вызов функции updateNotificationCount при полной загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
	// Проверка, находимся ли мы на странице уведомлений
	if (window.location.pathname === '/notifications/') {
	  markNotificationsAsRead();
	} else {
	  // Если мы не на странице уведомлений, обновляем количество уведомлений
	  updateNotificationCount();
	}
  });

// Обнуление счетчика количества сообщений
function markNotificationsAsRead() {
	fetch('/notifications/mark-read/', {
	  method: 'POST',
	  headers: {
		'X-CSRFToken': getCSRFToken(),
		'Content-Type': 'application/json',
	  },
	})
	.then(response => {
	  if (!response.ok) {
		throw new Error(`HTTP error! status: ${response.status}`);
	  }
	  return response.json();
	})
	.then(data => {
	  if (data.success) {
		const counterElement = document.getElementById('notificationCounter');
		if (counterElement) {
		  // Скрываем счетчик после подтверждения сервера, что уведомления прочитаны
		  counterElement.style.display = 'none';
		}
	  }
	})
	.catch(error => {
	  console.error('Error marking notifications as read:', error);
	});
  }
  
function getCSRFToken() {
	return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

if (window.location.pathname === '/notifications/') {
  markNotificationsAsRead();
}
