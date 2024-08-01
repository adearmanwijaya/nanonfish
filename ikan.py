import asyncio
import aiohttp
import time
from colorama import Fore, Style, init
import random
from datetime import datetime, timedelta

url_shop = "https://fishapi.xboost.io/zone/order/goodslist"
url_order_status = "https://fishapi.xboost.io/zone/order/status" #{"order_no":"7222987293051585536"}
url_create_order = "https://fishapi.xboost.io/zone/order/createorder" #{"goods_id":2}
login_tokens = []
check_counter = 0
previous_results = {}

custom_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://happy-aquarium.xboost.io",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://happy-aquarium.xboost.io/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}

def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

async def async_post(url, headers, json=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json) as response:
            return await response.json()

async def login(query):
    url = "https://fishapi.xboost.io/index/tglogin"
    custom_headers["content-type"] = "application/json"
    payload = {"initData": query}
    try:
        response = await async_post(url, custom_headers, json=payload)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

async def load_game_state(login_token):
    url = "https://fishapi.xboost.io/zone/user/gamestate"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    try:
        response = await async_post(url, custom_headers)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
async def delete_fish(fish_id, login_token):
    url = "https://fishapi.xboost.io/zone/user/gameactions"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"actions":[{"action":"recover","id":fish_id}]}
    try:
        response = await async_post(url, custom_headers, json=payload)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
async def combine_fishes(fish_id, login_token):
    url = "https://fishapi.xboost.io/zone/user/gameactions"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"actions":[{"action":"compose","id":fish_id}]}
    try:
        response = await async_post(url, custom_headers, json=payload)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
async def check_free_diamond(login_token):
    url = "https://fishapi.xboost.io/zone/order/goodslist"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    try:
        response = await async_post(url, custom_headers)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
async def create_order(goods_id, login_token):
    url = "https://fishapi.xboost.io/zone/order/createorder"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"goods_id": goods_id}
    try:
        response = await async_post(url, custom_headers, json=payload)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
async def check_order_status(order_no, login_token):
    url = "https://fishapi.xboost.io/zone/order/status"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"order_no": order_no}
    try:
        response = await async_post(url, custom_headers, json=payload)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None
    
async def buy_fish(fish_id, login_token):
    url = "https://fishapi.xboost.io/zone/user/gameactions"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    payload = {"actions":[{"action":"buy","id":fish_id}]}
    try:
        response = await async_post(url, custom_headers, json=payload)
        if response:
            return response
        else:
            return None
    except Exception as e:
        print(f"{Fore.RED}Error in buy_fish: {e}{Style.RESET_ALL}")
        return None

    
total_bought_counts = {}  # Dictionary to store total bought counts for each user

async def get_user_info(login_token):
    url = "https://fishapi.xboost.io/zone/task/plist"
    custom_headers["content-type"] = "application/json"
    custom_headers["authorization"] = login_token
    try:
        response = await async_post(url, custom_headers)
        if response:
            return response
        else:
            return None
    except Exception as e:
        # print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

async def fetch_and_print_user_data(login_token, index):
    query = login_token['query']
    token = login_token['login_token']
    color = get_random_color()

    # Initialize total bought count for the user if not already done
    if index not in total_bought_counts:
        total_bought_counts[index] = 0

    user_info = await get_user_info(token)
    username = user_info['data']['userinfo']['username'] if user_info and user_info.get('code') == 200 else "Unknown"

    await asyncio.sleep(random.randint(1, 5))
    while True:
        game_state = await load_game_state(token)
        if game_state and game_state.get('code', None) == 200:
            fishes = game_state['data']['fishes']
            fish_limit = game_state['data']['fishLimit']
            gold = game_state['data']['gold']
            level = game_state['data']['level']
       
            if gold in previous_results.values():
                await asyncio.sleep(random.randint(1, 5))
                continue
            else:
                previous_results[index] = gold

            # Hapus ikan dengan level di bawah batas
            if len(fishes) > 1:
                first_fish = fishes[0]
                # if first fish is the lowest level from the list, delete it
                if first_fish == min(fishes) and check_counter == 20:
                    await delete_fish(first_fish, token)

            fish_id = 0
            for fish in fishes:
                if fishes.count(fish) > 1:
                    fish_id = fish
                    break
            if fish_id != 0:
                await combine_fishes(fish_id, token)

            # Hitung jumlah ikan yang perlu dibeli
            # fish_to_buy = fish_limit - len(fishes) + len(fishes_to_delete)  # Adjust for deleted fishes
            # fish_id_to_buy = level - 4
            # for _ in range(fish_to_buy):
            #     buy_response = await buy_fish(fish_id_to_buy, token)
            #     if buy_response and buy_response.get('code') == 200:
            #         results = buy_response.get('data', {}).get('results', [])
            #         if not results or results[0] != "reach fish amount limit":
            #             total_bought_counts[index] += 1  # Increment the total bought count only on success
            #         else:
            #             print(f"{Fore.YELLOW}Akun {index + 1} | Buy fish result: {results}{Style.RESET_ALL}")
            #     else:
            #         print(f"{Fore.RED}Akun {index + 1} | Failed to buy fish: {buy_response}{Style.RESET_ALL}")

            result = (
                f"Akun {Style.BRIGHT}{color}{index + 1}{Style.RESET_ALL} {username} | "
                f"Level: {Style.BRIGHT}{color}{level}{Style.RESET_ALL} | "
                f"Gold: {Style.BRIGHT}{color}{gold}{Style.RESET_ALL} | "
                f"Fish Limit: {Style.BRIGHT}{color}{fish_limit}{Style.RESET_ALL} | "
                f"Fishes: {Style.BRIGHT}{color}{fishes}{Style.RESET_ALL} "
     
            )
            return result

        elif game_state and game_state.get('code', None) == 10006:
            # mendapatkan token login baru
            login_response = await login(query)
            if login_response and login_response.get('code', None) == 200:
                login_tokens[index] = ({
                    "query": query,
                    "login_token": login_response['data']['login_token']
                })
                return f"{Fore.GREEN}User Login in another device! Net login token: {login_response['data']['login_token']}{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Failed to fetch user data!{Style.RESET_ALL}"

async def main():
    print(f"{Fore.GREEN}Starting NanonFish Bot...{Style.RESET_ALL}")
    init(autoreset=True)
    next_check_shop = datetime.now()
    global check_counter
    with open("query.txt", "r") as file:
        querys = file.read().splitlines()
    
    for query in querys:
        login_response = await login(query)
        if login_response and login_response.get('code', None) == 200:
            login_tokens.append({
                "query": query,
                "login_token": login_response['data']['login_token']
            })
        else:
            print(f"{Fore.RED}Login Failed!{Style.RESET_ALL}")

    while True:
        results = []
        current_time = datetime.now()

        if current_time >= next_check_shop:
            for index, login_token in enumerate(login_tokens):
                check_list = await check_free_diamond(login_token['login_token'])
                if check_list and check_list.get('code') == 200:
                    goods = check_list['data']['goods']
                    for good in goods:
                        if good['price'] == 0:
                            ordersend = await create_order(good['id'], login_token['login_token'])
                            if ordersend and ordersend.get('code') == 200:
                                order_status = await check_order_status(ordersend['data']['info']['order_no'], login_token['login_token'])
                                if order_status and order_status.get('code') == 200:
                                    print(f"{Fore.GREEN}Akun {index + 1} | {order_status['data']['info']['name']} | Cost {order_status['data']['info']['price']} | {order_status['data']['info']['diamond']} Diamond{Style.RESET_ALL}")
            next_check_shop = current_time + timedelta(hours=3)

        tasks = [fetch_and_print_user_data(login_token, index) for index, login_token in enumerate(login_tokens)]
        results = await asyncio.gather(*tasks)
        
        if results:
            # Clear the previous output
            print("\033c", end="")  # ANSI escape code to clear the screen
            # Print How many seconds until next 
            time_diff = next_check_shop - current_time
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Next Check Shop in {hours} hours {minutes} minutes {seconds} seconds")
            # Print all results at once
            print("\n".join(results), end="\r", flush=True)

        if check_counter == 20:
            check_counter = 0
        else:
            check_counter += 1

if __name__ == "__main__":
    asyncio.run(main())