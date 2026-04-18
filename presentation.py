import streamlit as st
import reveal_slides as rs

def presentation_page():
    st.title("Презентация проекта")

    
    presentation_markdown = """
# Прогнозирование выплат
---
## Цель проекта
Разработать модель ML для предсказания итоговой стоимости страхового возмещения.
---
## Данные
Используется датасет **Workers Compensation** (100,000 записей).
---
## Предобработка
- Извлечение признаков из дат (Month, DayOfWeek, Delay).
- Кодирование категорий (Label Encoding).
- Стандартизация числовых признаков.
---
## Модели и результаты
- Linear Regression
- Random Forest (Лучшая точность)
- Ridge Regression
---
## Заключение
Модель готова к интеграции для оценки финансовых резервов.
"""

    with st.sidebar:
        st.header("Настройки")
        theme = st.selectbox("Тема", ["black", "white", "league", "beige"])
        transition = st.selectbox("Переход", ["slide", "convex", "zoom"])

    rs.slides(
        presentation_markdown,
        height=500,
        theme=theme,
        config={"transition": transition},
    )

if __name__ == "__main__":
    presentation_page()