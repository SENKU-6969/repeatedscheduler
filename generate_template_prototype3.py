import datetime
import calendar
import csv
import os
from collections import defaultdict

class TaskScheduler:
    def __init__(self):
        self.tasks = {}  # {task_name: {'intervals': [days], 'start_date': date}}
        self.schedule = defaultdict(list)  # {date: [tasks]}
        
    def add_task(self, task_name, intervals, start_date=None):
        """
        Add a new task with revision intervals
        
        Parameters:
        - task_name: Name of the chapter/task
        - intervals: List of days when to review (e.g., [1, 3, 7, 14, 30])
        - start_date: When to start the task (defaults to today)
        """
        if start_date is None:
            start_date = datetime.date.today()
        
        self.tasks[task_name] = {
            'intervals': intervals,
            'start_date': start_date
        }
        
        # Schedule the task based on intervals
        for interval in intervals:
            review_date = start_date + datetime.timedelta(days=interval)
            self.schedule[review_date].append(task_name)
    
    def add_task_with_repetitions(self, task_name, interval, repetitions, start_date=None):
        """
        Add a new task with a fixed interval repeated multiple times
        
        Parameters:
        - task_name: Name of the chapter/task
        - interval: Number of days between repetitions
        - repetitions: Number of times to repeat the task
        - start_date: When to start the task (defaults to today)
        """
        if start_date is None:
            start_date = datetime.date.today()
        
        # Calculate intervals based on repetitions
        intervals = []
        current_interval = 0
        
        for _ in range(repetitions):
            intervals.append(current_interval)
            current_interval += interval
        
        self.add_task(task_name, intervals, start_date)
    
    def generate_schedule(self, days=90):
        """Generate a schedule for the specified number of days"""
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=days)
        
        # Clear existing schedule
        self.schedule = defaultdict(list)
        
        # Regenerate schedule
        for task_name, task_info in self.tasks.items():
            for interval in task_info['intervals']:
                review_date = task_info['start_date'] + datetime.timedelta(days=interval)
                if start_date <= review_date <= end_date:
                    self.schedule[review_date].append(task_name)
    
    def get_tasks_for_date(self, date):
        """Get all tasks scheduled for a specific date"""
        return self.schedule.get(date, [])
    
    def export_to_csv(self, filename="schedule.csv"):
        """Export the schedule to a CSV file"""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Day', 'Tasks'])
            
            # Sort dates
            sorted_dates = sorted(self.schedule.keys())
            
            for date in sorted_dates:
                day_name = calendar.day_name[date.weekday()]
                tasks = ', '.join(self.schedule[date])
                writer.writerow([date.strftime('%Y-%m-%d'), day_name, tasks])
        
        return filename
    
    def print_monthly_calendar(self, year=None, month=None):
        """Print a monthly calendar with tasks"""
        if year is None or month is None:
            today = datetime.date.today()
            year = today.year
            month = today.month
        
        # Get the calendar for the month
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        print(f"\n{month_name} {year}")
        print("Mon Tue Wed Thu Fri Sat Sun")
        
        for week in cal:
            week_str = ""
            for day in week:
                if day == 0:
                    week_str += "    "
                else:
                    date = datetime.date(year, month, day)
                    task_count = len(self.schedule.get(date, []))
                    if task_count > 0:
                        week_str += f"{day:2d}* "
                    else:
                        week_str += f"{day:2d}  "
            print(week_str)
        
        # Print tasks for the month
        print("\nTasks this month:")
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            date = datetime.date(year, month, day)
            tasks = self.schedule.get(date, [])
            if tasks:
                print(f"{date.strftime('%Y-%m-%d')} ({calendar.day_name[date.weekday()]}): {', '.join(tasks)}")


def main():
    scheduler = TaskScheduler()
    
    print("===== Task Revision Scheduler =====")
    print("This program helps you schedule when to revise chapters/tasks.")
    
    while True:
        print("\nOptions:")
        print("1. Add a new task/chapter with custom intervals")
        print("2. Add a new task/chapter with fixed interval and repetitions")
        print("3. View schedule for a specific date")
        print("4. View monthly calendar")
        print("5. Export schedule to CSV")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            task_name = input("Enter task/chapter name: ")
            
            print("Enter revision intervals in days (comma-separated)")
            print("Example: 1,3,7,14,30 (review after 1 day, 3 days, etc.)")
            intervals_input = input("Intervals: ")
            
            try:
                intervals = [int(x.strip()) for x in intervals_input.split(',')]
                
                start_date_input = input("Start date (YYYY-MM-DD) or leave blank for today: ")
                if start_date_input:
                    start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d").date()
                else:
                    start_date = datetime.date.today()
                
                scheduler.add_task(task_name, intervals, start_date)
                print(f"Task '{task_name}' added successfully!")
                
            except ValueError:
                print("Invalid input. Please enter valid numbers for intervals.")
        
        elif choice == '2':
            task_name = input("Enter task/chapter name: ")
            
            try:
                interval = int(input("Enter interval between repetitions (in days): "))
                repetitions = int(input("Enter number of repetitions: "))
                
                start_date_input = input("Start date (YYYY-MM-DD) or leave blank for today: ")
                if start_date_input:
                    start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d").date()
                else:
                    start_date = datetime.date.today()
                
                scheduler.add_task_with_repetitions(task_name, interval, repetitions, start_date)
                
                # Show the scheduled dates
                print(f"\nTask '{task_name}' scheduled for:")
                for i in range(repetitions):
                    review_date = start_date + datetime.timedelta(days=i*interval)
                    print(f"  {review_date.strftime('%Y-%m-%d')} ({calendar.day_name[review_date.weekday()]})")
                
            except ValueError:
                print("Invalid input. Please enter valid numbers for interval and repetitions.")
        
        elif choice == '3':
            date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            
            try:
                if date_input:
                    date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
                else:
                    date = datetime.date.today()
                
                tasks = scheduler.get_tasks_for_date(date)
                
                print(f"\nTasks for {date.strftime('%Y-%m-%d')} ({calendar.day_name[date.weekday()]}):")
                if tasks:
                    for i, task in enumerate(tasks, 1):
                        print(f"{i}. {task}")
                else:
                    print("No tasks scheduled for this date.")
                    
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        elif choice == '4':
            try:
                year_input = input("Enter year (YYYY) or leave blank for current year: ")
                month_input = input("Enter month (1-12) or leave blank for current month: ")
                
                year = int(year_input) if year_input else datetime.date.today().year
                month = int(month_input) if month_input else datetime.date.today().month
                
                scheduler.print_monthly_calendar(year, month)
                
            except ValueError:
                print("Invalid input. Please enter valid year and month.")
        
        elif choice == '5':
            filename = input("Enter filename (default: schedule.csv): ")
            if not filename:
                filename = "schedule.csv"
            
            scheduler.generate_schedule()
            file_path = scheduler.export_to_csv(filename)
            print(f"Schedule exported to {os.path.abspath(file_path)}")
        
        elif choice == '6':
            print("Thank you for using the Task Scheduler. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
