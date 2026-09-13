import json
from pathlib import Path

INTENTS = [
    "billing_payment",
    "refund",
    "subscription_cancel",
    "subscription_plan",
    "account_login",
    "account_security",
    "premium_not_working",
    "playback_problem",
    "app_technical_problem",
    "playlist_music_problem",
    "family_student_plan",
    "gift_code",
    "feature_request",
    "general_complaint",
    "other",
]

INPUT_FILE = Path("artifacts/golden_template.jsonl")
OUTPUT_FILE = Path("artifacts/golden_set.jsonl")


def load_examples():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE}.\n"
            "Run prepare_data.py first."
        )

    examples = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                examples.append(json.loads(line))

    return examples


def show_intents():
    print("\nChoose an intent:")
    print("-" * 60)

    for i, intent in enumerate(INTENTS, start=1):
        print(f"{i:2}. {intent}")

    print("-" * 60)


def get_intent():
    while True:
        choice = input("Intent number: ").strip()

        if choice.lower() == "q":
            return None

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(INTENTS):
                return INTENTS[number - 1]

        print(
            f"Please enter a number between 1 and {len(INTENTS)}, "
            "or 'q' to quit."
        )


def get_route():
    while True:
        choice = input(
            "\nExpected route [A = AUTO, E = ESCALATE]: "
        ).strip().lower()

        if choice == "a":
            return "AUTO"

        if choice == "e":
            return "ESCALATE"

        if choice == "q":
            return None

        print("Please enter A or E.")


def save_examples(examples):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for example in examples:
            f.write(
                json.dumps(
                    example,
                    ensure_ascii=False
                ) + "\n"
            )


def main():
    examples = load_examples()

    # Resume from an existing golden set if one already exists.
    if OUTPUT_FILE.exists():
        print("\nExisting golden_set.jsonl found.")

        answer = input(
            "Resume existing labels? [Y/n]: "
        ).strip().lower()

        if answer != "n":
            labelled = {}

            with OUTPUT_FILE.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if line:
                        row = json.loads(line)
                        labelled[row["id"]] = row

            for example in examples:
                if example["id"] in labelled:
                    example.update(labelled[example["id"]])

    total = len(examples)

    print("\n" + "=" * 70)
    print("       SPOTIFY GOLDEN SET LABELLING TOOL")
    print("=" * 70)

    print(f"\nExamples to label: {total}")

    print(
        """
Instructions:

  - Read the customer message carefully.
  - Choose ONE intent.
  - Choose AUTO or ESCALATE.
  - The historical reply is shown only as context.
  - Do not let the historical reply determine the label automatically.
  - Type 'q' if you want to stop. Your progress will be saved.
"""
    )

    for index, example in enumerate(examples):

        # Skip already labelled examples.
        if (
            example.get("intent")
            and example.get("expected_route")
        ):
            continue

        print("\n")
        print("=" * 70)
        print(
            f"Example {index + 1} / {total} "
            f"({((index + 1) / total) * 100:.1f}%)"
        )
        print("=" * 70)

        print("\nCUSTOMER MESSAGE:")
        print("-" * 70)
        print(example["customer_message"])
        print("-" * 70)

        print("\nHISTORICAL BRAND REPLY:")
        print("-" * 70)
        print(example.get("historical_reply", ""))
        print("-" * 70)

        show_intents()

        intent = get_intent()

        if intent is None:
            save_examples(examples)
            print(
                f"\nProgress saved to:\n"
                f"{OUTPUT_FILE}"
            )
            return

        example["intent"] = intent

        route = get_route()

        if route is None:
            # Don't leave a partially labelled example.
            example["intent"] = ""
            save_examples(examples)

            print(
                f"\nProgress saved to:\n"
                f"{OUTPUT_FILE}"
            )
            return

        example["expected_route"] = route

        # Save after every example so progress isn't lost.
        save_examples(examples)

        print(
            f"\nSaved: {intent} | {route}"
        )

    print("\n" + "=" * 70)
    print("ALL EXAMPLES HAVE BEEN LABELLED")
    print("=" * 70)

    print(f"\nGolden set saved to:")
    print(OUTPUT_FILE)

    print("\nNext command:")
    print("python -m evaluation.run_all")


if __name__ == "__main__":
    main()