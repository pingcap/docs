# This script aims to assign editorial and translation tasks of "Improvements" and "Bug Fixes" in release notes among technical writers evenly based on the number of release note items for each component.
# For a component with most release note items, if its count exceeds the average count by two or more, the script splits it into two parts and assign the first two writers to these parts accordingly.
# After the assignment, this script inserts the assignment info "<!--tw@xxx: xxx notes-->" as comments to the release notes file.

release_notes_file = r'/Users/userid/Documents/GitHub/docs-cn/releases/release-8.3.0.md'
ignored_lines = ['(dup):', 'note [#issue]', 'tw@', '贡献者']
tw = ["lilin90","hfxsd","Oreoxmt","qiancai"]

from collections import OrderedDict
import re

def get_task_info(release_notes_file):
    tasks = {}
    line_numbers = {}
    current_section = None
    current_component = None
    with open(release_notes_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            line = line.strip()

            # Detect section headers
            section_match = re.match(r'^## (.+)$', line)
            if section_match:
                current_section = section_match.group(1).strip()
                current_component = None
                continue

            # Detect component headers
            component_match = re.match(r'^\+ (.+)$', line)
            if component_match:
                current_component = component_match.group(1).strip()
                if current_component == "Tools":  # Ignore "Tools" component
                    current_component = None
                elif current_component:
                    key = f"{current_section} -> {current_component}"
                    if key not in tasks:
                        tasks[key] = 0
                        line_numbers[key] = i
                continue

            # Detect sub-component headers (for example, under "Tools")
            subcomponent_match = re.match(r'^\+ (.+) > (.+)$', line)
            if subcomponent_match:
                current_component = f"{subcomponent_match.group(1)} -> {subcomponent_match.group(2)}"
                if "Tools" in current_component:  # Skip "Tools"
                    current_component = None
                elif current_component:
                    key = f"{current_section} -> {current_component}"
                    if key not in tasks:
                        tasks[key] = 0
                        line_numbers[key] = i
                continue

            if current_component and line.startswith('-') and all(substring not in line for substring in ignored_lines):
                key = f"{current_section} -> {current_component}"
                tasks[key] += 1

    return tasks, line_numbers

def get_person_with_least_subtasks(assignments, tasks):
    return min(assignments, key=lambda k: sum(tasks[task] for task in assignments[k]))

def insert_assignment_info(release_notes_file, assignments, tasks, line_numbers):
    with open(release_notes_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if (most_subtasks_count - target_subtasks) >= 2 and most_subtasks_task in line_numbers: # Insert the task split info if the most_subtasks_count is split
        line_index = line_numbers[most_subtasks_task]
        comment_a = f" <!--tw@{tw[0]}: the following {tasks[f'{most_subtasks_task} - part 1']} notes-->"
        lines[line_index] = lines[line_index].rstrip() + comment_a + "\n"
        subtask_count = 0
        for i in range(line_index + 1, len(lines)):
            if lines[i].strip().startswith('-') and all(substring not in lines[i] for substring in ignored_lines):
                subtask_count += 1
            if subtask_count == tasks[f'{most_subtasks_task} - part 1']:
                comment_b = f" <!--tw@{tw[1]}: the following {tasks[f'{most_subtasks_task} - part 2']} notes-->"
                lines[i] = lines[i].rstrip() + comment_b + "\n"
                break
    else:
        pass

    for person, assigned_tasks in assignments.items():
        for task in assigned_tasks:
            if task.split(" - part")[0] == most_subtasks_task:
                if (most_subtasks_count - target_subtasks) >= 2: # Skip the task split info if the most_subtasks_count is split
                    continue
                else:
                    pass
            if task in line_numbers:
                line_index = line_numbers[task]
                if tasks[task] > 1:
                    comment = f" <!--tw@{person}: {tasks[task]} notes-->"
                else:
                    comment = f" <!--tw@{person}: {tasks[task]} note-->"
                lines[line_index] = lines[line_index].rstrip() + comment + "\n"

    with open(release_notes_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

if __name__ == "__main__":

    assignments = {person: [] for person in tw}
    raw_tasks, line_numbers = get_task_info(release_notes_file)

    print ("\nTask list:")
    for component, count in raw_tasks.items():
        if count == 1:
            print(f"{component}: {count} note")
        elif count > 1:
            print(f"{component}: {count} notes")
        else:
            pass

    tasks = OrderedDict(sorted(raw_tasks.items(), key=lambda item: item[1], reverse=True)) # Sort tasks by the number of subtasks in descending order

    total_subtasks = sum(tasks.values()) # Calculate total number of subtasks
    target_subtasks = total_subtasks / len(assignments) # Calculate the target number of subtasks per person
    target_subtasks = round(target_subtasks, 1)

    print(f"\nTotal notes: {total_subtasks}")
    print (f"Target notes per person: {target_subtasks}")

    # Find the task with the most subtasks
    most_subtasks_task = max(tasks, key=tasks.get)
    most_subtasks_count = tasks[most_subtasks_task]

    if (most_subtasks_count - target_subtasks) >= 2: # Split the task with the most subtasks if it exceeds the target subtasks by two or more
        split_point = most_subtasks_count // 2
        tasks[f"{most_subtasks_task} - part 1"] = split_point
        tasks[f"{most_subtasks_task} - part 2"] = most_subtasks_count - split_point

        # Assign the split tasks
        assignments[tw[0]].append(f"{most_subtasks_task} - part 1")
        assignments[tw[1]].append(f"{most_subtasks_task} - part 2")

        del tasks[most_subtasks_task]

        # Assign the remaining tasks
        for task, subtasks in tasks.items():
            if subtasks !=0 and task not in assignments[tw[0]] and task not in assignments[tw[1]]:
                person = get_person_with_least_subtasks(assignments, tasks)
                assignments[person].append(task)
    else:
        for task, subtasks in tasks.items():
            if subtasks != 0:
                person = get_person_with_least_subtasks(assignments, tasks)
                assignments[person].append(task)

    # Print the final assignments with tasks sorted according to raw_tasks order
    for person, assigned_tasks in assignments.items():
        # Sort assigned tasks based on the original order in raw_tasks
        sorted_assigned_tasks = sorted(assigned_tasks, key=lambda task: list(raw_tasks.keys()).index(task.split(" - part")[0]))

        print(f"\n{person}: {sum(tasks[assigned_task] for assigned_task in sorted_assigned_tasks)} notes")
        for assigned_task in sorted_assigned_tasks:
            print(f"  - {assigned_task} ({tasks[assigned_task]})")

    insert_assignment_info(release_notes_file, assignments, tasks, line_numbers)