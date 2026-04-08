import asyncio


async def open_lootbox_for_player(user_id: int):
    from backend.core.logic.lootboxes import open_lootbox
    from backend.db.database import add_resources

    loot = open_lootbox(user_id)
    await add_resources(user_id, loot[0]["scrap"], loot[0]["tools"], loot[0]["steel"], loot[0]["ac_gold"])
    return loot
    # print(loot)



if __name__ == "__main__":
    # тестируем открытие лутбокса для игрока
    user_id = 12345678900
    data = asyncio.run(open_lootbox_for_player(user_id=user_id))

    print(f"Чек данных: {data[0]} \nИгрок {user_id} открыл {data[4]} лутбокс и получил: {data[0]['scrap']} запчастей" + 
          (f", {data[0]["tools"]} инструмент(ов)" if data[1] else "") +
          (f", {data[0]["steel"]} стали" if data[2] else "") +
          (f" и {data[0]["ac_gold"]} золотых монет AC." if data[3] else "."))