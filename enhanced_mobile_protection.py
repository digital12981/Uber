"""
Enhanced Mobile-Only Protection System
Impede acesso desktop e redireciona para about:blank
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
        'bot', 'spider', 'crawler', 'scraper'
    ]
    
    return any(tool in user_agent for tool in scraping_tools)

def generate_about_blank_response():
    """Gera resposta que redireciona imediatamente para about:blank"""
    return Response('''
    <!DOCTYPE html>
    <html>
    <head><title></title></head>
    <body>
        <script>
        // Múltiplos métodos de redirecionamento
        window.location.href='about:blank';
        window.location.replace('about:blank');
        window.location.assign('about:blank');
        document.location = 'about:blank';
        // Tentar fechar a aba se possível
        if (window.close) window.close();
        </script>
    </body>
    </html>
    ''', mimetype='text/html')

def mobile_only_enhanced(f):
    """Decorator para proteger rotas contra acesso desktop"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip protection in Replit environment for development
        if (os.environ.get('REPL_ID') or 
            os.environ.get('REPLIT_ENVIRONMENT') or 
            os.environ.get('REPL_SLUG') or
            'replit' in request.headers.get('Host', '').lower() or
            'repl.co' in request.headers.get('Host', '').lower() or
            'repl.app' in request.headers.get('Host', '').lower() or
            '--' in request.headers.get('Host', '')):
            return f(*args, **kwargs)
        
        user_agent = request.headers.get('User-Agent', '')
        
        # Verifica se é desktop ou ferramenta de scraping
        if is_scraping_tool(user_agent):
            return generate_about_blank_response()
        
        if is_desktop_browser(user_agent) and not is_mobile_device(user_agent):
            # Respostas variadas para confundir scrapers
            responses = [
                Response('', status=404),
                Response('', status=503),
                Response('Access denied', status=403),
                generate_about_blank_response()
            ]
            return random.choice(responses)
        
        # Verificações adicionais de segurança
        # Verifica largura da viewport se disponível
        viewport_width = request.headers.get('Viewport-Width', '')
        if viewport_width:
            try:
                width = int(viewport_width)
                if width > 1024:  # Tamanho típico de desktop
                    return generate_about_blank_response()
            except:
                pass
        
        # Verifica padrões suspeitos no Accept header
        accept_header = request.headers.get('Accept', '')
        if 'text/html' in accept_header and 'mobile' not in user_agent.lower():
            # Provável navegador desktop
            if not is_mobile_device(user_agent):
                return generate_about_blank_response()
        
        return f(*args, **kwargs)
    
    return decorated_function

def check_mobile_access_enhanced():
    """
    Verifica se o acesso atual deve ser permitido
    Retorna True se deve bloquear, False se mobile permitido
    """
    # Skip protection in Replit environment
    if (os.environ.get('REPL_ID') or 
        os.environ.get('REPLIT_ENVIRONMENT') or 
        os.environ.get('REPL_SLUG') or
        'replit' in request.headers.get('Host', '').lower() or
        'repl.co' in request.headers.get('Host', '').lower() or
        'repl.app' in request.headers.get('Host', '').lower() or
        '--' in request.headers.get('Host', '')):
        return False
    
    user_agent = request.headers.get('User-Agent', '')
    
    # Bloqueia ferramentas de scraping
    if is_scraping_tool(user_agent):
        return True
    
    # Bloqueia navegadores desktop
    if is_desktop_browser(user_agent) and not is_mobile_device(user_agent):
        return True
    
    return False