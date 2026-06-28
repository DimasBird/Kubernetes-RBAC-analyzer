from datetime import datetime

def send_report(args, report):
    save = args.save

    if not save:
        print(report)
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filepath = f"reports/{timestamp}"
    filepath += ".json" if args.json else ".txt"

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report)
        print(f"Report saved to {filepath}")
