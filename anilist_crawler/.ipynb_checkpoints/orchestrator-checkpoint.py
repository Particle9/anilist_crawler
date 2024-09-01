from anilist_crawler.crawler_utils import *
from anilist_crawler.image_utils import *


def orchestrator_user_data(username):
    list_media = crawl_user_anime(username)
    list_character = get_all_characters(list_media, preferred_language = 'en')
    return list_media, list_character

def orchestrator_character_randomizer(character_list,num_generation,roles_included = ['MAIN','SUPPORTING'], series_status_included = ['COMPLETED','REPEATING','CURRENT','PAUSED','DROPPED']):
    character_candidates = [c for c in character_list if (c['role'] in roles_included and c['series_user_status'] in series_status_included)]
    rand_characters = random.sample(character_candidates,k=num_generation)
    listCharImgs = [get_char_img(x['image'], x['name'], x['series']) for x in rand_characters]
    # fullGridImg = make_img_grid(listCharImgs)

    return listCharImgs