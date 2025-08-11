// Espera o conteúdo da página ser totalmente carregado 
document.addEventListener('DOMContentLoaded', () => {

    const mediaContainer = document.getElementById('media-container');
    const registerForm = document.getElementById('register-form');
    const registerModalElement = document.getElementById('registerModal');
    const registerModal = new bootstrap.Modal(registerModalElement);
    const modalTitle = document.getElementById('registerModalLabel');

    function showErrorToast(message) {
        const errorToastElement = document.getElementById('errorToast');
        const errorToastBody = document.getElementById('errorToastBody');

        const errorToast = new bootstrap.Toast(errorToastElement);

        errorToastBody.textContent = message;

        errorToast.show();
    }

    function showSuccessToast(message) {
        const successToastElement = document.getElementById('successToast');
        const successToastBody = document.getElementById('successToastBody');
        
        const successToast = new bootstrap.Toast(successToastElement);
        
        successToastBody.textContent = message;
        
        successToast.show();
    }

    // Lógica do formulário (cadastro e edição)
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const editingId = registerForm.dataset.editingId;

        const mediaData = {
            title: document.getElementById('media-title').value,
            genre: document.getElementById('media-genre').value,
            description: document.getElementById('media-description').value,
            image: document.getElementById('media-image').value
        };

        try {
            let response;
            const url = editingId ? `/medias/${editingId}` : '/medias';
            const method = editingId ? 'PUT' : 'POST';

            response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(mediaData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha na operação.');
            }

            registerModal.hide();
            showSuccessToast(`Mídia ${editingId ? 'atualizada' : 'cadastrada'} com sucesso!`);
            loadPage(); // Recarrega a página para mostrar as alterações

        } catch (error) {
            console.error('Erro no formulário:', error);
            showErrorToast(error.message);
        }
    });

    // Limpa o formulário quando o modal é fechado
    registerModalElement.addEventListener('hidden.bs.modal', () => {
        registerForm.reset();
        modalTitle.textContent = 'Cadastrar Nova Mídia';
        delete registerForm.dataset.editingId; // Garante que o modo "edição" é limpo
    });

    // Ouvinte único de eventos
    mediaContainer.addEventListener('click', async (e) => {
        const voteButton = e.target.closest('.vote-btn');
        const editButton = e.target.closest('.edit-btn');
        const deleteButton = e.target.closest('.delete-btn');

        if (voteButton) {
            e.preventDefault();
            handleVote(voteButton.dataset.id, voteButton.dataset.type);
        }

        if (editButton) {
            e.preventDefault();
            handleEdit(editButton.dataset.id);
        }

        if (deleteButton) {
            e.preventDefault();
            handleDelete(deleteButton.dataset.id);
        }
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

            await loadTotals();

        } catch (error) {
            console.error(`Erro ao votar: ${error}`);
            showErrorToast('Não foi possível registrar o seu voto. Tente novamente mais tarde.');
        }
    }

    async function handleEdit(mediaId) {
        try {
            const response = await fetch(`/medias/${mediaId}`);
            if (!response.ok) throw new Error('Mídia não encontrada para edição.');
            const media = await response.json();
            
            modalTitle.textContent = 'Editar Mídia';
            document.getElementById('media-title').value = media.title;
            document.getElementById('media-genre').value = media.genre;
            document.getElementById('media-description').value = media.description;
            document.getElementById('media-image').value = media.image;
            registerForm.dataset.editingId = media.id;
        } catch (error) {
            showErrorToast(error.message);
        }
    }

    async function handleDelete(mediaId) {
        if (confirm('Tem certeza que quer apagar esta mídia?')) {
            try {
                const response = await fetch(`/medias/${mediaId}`, { method: 'DELETE' });
                if (!response.ok) throw new Error('Falha ao deletar a mídia.');
                showSuccessToast('Mídia deletada com sucesso!');
                loadPage(); // Recarrega tudo
            } catch (error) {
                showErrorToast(error.message);
            }
        }
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

                const safeTitle = DOMPurify.sanitize(media.title);
                const safeDescription = DOMPurify.sanitize(media.description);
                const safeImage = DOMPurify.sanitize(media.image);
                const safeLikes = DOMPurify.sanitize(media.likes);
                const safeDislikes = DOMPurify.sanitize(media.dislikes);
                const safeGenre = DOMPurify.sanitize(media.genre);

                const cardHtml = `
                    <div class="card shadow text-bg-dark h-100 d-flex flex-column">
                        <img src="${safeImage}" class="card-img-top" alt="${safeTitle}" style="height: 180px; object-fit: cover;">
                        <div class="card-body d-flex flex-column flex-grow-1"> 
                            <h5 class="card-title">${safeTitle}</h5>
                            <p class="card-text small">${safeDescription}</p>
                            <div class="text-start mb-2">
                                <span class="badge badge-genre">${safeGenre}</span>
                            </div>
                            <div class="mt-auto pt-3">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="vote-buttons">
                                        <a id="likes-count-${media.id}" class="btn text-like btn-outline-success vote-btn" data-id="${media.id}" data-type="like">
                                            <i class="bi bi-hand-thumbs-up-fill"></i> ${safeLikes}
                                        </a>
                                        <a id="dislikes-count-${media.id}" class="btn text-dislike btn-outline-danger vote-btn ms-2" data-id="${media.id}" data-type="dislike">
                                            <i class="bi bi-hand-thumbs-down-fill"></i> ${safeDislikes}
                                        </a>
                                    </div>
                                    <div class="action-buttons">
                                        <a class="btn btn-outline-warning edit-btn" data-id="${media.id}" data-bs-toggle="modal" data-bs-target="#registerModal">
                                            <i class="bi bi-pencil-fill"></i>
                                        </a>
                                        <a class="btn text-dislike btn-outline-danger delete-btn ms-2" data-id="${media.id}">
                                            <i class="bi bi-trash-fill"></i>
                                        </a>
                                    </div>
                                </div>
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

    async function loadPage() {
        await loadMedias();
        await loadTotals();
    }

    loadPage();
});