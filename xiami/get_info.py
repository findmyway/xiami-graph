# -*- coding: utf-8 -*-
from xiami.items import UserItem, LibItem
from bs4 import BeautifulSoup
import re



class XiamiInfo:

    def __init__(self, page_content):
        """
        read the source page into soup
        :param page: the souce page
        :type page: str
        """
        self.soup = BeautifulSoup(page_content)

    def get_item(self, item_type):
        method_dict = {"user_info": self.get_userinfo,
                       "lib_song": self.get_libsong,
                       "unlib_song": self.get_libsong,
                       "lib_album": self.get_libalbum,
                       "lib_artist": self.get_libartist,
                       "song_weekrank": self.get_song_rank,
                       "song_totalrank": self.get_song_rank,
                       "album_totalrank": self.get_album_rank,
                       "album_weekrank": self.get_album_rank,
                       "artist_weekrank": self.get_artist_rank,
                       "artist_totalrank": self.get_artist_rank,
                       "collect": self.get_collect,
                       "collect_fav": self.get_collect,
                       "recent_listen": self.get_recent_listen,
                       "followings": self.get_followings,
                       "fans": self.get_followings
                       }


        return method_dict[item_type]()

    def get_userinfo(self):
        """
        analysis the soup to get necessory info of the user
        :return:
        """
        user_item = UserItem()
        user_item['name'] = self.soup.h1.text

        infoCount = self.soup.find(id='p_infoCount')
        short_desc, join_time = infoCount.find_all('p', "infos")
        join_time = join_time.text.split(' ')[0]
        user_item['join_time'] = join_time

        # analysis short_desc
        short_desc = short_desc.text.strip()
        sex = short_desc[-2:]
        if sex in [u'男生', u'女生', u'大虾']:
            user_item['sex'] = sex if sex != u'大虾' else None
        user_item['location'] = short_desc.strip(u'来自').split(u'的')[0]

        user_item['n_listen'] = int(infoCount.find(id='num').text)

        statisitcs = infoCount.text.strip().split('\n')
        for x in statisitcs:
            if x.endswith(u'次访问'):
                user_item['n_visit'] = int(x.rstrip(u'次访问'))
            if x.endswith(u'粉丝'):
                user_item['n_fans'] = int(x.rstrip(u'粉丝'))
            if x.endswith(u'关注'):
                user_item['n_followers'] = int(x.rstrip(u'关注'))
            if x.endswith(u'分享'):
                user_item['n_share'] = int(x.rstrip(u'分享'))

        return user_item

    def get_libsong(self):
        lib_song_item = LibItem()
        s = set()
        for x in self.soup.find_all(id=re.compile('lib_song_\d+')):
            s.add(x.attrs['id'].strip("lib_song_"))
        lib_song_item['items'] = s
        return lib_song_item

    def get_libalbum(self):
        lib_album_item = LibItem()
        s = set()
        for x in self.soup.find_all(id=re.compile('lib_album_\d+')):
            album_id = x.attrs['id'].strip("lib_song_")
            faved_time = x.find('span', 'faved_time').text
            s.add((faved_time, album_id))
        lib_album_item['items'] = s
        return lib_album_item

    def get_libartist(self):
        lib_artist_item = LibItem()
        s = set()
        for x in self.soup.find_all(id=re.compile('lib_artist_\d+')):
            s.add(x.attrs['id'].strip("lib_artist_"))
        lib_artist_item['items'] = s
        return lib_artist_item

    def get_song_rank(self):
        songs_rank = LibItem()
        s = set()
        for x in self.soup.find("div", "pool5").find("tbody").find_all("tr"):
            song_url = x.find("td", "song_name").a.attrs["href"]
            pattern = re.compile(r'/song/(\d+)')
            song_id = pattern.search(song_url).group(1)
            song_hot = x.find("td", "song_hot").text
            song_hot = int(song_hot) if song_hot else 1  # some song has empty song_hot
            s.add((song_id, song_hot))
        songs_rank['items'] = s
        return songs_rank

    def get_album_rank(self):
        album_rank = LibItem()
        s = set()
        for x in self.soup.find("div", "chart_album").find_all("div", "chart_album_item"):
            album_url = x.find("p", "name").a.attrs["href"]
            pattern = re.compile(r'/album/(\d+)')
            album_id = pattern.search(album_url).group(1)
            album_hot = x.find("em", "playcounts").text
            album_hot = int(album_hot) if album_hot else 1  # some album has empty album_hot
            s.add((album_id, album_hot))
        album_rank['items'] = s
        return album_rank

    def  get_artist_rank(self):
        artist_rank = LibItem()
        s = set()
        for x in self.soup.find_all("div", "chart_artist_item"):
            artist_url = x.find("a", "buddy").attrs["href"]
            pattern = re.compile(r'/artist/(\d+)')
            artist_id = pattern.search(artist_url).group(1)
            artist_hot = int(x.find("em", "playcounts").text)
            s.add((artist_id, artist_hot))
        artist_rank['items'] = s
        return artist_rank

    def get_collect(self):
        collect_item = LibItem()
        s = set()
        for x in self.soup.find_all("div", "info"):
            collect_url = x.find("p", "name").a.attrs["href"]
            pattern = re.compile(r'/collect/(\d+)')
            collect_id = pattern.search(collect_url).group(1)
            time_info = x.find("span", "time").text
            pattern = re.compile(r'([0-9\-]+)')
            collect_time = pattern.search(time_info).group(1)
            s.add((collect_id,collect_time))
        collect_item['items'] = s
        return collect_item

    def get_recent_listen(self):
        listen_list_item = LibItem()
        s = set()
        for x in self.soup.find("table", "track_list").find_all("tr"):
            song_id_info = x.attrs["id"].strip("track_")
            track_time = x.find("td", "track_time").text
            if u'前' in track_time:
                # 把不精确的时间抛弃, 避免影响对时间的分析结果
                track_time = None
            s.add((song_id_info, track_time))
        listen_list_item['items'] = s
        return listen_list_item

    def get_followings(self):
        followings_item = LibItem()
        s = set()
        for x in self.soup.find("ul", "clearfix user_list").find_all("li"):
            uid_info = x.find("p", "name").a.attrs["href"]
            pattern1 = re.compile(r'/u/(\d+)')
            uid = pattern1.search(uid_info).group(1)
            followings_fans_info = x.find("span").text
            pattern2 = re.compile(r'(\d+).+(\d+)')
            search_result = pattern2.search(followings_fans_info)
            n_followings = int(search_result.group(1))
            n_fans = int(search_result.group(2))
            s.add((uid, n_followings, n_fans))
        followings_item["items"] = s
        return followings_item
