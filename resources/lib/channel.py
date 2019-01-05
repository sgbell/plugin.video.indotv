from aussieaddonscommon import utils

class Channel(object):

    def __init__(self):
        self.id = -1
        self.name=None
        self.description=None
        self.slug=None
        self.hd_stream_url=None
        self.stream_url=None
        self.thumbnail_url=None
        self.is_live=None
        self.react_session_key=None
        self.signature=None
        self.video_partner_id=None
        self.decrypter_key=None

    def get_name(self):
        return utils.descape(self.name)

    def get_description(self):
        return utils.descape(self.description)

    def get_slug(self):
        return utils.descape(self.slug)

    def get_url(self):
        if self.hd_stream_url:
            return utils.descape(self.hd_stream_url)
        elif self.stream_url:
            return utils.descape(self.stream_url)

    def get_thumbnail_url(self):
        if self.thumbnail_url:
            return utils.descape(self.thumbnail_url)

    def is_live(self):
        return self.is_live

    def get_kodi_list_item(self):
        info_dict={}
        if self.get_name():
            info_dict['name']= self.get_name()
        if self.get_description():
            info_dict['description']= self.get_description()
        if self.get_slug():
            info_dict['slug']= self.get_slug()
        return info_dict

    def get_kodi_audio_stream_info(self):
        info_dict = {}
        info_dict['codec'] = 'aac'
        info_dict['language'] = 'id'
        info_dict['channels'] = '2'
        return info_dict

    def get_kodi_video_stream_info(self):
        info_dict = {}
        info_dict['codec'] = 'h264'
        if self.hd_stream_url:
            info_dict['width']=''
            info_dict['height']=''
        else:
            info_dict['width']=''
            info_dict['height']=''
        return info_dict

    def make_kodi_url(self):
        d={}
        if self.id:
           d['id']= self.id
        if self.name:
           d['name']= self.name
        if self.description:
           d['description']= self.description
        if self.slug:
           d['slug']=self.slug
        if self.hd_stream_url:
           d['hd_stream_url']=self.hd_stream_url
        if self.stream_url:
           d['stream_url']=self.stream_url
        if self.thumbnail_url:
           d['thumbnail_url']=self.thumbnail_url
        if self.is_live:
           d['is_live']=self.is_live
        if self.react_session_key:
           d['react_session_key']=self.react_session_key
        if self.signature:
           d['signature']=self.signature
        if self.video_partner_id:
           d['video_partner_id']=self.video_partner_id
        if self.decrypter_key:
           d['decrypter_key']=self.decrypter_key
        return utils.make_url(d)

    def parse_kodi_url(self, string):
        d = utils.get_url(string)
        self.id=d.get('id')
        self.name=d.get('name')
        self.description=d.get('description')
        self.slug=d.get('slug')
        self.hd_stream_url=d.get('hd_stream_url')
        self.stream_url=d.get('stream_url')
        self.thumbnail_url=d.get('thumbnail_url')
        self.is_live=d.get('is_live')
        self.react_session_key=d.get('react_session_key')
        self.signature=d.get('signature')
        self.video_partner_id=d.get('video_partner_id')
        self.decrypter_key=d.get('decrypter_key')
        
