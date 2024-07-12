import time,configparser,os,sys,requests,zipfile
from Static.Static import Static
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pytesseract
    from PIL import Image
    from fake_headers import Headers
    from colorama import Fore,Style
except:
    print('Installing Libraries...')
    os.system("pip install -r requirements.txt")
    print('Libraries installed. Restart the program!')
    sys.exit()

config = configparser.ConfigParser()
config.read('config.cfg')

TYPE = config.get('Settings','TYPE')
VIDEO = config.get('Settings','VIDEO_URL')
AMOUNT = config.getint('Settings','AMOUNT')

WAITING= f"{Fore.YELLOW}[WAITING] "
SUCCESS = f"{Fore.GREEN}[SUCCESS] "
INFO = f"{Fore.BLUE}[INFO] "
WARNING = f"{Fore.RED}[WARNING] "

def Credits():
    print(f"{INFO}{Fore.BLUE}Provided to you by {Fore.CYAN}Sneezedip.{Style.RESET_ALL}")
    print(f"{INFO}{Fore.BLUE}Join Our Discord For More Tools! {Fore.GREEN}https://discord.gg/htbep2Fx{Style.RESET_ALL}")

def Download(url, extract_to='.'):
    response = requests.get(url)
    zip_path = os.path.join(extract_to, "downloaded_file.zip")
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)
def CheckVersion(current_version):
    response = requests.get("https://raw.githubusercontent.com/Sneezedip/Tiktok-Booster/main/VERSION")
    if response.text.strip() != current_version:
        while True:
            u = input(f"{WARNING}{Fore.WHITE}NEW VERSION FOUND. Want to update? (y/n){Style.RESET_ALL}").lower()
            if u == "y":
                Download("https://codeload.github.com/Sneezedip/Tiktok-Booster/zip/refs/heads/main","./")
                print(INFO+"Updated. Check the new folder created.")
                sys.exit()
            elif u == "n":
                return
if not os.path.exists('Tesseract'):
    print(f'{INFO}{Fore.WHITE}Downloading Tesseract, please wait..{Style.RESET_ALL}')
    url = 'https://drive.usercontent.google.com/download?id=10X_TEAwUic4v3pt7TT4w3QNRcS1DNq87&export=download&authuser=0&confirm=t&uuid=19bcdcbd-e7ce-4617-8f41-caca15b5ab17&at=APZUnTWgmGxytaTOOxw-o87dMp8z%3A1720311459869'
    extract_to = './'
    Download(url, extract_to)

class Program():
    def __init__(self):
        self.Options = webdriver.ChromeOptions()
        for option in Static.ChromeOptions:
            self.Options.add_argument(option)
        if config.getboolean('Settings','HEADLESS'): self.Options.add_argument("--headless")
        print(f'\n{WAITING}{Fore.WHITE}Installing Extensions...{Style.RESET_ALL}',end="\r")
        self.Options.add_extension('Extensions/ub.crx')
        print(f"{SUCCESS}{Fore.WHITE}Extensions Installed Sucessfully!{Style.RESET_ALL}")
        self.driver = webdriver.Chrome(options=self.Options)
        self.driver.get('https://zefoy.com/')
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract/tesseract.exe'
        self.driver.find_element(By.XPATH,'/html/body/div[8]/div[2]/div[1]/div[3]/div[2]/button[1]').click()
        time.sleep(0.5)
        while not self.PassCaptcha():
            self.driver.refresh()
            time.sleep(1.5)
            continue
        time.sleep(3)
        self.SelectType()

    def PassCaptcha(self):
        with open('Captcha/captcha.png', 'wb') as file:
            file.write(self.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/form/div/div/img').screenshot_as_png)
        time.sleep(0.1)
        self.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/form/div/div/div/input').send_keys(pytesseract.image_to_string(Image.open('Captcha/captcha.png')))
        print(f"{WAITING}{Fore.WHITE}Passing Captcha..{Style.RESET_ALL}",end="\r")
        if self.PassedCaptcha():
            print(F"{SUCCESS}{Fore.WHITE}Captcha Passed Successfully!{Style.RESET_ALL}")
            return True
        return False
    def PassedCaptcha(self):
        try:
            self.driver.find_element(By.ID,'errorcapthcaclose').click()
            return False
        except:
            return True
        
    def SelectType(self):
        self.driver.find_element(By.XPATH,Static.typeValues[TYPE]).click()
        time.sleep(0.3)
        self.GetViews()

    def GetViews(self):
        time.sleep(0.5)
        self.driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/input').send_keys(VIDEO)
        for _ in range(AMOUNT):
            time.sleep(0.5)
            self.driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/div/button').click()
            time.sleep(3)
            waiting_timer = 0
            while True:
                if not self.isReady():
                    print(f"{WAITING}{Fore.WHITE}Waiting Timer... (x{waiting_timer}){Style.RESET_ALL}",end="\r")
                    time.sleep(3)
                    waiting_timer += 1
                    if waiting_timer >= 50:
                        print(f"{WARNING}Program is waiting for more than 3 minutes. Check Video Link!{Style.RESET_ALL}")
                        sys.exit()
                else:
                    time.sleep(1.5)
                    break
            waiting_timer = 0
            time.sleep(2)
            self.driver.find_element(By.XPATH,'/html/body/div[10]/div/form/div/div/button').click()
            time.sleep(2)
            try:
                self.driver.find_element(By.XPATH,'//*[@id="c2VuZC9mb2xeb3dlcnNfdGlrdG9V"]/div[1]/div/form/button').click()
                print(F"{SUCCESS}{Fore.WHITE}+1000 Views Added Successfully!{Style.RESET_ALL}")
            except:
                self.driver.refresh()
                time.sleep(2)
                self.SelectType()
    def isReady(self):
        return self.driver.find_element(By.XPATH,'//*[@id="c2VuZC9mb2xeb3dlcnNfdGlrdG9V"]/span[1]').text.__contains__('READY') or len(self.driver.find_element(By.XPATH,'//*[@id="c2VuZC9mb2xeb3dlcnNfdGlrdG9V"]/span[1]').text) <= 0
if __name__ == "__main__":  
    CheckVersion("1.1.2")     
    Credits()         
    Program()