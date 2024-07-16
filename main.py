import json
import os
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    title = """
    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
    ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
    ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
    ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    print(title)

def get_input(prompt, input_type=str):
    while True:
        try:
            user_input = input_type(input(prompt))
            if input_type == int and user_input <= 0:
                raise ValueError
            return user_input
        except ValueError:
            print("無効な入力です。再試行してください。")

def setup_config():
    config = {
        "token": "",
        "special_log_channels": {},
        "server_log_channels": {}
    }

    clear_screen()
    print_title()
    config["token"] = input("ユーザーアカウントのトークンを入力してください: ")

    while True:
        clear_screen()
        print_title()
        choice = input("特定のチャンネルを監視しますか？ (y/n): ").lower()
        if choice == 'y':
            channel_id = get_input("監視するチャンネルIDを入力してください: ", int)
            log_channel_id = get_input("ログを送信するチャンネルIDを入力してください: ", int)
            config["special_log_channels"][channel_id] = log_channel_id
        elif choice == 'n':
            break

    while True:
        clear_screen()
        print_title()
        choice = input("サーバー全体を監視しますか？ (y/n): ").lower()
        if choice == 'y':
            server_id = get_input("監視するサーバーIDを入力してください: ", int)
            log_channel_id = get_input("ログを送信するチャンネルIDを入力してください: ", int)
            config["server_log_channels"][server_id] = log_channel_id
        elif choice == 'n':
            break

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    print("設定を保存しました。")

def main():
    setup_config()
    print("Botを起動します...")
    subprocess.Popen(['python', 'bot.py'])
    print("Botがバックグラウンドで実行されています。")

if __name__ == "__main__":
    main()
