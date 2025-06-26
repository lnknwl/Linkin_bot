import os
import re
import vlc
import time
import json
import threading
from yt_dlp import YoutubeDL

class MusicPlayer:
    def __init__(self):
        self.queue = []
        self.queue_path = os.path.join(os.path.dirname(__file__), "queue.json")
        self.load_queue()

        self.current_user = None
        self.current_player = None
        self.current_title = None
        self.skip_requested = False

        self.playing = False
        self.music_dir = os.path.abspath(os.path.dirname(__file__))

        if self.queue and not self.playing:
            threading.Thread(target=self.play_queue, daemon=True).start()
    
    def load_queue(self):
        try:
            with open(self.queue_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.queue = [(item["url"], item["title"], item["user"]) for item in data]
        except FileNotFoundError:
            self.queue = []
        except Exception as e:
            print(f"Ошибка загрузки очереди: {e}")
            self.queue = []

    def save_queue(self):
        try:
            with open(self.queue_path, "w", encoding="utf-8") as f:
                json.dump(
                    [
                        {"url": url, "title": title, "user": user}
                        for url, title, user in self.queue
                    ],
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception as e:
            print(f"Ошибка сохранения очереди: {e}")

    def add_to_queue(self, url, username):
        try:
            audio_url, title = self.get_audio_url(url)
            clean_title = self.clean_title(title)  # Очищаем заголовок
            self.queue.append((audio_url, clean_title, username))
            self.save_queue()

            if not self.playing:
                threading.Thread(target=self.play_queue, daemon=True).start()

            return True
        except Exception as e:
            print(f"Ошибка добавления в очередь: {e}")
            return False
    
    def cancel_last_request(self, username):
        for i in range(len(self.queue) - 1, -1, -1):
            if self.queue[i][2] == username:
                removed = self.queue.pop(i)
                self.save_queue()
                return removed
        return None

    def get_audio_url(self, url):
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'noplaylist': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url'], info.get("title", "Неизвестно")
        
    def get_device(self, name_part):
        instance = vlc.Instance()
        player = instance.media_player_new()

        outputs = player.audio_output_device_enum()
        current = outputs

        while current:
            desc = current.contents.description.decode()
            dev_id = current.contents.device.decode()

            if name_part.lower() in desc.lower():
                return dev_id

            current = current.contents.next

        return None
    
    def clean_title(self, title: str) -> str:
        if not title:
            return "Неизвестно"

        title = re.sub(r'\[[^\]]*\]', '', title)
        title = re.sub(r'\([^\)]*\)', '', title)

        title = re.sub(r'[#@]\w+', '', title)

        blacklist = [
            '4k', '8k', 'remastered', 'enhanced', 'official video',
            'audio', 'version', 'hd', 'lyrics', 'live', 'full album',
            'full song', 'explicit', 'clean', 'visualizer'
        ]

        pattern = r'\b(?:' + '|'.join(map(re.escape, blacklist)) + r')\b'
        title = re.sub(pattern, '', title, flags=re.IGNORECASE)

        title = re.sub(r'\s{2,}', ' ', title).strip()

        return title or "Неизвестно"

    def save_current_track_info(self, clean_title, username):
        try:
            short_title = clean_title[:32] + "..." if len(clean_title) > 32 else clean_title
            with open(os.path.join(self.music_dir, "title.txt"), "w", encoding="utf-8") as f:
                f.write(f" {short_title} ")
        except Exception as e:
            print(f"Ошибка записи title.txt: {e}")

        try:
            with open(os.path.join(self.music_dir, "requester.txt"), "w", encoding="utf-8") as f:
                f.write(f"  Заказ от {username} ")
        except Exception as e:
            print(f"Ошибка записи requester.txt: {e}")
    
    def get_current_title(self):
        return self.current_title

    def play_queue(self):
        self.playing = True
        while self.queue:
            url, title, user = self.queue.pop(0)
            self.save_queue()

            cleaned_title = self.clean_title(title)
            self.save_current_track_info(cleaned_title, user)
            self.current_title = cleaned_title

            print(f"Сейчас играет: {title} от {user}")
            
            instance = vlc.Instance()
            player = instance.media_player_new()
            
            device = self.get_device('CABLE Input')
            if device:
                player.audio_output_device_set(None, device)

            media = instance.media_new(url)

            self.current_player = player
            self.current_user = user
            self.skip_requested = False

            player.set_media(media)
            time.sleep(0.2)
            player.play()

            for vol in range(0, 101, 20):
                player.audio_set_volume(vol)
                time.sleep(0.05)

            while True:
                state = player.get_state()
                if state in [vlc.State.Ended, vlc.State.Error] or self.skip_requested:
                    for vol in range(100, -1, -20):
                        player.audio_set_volume(vol)
                        time.sleep(0.05)
                    player.stop()
                    break
            
        self.current_player = None
        self.current_title = None
        self.current_user = None
        self.playing = False
