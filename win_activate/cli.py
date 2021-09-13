def setpass(service, username):
    import keyring
    import getpass
    keyring.set_password(service,
                         username,
                         getpass.getpass('Enter the ' + username + ' for ' + service + ': '))


def get_or_set_password(service, username):
    import keyring
    creds = keyring.get_password(service, username)
    if creds is None:
        setpass(service, username)
        creds = keyring.get_password(service, username)
    return creds


def get_chromedriver():
    from selenium import webdriver
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
        return driver
    except:
        import traceback
        import platform
        import subprocess
        import requests
        import re
        import zipfile
        import io
        import os
        print(traceback.format_exc())
        print("fetching new chromedriver...")
        URL = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'
        system = platform.system()
        if system == 'Darwin':  # macos
            version = subprocess.Popen('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
                                       shell=True,
                                       stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            chrome_version = re.match(r'.*?(\d+\.\d+\.\d+)\.\d+.*?', version).group(1)
            r = requests.get(url=URL + chrome_version)
            cd_version = r.content.decode('utf-8')
            dl_url = 'https://chromedriver.storage.googleapis.com/' + cd_version
            zip_file_url = dl_url + '/chromedriver_mac64.zip'
        else:  # system == 'Linux':
            version = subprocess.Popen('chromium --version',
                                       shell=True,
                                       stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            chrome_version = re.match(r'.*?(\d+\.\d+\.\d+)\.\d+.*?', version).group(1)
            r = requests.get(url=URL + chrome_version)
            cd_version = r.content.decode('utf-8')
            dl_url = 'https://chromedriver.storage.googleapis.com/' + cd_version
            zip_file_url = dl_url + '/chromedriver_linux64.zip'
        r2 = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r2.content))
        z.extractall('/usr/local/bin/')
        os.chmod('/usr/local/bin/chromedriver', 0o755)
        return get_chromedriver()


def main():
    import yamlarg
    import sys
    import os
    from pypsrp.client import Client
    import re
    pkgdir = sys.modules['win_activate'].__path__[0]
    args = yamlarg.parse(os.path.join(pkgdir, 'arguments.yaml'))
    for host in args['hosts'].split(','):
        if args['un'] is None:
            username = get_or_set_password(host, 'username')
        else:
            username = args['un']
        if args['pw'] is None:
            password = get_or_set_password(host, 'password')
        else:
            password = args['pw']
        if args['ssl'].lower() in ['false', 'f', 'no', 'n']:
            ssl = False
        else:
            ssl = True
        if args['cert_validation'].lower() in ['false', 'f', 'no', 'n']:
            cert_validation = False
        else:
            cert_validation = True
        with Client(server=host,
                    username=username,
                    password=password,
                    cert_validation=cert_validation,
                    ssl=ssl,
                    auth=args['auth']) as client:
            stdout, stderr, rc = client.execute_cmd('cscript.exe /nologo "%systemroot%\system32\slmgr.vbs" /ipk ' + args['pk'])
            print(stdout)
            if 'Installed product key' not in stdout:
                print('Product key not successfully installed on ' + host)
            else:
                stdout, stderr, rc = client.execute_cmd('cscript.exe /nologo "%systemroot%\system32\slmgr.vbs" /dti')
                # output = s.run_cmd('cscript.exe /nologo "%systemroot%\system32\slmgr.vbs" /dti')
                installation_id = re.match(r'Installation ID: (\d+)', stdout)
                print(stdout)
                if installation_id is None:
                    print('Error getting Installation ID on ' + host)
                else:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    driver = get_chromedriver()
                    driver.get(args['gointeract_url'])
                    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/ul/li[2]/a')))
                    button.click()
                    form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                        '/html/body/div[2]/div[2]/div/div[1]/p/table/tbody/tr[1]/td[1]/div[2]/div/input')))
                    form.send_keys('621269419226619141744168869550091732602151832659274865349851206')
                    button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/ul/li[1]/a')
                    button.click()
                    parts = ['/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[2]/td[1]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[2]/td[2]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[2]/td[3]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[4]/td[1]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[4]/td[2]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[4]/td[3]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[6]/td[1]',
                             '/html/body/div[2]/div[2]/div/div[1]/p/div/table/tbody/tr[6]/td[2]']
                    activation = ''
                    for part in parts:
                        p = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, part)))
                        activation += p.text
                    driver.quit()
                    stdout, stderr, rc = client.execute_cmd(
                        'cscript.exe /nologo "%systemroot%\system32\slmgr.vbs" /atp ' + activation)
                    print(stdout)
                    if 'deposited successfully' in stdout:
                        print("Activation successfull for " + host)
                    else:
                        print("Error on host " + host)

