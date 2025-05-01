import time
from typing import Optional
from datetime import datetime
import os
import pdb
from DrissionPage import ChromiumPage, ChromiumOptions
from config import CONFIG
from .utils import criar_diretorio_downloads, gerar_nome_arquivo, formatar_data_br

class Scraper:
    """Classe responsável pelo scraping dos documentos fiscais."""
    
    def __init__(self):
        """Inicializa o scraper com as configurações básicas."""
        # Configurando as opções do Chrome
        co = ChromiumOptions()
        co.set_argument('--remote-debugging-port=9222')
        co.set_argument('--no-sandbox')
        co.set_argument('--disable-dev-shm-usage')
        
        # Inicializando o Chrome com as opções configuradas
        self.page = ChromiumPage(co)
        self.download_path = criar_diretorio_downloads()
        self.arquivos_baixados = 0

    def esperar_elemento(self, seletor: str, timeout: int = 10) -> bool:
        """Espera um elemento aparecer na página."""
        for _ in range(timeout):
            if self.page.ele(seletor, timeout=1):
                return True
            time.sleep(1)
        return False

    def login(self) -> bool:
        """Aguarda a autenticação via certificado digital."""
        try:
            print("Iniciando processo de login...")
            url_login = CONFIG["BASE_URL"] + CONFIG["LOGIN_URL"]
            print(f"Acessando URL de login: {url_login}")
            self.page.get(url_login)
            
            # Aguarda tempo para certificado digital
            print("Aguardando seleção do certificado digital...")
            time.sleep(CONFIG["WAIT_TIME"])
            
            # Acessa página de consulta
            url_consulta = CONFIG["BASE_URL"] + CONFIG["CONSULTA_URL"]
            print(f"Acessando URL de consulta: {url_consulta}")
            self.page.get(url_consulta)
            
            # Aguarda carregamento da página
            print("Aguardando carregamento da página de consulta...")
            time.sleep(CONFIG["WAIT_TIME"])
            
            # Verifica se a página carregou corretamente
            print(f"URL atual: {self.page.url}")
            return True
        except Exception as e:
            print(f"Erro no login: {str(e)}")
            return False

    def preencher_campos(self, cnpj: str, tipo_documento: str, data_inicio: datetime, data_fim: datetime) -> bool:
        """Preenche o formulário de pesquisa."""
        try:
            print("Iniciando preenchimento dos campos...")
            
            # Espera e verifica cada campo antes de interagir
            print("Verificando campo CNPJ...")
            if not self.esperar_elemento('#CpfCnpj'):
                raise Exception("Campo CNPJ não encontrado")
            self.page.ele('#CpfCnpj').input(cnpj)
            print(f"CNPJ preenchido: {cnpj}")
            
            print("Verificando campo Tipo...")
            print("Aguardando elemento select do tipo...")
            
            # Aguardando o elemento aparecer na página
            js_select = """
            var select = document.querySelector('select[name="Tipo"]');
            if (select) {
                select.value = arguments[0];
                var event = new Event('change', { bubbles: true });
                select.dispatchEvent(event);
                return true;
            }
            return false;
            """
            # Executando o JavaScript para selecionar o tipo
            if not self.page.run_js(js_select, tipo_documento):
                print("HTML da página:")
                print(self.page.html)
                print("\nTentando encontrar qualquer elemento select na página:")
                selects = self.page.eles('select')
                print(f"Encontrados {len(selects)} elementos select")
                for select in selects:
                    print(f"Select encontrado: {select.html}")
                    print(f"Classes: {select.attr('class')}")
                    print(f"Name: {select.attr('name')}")
                    print(f"ng-model: {select.attr('ng-model')}")
                raise Exception("Campo Tipo não encontrado após timeout")
            
            print(f"Tipo de documento selecionado: {tipo_documento}")
            
            print("Verificando campo Data Início...")
            if not self.esperar_elemento('#DataInicio'):
                raise Exception("Campo Data Início não encontrado")
            self.page.ele('#DataInicio').input(formatar_data_br(data_inicio))
            print(f"Data início preenchida: {formatar_data_br(data_inicio)}")
            
            print("Verificando campo Data Fim...")
            if not self.esperar_elemento('#DataFim'):
                raise Exception("Campo Data Fim não encontrado")
            self.page.ele('#DataFim').input(formatar_data_br(data_fim))
            print(f"Data fim preenchida: {formatar_data_br(data_fim)}")
            
            print("Procurando botão de submit...")
            time.sleep(10)
            submit_button = self.page.ele('button[ng-click="ctrl.solicitar()"]')
            if not submit_button:
                # raise Exception("Botão de submit não encontrado")
                time.sleep(10)

                print("Clicando no botão de submit...")
                # Usando JavaScript para garantir que o botão está visível e clicável
                js_click = """
                var button = document.querySelector('button[ng-click="ctrl.solicitar()"]');
                if (button) {
                    button.click();
                    return true;
                }
                return false;
                """
            if not self.page.run_js(js_click):
                raise Exception("Não foi possível clicar no botão de submit")
            
            print("Aguardando processamento após submit...")
            time.sleep(CONFIG["WAIT_TIME"])
            
            return True
        except Exception as e:
            print(f"Erro ao preencher campos: {str(e)}")
            # print(f"HTML atual da página: {self.page.htm  l}")
            return False

    def verificar_resultados(self, max_tentativas: int = 10) -> int:
        """Verifica os resultados e baixa os arquivos XML."""
        tentativas = 0
        while tentativas < max_tentativas:
            try:
                print(f"Verificando resultados (tentativa {tentativas + 1}/{max_tentativas})...")
                pacotes = self.page.eles('tbody tr')
                if pacotes:
                    print(f"Encontrados {len(pacotes)} pacotes")
                    for pacote in pacotes:
                        if pacote.ele('td:contains("Concluído")'):
                            link = pacote.ele('a').attr('href')
                            print(f"Encontrado link para download: {link}")
                            if self.baixar_xml(link):
                                self.arquivos_baixados += 1
                                print(f"Arquivo XML baixado com sucesso. Total: {self.arquivos_baixados}")
                
                time.sleep(CONFIG["WAIT_TIME"])
                tentativas += 1
            except Exception as e:
                print(f"Erro ao verificar resultados: {str(e)}")
                break
        
        return self.arquivos_baixados

    def baixar_xml(self, link: str) -> bool:
        """Baixa o arquivo XML com base no link fornecido."""
        try:
            print(f"Iniciando download do XML: {link}")
            response = self.page.get(link)
            nome_arquivo = gerar_nome_arquivo(
                cnpj=self.page.ele('#CpfCnpj').attr('value'),
                tipo_documento=self.page.ele('select[name="Tipo"]').attr('value')
            )
            caminho_arquivo = os.path.join(self.download_path, nome_arquivo)
            
            print(f"Salvando arquivo em: {caminho_arquivo}")
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)
            print("Arquivo salvo com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao baixar XML: {str(e)}")
            return False 