from dotenv import load_dotenv
from googleapiclient.discovery import build
import os
import yt_dlp
import vlc_media_playing as vlc_player
import playlists
import multiprocessing as m_processing


class Local_Music_Player:
    def __init__(self, video_folder: str, playlist_folder: str, config_path: str) -> None:
        self.video_folder = video_folder
        self.playlist_folder = playlist_folder
        self.vlc_player = vlc_player.Vlc_media_player(
            video_list=[],
            config_path=config_path
        )

    def download_and_play_on_cmd(self, query: str | None = None) -> str:
        if query is None:
            query = input('Enter search query: ')
        youtube = self.init_youtube()
        search_results = self.search(query, youtube)
        result = self.choose_result_cmd(search_results)
        video_path = self.download_video(
            result['value'],
            result['name'],
            video_folder=video_folder
            )
        vlc_player.play_video_vlc(video_path)
        return video_path

    def create_playlist_on_cmd(self):
        playlist_name = input('Enter playlist name: ')
        plist = self.create_playlist(playlist_name)
        while input('Add to playlist? (y/n) ').lower() == 'y':
            video_name = input('Enter video name: ')
            video_path = os.path.join(self.video_folder, video_name + '.mp4')
            plist.add_video(video_path, video_name=video_name)
        return plist

    def init_youtube(self, ):
        load_dotenv()
        YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
        youtube = build(
            'youtube',
            'v3',
            developerKey=YOUTUBE_API_KEY
        )
        return youtube

    def search(self, query, youtube):
        request = youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=5,
            type='video'
        )

        response = request.execute()

        search_results = []

        for video in response['items']:
            title = video["snippet"]["title"]
            video_id = video["id"]["videoId"]
            item = {
                'name': title,
                'value': f'https://www.youtube.com/watch?v={video_id}',
            }

            search_results.append(item)

        return search_results

    def choose_result_cmd(self, search_results, display=True) -> dict:
        if display:
            print('Choose a result: ')
            for count, value in enumerate(search_results):
                print(f"{count}) {value['name']}")
            result = search_results[int(input('>>> '))]
        return result

    def download_video(self, video_url: str, video_name: str, video_folder: str) -> str:
        file_name_sanitized = yt_dlp.utils.sanitize_filename(video_name + '.mp4')
        file_path = os.path.join(video_folder, file_name_sanitized)
        options = {
            'outtmpl': file_path,
        }
        with yt_dlp.YoutubeDL(options) as youtube_dl:
            youtube_dl.download(video_url)
        return file_path

    def create_playlist(self, name: str):
        plist = playlists.Playlist(name, self.playlist_folder)
        plist.save_playlists()
        return plist

    def play_playlist(self, plist: playlists.Playlist, clear_queue=True):
        videos = plist.get_videos()
        if clear_queue:
            self.vlc_player.clear_queue()
        self.vlc_player.add_videos(videos)


def run_cmd():
    video_folder = input(
        'Enter video folder path (C:\\Users\\USERFOLDER\\Downloads): '
        )
    playlists_folder = input(
        'Enter playlist folder path (C:\\Users\\USERFOLDER\\Playlists): '
        )
    config_path = input(
        'Enter config path (C:\\Users\\USERFOLDER\\config.json): '
        )
    lmp = Local_Music_Player(video_folder, playlists_folder, config_path)
    plist = lmp.create_playlist_on_cmd()
    lmp.play_playlist(plist)
    lmp.vlc_player.open_media_player()
    # print('starting media player')
    # process_1 = m_processing.Process(target=lmp.vlc_player.open_media_player, args=(False,))
    # process_1.start()
    # print('starting cmd')
    # prosess_2 = m_processing.Process(target=lmp.create_playlist_on_cmd, args=())
    # prosess_2.start()
    # process_1.join()
    # prosess_2.join()


if __name__ == '__main__':
    run_cmd()
