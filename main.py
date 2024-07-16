import json
import os
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    title = f"""
{Fore.CYAN}{Style.BRIGHT}
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ███╗    ██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}
"""
    print(title)

def get_input(prompt, input_type=str):
    while True:
        try:
            user_input = input_type(input(Fore.GREEN + prompt + Style.RESET_ALL))
            if input_type == int and user_input <= 0:
                raise ValueError
            return user_input
        except ValueError:
            print(Fore.RED + "無効な入力です。再試行してください。" + Style.RESET_ALL)

def setup_config():
    config = {
        "token": "",
        "special_log_channels": {},
        "server_log_channels": {}
    }

    clear_screen()
    print_title()
    config["token"] = input(Fore.YELLOW + "ユーザーアカウントのトークンを入力してください: " + Style.RESET_ALL)

    while True:
        clear_screen()
        print_title()
        choice = input(Fore.YELLOW + "特定のチャンネルを監視しますか？ (y/n): " + Style.RESET_ALL).lower()
        if choice == 'y':
            channel_id = get_input("監視するチャンネルIDを入力してください: ", int)
            log_channel_id = get_input("ログを送信するチャンネルIDを入力してください: ", int)
            config["special_log_channels"][channel_id] = log_channel_id
        elif choice == 'n':
            break
        else:
            print(Fore.RED + "無効な入力です。再試行してください。" + Style.RESET_ALL)

    while True:
        clear_screen()
        print_title()
        choice = input(Fore.YELLOW + "サーバー全体を監視しますか？ (y/n): " + Style.RESET_ALL).lower()
        if choice == 'y':
            server_id = get_input("監視するサーバーIDを入力してください: ", int)
            log_channel_id = get_input("ログを送信するチャンネルIDを入力してください: ", int)
            config["server_log_channels"][server_id] = log_channel_id
        elif choice == 'n':
            break
        else:
            print(Fore.RED + "無効な入力です。再試行してください。" + Style.RESET_ALL)

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    print(Fore.GREEN + "設定を保存しました。" + Style.RESET_ALL)

def main():
    setup_config()
    print(Fore.CYAN + "Botを起動します..." + Style.RESET_ALL)
    subprocess.Popen(['python', 'bot.py'])
    print(Fore.CYAN + "Botがバックグラウンドで実行されています。" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
