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
                    currentRow.className = 'row align-items-center justify-content-center';
                    mediaContainer.appendChild(currentRow);
                }

                const col = document.createElement('div');
                col.className = 'col-md-2';

                const cardHtml = `
                    <div class="card text-bg-dark h-100">
                        <img src="${media.image}" class="card-header card-img-top" alt="${media.title}">
                        <div class="card-body">
                            <h5 class="card-title">${media.title}</h5>
                            <p class="card-text">${media.description}</p>
                            <a href="#" class="btn btn-success">
                                <i class="bi bi-hand-thumbs-up-fill"> Gostei</i> ${media.likes}
                            </a>
                            <a href="#" class="btn btn-danger">
                                <i class="bi bi-hand-thumbs-down-fill"> Não Gostei</i> ${media.dislikes}
                            </a>
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