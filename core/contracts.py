LIST_DATA_SCHEME = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "year": {"type": "number"},
        "color": {"type": "string"},
        "pantone_value": {"type": "string"},
    },
    "required": ["id", "name", "year", "color", "pantone_value"]
}

CREATE_USER_SCHEME = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}, # не Обязательное поле
        "job": {"type": "string"}, # не Обязательное поле
        "id": {"type": "string"}

    },
    "required": ["id"] # порядок перечисление НЕ важен
}

UPDATE_USER_SCHEME = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}, # не Обязательное поле
        "job": {"type": "string"} # не Обязательное поле

    },
    "required": [ ] # порядок перечисление НЕ важен
}
