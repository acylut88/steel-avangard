from backend.core.config import (LOOTBOX_WEIGHTS, LOOTBOX_TYPES, 
                         LOOTBOX_NORMAL_REWARD, LOOTBOX_RARE_REWARD, LOOTBOX_EPIC_REWARD)

import random

def open_lootbox(user_id: int):
    """Открывает лутбокс и выдаем награду в зависимости от типа."""
    rarity = random.choices(LOOTBOX_TYPES, weights=LOOTBOX_WEIGHTS, k=1)[0]

    # создаем пустой словарь для награды
    loot = {
        "rarity": rarity, 
        "scrap": 0, "tools": 0, "steel": 0, "ac_gold": 0
    }
    flag_tools, flag_steel, flag_ac_gold = False, False, False

    if rarity == 'normal':
        loot["scrap"] = LOOTBOX_NORMAL_REWARD["scrap"]
        if random.random() < LOOTBOX_NORMAL_REWARD["tools_random"]: 
            flag_tools = True
            loot["tools"] = 1

    elif rarity == "rare":
        loot["scrap"] = LOOTBOX_RARE_REWARD["scrap"]
        loot["tools"] = random.randint(LOOTBOX_RARE_REWARD["tools_min"], LOOTBOX_RARE_REWARD["tools_max"])
        flag_tools = True
        if random.random() < LOOTBOX_RARE_REWARD["steel_random"]:   
            flag_steel = True
            loot["steel"] = random.randint(LOOTBOX_RARE_REWARD["steel_min"], LOOTBOX_RARE_REWARD["steel_max"])
        if random.random() < LOOTBOX_RARE_REWARD["ac_gold_random"]:    
            flag_ac_gold = True
            loot["ac_gold"] = random.randint(LOOTBOX_RARE_REWARD["ac_gold_min"], LOOTBOX_RARE_REWARD["ac_gold_max"])
        
    elif rarity == "epic":
        loot["scrap"] = LOOTBOX_EPIC_REWARD["scrap"]
        loot["tools"] = random.randint(LOOTBOX_EPIC_REWARD["tools_min"], LOOTBOX_EPIC_REWARD["tools_max"])
        loot["steel"] = random.randint(LOOTBOX_EPIC_REWARD["steel_min"], LOOTBOX_EPIC_REWARD["steel_max"])
        loot["ac_gold"] = LOOTBOX_EPIC_REWARD["ac_gold"]
        flag_tools = flag_steel = flag_ac_gold = True

    return [loot, flag_tools, flag_steel, flag_ac_gold, rarity]
      
if __name__ == "__main__":
    # тестируем открытие лутбокса
    for _ in range(10):
        print(open_lootbox(123456789))