# Указываем базовый образ - образ python3
FROM python:3

# Устанавливаем метаданные
LABEL maintainer="elipandasyts@.gmail.com"

# Создаем рабочую директорию
WORKDIR /usr/src/app

# Устанавливаем значения по умолчанию для переменных времени сборки
ARG CIRCLE_R_ARG=10
ARG SQUARE_A_ARG=10

# Устанавливаем переменные среды для передачи информации
# в запускаемый контейнер
ENV CIRCLE_R=${CIRCLE_R_ARG}
ENV SQUARE_A=${SQUARE_A_ARG}

# Команда, выполняемая при каждом запуске контейнера
CMD ["./script.sh"]
