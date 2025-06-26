"""
Sistema de Proteção Desktop - Impede Acesso Desktop e Clonagem
Proteção server-side robusta contra tentativas de scraping e clonagem
"""
from flask import request, Response
from functools import wraps
import re
import random
import os

def is_mobile_device(user_agent):
    """Detecta se a requisição vem de um dispositivo móvel"""
    if not user_agent:
        return False
    
    user_agent = user_agent.lower()
    mobile_keywords = [
        'mobile', 'android', 'iphone', 'ipad', 'ipod', 
        'blackberry', 'windows phone', 'opera mini', 
        'silk', 'kindle', 'webos', 'palm'
    ]
    
    return any(keyword in user_agent for keyword in mobile_keywords)

def is_desktop_browser(user_agent):
    """Detecta navegadores desktop sem indicadores mobile"""
    if not user_agent:
        return True
    
    user_agent = user_agent.lower()
    
    desktop_patterns = [
        r'windows nt.*chrome',
        r'macintosh.*chrome',
        r'x11.*linux.*chrome',
        r'windows nt.*firefox',
        r'macintosh.*firefox',
        r'windows nt.*edge',
        r'macintosh.*safari(?!.*mobile)',
    ]
    
    mobile_exclusions = ['mobile', 'android', 'iphone', 'ipad']
    
    has_desktop_pattern = any(re.search(pattern, user_agent) for pattern in desktop_patterns)
    has_mobile_indicator = any(mobile in user_agent for mobile in mobile_exclusions)
    
    return has_desktop_pattern and not has_mobile_indicator

def is_scraping_tool(user_agent):
    """Detecta ferramentas de scraping e bots"""
    if not user_agent:
        return True
    
    user_agent = user_agent.lower()
    scraping_tools = [
        'wget', 'curl', 'httrack', 'webzip', 'teleport', 
        'offline explorer', 'web copier', 'sitesuck',
        'python', 'java', 'go-http-client', 'node',
        'bot', 'spider', 'crawler', 'scraper',
        'selenium', 'phantomjs', 'headless', 'requests'
    ]
    
    return any(tool in user_agent for tool in scraping_tools)

def desktop_protection(f):
    """Decorator para proteger rotas contra acesso desktop e clonagem"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Exceção para ambientes de desenvolvimento
        if (os.environ.get('REPLIT_DEV_DOMAIN') or 
            os.environ.get('DYNO') or
            request.host in ['localhost:5000', '127.0.0.1:5000']):
            return f(*args, **kwargs)
        
        user_agent = request.headers.get('User-Agent', '')
        
        # Verifica se é desktop, scraping tool ou bot
        if (is_desktop_browser(user_agent) and not is_mobile_device(user_agent)) or is_scraping_tool(user_agent):
            # Respostas variadas para confundir scrapers
            responses = [
                Response('', status=404),
                Response('', status=503),
                Response('Service Unavailable', status=503),
                Response('Access denied', status=403),
                Response('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title></title>
                    <meta name="robots" content="noindex, nofollow">
                </head>
                <body>
                    <script>
                        window.location.href='about:blank';
                    </script>
                </body>
                </html>
                ''', mimetype='text/html'),
                Response('', status=429),  # Too Many Requests
                Response('Not Found', status=404)
            ]
            return random.choice(responses)
        
        return f(*args, **kwargs)
    
    return decorated_function

def ultra_desktop_protection(f):
    """Proteção ultra rígida - bloqueia TUDO que não for mobile autêntico"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Exceção apenas para Replit
        if os.environ.get('REPLIT_DEV_DOMAIN'):
            return f(*args, **kwargs)
        
        user_agent = request.headers.get('User-Agent', '')
        
        # Só permite se for claramente mobile
        if not is_mobile_device(user_agent):
            return Response('', status=404)
        
        # Bloqueia se tiver qualquer indício de desktop
        if is_desktop_browser(user_agent) or is_scraping_tool(user_agent):
            return Response('', status=404)
        
        return f(*args, **kwargs)
    
    return decorated_function