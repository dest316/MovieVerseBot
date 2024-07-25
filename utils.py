def get_rolls_word(number: int) -> str:
    number = abs(number)
    if 11 <= number % 100 <= 19:
        return "рулетов"
    else:
        last_digit = number % 10
        if last_digit == 1:
            return "рулет"
        elif 2 <= last_digit <= 4:
            return "рулета"
        else:
            return "рулетов"


class TransferStatus:
    __statuses = {
        200: "Перевод успешно совершен",
        402: "На счету отправителя недостаточно средств",
        407: "Получатель и отправитель не могут являться одним и тем же лицом"
    }

    @property
    def statuses(self):
        return self.__statuses

