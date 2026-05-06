from playwright.sync_api import sync_playwright
import json
import time
import requests
import os
from io import BytesIO
from PIL import Image
from datetime import datetime

def download_image_clean(image_url):
    try:
        image_url = image_url.replace('\\', '')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=15)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"  [+] Gagal download: {e}")
        return None

def save_hd_image(image_url, username):
    try:
        save_dir = "tiktok_avatars"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        image_url = image_url.replace('\\', '')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.tiktok.com/'
        }
        
        response = requests.get(image_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_{timestamp}_HD_{width}x{height}.jpg"
        filepath = os.path.join(save_dir, filename)
        
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                rgb_img.paste(img, mask=img.split()[-1])
            else:
                rgb_img.paste(img)
            rgb_img.save(filepath, 'JPEG', quality=100)
        else:
            img.save(filepath, 'JPEG', quality=100)
        
        if '100x100' in image_url or 'webp' in image_url:
            hd_url = image_url.replace('100x100', '1080x1080').replace('.webp', '.jpg')
            if hd_url != image_url:
                try:
                    hd_response = requests.get(hd_url, headers=headers, timeout=15)
                    if hd_response.status_code == 200:
                        hd_img = Image.open(BytesIO(hd_response.content))
                        hd_w, hd_h = hd_img.size
                        hd_filepath = os.path.join(save_dir, f"{username}_{timestamp}_ULTRA_HD_{hd_w}x{hd_h}.jpg")
                        hd_img.save(hd_filepath, 'JPEG', quality=100)
                        return hd_filepath
                except:
                    pass
        
        return filepath
    except Exception as e:
        print(f"  [+] Gagal menyimpan HD image: {e}")
        return None

def show_image_truecolor(image_url, width=70, height=35):
    try:
        img = download_image_clean(image_url)
        if img is None: return False
        
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        if img.mode != 'RGB': img = img.convert('RGB')
        
        print("\n" + "="*80)
        print("Photo Profile Preview")
        print("="*80)
        for y in range(height):
            line = ""
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                line += f"\033[38;2;{r};{g};{b}m█\033[0m"
            print(line)
        print("="*80)
        return True
    except Exception as e:
        print(f"  [+] Gagal truecolor: {e}")
        return False

def scrape_tiktok_profile(username):
    username = username.replace('@', '')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print(f"\n[+] Mengakses profil @{username}...")
            page.goto(f"https://www.tiktok.com/@{username}", wait_until="networkidle")
            time.sleep(3)
            
            json_script = page.query_selector('script#__UNIVERSAL_DATA_FOR_REHYDRATION__')
            if not json_script:
                print("[+] Tidak menemukan data")
                return
            
            data = json.loads(json_script.text_content())
            user_info = data['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']
            user = user_info['user']
            stats = user_info.get('stats', {})
            
            avatar_url = user.get('avatarLarger', '') or user.get('avatarMedium', '')
            
            if avatar_url:
                show_image_truecolor(avatar_url)
                saved_file = save_hd_image(avatar_url, username)
                if saved_file:
                    print(f"\n[+] Avatar HD berhasil disimpan di: {saved_file}")
            
            print("\n" + "="*80)
            print(f"[+] USERNAME: @{user.get('uniqueId')}")
            print("="*80)
            print(f"[+] Nama: {user.get('nickname', 'N/A')}")
            print(f"[+] Followers: {stats.get('followerCount', 0):,}")
            print(f"[+] Following: {stats.get('followingCount', 0):,}")
            print(f"[+] Total Likes: {stats.get('heartCount', 0):,}")
            print(f"[+] Verified: {'Ya' if user.get('verified') else 'Tidak'}")
            if user.get('signature'):
                print(f"[+] Bio: {user['signature'][:150]}")
            print("="*80)
            
        except Exception as e:
            print(f"[+] Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           TIKTOK PROFILE SCANNER WITHOUT LOGIN               ║
    ╟──────────────────────────────────────────────────────────────╢
    ║                       PRAWIRA REXSA                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    username = input("Masukkan username TikTok (tanpa @): ").strip()
    if username:
        scrape_tiktok_profile(username)
    else:
        print("[+] Username tidak boleh kosong!")
