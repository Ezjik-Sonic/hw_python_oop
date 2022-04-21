from __future__ import annotations
from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: int,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration} ч.;'
                f' Дистанция: {self.distance} км;'
                f' Ср. скорость: {self.speed} км/ч;'
                f' Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки;
                 weight: float,  # вес спортсмена.
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.action,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.speed - self.coeff_calorie_2)
                * self.weight / self.M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        height: float = height

    def get_spent_calories(self) -> float:
        return ((0.035 * self.weight + (self.speed**2 // self.height)
                * 0.029 * self.weight) * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        length_pool: float = length_pool
        count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.speed + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    obj: Union[Swimming, SportsWalking, Running]
    if workout_type == 'RUN':
        obj: Swimming = Swimming(*data)
    elif workout_type == 'RUN':
        obj: Running = Running(*data)
    elif workout_type == 'WLK':
        obj: SportsWalking = SportsWalking(*data)

    return obj


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
