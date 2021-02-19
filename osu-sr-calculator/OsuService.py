from requests import get

# just downloads the .osu file from osu servers
class OsuService(object):
    def getOsuBeatmap(self, map_id):
        url = "https://osu.ppy.sh/osu/" + str(map_id)
        req = get(url)
        if(req):
            return req.text # check that later
        else:
            raise Exception("OsuService failed map_id GET request")