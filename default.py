import os
import sys
import xbmcaddon
import xbmcgui

from aussieaddonscommon import utils

# Add our resources/lib to the python path
addon_dir = xbmcaddon.Addon().getAddonInfo('path')
sys.path.insert(0, os.path.join(addon_dir, 'resources', 'lib'))

import channels

if __name__ == '__main__':
    params_str = sys.argv[2]
    params = utils.get_url(params_str)

    if (len(params)==0):
        channels.make_channel_list()
    elif 'play' in params:
        # play channel
        channels.play(params_str)
    elif 'category' in params:
        if params['category']=='settings':
            xbmcaddon.Addon().openSettings()
