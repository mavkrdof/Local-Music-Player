import vlc
import threading
import multiprocessing
import json
import os


class Vlc_media_player:
    def __init__(self, config_path: str):
        self.config_file_path = config_path
        self.vlc_instance: vlc.Instance = vlc.Instance()
        self.vlc_player: vlc.MediaListPlayer = self.vlc_instance.media_list_player_new()
        self.stop_player_event = threading.Event()
        self.update_volume_event = threading.Event()
        self.toggle_pause_player_event = threading.Event()
        self.add_video_event = threading.Event()
        self.new_video_list = []
        self.volume: int = self.get_volume()
        self.main_loop()

    def open_media_player(self, audio_only: bool = False):
        # hide the vlc window if audio_only is True
        if audio_only:
            self.vlc_player.add_option('--aout=opensles')
        # run player_play in a separate thread
        self.main_loop()
        print('Media player started')

    def get_volume(self) -> int:
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as file:
                config_data = json.load(file)
                volume = config_data['volume']
        else:
            with open(self.config_file_path, 'w') as file:
                volume = 100
                json.dump({'volume': volume}, file)
        return volume

    def main_loop(self):
        # play the video
        self.vlc_player.play()

    def clear_queue(self):
        pass

    def add_videos(self, video_list: list[str]):
        print(video_list)
        self.vlc_player.set_media_list(self.vlc_instance.media_list_new(video_list))
