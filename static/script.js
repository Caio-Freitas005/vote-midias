// Espera o conteúdo da página ser totalmente carregado 
document.addEventListener('DOMContentLoaded', () => {

    const registerForm = document.getElementById('register-form');
    const registerModalElement = document.getElementById('registerModal');
    const registerModal = new bootstrap.Modal(registerModalElement);

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const mediaData = {
            title: document.getElementById('media-title').value,
            genre: document.getElementById('media-genre').value,
            description: document.getElementById('media-description').value,
            image: document.getElementById('media-image').value
        };

        try {
            const response = await fetch('/medias', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(mediaData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha ao cadastrar a mídia.');
            }

            registerModal.hide();
            registerForm.reset(); // Limpa os campos do formulário
            
            await loadMedias(); 
            await loadTotals();

        } catch (error) {
            console.error('Erro ao cadastrar:', error);
            showErrorToast(error.message);
        }
    });

    const mediaContainer = document.getElementById('media-container');

    function showErrorToast(message) {
        const errorToastElement = document.getElementById('errorToast');
        const errorToastBody = document.getElementById('errorToastBody');

        const errorToast = new bootstrap.Toast(errorToastElement);

        errorToastBody.textContent = message;

        errorToast.show();
    }

    async function loadTotals() {
        try {
            const response = await fetch('/medias/totals');
            if (!response.ok) {
                console.error('Não foi possível carregar os totais.');
                return;
            }
            const totals = await response.json();

            const totalLikesElement = document.getElementById('total-likes');
            const totalDislikesElement = document.getElementById('total-dislikes');

            if (totalLikesElement && totalDislikesElement) {
                totalLikesElement.textContent = totals.total_likes;
                totalDislikesElement.textContent = totals.total_dislikes;
            }

        } catch (error) {
            console.error('Erro ao carregar totais:', error);
        }
    }

    mediaContainer.addEventListener('click', (e) => {
        const clickedButton = e.target.closest('.vote-btn');

        if (!clickedButton) {
            return;
        }

        e.preventDefault();

        const mediaId = clickedButton.dataset.id;
        const voteType = clickedButton.dataset.type;

        handleVote(mediaId, voteType);
    });

    async function handleVote(mediaId, voteType) {
        try {
            const url = `/medias/${mediaId}/${voteType}`;

            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            const response = await fetch(url, options);

            if (!response.ok) {
                throw new Error('Falha ao registrar o voto.');
            }

            const updatedMedia = await response.json();

            // Encontra os botões pelos seus IDs únicos
            const likesButton = document.getElementById(`likes-count-${mediaId}`);
            const dislikesButton = document.getElementById(`dislikes-count-${mediaId}`);

            if (likesButton && dislikesButton) {
                // Reconstrói o conteúdo de cada botão, mantendo o ícone
                likesButton.innerHTML = `<i class="bi bi-hand-thumbs-up-fill"></i> ${updatedMedia.likes}`;
                dislikesButton.innerHTML = `<i class="bi bi-hand-thumbs-down-fill"></i> ${updatedMedia.dislikes}`;
            }

            loadTotals();

        } catch (error) {
            console.error(`Erro ao votar: ${error}`);
            showErrorToast('Não foi possível registrar o seu voto. Tente novamente mais tarde.');
        }
    }

    async function loadMedias() {
        try {
            const response = await fetch('/medias');
            if (!response.ok) {
                throw new Error ('Falha ao carregar os dados da API.')
            }
            const medias = await response.json();
            
            mediaContainer.innerHTML = '';

            if (medias.length == 0) {
                mediaContainer.innerHTML = '<p class="text-center">Nenhuma mídia encontrada.</p>';
                return;
            }

            let currentRow;

            medias.forEach((media, index) => {
                // Adiciona nova linha a cada 5 índices percorridos, garantindo que 5 colunas serão criadas para cada linha
                if (index % 5 === 0) {
                    currentRow = document.createElement('div');
                    currentRow.className = 'row align-items-stretch justify-content-center';
                    mediaContainer.appendChild(currentRow);
                }

                const col = document.createElement('div');
                col.className = 'col-lg-2 col-md-4 col-sm-6 mb-4';

                const cardHtml = `
                    <div class="card text-bg-dark h-100 d-flex flex-column">
                        <img src="${media.image}" class="card-img-top" alt="${media.title}" style="height: 180px; object-fit: cover;">
                        <div class="card-body d-flex flex-column flex-grow-1"> 
                            <h5 class="card-title">${media.title}</h5>
                            <p class="card-text small">${media.description}</p>
                            <div class="mt-auto pt-3">
                                <p class="mb-2">
                                    <a id="likes-count-${media.id}" class="btn btn-outline-success vote-btn" data-id="${media.id}" data-type="like">
                                        <i class="bi bi-hand-thumbs-up-fill"></i> ${media.likes}
                                    </a>
                                    <a id="dislikes-count-${media.id}" class="btn btn-outline-danger vote-btn ms-2" data-id="${media.id}" data-type="dislike">
                                        <i class="bi bi-hand-thumbs-down-fill"></i> ${media.dislikes}
                                    </a>
                                </p>
                            </div>
                        </div>
                    </div>
                `;
                
                col.innerHTML = cardHtml;
                currentRow.appendChild(col);
            });
        } catch (error) {
            console.error('Erro:', error);
            mediaContainer.innerHTML = '<p class="text-danger text-center">Não foi possível carregar as mídias.</p>';
            showErrorToast('Não foi possível carregar as mídias da API.');
        }
    }

    loadMedias();
    loadTotals();
});