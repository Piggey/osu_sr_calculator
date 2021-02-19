from requests import get

# just downloads the .osu file from osu servers
class OsuService(object):
    def getOsuBeatmap(self, map_id):
        url = "https://osu.ppy.sh/osu/" + map_id
        request = get(url)
        if(request.ok):
            return request.content # check that later
        else:
            raise Exception("OsuService failed map_id request")