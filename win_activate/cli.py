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
    import winrm
    import re
    from string import Template
    pkgdir = sys.modules['win_activate'].__path__[0]
    args = yamlarg.parse(os.path.join(pkgdir, 'arguments.yaml'))
    print(args)

    target_template = Template(args['winrm_url'])

    for host in args['hosts'].split(','):
        if args['un'] is None:
            username = get_or_set_password(host, 'username')
        else:
            username = args['un']
        if args['pw'] is None:
            password = get_or_set_password(host, 'password')
        else:
            password = args['pw']
        s = winrm.Session(target=target_template.substitute(host=host),
                          auth=(username, password),
                          transport=args['transport'],
                          server_cert_validation=args['cert_validation'])
        output = s.run_cmd('cscript.exe /nologo "%systemroot%\system43\slmgr.vbs" /ipk ' + args['pk'])
        if 'Installed product key' not in output.std_out:
            print('Product key not successfully installed on ' + host)
        else:
            output = s.run_cmd('cscript.exe /nologo "%systemroot%\system32\slmgr.vbs" /dti')
            installation_id = re.match(r'Installation ID: (\d+)', output.std_out)
            if installation_id is None:
                print('Error getting Installation ID on ' + host)
            else:
                driver = get_chromedriver()
                driver.get(
                    'https://microsoft.gointeract.io/interact/index?interaction=1461173234028-3884f8602eccbe259104553afa8415434b4581-05d1&accountId=microsoft&loadFrom=CDN&appkey=196de13c-e946-4531-98f6-2719ec8405ce&Language=English&name=pana&CountryCode=en-US&Click%20To%20Call%20Caller%20Id=+17142064889&startedFromSmsToken=3jUenpr&dnis=26&token=0Yr8Nd')
                button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/ul/li[2]/a')
                button.click()
                form = driver.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/div/div[1]/p/table/tbody/tr[1]/td[1]/div[2]/div/input')
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
                    p = driver.find_element_by_xpath(part)
                    activation += p.text

                activation_cmd = s.run_cmd('cscript.exe /nologo "%systemroot%\system32\slmgr.vbs" /atp ' + activation)
                if 'deposited successfully' in activation_cmd.std_out:
                    print("Activation successfull for " + host)
                else:
                    print("Error on host " + host)
                    print(activation_cmd.std_out)

