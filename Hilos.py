from selenium import webdriver
import concurrent.futures
import time
import openpyxl

def measure_load_times(urls, num_executions):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    def measure_load_time(url):
        driver = webdriver.Chrome(options=chrome_options)

        start_time = time.time()
        driver.get(url)
        driver.implicitly_wait(10)
        end_time = time.time()

        load_time = end_time - start_time
        driver.quit()

        return load_time

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(num_executions):
            futures = [executor.submit(measure_load_time, url) for url in urls]
            load_times = [future.result() for future in concurrent.futures.as_completed(futures)]
            results.append(load_times)
            print("Carga completada en paralelo.")

    return results

def update_excel(file_path, results):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for load_times in results:
        last_row = sheet.max_row + 1
        for i, load_time in enumerate(load_times, start=1):
            column_letter = chr(66 + i)  # B corresponds to 66 in ASCII
            sheet[f'{column_letter}{last_row}'] = load_time

    workbook.save(file_path)
    print('Datos guardados en el archivo Excel.')

file_path = 'MismoServidor.xlsx' #Nombre del archivo de Excel
urls = [
    'https://anyelec.000webhostapp.com/',
    'https://anyelec.000webhostapp.com/'
]
num_executions = 3
results = measure_load_times(urls, num_executions)
update_excel(file_path, results)