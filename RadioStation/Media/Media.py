import ffmpeg
from datetime import timedelta

class Media:
    def __init__(self, path):
        self.path = path
        self._metadata = ffmpeg.probe(path)['format']

    @property
    def duration(self):
        return timedelta(seconds=float(self._metadata['duration']))

    @property
    def media_type(self):
        return str(self._metadata['format_name'])

    @property
    def size(self):
        return int(self._metadata['size'])

    @property
    def title(self):
        return str(self._metadata.get('tags', {}).get('title'))    




if __name__ == '__main__':
    media = Media('https://archive.org/download/dr_abohabiba_yahoo/%D8%A7%D9%84%D8%B4%D9%8A%D8%AE%20%D8%A3%D8%A8%D9%88%20%D8%A7%D9%84%D8%B9%D9%8A%D9%86%D9%8A%D9%86%20%D8%B4%D8%B9%D9%8A%D8%B4%D8%B9%20-%20%D8%A7%D9%84%D8%A3%D8%B0%D8%A7%D9%86.mp3')
    print(media.duration.total_seconds())
    print(media.size)
    print(media.title)
    print(media.media_type)