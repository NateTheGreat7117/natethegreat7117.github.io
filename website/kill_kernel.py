import os
import signal

# Function to restart the kernel
def restart_kernel():
    os.kill(os.getpid(), signal.SIGINT)

# Call the function to restart the kernel
restart_kernel()