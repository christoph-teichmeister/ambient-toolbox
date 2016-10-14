import os
from django.conf import settings
import subprocess
import re
import time
from time import gmtime, strftime


def generate_video_thumbnail(videofile, fallback_icon_path, image_path):
    base_path = settings.BASE_PATH
    file_path_wo_extension, extension = os.path.splitext(videofile.name)
    video_path = videofile.url
    full_path = "%s%s" % (base_path, video_path)
    length = getLength(full_path)

    try:
        duration = time.strptime(length, "%H:%M:%S")
        hour = duration.tm_hour
        min = duration.tm_min
        sec = duration.tm_sec
        ##### CONVERT TO SECONDS

        total_seconds = ((hour*60) + min)*60 + sec
        middle_point = total_seconds/2
        new_hor = int(middle_point/3600)
        new_minu = int((middle_point-(new_hor*3600))/60)
        new_seg = middle_point-((new_hor*3600)+(new_minu*60))
        middle_point_full_time = "%02d:%02d:%02d" % (new_hor, new_minu,new_seg)

    except ValueError:
        return fallback_icon_path

    try:
        command = ("ffmpeg -ss %s -i %s/%s -vframes 1 %s/%s -y" % (middle_point_full_time, base_path, video_path, base_path, image_path)).split()
        subprocess.call(command)
        return image_path

    except Exception, e:
        return fallback_icon_path


def getLength(filename):
    try:
        result = subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    except Exception, e:
        return "00:00:00"

    returnStr = [x for x in result.stdout.readlines() if "Duration" in x]

    if len(returnStr) > 0:
        matches = re.match('Duration:\s([0-9:]+)\.[0-9]+,', str(returnStr[0]).strip())
        return matches.group(1)
    else:
        return "00:00:00"

