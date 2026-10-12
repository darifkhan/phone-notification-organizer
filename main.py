import heapq
from datetime import datetime


class Notification:
    """One notification (like one WhatsApp or Instagram alert)."""

    def __init__(self, nid, app, message, priority):
        self.nid = nid
        self.app = app
        self.message = message
        self.priority = priority  # 1 = High, 2 = Medium, 3 = Low
        self.time = datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        names = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}
        return f"[#{self.nid}] [{names[self.priority]}] {self.app}: {self.message} ({self.time})"


class NotificationOrganizer:
    def __init__(self):
        self.heap = []         # PRIORITY QUEUE (heap): most important comes out first
        self.by_app = {}       # DICTIONARY (hash map): app name -> list of notifications
        self.read_stack = []   # STACK: last read notification is undone first
        self.next_id = 1

    def add(self, app, message, priority):
        n = Notification(self.next_id, app, message, priority)
        self.next_id += 1
        heapq.heappush(self.heap, (n.priority, n.nid, n))
        self.by_app.setdefault(app, []).append(n)
        print("Added:", n)

    def read_next(self):
        if not self.heap:
            print("No notifications left.")
            return
        _, _, n = heapq.heappop(self.heap)      # removes highest priority
        self.by_app[n.app].remove(n)
        if not self.by_app[n.app]:
            del self.by_app[n.app]
        self.read_stack.append(n)               # push onto stack
        print("You read:", n)

    def undo_read(self):
        if not self.read_stack:
            print("Nothing to undo.")
            return
        n = self.read_stack.pop()               # pop from stack
        heapq.heappush(self.heap, (n.priority, n.nid, n))
        self.by_app.setdefault(n.app, []).append(n)
        print("Restored:", n)

    def show_all(self):
        if not self.heap:
            print("No notifications.")
            return
        print("\n--- All notifications (most important first) ---")
        for _, _, n in sorted(self.heap):
            print(n)

    def show_by_app(self):
        if not self.by_app:
            print("No notifications.")
            return
        print("\n--- Grouped by app ---")
        for app_name, items in self.by_app.items():
            print(f"\n{app_name} ({len(items)})")
            for n in items:
                print("   ", n)

    def search(self, keyword):
        keyword = keyword.lower()
        found = False
        for _, _, n in self.heap:               # linear search
            if keyword in n.message.lower() or keyword in n.app.lower():
                print(n)
                found = True
        if not found:
            print("No match found.")

    def load_sample(self):
        self.add("WhatsApp", "Mom: Call me back", 1)
        self.add("Instagram", "Rahul liked your photo", 3)
        self.add("Bank", "Rs 500 debited from your account", 1)
        self.add("YouTube", "New video uploaded", 3)
        self.add("Gmail", "Interview schedule update", 2)


def main():
    organizer = NotificationOrganizer()

    while True:
        print("\n===== PHONE NOTIFICATION ORGANIZER =====")
        print("1. Add notification")
        print("2. Show all (by priority)")
        print("3. Show grouped by app")
        print("4. Read next (highest priority)")
        print("5. Undo last read")
        print("6. Search")
        print("7. Load sample data")
        print("8. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            app_name = input("App name: ").strip()
            message = input("Message: ").strip()
            priority = input("Priority (1=High, 2=Medium, 3=Low): ").strip()
            if not app_name or not message or priority not in ("1", "2", "3"):
                print("Invalid input. Try again.")
            else:
                organizer.add(app_name, message, int(priority))
        elif choice == "2":
            organizer.show_all()
        elif choice == "3":
            organizer.show_by_app()
        elif choice == "4":
            organizer.read_next()
        elif choice == "5":
            organizer.undo_read()
        elif choice == "6":
            organizer.search(input("Search word: "))
        elif choice == "7":
            organizer.load_sample()
        elif choice == "8":
            print("Bye!")
            break
        else:
            print("Wrong choice. Enter 1 to 8.")


if __name__ == "__main__":
    main()