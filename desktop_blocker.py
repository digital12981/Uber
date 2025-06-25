"""
Comprehensive desktop blocking system - Instant redirect to about:blank
Blocks ALL desktop access across the entire website
"""
from flask import request, Response
from functools import wraps
import os
import re

def is_mobile_device(user_agent):
    """
    Detect if the request is coming from a mobile device
    Enhanced detection for comprehensive mobile identification
    """
    if not user_agent:
        return False
    
    user_agent = user_agent.lower()
    
    # Comprehensive mobile device indicators
    mobile_patterns = [
        # Android devices
        r'android.*mobile', r'android.*phone', r'android',
        # iOS devices  
        r'iphone', r'ipod', r'ipad',
        # Windows Mobile
        r'windows phone', r'windows mobile', r'iemobile',
        # BlackBerry
        r'blackberry', r'bb10', r'rim\stablet',
        # Other mobile platforms
        r'mobile', r'mobi', r'phone', r'tablet',
        # Mobile browsers
        r'opera mini', r'opera mobi', r'mobile safari',
        # Mobile-specific strings
        r'mobile.*firefox', r'mobile.*chrome', r'crios', r'fxios',
        # Additional mobile indicators
        r'silk', r'kindle', r'webos', r'palm', r'symbian',
        r'nokia', r'samsung', r'htc', r'lg', r'motorola',
        r'mobile.*version', r'version.*mobile'
    ]
    
    # Check for any mobile pattern
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent):
            return True
    
    return False

def is_desktop_browser(user_agent):
    """
    Detect desktop browsers - comprehensive desktop detection
    """
    if not user_agent:
        return True  # Assume desktop if no user agent
    
    user_agent = user_agent.lower()
    
    # Desktop operating system patterns
    desktop_os_patterns = [
        r'windows nt', r'macintosh', r'mac os x', 
        r'x11.*linux', r'ubuntu', r'debian', r'fedora',
        r'win32', r'win64', r'wow64'
    ]
    
    # Desktop browser patterns
    desktop_browser_patterns = [
        r'chrome/[0-9]+\..*(?!.*mobile)', 
        r'firefox/[0-9]+\..*(?!.*mobile)',
        r'safari/[0-9]+\..*(?!.*mobile)(?!.*version.*mobile)',
        r'edge/[0-9]+', r'edg/[0-9]+',
        r'opera/[0-9]+.*(?!.*mini)(?!.*mobi)',
        r'msie [0-9]+', r'trident/[0-9]+'
    ]
    
    # Check for desktop OS
    has_desktop_os = any(re.search(pattern, user_agent) for pattern in desktop_os_patterns)
    
    # Check for desktop browser
    has_desktop_browser = any(re.search(pattern, user_agent) for pattern in desktop_browser_patterns)
    
    # Additional desktop indicators
    desktop_indicators = [
        'x11', 'wow64', 'win64', 'amd64', 'intel',
        'desktop', 'electron'
    ]
    
    has_desktop_indicator = any(indicator in user_agent for indicator in desktop_indicators)
    
    return has_desktop_os or has_desktop_browser or has_desktop_indicator

def generate_instant_redirect_response():
    """
    Generate immediate redirect to about:blank without showing any content
    """
    redirect_html = '''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script>
// Immediate redirect - no delay, no content visible
window.location.replace('about:blank');
// Fallback methods
if (window.location.href !== 'about:blank') {
    window.location.href = 'about:blank';
    window.location.assign('about:blank');
    document.location = 'about:blank';
}
// Close tab if possible
if (window.close) window.close();
</script>
</head><body></body></html>'''
    
    return Response(
        redirect_html, 
        mimetype='text/html',
        headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

def desktop_blocker(f):
    """
    Decorator that blocks ALL desktop access instantly
    Redirects to about:blank immediately for non-mobile devices
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip protection in Replit environment for development
        if os.environ.get('REPL_ID') or os.environ.get('REPLIT_ENVIRONMENT'):
            return f(*args, **kwargs)
        
        user_agent = request.headers.get('User-Agent', '')
        
        # Check if it's a mobile device
        if is_mobile_device(user_agent):
            # Mobile device - allow access
            return f(*args, **kwargs)
        
        # Check if it's a desktop browser
        if is_desktop_browser(user_agent):
            # Desktop browser - block with instant redirect
            return generate_instant_redirect_response()
        
        # Additional security checks for suspicious access
        
        # Check for missing or suspicious user agent
        if not user_agent or len(user_agent) < 10:
            return generate_instant_redirect_response()
        
        # Check for bot/scraper patterns
        bot_patterns = [
            'bot', 'spider', 'crawler', 'scraper', 'wget', 'curl',
            'python', 'java', 'go-http', 'node', 'phantom', 'headless'
        ]
        
        user_agent_lower = user_agent.lower()
        if any(pattern in user_agent_lower for pattern in bot_patterns):
            return generate_instant_redirect_response()
        
        # Check screen resolution hints (large screens = desktop)
        viewport_width = request.headers.get('Viewport-Width', '')
        if viewport_width:
            try:
                width = int(viewport_width)
                if width > 1024:  # Desktop screen size
                    return generate_instant_redirect_response()
            except:
                pass
        
        # Check for desktop-specific headers
        accept_header = request.headers.get('Accept', '')
        if 'text/html' in accept_header and 'mobile' not in user_agent_lower:
            # Likely desktop browser
            return generate_instant_redirect_response()
        
        # If we can't determine mobile, assume desktop and block
        return generate_instant_redirect_response()
    
    return decorated_function

def check_and_block_desktop():
    """
    Standalone function to check and block desktop access
    Returns True if should block, False if mobile access allowed
    """
    # Skip protection in Replit environment
    if os.environ.get('REPL_ID') or os.environ.get('REPLIT_ENVIRONMENT'):
        return False
    
    user_agent = request.headers.get('User-Agent', '')
    
    # Allow mobile devices
    if is_mobile_device(user_agent):
        return False
    
    # Block everything else (desktop, bots, unknown)
    return True