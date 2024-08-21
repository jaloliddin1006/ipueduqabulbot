from django.conf import settings
from tgbot.models import BotAdmin
from asgiref.sync import sync_to_async


async def get_admins():
    ADMINS = []
    ADMINS += settings.ADMINS

    BOT_ADMINS = await sync_to_async(
        lambda: list(BotAdmin.objects.filter(is_active=True).values_list('user__telegram_id', flat=True)),
        thread_sensitive=True
    )()
    ADMINS += BOT_ADMINS

    return ADMINS



import math

class IntegerPronunciation:
    def __init__(self):
        self.ONES = ['', 'bir', 'ikki', 'uch', 'to\'rt', 'besh', 'olti', 'yetti', 'sakkiz', 'to\'qqiz']
        self.TWOS = ['', 'o\'n', 'yigirma', 'o\'ttiz', 'qirq', 'ellik', 'oltmish', 'yetmish', 'sakson', 'to\'qson']
        self.OTHERS = ['', '', 'ming', 'million', 'milliard', 'trillion', 'kvadrillion', 'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 'decillion', 'undiscillion', 'duodecillion',]

    def son_to_str(self, son):
        l = len(son)
        if l == 1:
            return self.ONES[int(son)]
        if l == 2:
            return f"{self.TWOS[int(son[0])]} {self.son_to_str(son[1])}"
        if l == 3:
            if son[0] == '0':
                return self.son_to_str(son[1:])
            return f"{self.son_to_str(son[0])} yuz {self.son_to_str(son[1:])}"
        if l > 3:
            if son[0] == '0':
                return self.son_to_str(son[1:])
            s = math.ceil(l/3)
            n = (s-1)*3
            return f"{self.son_to_str(son[:-n])} {self.OTHERS[s]} {self.son_to_str(son[-n:])}"

    def main(self, son):
        start=False
        end=False
        if isinstance(son, int):
            son = str(son)
        if '-' in son:
            if son.strip().startswith('-'):
                start = True
            if son.strip().endswith('-'):
                end = True
            son = son.replace('-', '').strip()
            result = self.son_to_str(str(son)).replace('  ', ' ').strip()
            if start:
                result = 'minus ' + result
            if end:
                if son[-1] in '267':
                    result += 'nchi'
                else:
                    result += 'inchi'
        else:
            result = self.son_to_str(str(son)).replace('  ', ' ')
        return result.replace('   ', ' ')


# res = IntegerPronunciation().main(12121212)
# print(res)
