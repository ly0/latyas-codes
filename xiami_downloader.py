# -*- coding: utf-8 -*-
import requests
import urllib2
import json
from bs4 import BeautifulSoup
import os

def str2url(s):
    num_loc = s.find('h')
    rows = int(s[0:num_loc])
    strlen = len(s) - num_loc
    cols = strlen/rows
    right_rows = strlen % rows
    new_s = s[num_loc:]
    output = ''
    for i in xrange(len(new_s)):
        x = i % rows
        y = i / rows
        p = 0
        if x <= right_rows:
            p = x * (cols + 1) + y
        else:
            p = right_rows * (cols + 1) + (x - right_rows) * cols + y
        output += new_s[p]
    output = urllib2.unquote(output).replace('^', '0')
    return output
    
username = 'test@yopmail.com'
password = '19920330'
axel_opts = '-n20'
login_url = 'https://login.xiami.com/member/login'
song_prefix = 'http://www.xiami.com/song/gethqsong/sid/'
album_id = raw_input('ALBUM ID:')

data = {'email':username,
        'password':password,
        'done':'http://www.xiami.com/account',
        'submit':'登 录'
}
header = {'user-agent':'Mozilla/5.0'}
req = requests.session()
ret = req.post(login_url,data=data,headers=header)

songlist = req.get('http://www.xiami.com/album/' + album_id,headers=header)
bs = BeautifulSoup(songlist.text)
album_title = bs.find(attrs={'property':'v:itemreviewed'}).contents[0].replace('\'','')

try:
    os.system('mkdir "%s"' % album_title)
except:
    pass

for i in bs.findAll('td',attrs={'class':'song_name'}):
    link = i.findAll('a')[0]
    song_name = link.contents[0].replace('\'','')
    song_id = link.get('href').replace('/song/','')
    foo = json.loads(req.get(song_prefix + song_id,headers=header).text)['location']
    song_url = str2url(foo)
    
    #print song_name,song_id,song_url
    print 'Downloading %s' % song_name
    command = 'axel %s -q --user-agent="Mozilla/5.0" %s -o \'%s/%s.mp3\'' % (axel_opts,song_url,album_title,song_name)    
    ret = os.system(command)
    if ret != 0:
        print 'Downloading %s failed' % song_name