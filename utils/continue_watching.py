from colorama import Fore, Style
import json
import os
import sys

from . import anilist_requests
from . import mapper

def get_available_list(watchlist):
    user_list = []
    folder_map = mapper.get_folder_map()
    for folder in folder_map:
        if not os.path.isdir(folder):
            continue
        if folder_map[folder]["anilist_id"] in watchlist:
            watchlist[folder_map[folder]["anilist_id"]]["folder"] = folder
            user_list.append(watchlist[folder_map[folder]["anilist_id"]])
    return user_list

def get_episode_path(selected_anime_folder, selected_anime_episode):
    episodes = []
    for file in sorted(os.listdir(selected_anime_folder)):
        if file.startswith('.'):
            continue
        episodes.append(file)
    if selected_anime_episode > len(episodes):
        print(f"\n{Fore.RED}Episode not found! Check the folder below and add an episode offset if needed:\n{selected_anime_folder}")
        quit()
    return f"{selected_anime_folder}/{episodes[selected_anime_episode - 1]}"

def print_user_list(user_list):
    i = 1
    for anime in user_list:
        print(f'[{Fore.GREEN}{i}{Style.RESET_ALL}] {Fore.CYAN}{anime["title"]}{Style.RESET_ALL} - {Fore.YELLOW}Episode {int(anime["progress"]) + 1}{Style.RESET_ALL}')
        i += 1

def play_episode(episode_path):
    if not os.path.exists(episode_path):
        print(f"{Fore.RED}\n'{episode_path}' does not exist!")
        exit()
    episode_path = episode_path.replace("'", "'\\''")
    os.system(f"mpv '{episode_path}' >/dev/null 2>&1 & disown")


def continue_watching():
    print()
    watching_list = anilist_requests.get_watching_list()
    available_list = get_available_list(watching_list)
    print_user_list(available_list)
    selected_anime = available_list[int(input(f"\nSelect an anime:{Fore.GREEN} ")) - 1]
    selected_anime_folder = selected_anime["folder"]
    selected_anime_episode = selected_anime["progress"] + 1
    episode_path = get_episode_path(selected_anime_folder, selected_anime_episode)
    play_episode(episode_path)

if __name__ == "__main__":
    continue_watching()