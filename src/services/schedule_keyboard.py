from vkbottle import Keyboard, Text


def generate_keyboard():
    return (
        Keyboard(one_time=True, inline=False).add(
            Text(
                "1 курс",
                payload={"command": "schedule_request", "course": "1 курс"},
            ),
        ).add(
            Text(
                "2 курс",
                payload={"command": "schedule_request", "course": "2 курс"},
            ),
        ).row().add(
            Text(
                "3 курс",
                payload={"command": "schedule_request", "course": "3 курс"},
            ),
        ).add(
            Text(
                "4 курс",
                payload={"command": "schedule_request", "course": "4 курс"},
            ),
        )
    ).get_json()
