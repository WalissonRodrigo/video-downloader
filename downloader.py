import os
import sys
import json
from datetime import datetime
from tqdm import tqdm
import yt_dlp
from colorama import init, Fore, Style
# Import translations from the separate file
from translations import TRANSLATIONS

# Inicializa colorama para formatar texto no terminal
init()

# Dictionary with translations moved to translations.py

class VideoDownloader:
    def __init__(self, language='pt'):
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads", "VideoDownloader")
        self.history_file = os.path.join(self.download_path, "download_history.json")
        self.language = language
        self.texts = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        
        # Criar diretório de downloads se não existir
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        
        # Carregar histórico se existir
        self.history = self.load_history()
        self.progress_bar = None
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
    
    def download_progress_hook(self, d):
        if d['status'] == 'downloading':
            if self.progress_bar is None and 'total_bytes' in d:
                self.progress_bar = tqdm(
                    total=d['total_bytes'],
                    unit='B',
                    unit_scale=True,
                    desc=f"Baixando {d.get('filename', 'arquivo')}"
                )
            
            if self.progress_bar is not None:
                if 'downloaded_bytes' in d:
                    self.progress_bar.update(d['downloaded_bytes'] - self.progress_bar.n)
        
        elif d['status'] == 'finished':
            if self.progress_bar is not None:
                self.progress_bar.close()
            print(f"{Fore.GREEN}{self.texts['download_completed']}{Style.RESET_ALL}")
            self.progress_bar = None
    
    def download_video(self, url, quality='best'):
        print(f"{Fore.CYAN}{self.texts['analyzing_url'].format(url)}{Style.RESET_ALL}")
        
        self.progress_bar = None
        
        ydl_opts = {
            'format': 'best' if quality == 'best' else f'best[height<={quality}]',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.download_progress_hook],
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', self.texts['unknown_video'])
                
                print(f"{Fore.YELLOW}{self.texts['title'].format(title)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{self.texts['duration'].format(info.get('duration_string', self.texts['unknown_duration']))}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{self.texts['starting_download']}{Style.RESET_ALL}")
                
                ydl.download([url])
                
                # Salvar no histórico
                self.history.append({
                    'title': title,
                    'url': url,
                    'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    'quality': quality,
                    'platform': info.get('extractor', self.texts['unknown_duration'])
                })
                
                self.save_history()
                
                return True, title
                
        except Exception as e:
            print(f"{Fore.RED}{self.texts['download_error'].format(str(e))}{Style.RESET_ALL}")
            return False, str(e)
    
    def show_history(self):
        if not self.history:
            print(f"{Fore.YELLOW}{self.texts['no_history']}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{self.texts['history_title']}{Style.RESET_ALL}")
        for i, item in enumerate(self.history, 1):
            print(f"{Fore.WHITE}{i}. {item['title']}{Style.RESET_ALL}")
            print(f"   URL: {item['url']}")
            print(f"   Data: {item['date']}")
            print(f"   Plataforma: {item['platform']}")
            print(f"   Qualidade: {item['quality']}")
            print()
    
    def clear_history(self):
        self.history = []
        self.save_history()
        print(f"{Fore.GREEN}{self.texts['history_cleared']}{Style.RESET_ALL}")
    
    def change_language(self, language):
        if language in TRANSLATIONS:
            self.language = language
            self.texts = TRANSLATIONS[language]
            return True
        return False

def main():
    # Load default language from config file if exists
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    default_language = 'pt'
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_language = config.get('language', 'pt')
        except:
            pass
    
    downloader = VideoDownloader(language=default_language)
    
    while True:
        print(f"\n{Fore.CYAN}{downloader.texts['app_title']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{downloader.texts['menu_download']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{downloader.texts['menu_history']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{downloader.texts['menu_clear']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{downloader.texts['menu_language']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{downloader.texts['menu_exit']}{Style.RESET_ALL}")
        
        choice = input(f"\n{downloader.texts['choose_option']}")
        
        if choice == '1':
            url = input(f"{downloader.texts['enter_url']}")
            print(f"\n{downloader.texts['video_quality']}")
            print(f"{downloader.texts['best_quality']}")
            print(f"{downloader.texts['720p']}")
            print(f"{downloader.texts['480p']}")
            print(f"{downloader.texts['360p']}")
            
            quality_choice = input(f"{downloader.texts['choose_quality']}")
            
            quality_map = {
                '1': 'best',
                '2': '720',
                '3': '480',
                '4': '360'
            }
            
            quality = quality_map.get(quality_choice, 'best')
            
            success, message = downloader.download_video(url, quality)
            if success:
                print(f"{Fore.GREEN}{downloader.texts['download_success'].format(message)}{Style.RESET_ALL}")
                print(f"{downloader.texts['saved_in'].format(downloader.download_path)}")
        
        elif choice == '2':
            downloader.show_history()
        
        elif choice == '3':
            confirm = input(f"{downloader.texts['confirm_clear']}")
            if confirm.lower() in ['s', 'y']:
                downloader.clear_history()
        
        elif choice == '4':
            print(f"\n{downloader.texts['language_options']}")
            print(f"{downloader.texts['language_en']}")
            print(f"{downloader.texts['language_pt']}")
            
            lang_choice = input(f"{downloader.texts['choose_language']}")
            
            lang_map = {
                '1': 'en',
                '2': 'pt'
            }
            
            new_lang = lang_map.get(lang_choice)
            if new_lang and downloader.change_language(new_lang):
                print(f"{Fore.GREEN}{downloader.texts['language_changed']}{Style.RESET_ALL}")
                
                # Save language preference to config file
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump({'language': new_lang}, f, ensure_ascii=False, indent=4)
            else:
                print(f"{Fore.RED}{downloader.texts['invalid_option']}{Style.RESET_ALL}")
        
        elif choice == '5':
            print(f"{Fore.GREEN}{downloader.texts['exiting']}{Style.RESET_ALL}")
            break
        
        else:
            print(f"{Fore.RED}{downloader.texts['invalid_option']}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Get the current language from config file
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        language = 'pt'
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    language = config.get('language', 'pt')
            except:
                pass
        
        texts = TRANSLATIONS.get(language, TRANSLATIONS['en'])
        print(f"\n{Fore.YELLOW}{texts['interrupted']}{Style.RESET_ALL}")
        sys.exit(0)