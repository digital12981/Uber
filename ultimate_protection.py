"""
Sistema de Proteção Ultimate - Bloqueia TODA clonagem e acesso desktop
Detecta Electron, SaveWeb2Zip, HTTrack, WebCopier e outras ferramentas
"""
from flask import request, Response, abort
from functools import wraps
import re
import time
import hashlib
import hmac
import json
import random


class UltimateProtection:
    def __init__(self):
        self.blocked_fingerprints = set()
        self.suspicious_ips = {}
        self.electron_signatures = [
            'electron', 'electronjs', 'electronapp',
            'desktop app', 'nativefier', 'tauri'
        ]
        self.cloning_tools = [
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
        ]
        self.bot_signatures = [
            'bot', 'spider', 'crawler', 'scraper', 'fetcher',
            'python', 'java', 'curl', 'wget', 'requests',
            'selenium', 'phantomjs', 'headless', 'playwright',
            'puppeteer', 'chromedriver', 'webdriver',
            'scrapy', 'beautifulsoup', 'mechanize',
            'http client', 'api client', 'automation',
            'test framework', 'monitor', 'checker'
        ]
    
    def detect_electron(self, user_agent, headers):
        """Detecta aplicações Electron e desktop wrappers"""
        if not user_agent:
            return True
        
        user_agent_lower = user_agent.lower()
        
        # Assinaturas específicas do Electron
        for signature in self.electron_signatures:
            if signature in user_agent_lower:
                return True
        
        # Padrões suspeitos de Electron
        electron_patterns = [
            r'chrome/\d+\.\d+\.\d+\.\d+ electron',
            r'electronjs',
            r'desktop.*app',
            r'nativefier',
            r'tauri'
        ]
        
        for pattern in electron_patterns:
            if re.search(pattern, user_agent_lower):
                return True
        
        # Headers suspeitos de Electron
        suspicious_headers = {
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document'
        }
        
        electron_count = 0
        for header, value in suspicious_headers.items():
            if headers.get(header) == value:
                electron_count += 1
        
        # Se muitos headers suspeitos, provavelmente Electron
        if electron_count >= 2:
            return True
        
        return False
    
    def detect_cloning_tools(self, user_agent, headers):
        """Detecta ferramentas de clonagem de sites"""
        if not user_agent:
            return True
        
        user_agent_lower = user_agent.lower()
        
        # Detecta ferramentas de clonagem por nome
        for tool in self.cloning_tools:
            if tool in user_agent_lower:
                return True
        
        # Padrões suspeitos de clonagem
        cloning_patterns = [
            r'offline.*browser',
            r'web.*ripper',
            r'site.*sucker',
            r'web.*copier',
            r'download.*manager',
            r'mass.*downloader',
            r'website.*extractor'
        ]
        
        for pattern in cloning_patterns:
            if re.search(pattern, user_agent_lower):
                return True
        
        # Headers típicos de ferramentas de clonagem
        if 'range' in headers and 'if-range' not in headers:
            return True
        
        # Accept headers suspeitos
        accept = headers.get('accept', '').lower()
        if accept and ('*/*' in accept or 'application/octet-stream' in accept):
            if 'text/html' not in accept:
                return True
        
        return False
    
    def detect_bots_scrapers(self, user_agent):
        """Detecta bots e scrapers"""
        if not user_agent:
            return True
        
        user_agent_lower = user_agent.lower()
        
        for signature in self.bot_signatures:
            if signature in user_agent_lower:
                return True
        
        return False
    
    def analyze_browser_fingerprint(self, user_agent, headers):
        """Analisa fingerprint do navegador para detectar falsificação"""
        score = 0
        
        # Verifica consistência do User-Agent
        if user_agent:
            ua_lower = user_agent.lower()
            
            # Chrome sem indicadores móveis
            if 'chrome' in ua_lower and 'mobile' not in ua_lower:
                score += 2
            
            # Versões muito antigas ou novas demais
            chrome_match = re.search(r'chrome/(\d+)', ua_lower)
            if chrome_match:
                version = int(chrome_match.group(1))
                if version < 90 or version > 130:  # Versões suspeitas
                    score += 1
            
            # User-Agent muito simples (típico de bots)
            if len(user_agent) < 50:
                score += 2
        
        # Headers inconsistentes
        accept_language = headers.get('accept-language', '')
        if not accept_language or len(accept_language) < 5:
            score += 1
        
        # Falta de headers importantes
        important_headers = ['accept', 'accept-encoding', 'connection']
        missing_headers = sum(1 for h in important_headers if not headers.get(h))
        score += missing_headers
        
        return score > 3
    
    def detect_mobile_spoofing(self, user_agent, headers):
        """Detecta quando desktop tenta fingir ser mobile"""
        if not user_agent:
            return True
        
        ua_lower = user_agent.lower()
        
        # Tem indicadores móveis mas outros sinais de desktop
        has_mobile = any(indicator in ua_lower for indicator in [
            'mobile', 'android', 'iphone', 'ipad'
        ])
        
        if has_mobile:
            # Verifica se tem sinais de desktop também
            desktop_signs = [
                'windows nt', 'macintosh', 'linux x86_64',
                'wow64', 'win64', 'x11'
            ]
            
            has_desktop = any(sign in ua_lower for sign in desktop_signs)
            
            if has_desktop:
                return True  # Mobile + Desktop = Spoofing
        
        return False
    
    def generate_decoy_response(self):
        """Gera resposta falsa para confundir clonadores"""
        decoy_responses = [
            ('', 404),
            ('Service Temporarily Unavailable', 503),
            ('Forbidden', 403),
            ('Bad Request', 400),
            ('Too Many Requests', 429),
            ('Gateway Timeout', 504)
        ]
        
        return Response(*random.choice(decoy_responses))
    
    def is_legitimate_mobile(self, user_agent, headers):
        """Verifica se é realmente um dispositivo móvel legítimo"""
        if not user_agent:
            return False
        
        ua_lower = user_agent.lower()
        
        # Deve ter indicadores móveis
        mobile_indicators = [
            'mobile', 'android', 'iphone', 'ipad', 'ipod'
        ]
        
        has_mobile = any(indicator in ua_lower for indicator in mobile_indicators)
        if not has_mobile:
            return False
        
        # Não deve ter sinais de desktop
        desktop_indicators = [
            'windows nt', 'macintosh', 'linux x86_64',
            'wow64', 'win64', 'x11'
        ]
        
        has_desktop = any(indicator in ua_lower for indicator in desktop_indicators)
        if has_desktop:
            return False
        
        # Deve ter headers típicos de mobile
        mobile_headers = [
            'sec-ch-ua-mobile',
            'sec-ch-ua-platform'
        ]
        
        # Pelo menos um header mobile
        has_mobile_header = any(headers.get(h) for h in mobile_headers)
        
        return has_mobile_header or 'mobile' in ua_lower


def ultimate_mobile_only(f):
    """
    Decorator com proteção ultimate contra clonagem e acesso desktop
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        protection = UltimateProtection()
        
        user_agent = request.headers.get('User-Agent', '')
        headers = dict(request.headers)
        ip = request.remote_addr
        
        # Teste 1: Detecta Electron
        if protection.detect_electron(user_agent, headers):
            print(f"🚫 ELECTRON DETECTED: {user_agent}")
            return protection.generate_decoy_response()
        
        # Teste 2: Detecta ferramentas de clonagem
        if protection.detect_cloning_tools(user_agent, headers):
            print(f"🚫 CLONING TOOL DETECTED: {user_agent}")
            return protection.generate_decoy_response()
        
        # Teste 3: Detecta bots e scrapers
        if protection.detect_bots_scrapers(user_agent):
            print(f"🚫 BOT/SCRAPER DETECTED: {user_agent}")
            return protection.generate_decoy_response()
        
        # Teste 4: Analisa fingerprint suspeito
        if protection.analyze_browser_fingerprint(user_agent, headers):
            print(f"🚫 SUSPICIOUS FINGERPRINT: {user_agent}")
            return protection.generate_decoy_response()
        
        # Teste 5: Detecta mobile spoofing
        if protection.detect_mobile_spoofing(user_agent, headers):
            print(f"🚫 MOBILE SPOOFING DETECTED: {user_agent}")
            return protection.generate_decoy_response()
        
        # Teste 6: Verifica se é realmente mobile legítimo
        if not protection.is_legitimate_mobile(user_agent, headers):
            print(f"🚫 NOT LEGITIMATE MOBILE: {user_agent}")
            return protection.generate_decoy_response()
        
        # Se passou em todos os testes, permite acesso
        print(f"✅ LEGITIMATE MOBILE ACCESS: {user_agent}")
        return f(*args, **kwargs)
    
    return decorated_function


def check_ultimate_protection():
    """Função para testar proteção em qualquer lugar"""
    protection = UltimateProtection()
    user_agent = request.headers.get('User-Agent', '')
    headers = dict(request.headers)
    
    # Testa todos os filtros
    tests = [
        protection.detect_electron(user_agent, headers),
        protection.detect_cloning_tools(user_agent, headers),
        protection.detect_bots_scrapers(user_agent),
        protection.analyze_browser_fingerprint(user_agent, headers),
        protection.detect_mobile_spoofing(user_agent, headers),
        not protection.is_legitimate_mobile(user_agent, headers)
    ]
    
    return any(tests)  # Se qualquer teste falhar, bloqueia