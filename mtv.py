#!/usr/bin/env python
"""
Given an audio file and an artwork file, create a music video!
You can upload the result to YouTube, etc.
The ffmpeg command is required because that's where the
magic happens.
"""
import traceback
try:
    from contextlib import contextmanager
    import json
    import optparse
    import os
    import sys
    import subprocess
    import tempfile
except ImportError:
    traceback.print_exc()
    print '-' * 80
    print 'Python 2.6 or greater is required'
    print '-' * 80


def main():
    op = optparse.OptionParser(usage='%prog [options]\n' +
                               __doc__)
    op.add_option('-s', '--song', help='path to music song file')
    op.add_option('-a', '--art', help='path to cover art file')
    op.add_option('-o', '--out', help='path to output file', default="mtv.mp4")
    (options, args) = op.parse_args()
    if not options.song or not options.art:
        op.error('incorrect usage')
    if not find_executable('ffmpeg'):
        op.error('could not find the ffmpeg executable')
        
    secs = length(options.song)
    
    try:
        out = os.path.join(os.getcwd(), options.out)
        if os.path.exists(out):
            os.unlink(out)
        # Combine the cover art with the audio.
        ffmpeg_command = ['ffmpeg', '-y', '-loop', '1', '-framerate', '1/60', 
                            '-i', options.art,
                            '-i', options.song,
                            '-strict', '-2',
                            '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-pix_fmt', 'yuv420p',
                            '-t', secs,
                            '-vf', 'scale=w=1920:h=1080:force_original_aspect_ratio=1,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
                            out]
        print " ".join(ffmpeg_command)
        subprocess.check_call(ffmpeg_command)
    finally:
        pass
    with report():
        print 'Your music video awaits: %s' % out.replace(os.getcwd(), '.')

@contextmanager
def report():
    print '-' * 80
    yield
    print '-' * 80


def length(filename):
    sp = subprocess.Popen(['ffprobe', '-v', 'quiet', '-print_format',
                           'json', '-show_format', '-show_streams',
                           filename],
                          stdout=subprocess.PIPE)
    data = json.load(sp.stdout)
    ret = sp.wait()
    if ret != 0:
        raise RuntimeError('ffprobe failed')
    return data['streams'][0]['duration']


def find_executable(name):
    for pt in os.environ.get('PATH', '').split(':'):
        candidate = os.path.join(pt, name)
        if os.path.exists(candidate):
            return candidate


if __name__ == '__main__':
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        traceback.print_exc()
        with report():
            print 'Whoops, that was unexpected'
            print 'You can file a bug: https://github.com/kumar303/mtv/issues'
        sys.exit(1)
