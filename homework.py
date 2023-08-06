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

    def get_message(self):
        encouring_message = (f'Тип тренировки: {self.training_type}; '
                             f'Длительность: {self.duration:.3f} ч.; '
                             f'Дистанция: {self.distance:.3f} км; '
                             f'Ср. скорость: {self.speed:.3f} км/ч; '
                             f'Потрачено ккал: {self.calories:.3f}.')
        return encouring_message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.average_speed: float = self.get_distance() / self.duration
        return self.average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                               * self.get_mean_speed()
                               + self.CALORIES_MEAN_SPEED_SHIFT)
                               * self.weight / self.M_IN_KM
                               * self.duration * self.M_IN_H)
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1: float = 0.035
    K_2: float = 0.029
    M_S_IN_KM_H: float = 0.278
    S_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.K_1 * self.weight
                               + ((self.get_mean_speed() * self.M_S_IN_KM_H)**2
                                / (self.height / self.S_IN_M))
                               * self.K_2 * self.weight)
                               * self.duration * self.M_IN_H)
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    K_1: float = 1.1
    K_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.average_speed: float = (self.length_pool * self.count_pool
                                     / self.M_IN_KM / self.duration)
        return self.average_speed

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.get_mean_speed() + self.K_1)
                               * self.K_2 * self.weight * self.duration)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking,
                          }
    workout_object: Training = workout_dict[workout_type]
    training = workout_object(*data)
    return training


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
