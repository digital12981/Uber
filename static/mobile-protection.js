/**
 * Mobile-Only Protection System
 * Active in production, disabled in Replit development
 */

// Check if running in Replit - disable protection for development
// Execute protection on all domains including production and development
    (function() {
        'use strict';
    
    // Comprehensive mobile detection
    function isMobileDevice() {
        // Check user agent for mobile indicators
        const userAgent = navigator.userAgent.toLowerCase();
        const mobileKeywords = [
            'mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 
            'windows phone', 'opera mini', 'silk', 'kindle'
        ];
        
        const hasMobileKeyword = mobileKeywords.some(keyword => 
            userAgent.includes(keyword)
        );
        
        // Check screen size (mobile typically < 768px width)
        const hasSmallScreen = window.screen.width <= 768 || window.innerWidth <= 768;
        
        // Check for touch capability
        const hasTouchScreen = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        
        // Check orientation support (mobile feature)
        const hasOrientationSupport = typeof window.orientation !== 'undefined';
        
        // Combined mobile detection
        return hasMobileKeyword || (hasSmallScreen && hasTouchScreen) || hasOrientationSupport;
    }
    
    // Additional desktop detection patterns
    function isDesktopCloner() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        // Common desktop browsers without mobile indicators
        const desktopBrowsers = [
            'chrome', 'firefox', 'safari', 'edge', 'opera'
        ];
        
        const mobileExclusions = [
            'mobile', 'android', 'iphone', 'ipad'
        ];
        
        const hasDesktopBrowser = desktopBrowsers.some(browser => 
            userAgent.includes(browser)
        );
        
        const lacksMobileIndicators = !mobileExclusions.some(mobile => 
            userAgent.includes(mobile)
        );
        
        // Large screen size typical of desktop
        const hasLargeScreen = window.screen.width > 1024 && window.screen.height > 768;
        
        return hasDesktopBrowser && lacksMobileIndicators && hasLargeScreen;
    }
    
    // Check for common scraping tools
    function isScrapingTool() {
        const userAgent = navigator.userAgent.toLowerCase();
        const scrapingTools = [
            'wget', 'curl', 'httrack', 'webzip', 'teleport', 
            'offline explorer', 'web copier', 'sitesuck',
            'python', 'java', 'go-http-client', 'node'
        ];
        
        return scrapingTools.some(tool => userAgent.includes(tool));
    }
    
    // Execute protection immediately
    function executeProtection() {
        if (!isMobileDevice() || isDesktopCloner() || isScrapingTool()) {
            // Immediate redirect to about:blank for desktop browsers
            window.location.replace('about:blank');
            
            // Backup methods in case replace fails
            window.location.href = 'about:blank';
            window.location.assign('about:blank');
            
            // Clear content as fallback
            try {
                document.documentElement.innerHTML = '';
                document.body.innerHTML = '';
                document.title = '';
            } catch(e) {}
            
            // Block any further script execution
            window.stop && window.stop();
            
            return false;
        }
        return true;
    }
    
    // Execute protection immediately when script loads
    if (!executeProtection()) {
        return;
    }
    
    // Monitor for window resize (desktop users might resize to mimic mobile)
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (!isMobileDevice() || isDesktopCloner()) {
                executeProtection();
            }
        }, 100);
    });
    
    // Monitor for developer tools opening (common for cloners)
    let devToolsOpen = false;
    const devToolsChecker = setInterval(() => {
        if (window.outerHeight - window.innerHeight > 200 || 
            window.outerWidth - window.innerWidth > 200) {
            if (!devToolsOpen) {
                devToolsOpen = true;
                executeProtection();
            }
        } else {
            devToolsOpen = false;
        }
    }, 1000);
    
    // Block right-click context menu (prevent inspect element)
    document.addEventListener('contextmenu', function(e) {
        if (!isMobileDevice()) {
            e.preventDefault();
            executeProtection();
            return false;
        }
    });
    
    // Block common developer shortcuts
    document.addEventListener('keydown', function(e) {
        // Block F12, Ctrl+Shift+I, Ctrl+Shift+C, Ctrl+U
        if (e.key === 'F12' || 
            (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'C')) ||
            (e.ctrlKey && e.key === 'u')) {
            e.preventDefault();
            executeProtection();
            return false;
        }
    });
    
    // Additional protection against iframe embedding
    if (window.top !== window.self) {
        executeProtection();
    }
    
    })(); // End mobile protection