import json
import os
import vlc_media_playing as vlc_player


class Playlists:
    def __init__(self, name, playlists_folder):
        self.name = name
        self.file_path = os.path.join(playlists_folder, name) + '.json'
        self.playlist = self.load_playlists()

    def load_playlists(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        else:
            return {
                'songs': {}
                }

    def save_playlists(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.playlist, file)

    def add_video(self, video_path, video_name):
        self.playlist['songs'][video_name] = video_path
        self.save_playlists()

    def remove_video(self, video_name):
        del self.playlist['songs'][video_name]
        self.save_playlists()

    def play_playlist(self):
        for video_path in self.playlist['songs'].values():
            vlc_player.play_video_vlc(video_path)
