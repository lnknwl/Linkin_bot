import os
import vlc
import time
import threading
from yt_dlp import YoutubeDL

class MusicPlayer:
    def __init__(self):
        self.queue = []
        self.playing = False
        self.music_dir = os.path.abspath(os.path.dirname(__file__))

    def add_to_queue(self, url, username):
        try:
            audio_url, title = self.get_audio_url(url)
            self.queue.append((audio_url, title, username))

            if not self.playing:
                threading.Thread(target=self.play_queue, daemon=True).start()

            return True
        except Exception as e:
            print(f"[Ошибка добавления в очередь] {e}")
            return False

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

    def play_queue(self):
        self.playing = True
        while self.queue:
            url, title, user = self.queue.pop(0)
            print(f"Играет: {title} от {user}")
            
            instance = vlc.Instance()
            player = instance.media_player_new()
            
            device = self.get_device('CABLE Input')
            player.audio_output_device_set(None, device)

            media = instance.media_new(url)
            player.set_media(media)
            player.play()

            while True:
                state = player.get_state()
                if state == vlc.State.Ended or state == vlc.State.Error:
                    break

        self.playing = False
