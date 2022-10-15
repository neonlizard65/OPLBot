# -*- coding: utf-8 -*-
class Player:
    def __init__(self, z_type, fio, birthday=None, position=None, photo=None):
        """
        Parameters
        ----------
        z_type : str
            Тип заявки
        fio : str
            ФИО игрока
        birthday : int, optional
            Дата рождения игрока
        position : str, optional
            Амплуа игрока
        photo : str, optional
            Фото игрока
        """
        self.z_type = z_type
        self.fio = fio
        self.birthday = birthday
        self.position = position
        self.photo = photo