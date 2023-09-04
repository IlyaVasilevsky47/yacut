# yacut
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Основная возможность:
- Генерация коротких ссылок и связь их с исходными длинными ссылками;
- Переадресация на исходный адрес при обращении к коротким ссылкам.

## Запуск проекта:
1. Клонируем проект.
```bash
    git clone git@github.com:IlyaVasilevsky47/yacut.git
```

2. Создаем и активируем виртуальное окружение.
```bash
    python -m venv venv
    # Windows
    source venv/scripts/activate
```

3. Обновляем менеджер пакетов pip и устанавливаем зависимости из файла requirements.txt.
```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

4. Создаем базу данных. 
```bash
    flask shell
    from yacut import db
    db.create_all()
    exit()
```

5. Запускаем проект.
```bash
    flask run
```

## Автор:
- Василевский И.А.
- [Почта](vasilevskijila047@gmail.com)
- [Вконтакте](https://vk.com/ilya.vasilevskiy47)


## Технический стек
- Python 3.7.9
- Flask 2.0.2
- Flask-SQLAlchemy 2.5.1
- Flask-WTF 1.0.0
- Flask-Migrate 3.1.0
