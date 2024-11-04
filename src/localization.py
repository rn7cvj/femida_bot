
DOCS = { 
    "Административные штраф": "docs/Административные штрафы.pdf",
    "Брачный договор": "docs/Брачный договор.pdf",
    "Договор дарения": "docs/Договор дарения.pdf",
    "Договор займа" : "docs/Договор займа.pdf",
    "Завещание": "docs/Завещание.pdf",
    "Расписка": "docs/Расписка.pdf",
    "Трудовой договор": "docs/Трудовой договор.pdf",
}

TEXTS = {
    "start_message": (
        "Здравствуйте! Я - Фемида, Ваш юридический консультант. Вы можете задать мне вопрос, и я на него отвечу.\n\n"
        "Перед тем, как начать диалог, подтвердите свое согласие на обработку персональных данных и согласие на правила "
        "пользования юридическим консультантом Фемида. Если вы нарушите правила, вы несете юридическую ответственность.\n\n"
        "Нажмите 'Согласен', если принимаете условия, или 'Не согласен', чтобы завершить работу."
    ),
    "agree_message": "Ваше согласие принято.",
    "disagree_message": "Ваша работа завершена. Чтобы начать снова, нажмите - /start",
    "choose_category" : "Выберите категорию к которой относится ваш запрос.",
    "choose_subcategory": "Вы выбрали категорию %% CATEGORY_NAME %%. Теперь выберите подкатегорию.",
    "error_category": "Ошибка выбора. Попробуйте снова.",
    "request_instructions": (
        "Вы выбрали категорию: %% CATEGORY_NAME %%.\n"
        "Пункт: %% SUBCATEGORY_NAME %%.\n\n"
        "Просим оформить запрос в виде файла Word:\n\n"
        "- Дайте файлу название с указанием даты\n"
        "- На первой строке укажите Ваше ФИО, дату рождения, номер телефона и почту.\n"
        "- Включите текст запроса, таблицы, фотографии, чеки и др. информацию, если нужно.\n"
        "- После завершения загрузите и отправьте файл."
    ),
    "file_received": (
        "Ваш файл получен! Запрос находится в обработке. В течение 3 дней вам придет ответ на указанную Вами почту "
        "или свяжутся по телефону.\n"
        "Чтобы начать снова, нажмите - /start"
    ),
    "file_received_fail": (
        "Ошибка при загрузке файла. Попробуйте снова позже."
        "Чтобы начать снова, нажмите - /start"
        ),
    "file_error": "Ошибка: пожалуйста, загрузите файл.",
    "agreement_buttons": {"agree": "Согласен", "disagree" : "Не согласен",},
    "back" : "Назад",
    "document_caption" : "Документация по %% SUBCATEGORY_NAME %%"
}

CATEGORIES = {
    "Гражданские правоотношения": [
        "Право собственности", "Наследственное право", "Семейное право", 
        "Корпоративное право", "Жилищное право", "Право интеллектуальной собственности"
    ],
    "Трудовые правоотношения": [
        "Обеспечение занятости и трудоустройства", "Охрана труда и здоровья работника",
        "Трудовой договор", "Локальный нормативный акт", "Зарплата/Премия/Надбавка"
    ],
    "Административные правоотношения": [
        "Административный штраф", "Административное предупреждение", 
        "Лишение водительских прав", "Приостановление деятельности организации", "Административный арест"
    ],
    "Документация": list(DOCS.keys()),
}


