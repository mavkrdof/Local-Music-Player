import vlc
import asyncio


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