# coding=utf-8
"""
XML TV EPG Generator
"""
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime as dt
import re
from EpgDataProvider import EpgDataProvider
from ElementTree_pretty import prettify

class XmlTvGen(object):
    def __init__(self, lang_list, start_date, end_date, channels, datafile, timezone=None):
        """
        Init XmlTvGen object
        :param lang_list:
        :param start_date: start date in format %Y-%m-%d eg. 2014-12-06
        :param end_date: end date in format %Y-%m-%d eg. 2014-12-06
        :param channels: channel list with (channel_name, [display_name_list], genre) tuples
        :param timezone: optional timezone offset eg. +3300, +0100
        :return:
        """
        # Supported languages
        self._suplangs = {'en', 'fa'}
        self._dataprovider = EpgDataProvider(datafile)
        # Set languages and check if all are supported
        self._langs = lang_list
        for lang in self._langs:
            if lang not in self._suplangs:
                raise ValueError('%r is not in list of supported languages.' % (lang))
        # Set start and end time for EPG data and check start time is not greater than end time
        self._start_date = self._datestring_to_datetime(start_date)
        self._end_date = self._datestring_to_datetime(end_date)
        if self._start_date > self._end_date:
            raise ValueError('Start time is greater than end time.')
        # Set timezone data if passed as parameter, otherwise default to UTC
        if timezone == None:
            self._tz = '+0000'
        else:
            self._tz = timezone
        if not self._validate_timezone_offset(self._tz):
            raise ValueError('Invalid timezone offset %r' % (self._tz))
        # Set channels
        self._channels = channels
        # Initialize TV tag of XMLTV
        self._tv = Element('tv')
        # Populate channel data
        self._last_title = u'' # Helper for preventing duplicate succesive shows
        for ch in self._channels:
            self._add_channel_tag(ch[0], ch[1])
        for ch in self._channels:
            self._add_channel_programmes(ch[0], ch[2], self._start_date, self._end_date)

    def __str__(self):
        return prettify(self._tv).encode(encoding='utf-8')

    def _add_channel_tag(self, id, display_name_list):
        """
        Adds child channel tags to tv element
        :param id: channel id
        :param display_name_list: list of display names
        :return:
        """
        channel = SubElement(self._tv, 'channel', {'id': id})
        # Add display name elements to channel, do not allow duplicates
        for dn in display_name_list:
            if not self._find_item(channel, 'display-name', dn):
                x_dn = SubElement(channel, 'display-name')
                x_dn.text = dn

    def _add_channel_programmes(self, channel_id, channel_genre, start_time, end_time):
        """
        Adds child programme tags to tv element for [start_time, end_time) interval
        :param channel_id: id of the channel, must match one from channel definition
        :param channel_genre: genre of the channel
        :param start_time: datetime object with start time
        :param end_time: datetime object with end time
        :return:
        """
        ct = start_time
        # Add new programmes until current time > end time
        a = 0
        while ct < end_time:
            show_start = ct
            data = self._dataprovider.get_random_show(self._langs, channel_genre)
            # Check data title against _last_title to prevent duplicates
            if data[2] != self._last_title:
                self._last_title = data[2]
                #print 'Adding new programme to ' + ch_id + ', starting: ' + show_start.strftime('%Y-%d-%m %H:%M') + ', ending: ' + show_end.strftime('%Y-%d-%m %H:%M')
                programme = SubElement(self._tv, 'programme')
                programme.set('channel', channel_id)
                programme.set('start', show_start.strftime('%Y%m%d%H%M%S') + ' ' + self._tz)
                show_end = ct + dt.timedelta(minutes=data[0])
                programme.set('stop', show_end.strftime('%Y%m%d%H%M%S') + ' ' + self._tz)
                # Get random programme data from EpgDataProvider based on channel genre and add it to the current programme
                for lang in self._langs:
                    self._add_programme_data(programme, data[1][lang], lang)
                ct = show_end
            else:
                #print 'Duplicate show %r, not adding it to data structure' % (self._last_title)
                pass
        # Reset _last_title for next channel
        self._last_title = ''

    def _add_programme_data(self, parent, programme_data, language):
        """
        Populate parent programme tag with data
        :param parent:
        :param programme_data:
        :param language:
        :return:
        """
        # Unpack the values in programme_list to variables
        titles, sub_title, descriptions, rating, star_rating = programme_data[:5]
        episode_num, categories, icon, directors, actors = programme_data[5:10]
        url = programme_data[10]
        # Add title element
        x_title = SubElement(parent, 'title', {'lang': language})
        x_title.text = titles
        # Add sub-title element
        if len(sub_title) > 0:
            x_sub_title = SubElement(parent, 'sub-title', {'lang': language})
            x_sub_title.text = sub_title
        # Add desc element
        if len(descriptions) > 0:
            x_desc = SubElement(parent, 'desc', {'lang': language})
            x_desc.text = descriptions
        # Add rating element
        if len(rating) > 0:
            x_rating = SubElement(parent, 'rating')
        # Add star-rating element
        if len(star_rating) > 0:
            x_star_rating = SubElement(parent, 'star-rating')
        # Add episode-num element
        # TODO
        # Add category elements
        # TODO
        # Add icon element, do not allow duplicates
        # Currently disabled due to bug in target platform
        #if len(icon) > 0:
        #    if not self._find_item(parent, u'icon', icon):
        #        x_icon = SubElement(parent, u'icon')
        #        x_icon.text = icon
        # Add director elements, do not allow duplicates
        if len(directors) > 0:
            for director in directors.split(','):
                director = director.lstrip().rstrip()
                if not self._find_item(parent, 'director', director):
                    x_director = SubElement(parent, 'director')
                    x_director.text = director
        # Add actor elements, do not allow duplicates
        if len(actors) > 0:
            for actor in actors.split(','):
                actor = actor.lstrip().rstrip()
                if not self._find_item(parent, 'actor', actor):
                    x_actor = SubElement(parent, 'actor')
                    x_actor.text = actor
        # Add url element, do not allow duplicates
        if len(url) > 0:
            if not self._find_item(parent, 'url', url):
                x_url = SubElement(parent, 'url')
                x_url.text = url
        #print [ x.text for x in parent.iter('actor') ]

    def get_supported_langs(self):
        return self._suplangs

    # Static methods
    @staticmethod
    def _datestring_to_datetime(datestring):
        """
        Creates datetime object from string
        :param datestring: date string in format %Y-%m-%d eg. 2014-12-06
        :return: datetime
        """
        return dt.datetime.strptime(datestring, '%Y-%m-%d')

    @staticmethod
    def _validate_timezone_offset(timezone_offset):
        """
        Regex validation of timezone offset
        :param timezone_offset: timezone offset eg. +3300, +0100
        :return:
        """
        tzoregex = re.compile("^[+,-]{1}[0-9]{4}$")
        if len(tzoregex.findall(timezone_offset)) == 1:
            return True
        return False

    @staticmethod
    def _find_item(element, tag, name):
        """
        Check if child item tag with text name exists in XML element
        :param element:
        :param tag:
        :param name:
        :return: boolean
        """
        names = [ e.text for e in element.iter(tag)]
        if name in names:
            return True
        return False

#xmltv = XmlTvGen(['en', 'fa'], '2014-12-10', '2014-12-12', [('Channel2', ['Channel2', 'Ch2'], 'movie')], 'data/movies.csv', timezone='+0330')
#print xmltv