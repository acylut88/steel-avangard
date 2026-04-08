# Настройка базы данных
DB_PATH = "backend\\db\\avangard.db"

# Шансы выпадения лутбоксов
LOOTBOX_WEIGHTS = [80, 15, 5]  # 80% обычный, 15% редкий, 5% эпический
LOOTBOX_TYPES = ['normal', 'rare', 'epic']
LOOTBOX_NORMAL_REWARD = {"scrap": 250, 
                         "tools_random": 0.1
}
LOOTBOX_RARE_REWARD = {"scrap": 1_500, 
                       "tools_min": 1, "tools_max": 3,  
                       "steel_random": 0.5, "steel_min": 1, "steel_max": 1,
                       "ac_gold_random": 0.7, "ac_gold_min": 1, "ac_gold_max": 1
}
LOOTBOX_EPIC_REWARD = {"scrap": 5_000, 
                       "tools_min": 5, "tools_max": 10, 
                       "steel_min": 1, "steel_max": 3, 
                       "ac_gold": 2}


# Настройка Боссов
BOSS_TIME_LIMIT = 15  # в минутах. 
BOSS_DEFAULT_HP = 1000

# коэффициента роста стоимости улучшений
UPGRADE_COEFFICIENT = {
    'low': 1.05,
    'mid': 1.15,
    'high': 1.25
}

# Базовый урон таноков
BASE_DAMAGE = {
    'lt': 1,
    'st': 2,
    'td': 4,
    'tt': 5
}

