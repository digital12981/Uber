/**
 * Sistema de Proteção Ultimate JavaScript
 * Detecta e bloqueia Electron, SaveWeb2Zip, HTTrack e outras ferramentas de clonagem
 */

(function() {
    'use strict';
    
    // Verifica ambiente Replit PRIMEIRO
    function isReplitEnvironment() {
        return window.location.hostname.includes('replit.') || 
               window.location.hostname.includes('.repl.co') ||
               window.location.hostname.includes('replit.app') ||
               window.location.hostname.includes('replit.dev');
    }
    
    // Se está no Replit, desativa proteção completamente
    if (isReplitEnvironment()) {
        console.log('🔧 Ultimate protection disabled in Replit environment');
        return;
    }
    
    let protectionActive = true;
    let detectionAttempts = 0;
    const maxDetectionAttempts = 5;
    
    // Assinaturas de ferramentas de clonagem
    const cloningSiganturas = {
        electron: [
            'electron', 'electronjs', 'electronapp', 'nativefier',
            'desktop app', 'wrapped app', 'tauri'
        ],
        cloningTools: [
            'saveweb2zip', 'httrack', 'webcopier', 'teleport',
            'offline explorer', 'web ripper', 'sitesuck',
            'webzip', 'grab', 'copier', 'downloader',
            'webhttrack', 'winhttrack', 'sitesucker',
            'ivisit', 'webripper', 'getleft', 'webwhacker',
            'backstreet browser', 'pavuk', 'webbandit',
            'blue squirrel', 'mass downloader', 'download ninja',
            'cyotek webcopy', 'visual web ripper', 'screaming frog',
            'website extractor', 'website ripper copier',
            'website downloader', 'web scraper', 'web grabber'
        ],
        bots: [
            'bot', 'spider', 'crawler', 'scraper', 'fetcher',
            'python', 'java', 'curl', 'wget', 'requests',
            'selenium', 'phantomjs', 'headless', 'playwright',
            'puppeteer', 'chromedriver', 'webdriver',
            'scrapy', 'beautifulsoup', 'mechanize'
        ]
    };
    
    // Detecta se está rodando em Electron
    function detectElectron() {
        // Método 1: Verifica se o processo do Electron existe
        if (typeof window !== 'undefined' && window.process && window.process.type) {
            return true;
        }
        
        // Método 2: Verifica variáveis globais do Electron
        if (typeof window !== 'undefined' && (window.require || window.electron)) {
            return true;
        }
        
        // Método 3: Verifica User Agent
        const userAgent = navigator.userAgent.toLowerCase();
        for (const signature of cloningSiganturas.electron) {
            if (userAgent.includes(signature)) {
                return true;
            }
        }
        
        // Método 4: Verifica se tem APIs específicas do Electron
        if (typeof window !== 'undefined' && window.electronAPI) {
            return true;
        }
        
        // Método 5: Verifica se tem require do Node.js
        if (typeof require !== 'undefined') {
            try {
                require('electron');
                return true;
            } catch (e) {
                // Electron não disponível
            }
        }
        
        // Método 6: Verifica propriedades específicas do Electron
        if (typeof window !== 'undefined' && window.webContents) {
            return true;
        }
        
        return false;
    }
    
    // Detecta ferramentas de clonagem
    function detectCloningTools() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        // Verifica todas as ferramentas de clonagem
        const allTools = [...cloningSiganturas.cloningTools, ...cloningSiganturas.bots];
        
        for (const tool of allTools) {
            if (userAgent.includes(tool)) {
                return true;
            }
        }
        
        return false;
    }
    
    // Detecta se é um navegador desktop fingindo ser mobile
    function detectMobileSpoofing() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        // Tem indicadores móveis
        const hasMobile = /mobile|android|iphone|ipad|ipod/.test(userAgent);
        
        if (hasMobile) {
            // Mas também tem indicadores desktop
            const hasDesktop = /windows nt|macintosh|linux x86_64|wow64|win64|x11/.test(userAgent);
            
            if (hasDesktop) {
                return true; // Spoofing detectado
            }
        }
        
        return false;
    }
    
    // Verifica se a tela é muito grande para ser mobile
    function detectLargeScreen() {
        if (window.screen) {
            const width = window.screen.width;
            const height = window.screen.height;
            
            // Telas maiores que 1200px são suspeitas para mobile
            if (width > 1200 || height > 1200) {
                return true;
            }
        }
        
        return false;
    }
    
    // Detecta se não tem capacidade de toque
    function detectNoTouch() {
        // Verifica se suporta eventos de toque
        const hasTouch = 'ontouchstart' in window || 
                        navigator.maxTouchPoints > 0 || 
                        navigator.msMaxTouchPoints > 0;
        
        // Se não tem toque, provavelmente é desktop
        return !hasTouch;
    }
    
    // Detecta developer tools abertos
    function detectDevTools() {
        const threshold = 160;
        
        // Verifica diferença entre janela externa e interna
        const widthDiff = window.outerWidth - window.innerWidth;
        const heightDiff = window.outerHeight - window.innerHeight;
        
        return widthDiff > threshold || heightDiff > threshold;
    }
    
    // Detecta se está em iframe (tentativa de embedding)
    function detectIframe() {
        return window.top !== window.self;
    }
    
    // Detecta características específicas do ambiente
    function detectEnvironmentTampering() {
        const suspiciousChecks = [
            // Verifica se console foi modificado
            () => {
                const originalLog = console.log;
                try {
                    console.log = function() {};
                    if (console.log !== originalLog) {
                        return true;
                    }
                } catch (e) {
                    return true;
                }
                console.log = originalLog;
                return false;
            },
            
            // Verifica se Date foi modificada
            () => {
                try {
                    const now = Date.now();
                    const date = new Date();
                    const diff = Math.abs(now - date.getTime());
                    return diff > 1000; // Mais de 1 segundo de diferença
                } catch (e) {
                    return true;
                }
            },
            
            // Verifica se Math foi modificada
            () => {
                try {
                    return Math.random() === Math.random();
                } catch (e) {
                    return true;
                }
            }
        ];
        
        return suspiciousChecks.some(check => check());
    }
    
    // Executa proteção imediata
    function executeProtection(reason) {
        if (!protectionActive) return;
        
        console.log(`🚫 ULTIMATE PROTECTION TRIGGERED: ${reason}`);
        
        // Limpa todo o conteúdo
        try {
            document.documentElement.innerHTML = '';
            document.body.innerHTML = '';
            document.head.innerHTML = '';
            document.title = '';
        } catch (e) {
            // Silencioso
        }
        
        // Remove todos os estilos
        try {
            const stylesheets = document.querySelectorAll('link[rel="stylesheet"], style');
            stylesheets.forEach(sheet => sheet.remove());
        } catch (e) {
            // Silencioso
        }
        
        // Para todos os scripts
        try {
            window.stop && window.stop();
        } catch (e) {
            // Silencioso
        }
        
        // Redireciona para página em branco
        setTimeout(() => {
            try {
                window.location.href = 'about:blank';
            } catch (e) {
                // Silencioso
            }
        }, 50);
        
        // Desativa proteção para evitar loops
        protectionActive = false;
        
        return false;
    }
    
    // Executa todas as verificações
    function runAllChecks() {
        if (!protectionActive) return true;
        
        detectionAttempts++;
        
        // Verifica Electron
        if (detectElectron()) {
            return executeProtection('Electron detected');
        }
        
        // Verifica ferramentas de clonagem
        if (detectCloningTools()) {
            return executeProtection('Cloning tool detected');
        }
        
        // Verifica spoofing mobile
        if (detectMobileSpoofing()) {
            return executeProtection('Mobile spoofing detected');
        }
        
        // Verifica tela grande
        if (detectLargeScreen()) {
            return executeProtection('Large screen detected');
        }
        
        // Verifica falta de toque
        if (detectNoTouch()) {
            return executeProtection('No touch capability detected');
        }
        
        // Verifica developer tools
        if (detectDevTools()) {
            return executeProtection('Developer tools detected');
        }
        
        // Verifica iframe
        if (detectIframe()) {
            return executeProtection('Iframe embedding detected');
        }
        
        // Verifica modificações no ambiente
        if (detectEnvironmentTampering()) {
            return executeProtection('Environment tampering detected');
        }
        
        return true;
    }
    
    // Verifica ambiente Replit primeiro
    if (isReplitEnvironment()) {
        console.log('🔧 Ultimate protection disabled in Replit environment');
        return;
    }
    
    // Executa verificação imediata
    if (!runAllChecks()) {
        return;
    }
    
    // Monitora continuamente
    const monitoringInterval = setInterval(() => {
        if (!runAllChecks()) {
            clearInterval(monitoringInterval);
            return;
        }
        
        // Para monitoramento após muitas tentativas
        if (detectionAttempts > maxDetectionAttempts) {
            clearInterval(monitoringInterval);
        }
    }, 1000);
    
    // Monitora mudanças na janela
    window.addEventListener('resize', () => {
        if (!runAllChecks()) {
            clearInterval(monitoringInterval);
        }
    });
    
    // Monitora focus/blur (pode indicar dev tools)
    let blurCount = 0;
    window.addEventListener('blur', () => {
        blurCount++;
        if (blurCount > 3) {
            if (!runAllChecks()) {
                clearInterval(monitoringInterval);
            }
        }
    });
    
    // Bloqueia atalhos de teclado
    document.addEventListener('keydown', function(e) {
        // F12, Ctrl+Shift+I, Ctrl+Shift+C, Ctrl+U, Ctrl+S
        if (e.key === 'F12' || 
            (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'C')) ||
            (e.ctrlKey && e.key === 'u') ||
            (e.ctrlKey && e.key === 's')) {
            e.preventDefault();
            executeProtection('Keyboard shortcut blocked');
            return false;
        }
    });
    
    // Bloqueia menu de contexto
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        executeProtection('Context menu blocked');
        return false;
    });
    
    // Monitora mutações no DOM
    const observer = new MutationObserver(function(mutations) {
        if (mutations.length > 50) {
            // Muitas mutações podem indicar scraping
            executeProtection('Excessive DOM mutations detected');
        }
    });
    
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        attributes: true
    });
    
    // Verifica se está em modo Replit (ambiente de desenvolvimento)
    function isReplitEnvironment() {
        return window.location.hostname.includes('replit.') || 
               window.location.hostname.includes('.repl.co') ||
               window.location.hostname.includes('replit.app') ||
               window.location.hostname.includes('replit.dev');
    }
    
    // Se está no Replit, desativa proteção para desenvolvimento
    if (isReplitEnvironment()) {
        console.log('🔧 Ultimate protection disabled in Replit environment');
        protectionActive = false;
        clearInterval(monitoringInterval);
        return;
    }
    
    console.log('🛡️ Ultimate protection active - Desktop/Cloning blocked');
    
})();