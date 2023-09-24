/*
{ 'artists': [{'id': 'UCdHscQsCBWSfcW50NjdJWkA', 'name': 'Will Smith'}],
    'category': 'Top result',
    'duration': '3:50',
    'duration_seconds': 230,
    'resultType': 'video',
    'thumbnails': [ { 'height': 225,
                      'url': 'https://i.ytimg.com/vi/3JcmQONgXJM/sddefault.jpg?sqp=-oaymwEWCJADEOEBIAQqCghqEJQEGHgg6AJIWg&rs=AMzJL3lSHVojAqxhCJlFiV6NCEE9e2YUtA',
                      'width': 400}],
    'title': "Gettin' Jiggy Wit It",
    'videoId': '3JcmQONgXJM',
    'videoType': 'MUSIC_VIDEO_TYPE_OMV',
    'views': '113M'},
  { 'album': {'id': 'MPREb_IoQ3ySwHPDi', 'name': 'Live 8 (Live, July 2005)'},
    'artists': [],
    'category': 'More from YouTube',
    'duration': '5:52',
    'duration_seconds': 352,
    'feedbackTokens': {'add': None, 'remove': None},
    'isExplicit': False,
    'resultType': 'song',
    'thumbnails': [ { 'height': 60,
                      'url': 'https://lh3.googleusercontent.com/63pN5WF_ek6zIkmhNyb640s1zX-fyjR0m-ykqCtrjEmR4J4BtuZr0_lOOE92hT9S8qO3MzsKSZaKCtS91g=w60-h60-l90-rj',
                      'width': 60},
                    { 'height': 120,
                      'url': 'https://lh3.googleusercontent.com/63pN5WF_ek6zIkmhNyb640s1zX-fyjR0m-ykqCtrjEmR4J4BtuZr0_lOOE92hT9S8qO3MzsKSZaKCtS91g=w120-h120-l90-rj',
                      'width': 120}],
    'title': "Gettin' Jiggy Wit It & Switch (Live at Live 8, Benjamin Franklin "
             'Parkway, Philadelphia, 2nd July 2005)',
    'videoId': 'gaI9-ToO0mQ',
    'videoType': 'MUSIC_VIDEO_TYPE_ATV',
    'year': None}
*/

function displayResults(results) {
    var resultlist = document.getElementById("results")
    results.forEach((res) => {
        let listitem = document.createElement("div")
        let artistname = res.artists[0].name 
        //let thumbnail = res.thumbnails[0].url
        listitem.innerHTML = `${artistname} - ${res.title}`
        resultlist.appendChild(listitem)
    })
}