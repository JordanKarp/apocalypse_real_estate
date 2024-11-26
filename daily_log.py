from dataclasses import dataclass


@dataclass
class LogEntry:
    day: int = 0
    text: str = "This is what happened."

    def __str__(self):
        return f"Day {self.day} - {self.text}"


class DailyLog:
    def __init__(self):
        self.log = {}

    def add_entry(self, day_num, entry_text, print_entry=True):
        entry = LogEntry(day_num, entry_text)
        if self.log.get(entry.day):
            self.log[entry.day].text += f", {entry.text}"
        else:
            self.log[entry.day] = entry

        if print_entry:
            print(entry.text)

    def print_log(self):
        for _, entry in self.log.items():
            print(entry)


# dl = DailyLog()

# dl.add_entry(LogEntry(1, "Scouted nearby homes"))
# dl.add_entry(LogEntry(2, "Settled a home"))
# dl.add_entry(LogEntry(3, "Scavenged nearby"))
# dl.add_entry(LogEntry(4, "Did nothing"))
# dl.add_entry(LogEntry(4, "Did more of nothing"))

# dl.print_log()
