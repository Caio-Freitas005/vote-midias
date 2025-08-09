// Espera o conteúdo da página ser totalmente carregado 
document.addEventListener('DOMContentLoaded', () => {

    const mediaContainer = document.getElementById('media-container');

    async function loadMedias() {
        try {
            const response = await fetch('http://localhost:8000/medias');
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
                                    <span class="badge text-bg-success">
                                        <i class="bi bi-hand-thumbs-up-fill"></i> ${media.likes}
                                    </span>
                                    <span class="badge text-bg-danger ms-2">
                                        <i class="bi bi-hand-thumbs-down-fill"></i> ${media.dislikes}
                                    </span>
                                </p>
                                <a href="#" class="btn btn-outline-success btn-sm">Gostei</a>
                                <a href="#" class="btn btn-outline-danger btn-sm">Não Gostei</a>
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
        }
    }

    loadMedias();
});