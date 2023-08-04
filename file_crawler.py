import os
import subprocess


# this is where you change the path, see that you need to escape the escape character so every slash needs to be doubled
path = "C:\\Music\\yt-dlp"



# def thumbnail_data():
#     headers = {
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
#         'Cookie': 'SOCS=CAESOAgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwNzI1LjAyX3AxGgVlbi1HQiAEGgYIgIqMpgY',
#     'Accept-Language': 'en'}
#
#     def getdata(url):
#         session = HTMLSession();
#         r = session.get(url=url, headers=headers)
#         return r.text
#
#     htmldata = getdata("https://music.youtube.com/playlist?list=OLAK5uy_m3LoSftJh76j_mowaS4hBhw9-pa3Avy0M")
#     print(htmldata)
#     soup = BeautifulSoup(htmldata, 'html.parser')
#     for item in soup.find_all('img'):
#         continue
#         print(item)

# remove album prefix before albums
def rename():
    artist_ls = os.listdir(path)
    for artist in artist_ls:
        album_ls = os.listdir(f"{path}\\{artist}")
        for album in album_ls:
            if album[0:8] == "Album - ":
                os.rename(f"{path}\\{artist}\\{album}",f"{path}\\{artist}\\{album[8:]}")
                print(f'renamed: {album[8:]}')

def get_links():
    with open('song_links.txt', 'r', encoding='utf-8') as links:
        return links.readlines()

def make_batch():
    links_ls = get_links()
    file = open('script.bat', 'w')
    for link in links_ls:
        command = f"yt-dlp --embed-metadata -P \"{path}\" --extract-audio -o " \
                  f"\"%%(artist)s/%%(playlist)s/%%(playlist_index)s - %%(title)s.%%(ext)s\" \"{link.strip()}\"\n"
        file.write(command)
    file.close()
    return

def run_ytdlp():
    links_ls = get_links()
    for link in links_ls:

        command_args = ["yt-dlp", "--embed-metadata", '-P', f"{path}", '--audio-format', 'mp3', '--extract-audio',
                        '-o', '%(artist)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s', f'{link.strip()}']

        subprocess.run(command_args)
    else:
        print('no songerinos in song_list.txt')

def convert():

    command = 'ffmpeg -i Gurzle.opus -map_metadata 0 -map_metadata 0:s:0 Gurzle.mp3'
    subprocess.Popen()

def dir_scan():
    ret = {}
    artist_ls = os.listdir(path)
    for artist in artist_ls:
        album_ls = os.listdir(f"{path}\\{artist}")
        ret[artist] = album_ls
    return ret

def write_changes(old_dir):

    new_dir = dir_scan()
    file = open('changelog.txt', 'a')
    # print(old_dir)
    # print(new_dir)


    # now mario makes it so that it only shows the difference
    for artist in new_dir:
        if artist in old_dir:
            old_ls = old_dir[artist]
            new_ls = new_dir[artist]
            if old_ls == new_ls:
                continue
            else:
                for album in new_ls:
                    if album not in old_ls:
                        print(f'{artist}: {album}')
                        file.write(f'{artist}: {album}\n')
        else:
            print(f'{artist}: {new_dir[artist]}')
            file.write(f'{artist}: {new_dir[artist]}\n')
    file.close()


def clear_song_links():
    file = open('song_links.txt', 'w')
    file.write('')
    file.close()

if __name__=="__main__":
    current_dir = dir_scan()
    run_ytdlp()
    rename()
    write_changes(current_dir)
    clear_song_links()
