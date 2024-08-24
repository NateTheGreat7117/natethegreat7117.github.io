from googleapiclient.discovery import build
import webbrowser

credentials = "AIzaSyB518ewVKogxxoj7shnh3_ac0RkXI7s5HQ"
service = build("youtube", "v3", developerKey=credentials)

def youtube(command):
    command = command.lower()
    request = service.playlists().list(part="snippet",
                                       channelId="UCtGX_-okmXL0ib5cpi6yVmA")
    response = request.execute()

    # Check if it is a playlist name
    playlists = response["items"]
    for i in range(len(playlists)):
        if playlists[i]["snippet"]["localized"]["title"].lower() == command:
            request2 = service.playlistItems().list(part="snippet",
                                                    playlistId=playlists[i]["id"],
                                                    maxResults=50)
            response2 = request2.execute()
            videos = response2["items"]
            webbrowser.open_new_tab(f"https://www.youtube.com/watch?v={videos[0]['snippet']['resourceId']['videoId']}&list={playlists[i]['id']}")
            return
    
    # Check if it is one of my playlists
    for i in range(len(playlists)):
        request2 = service.playlistItems().list(part="snippet",
                                                playlistId=playlists[i]["id"],
                                                maxResults=50)
        response2 = request2.execute()
        videos = response2["items"]
        run = True
        prev = videos[0]["snippet"]["title"]
        count = 0
        start = 0
        while run:
            # Run through all videos in the playlist
            for j in range(start, len(videos)):
                if command.lower() in videos[j]["snippet"]["title"].lower():
                    webbrowser.open_new_tab(f"https://www.youtube.com/watch?v={videos[j]['snippet']['resourceId']['videoId']}&list={playlists[i]['id']}")
                    return
            run = False
            
            # Go through next 50 songs
            if len(videos) == 50:
                nextPageToken = response.get('nextPageToken')
                request2 = service.playlistItems().list(part="snippet",
                                        playlistId=playlists[i]["id"],
                                        maxResults=50,
                                        pageToken=response2.get('nextPageToken'))
                response2 = request2.execute()
                videos = response2["items"]
                prev = videos[0]["snippet"]["title"]
                run = True
                
    request = service.search().list(part="id", q=command)
    response = request.execute()
                
    webbrowser.open_new_tab(f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}")