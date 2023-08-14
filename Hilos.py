from selenium import webdriver
import concurrent.futures
import time
import openpyxl

def measure_load_time(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    
    start_time = time.time()
    driver.get(url)
    driver.implicitly_wait(10)
    end_time = time.time()
    
    load_time = end_time - start_time
    driver.quit()
    
    return load_time

def update_excel(file_path, results):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    
    # Encontrar la última fila con datos en la columna B y C
    last_row_b = sheet.max_row + 1
    last_row_c = sheet.max_row + 1
    
    # Agregar nuevos datos debajo de los datos existentes
    for i, load_time in enumerate(results, start=1):
        if i == 1:  # index.html data in column B
            sheet[f'B{last_row_b}'] = load_time
            last_row_b += 1
        elif i == 2:  # anyel.html data in column C
            sheet[f'C{last_row_c}'] = load_time
            last_row_c += 1
    
    workbook.save(file_path)
    print('Datos guardados en el archivo Excel.')

def measure_load_time(url, delay):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    
    start_time = time.time()
    driver.get(url)
    driver.implicitly_wait(10)
    end_time = time.time()
    
    load_time = end_time - start_time
    driver.quit()

    # Agregar un retardo antes de cargar la próxima URL
    time.sleep(delay)
    
    return load_time

file_path = 'Tefita.xlsx'
urls = [
    'https://anyelec.000webhostapp.com/',
    'https://www.anyel.lovestoblog.com/'
]

num_executions = 3

for _ in range(num_executions):
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(measure_load_time, url, 1): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            load_time = future.result()
            results.append(load_time)
            print(f'Valor guardado para {url}: {load_time:.6f} segundos')

    # Actualizar y guardar los datos en el archivo Excel
    update_excel(file_path, results)
