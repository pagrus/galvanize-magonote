import requests

'''

Get HTML, stash in appropriate dirs
Show progress, other stats

'''

def get_game_pages(max_pages):
    '''
    gets game description pages, stopping after max_pages
    '''
    pass

def get_tag_list:
    '''
    get a list of tags and stats
    '''
    pass

def get_comment_page(index):
    '''
    get comment page HTML
    
    '''
    base_url = 'https://itch.io/post/'
    post_url = base_url + str(index)
    return requests.get(post_url)
