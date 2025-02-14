from pathlib import Path
from moviepy.editor import VideoFileClip
from loguru import logger
from utils import configure_logger

configure_logger("extract_audio")


def extract_audio_from_video(video_file_path: Path, base_audio_dir: Path) -> None:
    """
    Extracts the audio from a given video file and saves it as an MP3 file in the specified directory.

    Parameters
    ----------
    video_file_path : Path
        The path to the video file from which audio is to be extracted.
    base_audio_dir : Path
        The base directory where the extracted audio file will be saved.

    Returns
    -------
    None
    """
    try:
        # Construct the output audio file path
        relative_path = video_file_path.relative_to(base_video_dir)
        audio_file_path = base_audio_dir / relative_path.with_suffix('.mp3')

        # Skip if audio file already exists
        if audio_file_path.exists():
            logger.info(f"Audio file {audio_file_path} already exists. Skipping...")
            return

        # Ensure the output directory exists
        audio_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Process the video file
        video = VideoFileClip(str(video_file_path))
        audio = video.audio
        audio.write_audiofile(str(audio_file_path), fps=16_000)
        logger.info(f"Extracted audio from {video_file_path} to {audio_file_path}")
    except Exception as e:
        logger.error(f"Error processing {video_file_path}: {e}")


def process_files(base_video_dir: Path, base_audio_dir: Path) -> None:
    """
    Processes all video files in a given directory, extracting the audio to a specified directory.

    Parameters
    ----------
    base_video_dir : Path
        The directory containing the video files to process.
    base_audio_dir : Path
        The directory where the extracted audio files will be saved.

    Returns
    -------
    None
    """
    for video_file_path in base_video_dir.rglob('*.mkv'):
        extract_audio_from_video(video_file_path, base_audio_dir)


if __name__ == "__main__":
    # Base directories
    base_video_dir = Path('./../data/video')  # Video files directory
    base_audio_dir = Path('./../data/audio')  # Audio files directory

    # Process all files
    process_files(base_video_dir, base_audio_dir)
