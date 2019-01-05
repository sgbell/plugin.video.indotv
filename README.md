Indonesian TV addon for Kodi, using external libraries from Aussie Addon
========================================================================

1. To Configure this plugin for your own use:
  You need to obtain a auth token for the mivo website using your google account. I do not use this, and I'm not connected with mivo.com, just using their service
  a) This takes a little bit of tech - knowhow, but first you need to open a browser and have the developer console open.
  b) Go to https://api.mivo.com/v4/web/oauth/google in your browser and log in to your google account
  c) Look at the network responses after you have logged in to your google account, and look at the response for:
     https://api.mivo.com/v2/web/oauth/google (the current url in your url bar)
  d) For each of the values in var oauth_pairs, you need to copy and paste those values into the file: resources/lib/comm.py From line 11-24
  e) From the look of it, the auth token expires in 12 months, so rinse and repeat in 12 months time.

2. For this plugin to work, it requires the following plugins installed in Kodi:
   AussieAddonsCommon - https://github.com/aussieaddons/script.module.aussieaddonscommon
   script.common.plugin.cache - This should be installed with kodi automatically
