document.addEventListener('DOMContentLoaded', function() {
	let likeButtons = document.querySelectorAll('.like-button');

	likeButtons.forEach(button => {
		button.addEventListener('click', function(event) {
			event.preventDefault();
			let photoId = button.dataset.photoId;
			let icon = button.querySelector('.fa-heart');

			const formData = new FormData();
			formData.append('toggle_like', 'toggle_like');
			formData.append('photo_id', photoId);
			
			fetch(`/tools/like/`, {
				method: 'POST',
				headers: {
					'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
				},
				body: formData
			})
			.then(response => response.json())
			.then(data => {
				if (data.liked) {
					icon.classList.add('liked');
				} else {
					icon.classList.remove('liked');
				}
			});
		});
	});
});

function showSelectedPhoto(event) {
	var selectedPhotoContainer = document.getElementById('selectedPhotoContainer');
	var selectedPhoto = document.getElementById('selectedPhoto');
	var confirmButton = document.getElementById('confirmButton');

	if (event.target.files && event.target.files[0]) {
			var reader = new FileReader();

			reader.onload = function(e) {
					selectedPhoto.src = e.target.result;
					selectedPhotoContainer.style.display = 'block';
					confirmButton.style.display = 'block';
			}

			reader.readAsDataURL(event.target.files[0]);
	} else {
			selectedPhotoContainer.style.display = 'none';
			confirmButton.style.display = 'none';
	}
}

function confirmUpload() {
	document.getElementById('uploadButton').click();
}

document.getElementById('openModal').addEventListener('click', function(event) {
	var modal = document.getElementById('myModal');
	modal.style.display = 'block';

	var span = document.getElementsByClassName('close')[0];
	span.onclick = function() {
			modal.style.display = 'none';
	}

	window.onclick = function(event) {
			if (event.target == modal) {
					modal.style.display = 'none';
			}
	}
});

document.addEventListener("DOMContentLoaded", function() {
	const commentAreas = document.querySelectorAll(".comment__area");
	const sendButtons = document.querySelectorAll(".card__send__comment");

	commentAreas.forEach((commentArea, index) => {
		const sendButton = sendButtons[index];

		commentArea.addEventListener("input", function() {
			if (commentArea.value.trim() !== "") {
				sendButton.style.display = "block";
			} else {
				sendButton.style.display = "none";
			}
		});
	});
});


document.addEventListener('DOMContentLoaded', function() {
    const editProfileButton = document.getElementById('editProfileButton');
    const deleteButtons = document.querySelectorAll('.deleteButton');
    const uploadBtn = document.querySelector('.fa-circle-plus.upload_btn');
	const avatarUploadInput = document.getElementById('avatarUpload');

		
    // Переключение отображения кнопок удаления и кнопки загрузки изображения
    editProfileButton.addEventListener('click', function(event) {
        event.preventDefault();

        deleteButtons.forEach(button => {
            button.style.display = (button.style.display === 'none' || !button.style.display) ? 'block' : 'none';
        });

        if (uploadBtn) {
            uploadBtn.style.display = (uploadBtn.style.display === 'none' || !uploadBtn.style.display) ? 'block' : 'none';
        }
    });

    // Обработчики для кнопок удаления
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            event.preventDefault();

            let confirmation = confirm("Вы действительно хотите удалить эту фотографию?");
            if (confirmation) {
                const photo = button.parentElement;
                const photoId = photo.dataset.id;

                let formData = new FormData();
                formData.append('delete-photo', '');

                fetch('/tools/delete_photo/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: 'photo_id=' + photoId
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload(); 
                    } else {
                        alert('Ошибка при загрузке аватара!');
                    }
                });
            }
        });
    });

    // Обработчик для кнопки загрузки изображения
    if (uploadBtn) {
        const avatarUploadInput = document.getElementById('avatarUpload');
        uploadBtn.addEventListener('click', function() {
            avatarUploadInput.click();
        });
    }

    // Обработчик события изменения для input[type="file"]
    if (avatarUploadInput) {
        avatarUploadInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                // Создание FormData объекта и добавление выбранного файла
                const formData = new FormData();
                formData.append('file', this.files[0]);
                formData.append('upload-avatar', 'upload-avatar');

                // Отправка FormData на сервер
                fetch('/tools/upload_avatar/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Ошибка при загрузке аватара!');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
            }
        });
    }
});