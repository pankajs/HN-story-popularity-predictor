import re
from urllib2 import build_opener, HTTPCookieProcessor

from ..models import *


class HackerNews(object):
    """ Content parser class for news.ycombinator.com """
    def __init__(self):
        self.opener = build_opener(HTTPCookieProcessor())
        self.url = 'http://news.ycombinator.com/'

    def update_items(self):
        """ Download list of hn items """
        page = self.opener.open(self.url).read()
        # fetch all items from crawled page
        item_links = re.findall(
            r'<tr><td align=right valign=top class="title">(.+?)'
            r'<tr style="height:5px"></tr>', page)
        if not item_links:
            raise SyntaxWarning("Cannot parse list of items")
        
        # fetch details for each item
        counter = 0
        items_map = {}
        for path in set(item_links):
            # parse hn item id
            item_id = re.search(r'<span id=score_(\d+)>', path)
            item_id = item_id and item_id.group(1) or 0
            if item_id > 0:
                # check item id into database
                qs = HNItems.objects.filter(itemid=item_id)
                hnitem = len(qs) and qs[0] or HNItems(itemid=item_id)
                if not hnitem.id:
                    # parse hn item link
                    l = re.search(r'<td class="title">(.+?)</td>', path)
                    l = l and l.group(1) or ''
                    link = re.search(r'<a href="(.+?)"', l)
                    link = link and link.group(1) or ''
                    
                    # parse hn link submission text
                    link_text = l.split('</a>')
                    if link_text:
                        link_text = link_text[0]
                        link_text = link_text.split('>')[1]
                    else:
                        link_text = ''

                    # parse hn details section
                    s = re.search(
                        r'<td class="subtext">(.+?)</td>', path)
                    s = s and s.group(1) or ''

                    # parse hn item score
                    score = re.search(
                        r'<span id=score_\d+>(.+?) point', s)
                    score = score and score.group(1) or 0

                    # parse hn item posted by
                    u_id = re.search(r'<a href="user?(.+?)">', s)
                    u_id = u_id and u_id.group(1) or ''
                    u_id = u_id.split('=')[1]

                    # parse total comments for hn item
                    comments = re.search(r'id='+item_id+'">(.*?) comment', s)
                    comments = comments and comments.group(1) or 0         

                    item_link = 'item?id=%s' % item_id

                    # map hn item details
                    items_map['itemid'] = item_id
                    items_map['link'] = link
                    items_map['header'] = link_text
                    items_map['score'] = score
                    items_map['user_id'] = u_id
                    items_map['user_name'] = u_id
                    items_map['comments'] = comments      
                    items_map['linkcomments'] = ('%s/%s' %
                                                 (self.url, item_link))
                    
                    # check if link submission or hn comments
                    if link == item_link:
                        items_map['linkcontents'] = ''
                        items_map['linktype'] = 0
                    else:
                        # parse content of the target page
                        try:
                            tmp = self.opener.open(link).read()
                            items_map['linkcontents'] = tmp
                        except:
                            items_map['linkcontents'] = link
                        items_map['linktype'] = 1
                        
                    # save item into database
                    rev = HNItems(**items_map)
                    try:
                        rev.save()
                        print '%d: %s - %s' % (counter, item_id, link)
                        counter += 1
                    except:
                        print 'Error during save item # %s' % item_id                        
        print 'Total items imported: %d' % counter

