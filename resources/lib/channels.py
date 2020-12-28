import comm
import sys
import xbmcgui
import xbmcplugin
import urllib
from channel import Channel

from aussieaddonscommon import utils
from future.moves.urllib.parse import quote_plus

def make_channel_list():
    try:
        channels = comm.getChannels()

        ok = True
        for c in channels:
            listitem = xbmcgui.ListItem(label=c.get_name())
            listitem.setArt({'icon':c.get_thumbnail_url(),
                            'thumb':c.get_thumbnail_url()})
            listitem.setInfo('video', c.get_kodi_list_item())
            listitem.setProperty('IsPlayable', 'true')
 
            # Below is the url we will use for playing the channel
            url = "%s?play=true&%s" % (sys.argv[0], c.make_kodi_url())

            utils.log("{} : {}".format(c.get_name(),c.make_kodi_url()))
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                             url=url,
                                             listitem=listitem,
                                             isFolder=False,
                                             totalItems=len(channels))
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
        xbmcplugin.setContent(handle=int(sys.argv[1]), content='movies')

    except Exception:
        utils.handle_error('Unable to fetch channel list')

def play(url):
    try:
        authToken = comm.getAuthToken()
        channel = Channel()
        channel.parse_kodi_url(url)

        stream = channel.get_url()
        stream_url = '{}{}|User-Agent={}&Cookie={}'.format(stream,authToken['wms_auth'],quote_plus(authToken['User-Agent']),quote_plus(authToken['cookies']))
        listitem = xbmcgui.ListItem(label=channel.get_name(),
                                    path=stream_url)
        listitem.setArt({"icon":channel.get_thumbnail_url(),
                         "thumb":channel.get_thumbnail_url()})
                         
        listitem.setInfo('video', channel.get_kodi_list_item())
        if hasattr(listitem, 'addStreamInfo'):
            listitem.addStreamInfo('audio', channel.get_kodi_audio_stream_info())
            listitem.addStreamInfo('video', channel.get_kodi_video_stream_info())

        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=listitem)
    except Exception:
        utils.handle_error('Unable to play stream')
