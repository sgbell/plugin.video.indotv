import requests
import re
import json
from channel import Channel

from aussieaddonscommon import session
from aussieaddonscommon import utils

# The following mivoAuthToken is is where you fill out your own google auth token
mivoAuthTokens={}
mivoAuthTokens['id']=""
mivoAuthTokens['email']=""
mivoAuthTokens['firebase_jwt']=""
mivoAuthTokens['birthday']= ""
mivoAuthTokens['name']=""
mivoAuthTokens['token']=""
mivoAuthTokens['avatar_url']=""
mivoAuthTokens['role']=""
mivoAuthTokens['source']=""
mivoAuthTokens['access_token']=""
mivoAuthTokens['username']=""
mivoAuthTokens['socmed']=""
mivoAuthTokens['can_upload']=False
mivoAuthTokens['premium_until']=0

def fetch_url(url, headers=None):
    with session.Session() as sess:
        sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        if headers:
           sess.headers.update(headers)
        request = sess.get(url)
        try:
            request.raise_for_status()
        except Exception as e:
            raise e
        data = request.text
    return data

def getMivoApiUrls():
    urlList = {}

    urlList['mivoApiService']='https://api.mivo.com/v4/web/'
    urlList['channelList']='channels/watchable/list'
    return urlList

    request = fetch_url("https://www.mivo.com/")
    for mivo_index_line in request.splitlines():
        if mivo_index_line.find('mivo-frontend')!=-1 and mivo_index_line.find('javascript')!=-1:
   #        print(mivo_index_line)
            script_tag_regex = re.compile(r'^.*src=\'(.*\.js).*')
            mivo_frontend_js = script_tag_regex.search(mivo_index_line)
            if mivo_frontend_js.group(1).startswith('http'):
                mivo_frontend_js = mivo_frontend_js.group(1)

    if mivo_frontend_js=='':
        print('Need to check www.mivo.com website, as it has changed')
        exit(1)


    request = fetch_url(mivo_frontend_js)

    mivoApiServer_regex = re.compile(r'mivoApiServer="([^"]*)')
    mivoApiServerMatch = mivoApiServer_regex.search(request)
    urlList['mivoApiService']=mivoApiServerMatch.group(1)

    channelListFunction_regex = re.compile(r'getChannelListAsync=function\(\){(.*)},this.getpart')
    channelListFunction = channelListFunction_regex.search(request)
    channelListUrl_regex = re.compile(r'url:a\.(.*),withCred')
    channelListUrl = channelListUrl_regex.search(channelListFunction.group(1))
    #print(channelListUrl.group(1))
    channelListUrl = channelListUrl.group(1)
    channelListUrl = re.sub(r'mivoApiServer\+"',urlList['mivoApiService'],channelListUrl)
    urlList['channelList']=re.sub(r'"$', '', channelListUrl)
    
    return urlList

def getChannels():
    urlList = getMivoApiUrls()

    request = fetch_url(urlList['mivoApiService']+urlList['channelList'])
    channelList_json = json.loads(request)
    channels = convertChannelList(channelList_json)
    return channels

def convertChannelList(channel_json):
    channelList=[]
    for item in channel_json['data']:
        if item['model']=='CHANNEL':
           channel = Channel()
           channel.name=item['name']
           channel.description=item['description']
           channel.slug=item['slug']
           channel.hd_stream_url=item['hd_stream_url']
           channel.stream_url=item['stream_url']
           channel.thumbnail_url=item['thumbnail_url']
           channel.is_live=item['is_live']
           channel.id=item['id']
           channel.react_session_key=item['react_session_key']
           channel.signature=item['signature']
           channel.video_partner_id=item['video_partner_id']
           channel.decrypter_key=item['decrypter_key']
           channelList.append(channel)
    return channelList
    
def getAuthToken():
    tokenData={}
    urlList = getMivoApiUrls()
    mivoApiServer = urlList['mivoApiService']

    sess = requests.Session()
    sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    sess.headers['referer'] = 'https://www.mivo.com'
    sess.headers['Authorization'] = mivoAuthTokens['token']
    request = sess.get(mivoApiServer+"channels/wms-auth")
    tokenData['wms_auth'] = json.loads(request.text)['sign']
    tokenData['cookies']=cookies_to_string(request.cookies);
    tokenData['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

    return tokenData

def cookies_to_string(cookiejar):
    cookies = []
    for cookie in cookiejar:
        cookies.append('{0}={1}; path={2}; domain={3};'.format(
            cookie.name, cookie.value, cookie.path, cookie.domain))
    return ' '.join(cookies)
