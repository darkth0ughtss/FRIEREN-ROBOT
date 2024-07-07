import yt_dlp
import os

def download_instagram_reel(link, download_path):
    """
    Download Instagram reel from the given link.

    Args:
        link (str): The link to the Instagram reel.
        download_path (str): The path to download the reel to.

    Returns:
        str: Path to the downloaded video file, or None if failed.
    """
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(id)s.%(ext)s'),
        'format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            video_id = info_dict.get("id", None)
            video_path = os.path.join(download_path, f"{video_id}.mp4")

            if os.path.exists(video_path):
                return video_path
    except Exception as e:
        print(f"Failed to download reel: {e}")
        return None
