import datetime as dt
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id).items
    count = 0
    sumage = 0
    currage = dt.datetime.now().year
    for i in range(0, len(friends)):
        try:
            sumage += currage - int(friends[i]["bdate"][5:])
            count += 1
        except:
            pass
    if count > 0:
        return sumage // count
    return None
