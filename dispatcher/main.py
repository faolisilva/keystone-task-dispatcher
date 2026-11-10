import time
from dispatcher.core import get_connection, init_db

def execute_task(task_id, task_data):
    # This is where the actual business logic would go.
    # For now, we just print and sleep to simulate heavy lifting.
    print(f"-> Worker picked up task {task_id}: {task_data}")
    time.sleep(2) 
    print(f"<- Worker completed task {task_id}")

def start_dispatcher():
    init_db()
    
    # Infinite polling loop. 
    # TODO: Add a way to gracefully shut this down (SIGTERM handler).
    while True:
        with get_connection() as conn:
            # Naive grab: just get the first thing that is queued.
            # We know this is racy if multiple workers run at once, but we only run 1 right now.
            row = conn.execute(
                "SELECT * FROM task_queue WHERE state = 'queued' LIMIT 1"
            ).fetchone()
            
            if row:
                t_id = row['id']
                t_data = row['data']
                
                # Flip state to 'running' before doing the work so we don't pick it up again.
                # BUG: If the process dies here, this task is stuck in 'running' forever.
                conn.execute("UPDATE task_queue SET state = 'running' WHERE id = ?", (t_id,))
                conn.commit()
                
                try:
                    execute_task(t_id, t_data)
                    # Mark as completed only if the work actually finished
                    conn.execute("UPDATE task_queue SET state = 'completed' WHERE id = ?", (t_id,))
                    conn.commit()
                except Exception as err:
                    print(f"Task {t_id} blew up: {err}")
                    # TODO: Add retry logic. Right now a single failure just drops it.
                    conn.execute("UPDATE task_queue SET state = 'error' WHERE id = ?", (t_id,))
                    conn.commit()
            else:
                # Nothing to do, wait a bit to avoid pegging the CPU
                time.sleep(1)

if __name__ == "__main__":
    start_dispatcher()
