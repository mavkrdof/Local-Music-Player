import vlc
import asyncio
import json
import os


class Vlc_media_player:
    def __init__(self, video_list: list[str], config_path: str):
        self.config_file_path = config_path
        self.vlc_instance: vlc.Instance = vlc.Instance()
        self.vlc_player: vlc.MediaPlayer = self.vlc_instance.media_player_new('E:\\Concs\\Documents\\Coding\\Local-Music-Player\\videos\\tiny bald man.mp4')
        self.stop_player_event = asyncio.Event()
        self.update_volume_event = asyncio.Event()
        self.toggle_pause_player_event = asyncio.Event()
        self.volume: int = self.get_volume()
        self.player_play()

    def open_media_player(self, audio_only: bool = False):
        # hide the vlc window if audio_only is True
        if audio_only:
            self.vlc_player.add_option('--aout=opensles')
        self.player_play()

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

    def cmd_vid_control(self):
        if input('Press enter to exit') == '':
            self.stop_player_event.set()

    def player_play(self):
        print('Starting player...')
        # play the video
        self.vlc_player.play()
        # wait for the player to load
        while not self.vlc_player.is_playing():
            pass
        # wait for the player to finish
        while self.vlc_player.is_playing():
            # stop the player
            if self.stop_player_event.is_set():
                self.stop_player_event.clear()
                break
            # update the volume
            if self.update_volume_event.is_set():
                self.update_volume_event.clear()
                self.volume = self.get_volume()
                self.vlc_player.audio_set_volume(self.volume)
            # pause the player
            if self.toggle_pause_player_event.is_set():
                self.toggle_pause_player_event.clear()
                if self.vlc_player.is_playing():
                    self.vlc_player.set_pause(False)
                else:
                    self.vlc_player.set_pause(True)
        # stop the player
        self.vlc_player.stop()

    def clear_queue(self):
        self.vlc_player.release()

    def add_videos(self, video_list: list[str]):
        for video in video_list:
            media = vlc.Media(video)
        self.vlc_player.stop()
        self.vlc_player.set_media(media)
        self.player_play()
