from datetime import datetime
from selenium.webdriver.common.keys import Keys
from ast import Try
import time
import undetected_chromedriver as uc
import os
import sys
from retry import retry
from selenium.webdriver.common.by import By
import requests

if __name__ == '__main__':
	token = '1bad0b44-9e00-4979-8b22-f2ed8bc23b75-af5261f9-68b0-479b-aaec-dbfd0f80828c';
	
	def consultar_cnpj(cnpj):
		# time.sleep(3)
		url = f'https://api.cnpja.com/office/{cnpj}'
		headers = {'Authorization': token}

		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			return response.json()
		else:
			raise Exception('Não foi possível consultar o CNPJ.')
	
	def escrever_no_arquivo(texto):
		with open("Contatos.txt", "a") as f:
				f.write('\n' + texto)

	def desformatar(texto):
		return texto.replace('.', '').replace('/', '').replace('-', '')
	
	@retry(tries=3, delay=2)
	def ir_para_url(url):
		driver.get(url)

	options = uc.ChromeOptions()
	options.add_argument('--incognito')
	options.add_argument('--start-maximized')
	options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

	options.page_load_strategy = 'eager'
	driver = uc.Chrome(options=options)
	with driver:
			ir_para_url('https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada')

	todosOsCnpjs = []
	paginaAtual = 1;

	driver.find_element(By.XPATH, "//input[@placeholder='Selecione o estado']").send_keys('Distrito Federal')
	driver.find_element(By.XPATH, "//input[@placeholder='Selecione o estado']").send_keys(Keys.ARROW_DOWN)
	driver.find_element(By.XPATH, "//input[@placeholder='Selecione o estado']").send_keys(Keys.ENTER)

	driver.find_element(By.XPATH, "//input[@placeholder='A partir de']").send_keys(datetime.now().strftime('%d-%m-%Y'))

	driver.find_element(By.XPATH,  "//a[text()='Pesquisar']").click()

	pagination_list = driver.find_element(By.CLASS_NAME, "pagination-list")

	time.sleep(1)

    # Encontrar todos os elementos filhos do elemento pagination-list
	paginas = pagination_list.find_elements(By.TAG_NAME, "a")

	qtdMaximaDePaginas = int(paginas[-1].text);

	while paginaAtual <= qtdMaximaDePaginas:
		time.sleep(1)

		cnpjsDaPagina = driver.find_elements(By.CSS_SELECTOR, '#__nuxt > div > div.top-footer > section > div:nth-child(11) > div.column.is-offset-1.is-6 > div > div > div > div > div > article > div > div > p > strong:nth-child(1)')

		for cnpj in cnpjsDaPagina:
			try:
				time.sleep(7)
				
				respostaCnpjJa = consultar_cnpj(desformatar(cnpj.text))

				numero = ' / '.join(a['area'] + a['number'] for a in respostaCnpjJa['phones'])
				email = ' / '.join(a['address'] for a in respostaCnpjJa['emails'])

				texto =  cnpj.text + '  :  ' + numero + '  :  ' + email

				escrever_no_arquivo(texto)


				todosOsCnpjs.append(cnpj.text)

			except Exception as ex:
				time.sleep(5)
				escrever_no_arquivo(str(ex) + '  ' + cnpj.text)

		paginaAtual = paginaAtual + 1
		driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div[2]/section/div[8]/div/nav/a[2]').click()
	
		

	time.sleep(1)
		
