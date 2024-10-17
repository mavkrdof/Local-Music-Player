import json
import os


class Playlist:
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

    def get_videos(self) -> list[str]:
        return self.playlist['songs']
