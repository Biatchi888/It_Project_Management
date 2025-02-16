CONVERSIONS = {     # Conversion dictionary
    'cup': {
        'tablespoon': 16,
        'teaspoon': 48,
        'ounce': 8,
        'pound': 0.5,
        'gram': 128,
    },
    'tablespoon': {
        'cup': 1 / 16,
        'teaspoon': 3,
        'ounce': 0.5,
        'pound': 1 / 32,
        'gram': 16,
    },
    'teaspoon': {
        'cup': 1 / 48,
        'tablespoon': 1 / 3,
        'ounce': 1 / 6,
        'pound': 1 / 96,
        'gram': 5.69,
    },
    'ounce': {
        'cup': 1 / 8,
        'tablespoon': 2,
        'teaspoon': 6,
        'pound': 1 / 16,
        'gram': 28.35,
    },
    'pound': {
        'cup': 1.92,
        'tablespoon': 32,
        'teaspoon': 96,
        'ounce': 16,
        'gram': 453.592,
    },
    'gram': {
        'cup': 1 / 128,
        'tablespoon': 1 / 16,
        'teaspoon': 1 / 5.33,
        'ounce': 1 / 28.35,
        'pound': 1 / 453.592,
    },
}


# Initialize conversation history list
conversation_history = []


def convert_measurement(query):
    parts = query.split()
    if len(parts) != 4 or parts[2] != 'to':
        return 'Invalid query. Please provide a valid conversion query.'

    source_measurement = parts[1]
    target_measurement = parts[3]

    if source_measurement not in CONVERSIONS or target_measurement not in CONVERSIONS[source_measurement]:
        return 'Invalid measurement units. Please provide valid units.'

    conversion_factor = CONVERSIONS[source_measurement][target_measurement]
    result = conversion_factor * float(parts[0])

    return f'{parts[0]} {source_measurement} is equal to {result} {target_measurement}.'

