from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE: str = ("Тип тренировки: {training_type};"
                         " Длительность: {duration:.3f} ч.;"
                         " Дистанция: {distance:.3f} км;"
                         " Ср. скорость: {speed:.3f} км/ч;"
                         " Потрачено ккал: {calories:.3f}.")

    def get_message(self):
        """Возвращаем данные о тренировке."""
        return(self.INFO_MESSAGE.format(**asdict(self)))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: float
    duration: float
    weight: float

    M_IN_KM: ClassVar[float] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_H: ClassVar[float] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Определите get_spent_calories в %s." % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    action: float
    duration: float
    weight: float

    COEFF_RUNNING_FACTOR: ClassVar[float] = 18.0
    COEFF_RUNNING_SUBTR: ClassVar[float] = 20.0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((self.COEFF_RUNNING_FACTOR * self.get_mean_speed()
                 - self.COEFF_RUNNING_SUBTR)
                * self.weight / self.M_IN_KM * self.duration * self.M_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: float
    duration: float
    weight: float
    height: float

    COEFF_WALKING_1: ClassVar[float] = 0.035
    COEFF_WALKING_2: ClassVar[float] = 0.029
    DEEGRE_RUNNING: ClassVar[float] = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        return ((self.COEFF_WALKING_1 * self.weight
                + (self.get_mean_speed()**self.DEEGRE_RUNNING // self.height)
                * self.COEFF_WALKING_2 * self.weight)
                * self.duration * self.M_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: float
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    COEFF_SWIMMING_1: ClassVar[float] = 1.1
    COEFF_SWIMMING_2: ClassVar[float] = 2
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения во время плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время плавания."""
        return ((self.get_mean_speed() + self.COEFF_SWIMMING_1)
                * self.COEFF_SWIMMING_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    WORKOUT: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type not in WORKOUT:
        raise Exception(f"Тренировка типа:"
                        f" {workout_type} Неподдерживается.\n"
                        f"Поддерживаемые типы:"
                        f" SWM - Swimming,"
                        f" RUN - Running,"
                        f" WLK - SportsWalking")
    return WORKOUT[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [9000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
