/**
 * Client-side desktop blocking protection
 * Immediate redirect to about:blank for non-mobile devices
 */

(function() {
    'use strict';
    
    // Skip protection in Replit environment
    if (window.location.hostname.includes('replit') || 
        window.location.hostname.includes('repl.co') ||
        window.location.hostname.includes('--')) {
        return;
    }
    
    function isMobileDevice() {
        // Enhanced mobile detection
        const userAgent = navigator.userAgent.toLowerCase();
        
        // Mobile patterns
        const mobilePatterns = [
            /android.*mobile/i,
            /android.*phone/i,
            /android/i,
            /iphone/i,
            /ipod/i,
            /ipad/i,
            /windows phone/i,
            /windows mobile/i,
            /iemobile/i,
            /blackberry/i,
            /bb10/i,
            /mobile/i,
            /mobi/i,
            /phone/i,
            /tablet/i,
            /opera mini/i,
            /opera mobi/i,
            /mobile safari/i,
            /silk/i,
            /kindle/i,
            /webos/i,
            /palm/i,
            /symbian/i,
            /nokia/i,
            /samsung/i,
            /htc/i,
            /lg/i,
            /motorola/i
        ];
        
        // Check user agent patterns
        for (let pattern of mobilePatterns) {
            if (pattern.test(userAgent)) {
                return true;
            }
        }
        
        // Check screen size (mobile typically < 1024px width)
        if (window.screen && window.screen.width && window.screen.width < 1024) {
            return true;
        }
        
        // Check touch capability
        if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
            return true;
        }
        
        return false;
    }
    
    function isDesktopBrowser() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        // Desktop OS patterns
        const desktopPatterns = [
            /windows nt/i,
            /macintosh/i,
            /mac os x/i,
            /x11.*linux/i,
            /ubuntu/i,
            /debian/i,
            /fedora/i,
            /win32/i,
            /win64/i,
            /wow64/i
        ];
        
        // Check for desktop OS
        for (let pattern of desktopPatterns) {
            if (pattern.test(userAgent)) {
                return true;
            }
        }
        
        // Check screen resolution (desktop typically > 1024px)
        if (window.screen && window.screen.width && window.screen.width > 1024) {
            return true;
        }
        
        // Check for desktop-specific properties
        if (window.chrome || window.safari || window.opera) {
            // Desktop browsers often have these properties
            return true;
        }
        
        return false;
    }
    
    function blockDesktopAccess() {
        // Multiple redirect methods for maximum effectiveness
        try {
            window.location.replace('about:blank');
        } catch(e) {}
        
        try {
            window.location.href = 'about:blank';
        } catch(e) {}
        
        try {
            window.location.assign('about:blank');
        } catch(e) {}
        
        try {
            document.location = 'about:blank';
        } catch(e) {}
        
        // Close tab if possible
        try {
            window.close();
        } catch(e) {}
        
        // Hide all content immediately
        try {
            document.documentElement.style.display = 'none';
            document.body.style.display = 'none';
        } catch(e) {}
    }
    
    // Immediate check on script load
    if (!isMobileDevice() || isDesktopBrowser()) {
        blockDesktopAccess();
        return;
    }
    
    // Additional checks when DOM loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            if (!isMobileDevice() || isDesktopBrowser()) {
                blockDesktopAccess();
            }
        });
    } else {
        // DOM already loaded
        if (!isMobileDevice() || isDesktopBrowser()) {
            blockDesktopAccess();
        }
    }
    
    // Continuous monitoring every 100ms for the first 5 seconds
    let checkCount = 0;
    const maxChecks = 50; // 5 seconds
    
    const intervalCheck = setInterval(function() {
        checkCount++;
        
        if (!isMobileDevice() || isDesktopBrowser()) {
            clearInterval(intervalCheck);
            blockDesktopAccess();
            return;
        }
        
        if (checkCount >= maxChecks) {
            clearInterval(intervalCheck);
        }
    }, 100);
    
    // Monitor for window resize (user might be simulating mobile)
    window.addEventListener('resize', function() {
        setTimeout(function() {
            if (!isMobileDevice() || isDesktopBrowser()) {
                blockDesktopAccess();
            }
        }, 100);
    });
    
    // Monitor for developer tools (common on desktop)
    let devtools = {
        open: false,
        orientation: null
    };
    
    const threshold = 160;
    
    setInterval(function() {
        if (window.outerHeight - window.innerHeight > threshold || 
            window.outerWidth - window.innerWidth > threshold) {
            if (!devtools.open) {
                devtools.open = true;
                // Developer tools opened - likely desktop
                blockDesktopAccess();
            }
        } else {
            devtools.open = false;
        }
    }, 500);
    
})();