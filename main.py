from dotenv import load_dotenv
from googleapiclient.discovery import build
import os
import yt_dlp


def main(video_folder: str = None, query: str | None = None) -> str:
    if video_folder is None:
        video_folder = input(
            'Enter video folder path (C:\\Users\\USERFOLDER\\Downloads): '
            )
    if query is None:
        query = input('Enter search query: ')
    youtube = init_youtube()
    search_results = search(query, youtube)
    result = choose_result(search_results)
    print(result)
    video_path = download_video(
        result['value'],
        result['name'],
        video_folder=video_folder
        )
    video_path = ''
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

def choose_result(search_results, display=True) -> dict:
    if display:
        print('Choose a result: ')
        for count, value in enumerate(search_results):
            print(f"{count}) {value['name']}")
        result = search_results[int(input('>>> '))]
    return result


def download_video(video_url: str, video_name: str, video_folder: str) -> str:
    file_path = os.path.join(video_folder, f'{video_name}.mp4')
    options = {
        'outtmpl': file_path,
    }
    with yt_dlp.YoutubeDL(options) as youtube_dl:
        youtube_dl.download(video_url)
    return file_path


if __name__ == '__main__':
    main()
