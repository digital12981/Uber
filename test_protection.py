"""
Script de teste para verificar o sistema de proteção ultimate
Simula diferentes tipos de acesso para validar a proteção
"""
import requests
import time

# Lista de User-Agents suspeitos para testar
test_user_agents = [
    # Electron
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) MyApp/1.0.0 Chrome/100.0.4896.75 Electron/18.0.1 Safari/537.36",
    
    # Ferramentas de clonagem
    "HTTrack/3.0",
    "WebZIP/7.0 (WinNT)",
    "SaveWeb2Zip",
    "TeleportPro/1.40",
    "Offline Explorer/2.5",
    "WebCopier v4.6",
    "SiteSucker/2.3.4",
    
    # Bots e scrapers
    "Python-requests/2.25.1",
    "curl/7.68.0",
    "wget/1.20.3",
    "Scrapy/2.5.0 (+https://scrapy.org)",
    "Selenium",
    "PhantomJS/2.1.1",
    "HeadlessChrome/91.0.4472.114",
    
    # Desktop browsers (devem ser bloqueados)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    
    # Mobile legítimo (deve passar)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]

def test_protection(base_url="http://localhost:5000"):
    """
    Testa a proteção em diferentes rotas com diferentes User-Agents
    """
    routes_to_test = [
        "/",
        "/vagas", 
        "/pagamento",
        "/finalizar",
        "/cartao"
    ]
    
    print("🔍 TESTANDO SISTEMA DE PROTEÇÃO ULTIMATE")
    print("=" * 50)
    
    for route in routes_to_test:
        print(f"\n🌐 Testando rota: {route}")
        print("-" * 30)
        
        for user_agent in test_user_agents:
            try:
                response = requests.get(
                    f"{base_url}{route}",
                    headers={"User-Agent": user_agent},
                    timeout=5,
                    allow_redirects=False
                )
                
                # Categorizar User-Agent
                if any(x in user_agent.lower() for x in ['iphone', 'android', 'mobile']):
                    category = "📱 MOBILE"
                    expected = "ALLOW"
                elif any(x in user_agent.lower() for x in ['electron', 'httrack', 'saveweb', 'python', 'curl', 'wget', 'scrapy']):
                    category = "🚫 MALICIOUS"
                    expected = "BLOCK"
                else:
                    category = "💻 DESKTOP"
                    expected = "BLOCK"
                
                # Verificar resultado
                if response.status_code == 200:
                    result = "✅ PERMITIDO"
                elif response.status_code in [403, 404, 503]:
                    result = "🚫 BLOQUEADO"
                else:
                    result = f"❓ STATUS {response.status_code}"
                
                # Verificar se o resultado está correto
                if (expected == "ALLOW" and response.status_code == 200) or \
                   (expected == "BLOCK" and response.status_code in [403, 404, 503]):
                    status = "✅ CORRETO"
                else:
                    status = "❌ INCORRETO"
                
                print(f"{category} - {result} - {status}")
                print(f"    UA: {user_agent[:60]}...")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ ERRO DE CONEXÃO: {str(e)}")
            
            # Pequena pausa entre requests
            time.sleep(0.1)

def test_specific_threats():
    """
    Testa ameaças específicas conhecidas
    """
    print("\n🎯 TESTANDO AMEAÇAS ESPECÍFICAS")
    print("=" * 50)
    
    specific_threats = {
        "Electron App": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 MyApp/1.0.0 Chrome/100.0.4896.75 Electron/18.0.1",
        "HTTrack": "HTTrack/3.49-2+hts+default",
        "SaveWeb2Zip": "SaveWeb2Zip v3.1.2",
        "Python Requests": "python-requests/2.25.1",
        "cURL": "curl/7.68.0 (x86_64-pc-linux-gnu)",
        "Wget": "Wget/1.20.3 (linux-gnu)",
        "Scrapy": "Scrapy/2.5.0 (+https://scrapy.org)",
        "Selenium": "selenium/3.141.0 (python linux)",
        "Cyotek WebCopy": "Cyotek WebCopy 1.7.0",
        "Visual Web Ripper": "Visual Web Ripper 3.0.20"
    }
    
    for threat_name, user_agent in specific_threats.items():
        try:
            response = requests.get(
                "http://localhost:5000/",
                headers={"User-Agent": user_agent},
                timeout=5,
                allow_redirects=False
            )
            
            if response.status_code in [403, 404, 503]:
                print(f"✅ {threat_name}: BLOQUEADO (Status {response.status_code})")
            else:
                print(f"❌ {threat_name}: NÃO BLOQUEADO (Status {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {threat_name}: ERRO DE CONEXÃO")

if __name__ == "__main__":
    print("Iniciando testes de proteção...")
    test_protection()
    test_specific_threats()
    print("\n✅ Testes concluídos!")