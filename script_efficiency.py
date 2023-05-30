import time
import os
import psutil
import logging

# Function to get current process info
def get_process_info():
    pid = os.getpid()
    py = psutil.Process(pid)
    memory_use = py.memory_info()[0] / 2. ** 30  # memory use in GB...
    return f"memory GB:{memory_use}"

# Function to test the efficiency of a given function
def test_efficiency(func, params, num_of_checkpoints):
    # Set up logging
    log_filename = f"{func.__name__}_log.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')

    # Start times
    start_time_wall = time.time()
    start_time_cpu = time.process_time()
    logging.info(f"Start time (wall): {start_time_wall}")
    logging.info(f"Start time (CPU): {start_time_cpu}")
    logging.info(f"Start {get_process_info()}")

    # Run function and record checkpoints
    for i in range(num_of_checkpoints):
        func(**params)

        # Checkpoint
        checkpoint_wall = time.time()
        checkpoint_cpu = time.process_time()
        logging.info(f"Checkpoint {i+1} (wall): {checkpoint_wall}, elapsed time (wall): {checkpoint_wall - start_time_wall}")
        logging.info(f"Checkpoint {i+1} (CPU): {checkpoint_cpu}, elapsed time (CPU): {checkpoint_cpu - start_time_cpu}")
        logging.info(f"Checkpoint {i+1} {get_process_info()}")

    # End times
    end_time_wall = time.time()
    end_time_cpu = time.process_time()
    logging.info(f"End time (wall): {end_time_wall}, total elapsed time (wall): {end_time_wall - start_time_wall}")
    logging.info(f"End time (CPU): {end_time_cpu}, total elapsed time (CPU): {end_time_cpu - start_time_cpu}")
    logging.info(f"End {get_process_info()}")

