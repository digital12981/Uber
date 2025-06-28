/**
 * Sistema universal de precarregamento do cartão Uber
 * Carrega todas as imagens e recursos do cartão em background
 */

// Lista completa de todas as imagens do cartão
const CARD_IMAGES = [
    'https://i.ibb.co/Z6rZ8R1v/13093103960002-1-removebg-preview.png', // Logo Uber branco
    'https://i.ibb.co/wFFn5HSn/13093103960002-1.png', // Logo Uber original
    'https://i.ibb.co/B5B61LdW/Noti-cias-Dia-rias-Post-Feed-Para-Instagram-Vermelho-E-Branco-24-1-2-1-removebg-preview.png', // Logo parceiro
    'https://i.ibb.co/8DrZxqnq/c-HJpdm-F0-ZS9sci9pb-WFn-ZXMvd2-Vic2l0-ZS8y-MDIy-LTA3-L2pv-Yj-Ew-Njgt-ZWxlb-WVud-C1ja-Glw-LTAy-LWw1d.png', // Chip dourado
    'https://i.ibb.co/5h1TwChY/Noti-cias-Dia-rias-Post-Feed-Para-Instagram-Vermelho-E-Branco-25-1-1.png', // Mastercard logo
    'https://i.ibb.co/1JQ5QnxH/1-1.png', // Imagem do adesivo
];

// Função para precarregar todas as imagens do cartão
function preloadCardImages() {
    console.log('🚀 Precarregando imagens do cartão...');
    
    const promises = CARD_IMAGES.map(imageUrl => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                console.log('✅ Imagem precarregada:', imageUrl.split('/').pop());
                resolve(imageUrl);
            };
            img.onerror = () => {
                console.log('❌ Erro ao precarregar:', imageUrl.split('/').pop());
                reject(imageUrl);
            };
            img.src = imageUrl;
        });
    });
    
    // Também adicionar as imagens ao DOM invisível para forçar cache
    const preloadContainer = document.createElement('div');
    preloadContainer.style.cssText = 'position: absolute; opacity: 0; pointer-events: none; left: -9999px; top: -9999px; z-index: -1;';
    preloadContainer.id = 'card-preload-container';
    
    CARD_IMAGES.forEach(imageUrl => {
        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.cssText = 'width: 1px; height: 1px;';
        preloadContainer.appendChild(img);
    });
    
    // Remover container existente se houver
    const existingContainer = document.getElementById('card-preload-container');
    if (existingContainer) {
        existingContainer.remove();
    }
    
    document.body.appendChild(preloadContainer);
    
    return Promise.allSettled(promises);
}

// Função para precarregar fontes do cartão
function preloadCardFonts() {
    console.log('🔤 Precarregando fontes do cartão...');
    
    const fontPromises = [
        document.fonts.load('16px UberMoveText-Medium'),
        document.fonts.load('20px UberMoveText-Medium'),
        document.fonts.load('24px UberMoveText-Medium'),
    ];
    
    return Promise.allSettled(fontPromises).then(() => {
        console.log('✅ Fontes do cartão precarregadas');
    });
}

// Função principal de precarregamento automático
function autoPreloadCardAssets() {
    // Só executa se ainda não foi executado nesta sessão
    if (sessionStorage.getItem('cardAssetsPreloaded')) {
        console.log('📦 Assets do cartão já precarregados nesta sessão');
        return;
    }
    
    // Aguardar um pouco para não interferir no carregamento da página
    setTimeout(() => {
        Promise.all([
            preloadCardImages(),
            preloadCardFonts()
        ]).then(() => {
            sessionStorage.setItem('cardAssetsPreloaded', 'true');
            console.log('🎉 Todos os assets do cartão precarregados com sucesso!');
        });
    }, 1000);
}

// Executar automaticamente quando o script é carregado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoPreloadCardAssets);
} else {
    autoPreloadCardAssets();
}

// Também expor a função para uso manual
window.preloadCardAssets = autoPreloadCardAssets;
window.preloadCardImages = preloadCardImages;