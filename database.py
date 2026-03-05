import aiosqlite

DB_NAME = "quotes.db"


# 1. Функция создания таблицы (вызывается один раз при старте)
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем виртуальную таблицу для быстрого поиска (FTS5)
        # content — текст цитаты, author — имя человека
        # tokenize="unicode61" — чтобы поиск понимал русский язык и регистр (Аа)
        await db.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS quotes_index 
            USING fts5(content, author, tokenize="unicode61")
        """
        )
        await db.commit()


# 2. Функция для сохранения цитаты в базу
async def add_quote(content: str, author: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO quotes_index (content, author) VALUES (?, ?)",
            (content, author),
        )
        await db.commit()


# 3. Функция поиска (тот самый продвинутый поиск)
async def search_quotes(query: str):
    async with aiosqlite.connect(DB_NAME) as db:
        # Используем MATCH для полнотекстового поиска
        # Звездочка в конце f"{query}*" позволяет искать по началу слова
        cursor = await db.execute(
            "SELECT content, author FROM quotes_index WHERE quotes_index MATCH ? LIMIT 15",
            (f"{query}*",),
        )
        return await cursor.fetchall()
