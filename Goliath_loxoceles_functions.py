import requests
import pandas as pd
import numpy as np

def art_info(mbid):


    url_art='https://musicbrainz.org/ws/2/artist/'
    url_art_compl='?inc=aliases&fmt=json'
    
    
    urlFinal = url_art.strip() + mbid.strip() + url_art_compl.strip()
    w = requests.get(urlFinal)
    wjson = w.json()
    
    wdf = pd.DataFrame({ key:pd.Series(value) for key, value in wjson.items() })
    wdf.to_csv('testanto_goliath.csv')
    return wdf






def geo_chart(country,apiKey,limit,page,clean):
    
    page1 = str(page)
    limit1 = str(limit)
    geoReq = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country='
    geoReqLine = geoReq.strip() + country.strip() + "&api_key=".strip() + apiKey.strip() + "&format=json".strip() +  "&limit=".strip() + limit1.strip() + "&page=".strip() + page1.strip()
    geoResponse = requests.get(geoReqLine)
    geoJson = geoResponse.json()
    topArt = geoJson["topartists"]
    artists = topArt["artist"]
    geoChart = pd.DataFrame(artists)
    geoChartclean1 = geoChart.replace([''], np.nan, regex=True)
    geoChartClean2 = geoChartclean1.dropna()
    geoChartClean2.to_csv('GEOCHART.csv')
    if clean == 'yes':
        return geoChartClean2
    if clean == 'no':
        return geoChart
    





def global_chart(apiKey,limit,page,clean):
    page1 = str(page)
    limit1 = str(limit)
    gloReq = 'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks'
    artists = []
    gloReqLine = gloReq.strip() + "&api_key=".strip() + apiKey.strip() + "&format=json".strip() +  "&limit=".strip() + limit1.strip() + "&page=".strip() +page1.strip()
    gloResponse = requests.get(gloReqLine)
    gloJson = gloResponse.json()
    topTrack = gloJson["tracks"]
    tracks = topTrack["track"]

    tracksToDict = { j : tracks[j] for j in range(len(tracks) ) }

    for i in tracksToDict:
        artist = tracksToDict[i]["artist"]['name']
        artists.append(artist)
    
    artistisDF = pd.DataFrame(artists)
    artistisDF.columns=['artist']
    
    gloChart = pd.DataFrame(tracks)
    gloChart['artist'] = artistisDF['artist']
    gloChartClean = gloChart.replace([""], np.nan, regex=True)

    gloChartClean2 = gloChartClean.dropna()
    gloChartClean2.to_csv('Global_Chart.csv')
    if clean == 'yes':
        return gloChartClean2
    if clean == 'no':
        return gloChart

def track_info_LFM(apiKey,song,artist):

    trackReq = 'http://ws.audioscrobbler.com/2.0/?method=track.search&track='

    
    trackReqLine = trackReq.strip() + song.strip() + "&api_key=".strip() + apiKey.strip() + '&artist='.strip() + artist.strip()+ "&format=json".strip() 
    
    trackResponse = requests.get(trackReqLine)
    trackJson = trackResponse.json()
    
    trackPiece = trackJson['results']
    tracks = trackPiece["trackmatches"]
    TrackInfoReal = tracks['track']
    
    trackInfo = pd.DataFrame(TrackInfoReal)
    
    TrackInfoClean = trackInfo.replace([""], np.nan, regex=True)
    TrackInfoClean2= TrackInfoClean.dropna()
    
    TrackInfoCleanFinal = TrackInfoClean2.to_csv("TrackInfo.csv")
    return TrackInfoClean

def track_info_MB(mbid):

    url_song='https://musicbrainz.org/ws/2/recording/'
    url_song_compl='?inc=aliases&fmt=json'
    
    
    urlFinal = url_song.strip() + mbid.strip() + url_song_compl.strip()
    w = requests.get(urlFinal)
    wjson = w.json()
    
    wdf = pd.DataFrame({ key:pd.Series(value) for key, value in wjson.items() })

    return wdf

def single_high_level(mbid):
 
    url_ab='https://acousticbrainz.org/api/v1/'
    url_hl_compl='/high-level'
    
    urlFinal = url_ab.strip() + mbid.strip() + url_hl_compl.strip()
    w = requests.get(urlFinal)
    wjson = w.json()
    wjson1 = wjson['highlevel']
    prefinal = pd.DataFrame.from_dict(wjson1,orient='index',columns=['probability','value'])
    dfinal = prefinal.T
    return dfinal
