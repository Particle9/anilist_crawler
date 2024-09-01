import requests
import json

# Here we define our query as a multi-line string
query = '''
query ($userName: String, $page: Int, $perPage: Int,) { # Define which variables will be used in the query (id)
  Page (page: $page, perPage: $perPage) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    mediaList(userName: $userName, status_in:[CURRENT,COMPLETED,DROPPED,REPEATING,PAUSED], sort:SCORE_DESC, type:ANIME) {
      id
      score
      status
      media{
        id
        title {
          romaji
          english
          native
          userPreferred
        }
        coverImage {
          extraLarge
        }
        bannerImage
        averageScore
        description
        season
        seasonYear
        startDate {
          year
          month
          day
        }
        characters{
          nodes{
            id
            name {
              first
              middle
              last
              full
              native
              userPreferred
            }
            gender
            image {
              large
              medium
            }
            siteUrl
            favourites
            media {
              edges {
                id
                characterRole
              }
            }
            description
          }
        }
        characters2: characters(page:2){
          nodes{
            id
            name {
              first
              middle
              last
              full
              native
              userPreferred
            }
            gender
            image {
              large
              medium
            }
            siteUrl
            favourites
            media {
              edges {
                id
                characterRole
              }
            }
            description
          }
        }
        characters3: characters(page:3){
          nodes{
            id
            name {
              first
              middle
              last
              full
              native
              userPreferred
            }
            gender
            image {
              large
              medium
            }
            siteUrl
            favourites
            media {
              edges {
                id
                characterRole
              }
            }
            description
          }
        }
        characters4: characters(page:4){
          nodes{
            id
            name {
              first
              middle
              last
              full
              native
              userPreferred
            }
            gender
            image {
              large
              medium
            }
            siteUrl
            favourites
            media {
              edges {
                id
                characterRole
              }
            }
            description
          }
        }
      }
      
    }
  }
}

'''


def crawl_user_anime(username):
    url = 'https://graphql.anilist.co'
    list_media = []
    for i in range(1,11):
        variables = {
            'userName': username,
            'page':i,
            'perPage':100
        }
        
        
        # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables})
        
        dctx = json.loads(response.text)
        list_media += dctx['data']['Page']['mediaList']
        if not(dctx['data']['Page']['pageInfo']['hasNextPage']):
            break

    return list_media

def get_all_characters(list_media, preferred_language = 'en'):
    character_list = []
    character_id_list =[]
    for dct_media in list_media:
        character_list_temp = dct_media['media']['characters']['nodes'] + dct_media['media']['characters2']['nodes'] + dct_media['media']['characters3']['nodes'] + dct_media['media']['characters4']['nodes']
        for character_temp in character_list_temp:
            if character_temp['id'] in character_id_list:
                continue
            else:
                character_id_list += [character_temp['id']]
            
            char_role = 'BACKGROUND'
            for x in character_temp['media']['edges']:
                if x['characterRole'] == 'MAIN':
                    char_role = 'MAIN'
                    break
                elif (x['characterRole'] == 'SUPPORTING') and (char_role == 'BACKGROUND'):
                    char_role = 'SUPPORTING'
                else:
                    continue
            
            if preferred_language == 'en':
                series_name = dct_media['media']['title']['english'] if dct_media['media']['title']['english'] else (dct_media['media']['title']['romaji'] if dct_media['media']['title']['romaji'] else dct_media['media']['title']['native'])
            else:
                series_name = dct_media['media']['title']['romaji'] if dct_media['media']['title']['romaji'] else (dct_media['media']['title']['english'] if dct_media['media']['title']['english'] else dct_media['media']['title']['native'])
            
            character_elmt = {
                'name': character_temp['name']['userPreferred'] if character_temp['name']['userPreferred'] else character_temp['name']['full'],
                'gender': character_temp['gender'],
                'image': character_temp['image']['large'],
                'siteUrl': character_temp['siteUrl'],
                'countFavourites': character_temp['favourites'],
                'role': char_role,
                'description': character_temp['description'],
                'series': series_name,
                'series_url': "https://anilist.co/anime/" + str(dct_media['media']['id']),
                'series_user_score': dct_media['score'],
                'series_user_status': dct_media['status'],
                'series_cover_image': dct_media['media']['coverImage']['extraLarge'],
                'series_banner_image': dct_media['media']['bannerImage'],
                'series_average_score': dct_media['media']['averageScore'],
                'series_season': str(dct_media['media']['season'] if dct_media['media']['season'] else "")  + " " + str(dct_media['media']['seasonYear'])
            }
            character_list += [character_elmt]

    character_list = sorted(character_list, key=lambda elmt: elmt['countFavourites'], reverse=True)
    return character_list