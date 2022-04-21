from __future__ import annotations
from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
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
        """Возвращаем данные о тренировке."""
        return (f"Тип тренировки: {self.training_type};"
                f" Длительность: {self.duration:.3f} ч.;"
                f" Дистанция: {self.distance:.3f} км;"
                f" Ср. скорость: {self.speed:.3f} км/ч;"
                f" Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    M_IN_H: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    """Тренировка: бег."""
    coeff_running_1: int = 18
    coeff_running_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_running_1 * self.speed - self.coeff_running_2)
                * self.weight / self.M_IN_KM * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_walking_1: float = 0.035
    coeff_walking_2: float = 0.029
    deegre_running: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        self.height: float = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.coeff_walking_1 * self.weight
                + (self.speed**self.deegre_running // self.height)
                * self.coeff_walking_2 * self.weight)
                * self.duration * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_swimming_1: float = 1.1
    coeff_swimming_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения во время плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время плавания."""
        return ((self.speed + self.coeff_swimming_1)
                * self.coeff_swimming_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout: Union[Swimming, SportsWalking, Running]

    if workout_type == 'SWM':
        workout: Swimming = Swimming(*data)
    elif workout_type == 'RUN':
        workout: Running = Running(*data)
    elif workout_type == 'WLK':
        workout: SportsWalking = SportsWalking(*data)

    return workout


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
