from dotenv import load_dotenv
from googleapiclient.discovery import build
import os
import yt_dlp
import vlc
import asyncio


def main(video_folder: str = None, query: str | None = None, input_mode: str = 'cmd') -> str:
    if video_folder is None:
        video_folder = input(
            'Enter video folder path (C:\\Users\\USERFOLDER\\Downloads): '
            )
    if query is None:
        if input_mode == 'cmd':
            query = input('Enter search query: ')
    youtube = init_youtube()
    search_results = search(query, youtube)
    if input_mode == 'cmd':
        result = choose_result_cmd(search_results)
    video_path = download_video(
        result['value'],
        result['name'],
        video_folder=video_folder
        )
    if input_mode == 'cmd':
        play_video_vlc(video_path)
    return video_path


def init_youtube():
    load_dotenv()
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    youtube = build(
        'youtube',
        'v3',
        developerKey=YOUTUBE_API_KEY
    )
    return youtube


def search(query, youtube):
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


def choose_result_cmd(search_results, display=True) -> dict:
    if display:
        print('Choose a result: ')
        for count, value in enumerate(search_results):
            print(f"{count}) {value['name']}")
        result = search_results[int(input('>>> '))]
    return result


def download_video(video_url: str, video_name: str, video_folder: str) -> str:
    file_name_sanitized = yt_dlp.utils.sanitize_filename(video_name + '.mp4')
    file_path = os.path.join(video_folder, file_name_sanitized)
    options = {
        'outtmpl': file_path,
    }
    with yt_dlp.YoutubeDL(options) as youtube_dl:
        youtube_dl.download(video_url)
    return file_path


def play_video_open(video_path: str):
    os.startfile(video_path)


def play_video_vlc(video_path: str, audio_only: bool = False):
    vlc_instance = vlc.Instance()
    vlc_player = vlc_instance.media_player_new(video_path)
    # hide the vlc window if audio_only is True
    if audio_only:
        vlc_player.add_option('--aout=opensles')
    asyncio.create_task(player_play(vlc_player))
    if input('Press enter to exit') == '':
        vlc_player.stop()


def player_play(vlc_player):
    # play the video
    vlc_player.play()
    # wait for the player to load
    while not vlc_player.is_playing():
        pass
    # wait for the player to finish
    while vlc_player.is_playing():
        pass


if __name__ == '__main__':
    main()
