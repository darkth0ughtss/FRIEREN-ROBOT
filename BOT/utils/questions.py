from ..state import session

async def get_question():
    async with session.get("https://opentdb.com/api.php?amount=1&category=31&type=multiple") as resp:
        data = await resp.json()
        return {
            "question": data["results"][0]["question"],
            "options": data["results"][0]["incorrect_answers"] + [data["results"][0]["correct_answer"]],
            "correct": data["results"][0]["correct_answer"]
        }
