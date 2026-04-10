import asyncio

from backend.core.config import BASE_COSTS, UPGRADE_COEFFICIENT, UPGRADE_FOR_TOOLS
from backend.db.database import DB_PATH, get_player, apply_upgrade_tank, apply_upgrade_technology

"""
ЛОГИКА УЛУЧШЕНИЙ ТАНКОВ:
- Стоимость улучшения танка растет экспоненциально в зависимости от его уровня, с тремя разными коэффициентами роста для разных диапазонов уровней (1-49, 50-99, 100+).
- Для улучшения танков используются запчасти (scrap) и инструменты (tools). 
    Инструменты требуются только на определенных уровнях (каждые 10 уровней), и их количество также растет с уровнем.
"""
# - Улучшения танков дают конкретные бонусы: 
#     легкий танк увеличивает шанс найти сталь/инструменты, 
#     средний танк увеличивает количество запчастей в поставке, 
#     тяжелый танк увеличивает общий урон всей техники, а 
#     пт-сау улучшает шанс и силу критического удара.
# - Игроки должны стратегически планировать свои улучшения, учитывая растущую стоимость и необходимость участия в событиях 
# (например, убийство Босса для получения инструментов) для достижения более высоких уровней улучшений.  
# ""

def get_upgrade_cost(tank_type, level):
    """Расчет стоимости улучшения танка в зависимости от его типа и уровня. Ресурс - Запчасти (scrap)."""

    # Берем базовую цену из конфига 
    base = BASE_COSTS[tank_type]
    
    if level <= 50:
        return int(base * (UPGRADE_COEFFICIENT["low"] ** (level - 1)))  
    cost_50 = int(base * (UPGRADE_COEFFICIENT["low"] ** 49))  # стоимость 50-го уровня

    if level <= 100:
        # Цена 50-го уровня * 1.15 в нужной степени
        return int(cost_50 * (UPGRADE_COEFFICIENT["mid"] ** (level - 50)))
    cost_100 = int(cost_50 * (UPGRADE_COEFFICIENT["mid"] ** 50))  # стоимость 100-го уровня
    
    if level > 100:
        # Цена 100-го уровня * 1.25 в нужной степени
        return int(cost_100 * (UPGRADE_COEFFICIENT["high"] ** (level - 100)))
    
def get_tools_price(level: int) -> int:
    """Возвращает сколько инструментов (tools) нужно для апа на этот уровень"""
    if level % 10 != 0:
        return 0
    return int((level * UPGRADE_FOR_TOOLS) / 10)


async def process_upgrade(user_id, tank_type):
    """ Получаем данные игрока из БД (get_player).
        Считаем цену в запчастях и инструментах для следующего уровня (current_level + 1).
        Проверяем, хватает ли ресурсов.
        Если хватает — вызываем функцию add_resources
            обновить уровень танка в БД.
        Если не хватает — вернуть сообщение об ошибке.
    """
    # Чекаем юзера в БД
    player = await get_player(user_id)
    if not player:  return 
    
    # рассчитываем стоимость улучшения в запчастях и инструментах для следующего уровня
    upgrade_cost = get_upgrade_cost(tank_type, player[f"{tank_type}_lvl"] + 1)  # в запчастях 
    tools_cost = get_tools_price(player[f"{tank_type}_lvl"] + 1)  # в инструментах 
    
    if player["scrap"] >= upgrade_cost and player["tools"] >= tools_cost:
        await apply_upgrade_tank(user_id, tank_type, upgrade_cost, tools_cost)
        return print(f"✅ Танку типа {tank_type.upper()} успешно улучшен до уровня {player[f'{tank_type}_lvl'] + 1}!")

    return print("У вас недостаточно ресурсов для улучшения!")

   
async def process_upgrade_technology(user_id, tech_type):
    """ процесс улучшения технологии 
    """
    # Чекаем юзера в БД
    player = await get_player(user_id)
    if not player:  return 

    steel_cost = player[f"{tech_type}_upg"] + 1  # рассчитываем стоимость улучшения в стали

    if player["steel"] >= steel_cost:
        await apply_upgrade_technology(user_id, tech_type, steel_cost)
        return print(f"✅ Технология {tech_type.upper()} успешно улучшена до уровня {player[f'{tech_type}_upg'] + 1}!")
    return print("У вас недостаточно стали для улучшения!")
    
if __name__ == "__main__":
    # тестируем расчет стоимости улучшений
    # for tank in ["lt", "st", "td", "tt"]:
    #     print(f"Стоимость улучшений для {tank.upper()}:")
    #     for lvl in [1, 10, 50, 51, 75, 100, 101, 110]:
    #         if lvl % 10 == 0:
    #             print(f"  Уровень {lvl}: {get_upgrade_cost(tank, lvl)} запчастей и {get_tools_price(lvl)} инструментов")
    #         else: print(f"  Уровень {lvl}: {get_upgrade_cost(tank, lvl)} запчастей")

    # asyncio.run(process_upgrade(12345678900, "lt"))
    asyncio.run(process_upgrade_technology(123456789, "lt"))