# LoaderScript
Этот проект предназначен для загрузки содержимого репозитория и вычисления SHA256 хэшей для всех файлов в репозитории. После выполнения скрипта, файлы будут скачаны в  директорию, а хэши файлов будут сохранены в файл формата `json`.

## Установка

Убедитесь, что у вас установлен Poetry. Если нет, установите его, следуя инструкциям на официальном сайте.

1. Клонируйте репозиторий:

```
git clone https://github.com/GrigoriyKruchinin/LoaderScript.git
```
2. Перейдите в каталог проекта:

```
cd LoaderScript
```

3. Установите зависимости с помощью Poetry:

```
poetry install
```
4. Активируйте виртуальное окружение:

```
poetry shell
```

## Команды для выполнения перед запуском приложения
Перед тем как запускать основное приложение, рекомендуется выполнить следующие команды для проверки качества кода и покрытия тестами:

1. Проверка с помощью Nitpick:

```
make nitpick
```

Эта команда проверяет проект на соответствие стандартам кода, заданным в конфигурационных файлах.

2. Линтинг с помощью Flake8:

```
make lint
```

Эта команда выполняет проверку качества кода с помощью линтера Flake8, выявляя потенциальные проблемы в коде, такие как ошибки стиля и синтаксиса.

3. Покрытие тестов с помощью pytest:

```
make test_cov
```

Эта команда запускает тесты и выводит отчет о покрытии кода тестами, что позволяет убедиться, что тесты покрывают достаточное количество кода проекта.

## Запуск основного приложения
Для запуска основного приложения выполните следующую команду:

```
make start
```

Эта команда скачает содержимое репозитория https://gitea.radium.group/radium/project-configuration в папку `project-configuration`, которая появится в корне проекта. Внутри этой папки также появится файл `hashes.json`, который будет содержать хэши каждого скаченного файла.

## Благодарность и контакты

Буду рад обратной связи!

- Автор: Grigoriy Kruchinin
- [GitHub](https://github.com/GrigoriyKruchinin)
- [Email](mailto:gkruchinin75@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/grigoriy-kruchinin/)