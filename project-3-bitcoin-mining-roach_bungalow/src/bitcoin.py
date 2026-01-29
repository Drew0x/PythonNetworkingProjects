'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student(s): Andrew Stephens, Oliver Yang
Description: Project 3 - Bitcoin Simulation
'''

import time
import sys
import stomp
import json
import threading
import hashlib
import random

# TODO: change STUDENT_ID, BROKER_USER, and BROKER_PASSWD
STUDENT_ID      = 'Roach'
TASKS_TOPIC     = f'/topic/bitcoin/{STUDENT_ID}_tasks'
SOLUTIONS_TOPIC = f'/topic/bitcoin/{STUDENT_ID}_solutions'
BROKER_ENDPOINT = 'cs3700c.msudenver.edu'
BROKER_PORT     = 61613
BROKER_USER     = 'admin'
BROKER_PASSWD   = 'admin'

# PROPER shared variable
solution_found = None     # either None OR a full solution dict
semaphore = threading.Semaphore(1)


# Load tasks-
def load_tasks(file_name):
    tasks = []
    with open(file_name, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            left, zeros_raw = line.split(',')
            data = [int(b) for b in left.split()]
            zeros = int(zeros_raw) * 8       # convert 1→8 bits, 2→16 bits, etc.
            tasks.append({'data': data, 'zeros': zeros})
    print(f'{len(tasks)} tasks loaded!')
    return tasks


# Save solution
def save_solution(file_name, solution):
    with open(file_name, 'at') as f:
        for b in solution['data']:
            f.write(f'{b} ')
        f.write(f", {solution['zeros']//8}, ")
        for b in solution['nonce']:
            f.write(f'{b} ')
        f.write('\n')


# Check digest for leading-zero BYTES
def is_solved(task, digest):
    zero_bytes = task['zeros'] // 8
    return all(digest[i] == 0 for i in range(zero_bytes))


# Mining function
def mine(conn, id, task):
    global solution_found

    print(f"-> Miner {id} working on task (zeros={task['zeros']})...")

    while True:
        with semaphore:
            if solution_found is not None:
                return  # Some miner already solved this task

        # generate 4-byte nonce
        nonce = random.getrandbits(32).to_bytes(4, 'big')

        h = hashlib.md5()
        h.update(bytes(task['data']) + nonce)
        digest = h.digest()

        if is_solved(task, digest):
            # Found it!
            with semaphore:
                if solution_found is None:  # claim it
                    solution_found = {
                        'data': task['data'],
                        'zeros': task['zeros'] // 8,
                        'nonce': list(nonce)
                    }
                    conn.send(body=json.dumps(solution_found),
                              destination=SOLUTIONS_TOPIC)
                    print(f"[{id}] FOUND SOLUTION and announced!")
            return


# TASKS Listener (only for miners)
class TasksListener(stomp.ConnectionListener):

    def __init__(self, conn, id):
        super().__init__()
        self.conn = conn
        self.id = id

    def on_message(self, frame):
        global solution_found
        self.conn.ack(frame.headers['message-id'], frame.headers['subscription'])
        task = json.loads(frame.body)

        print(f"[{self.id}] Received task: zeros={task['zeros']}")

        # Reset the shared solution
        with semaphore:
            solution_found = None

        # Start mining thread
        t = threading.Thread(target=mine, args=(self.conn, self.id, task))
        t.start()



# SOLUTIONS Listener (both roles)
class SolutionsListener(stomp.ConnectionListener):

    def __init__(self, conn, role):
        super().__init__()
        self.conn = conn
        self.role = role

    def on_message(self, frame):
        global solution_found
        self.conn.ack(frame.headers['message-id'], frame.headers['subscription'])
        sol = json.loads(frame.body)

        print(f"[{self.role}] Solution received: {sol}")

        with semaphore:
            solution_found = sol

        save_solution('data/solutions.txt', sol)

        # If main, send next task
        if self.role == 'm' and tasks:
            next_task = tasks.pop(0)
            print(f"[MAIN] Sending next task: zeros={next_task['zeros']}")
            self.conn.send(body=json.dumps(next_task),
                           destination=TASKS_TOPIC)



# MAIN
if __name__ == '__main__':

    if len(sys.argv) not in [2, 3]:
        print(f'Use {sys.argv[0]} m|b id')
        sys.exit(1)

    role = sys.argv[1].lower()
    if role not in ['m', 'b']:
        print("Unknown role!")
        sys.exit(1)

    id = 'main' if role == 'm' else f'miner #{sys.argv[2]}'
    print(f"Running as {id}")

    conn_tasks = stomp.Connection([(BROKER_ENDPOINT, BROKER_PORT)])
    conn_solutions = stomp.Connection([(BROKER_ENDPOINT, BROKER_PORT)])

    print("Connecting to broker...")
    conn_tasks.connect(BROKER_USER, BROKER_PASSWD, wait=True)
    conn_solutions.connect(BROKER_USER, BROKER_PASSWD, wait=True)
    print("Connected!")

    # Solutions listener always active
    solutions_listener = SolutionsListener(conn_solutions, role)
    conn_solutions.set_listener('', solutions_listener)
    conn_solutions.subscribe(destination=SOLUTIONS_TOPIC,
                             id=2, ack='client-individual')

    # MAIN role
    if role == 'm':
        tasks = load_tasks('data/input.txt')
        first = tasks.pop(0)
        print(f"[MAIN] Sending first task...")
        conn_tasks.send(body=json.dumps(first),
                        destination=TASKS_TOPIC)

    # MINER role
    if role == 'b':
        tasks_listener = TasksListener(conn_tasks, id)
        conn_tasks.set_listener('', tasks_listener)
        conn_tasks.subscribe(destination=TASKS_TOPIC,
                             id=1, ack='client-individual')

    while True:
        time.sleep(1)