import time
import threading
import matplotlib.pyplot as plt
from neulog import neulog

# Initialize empty lists for sensor data
respiration_values = []
pulse_values = []
time_values_r = []
time_values_p = []

def fetch_data():
    while True:
        start_time = time.time()
        
        # Fetch respiration data (replace with actual logic)
        # req_start = time.time()
        respiration_value = float(device.getSensorsData('Respiration', 1))
        # print(f"Respiration: {respiration_value} after {time.time() - req_start}")
        respiration_values.append(respiration_value)
        time_values_r.append(time.time())

        # Fetch pulse data (replace with actual logic)
        # req_start = time.time()
        pulse_value = float(device.getSensorsData('Pulse', 1))
        # print(f"Pulse: {pulse_value} after {time.time() - req_start}")
        pulse_values.append(pulse_value)
        time_values_p.append(time.time())

        # Keep only the last value
        if len(time_values_r) > 100:
            time_values_r.pop(0)
            respiration_values.pop(0)  # Remove oldest respiration data
        if len(time_values_p) > 100:
            time_values_p.pop(0)
            pulse_values.pop(0)  # Remove oldest pulse data
            
        diff = time.time() - start_time
        if diff < update_period:
            time.sleep(diff)
            # print(f"Updatet time fetch_data: {diff}")
        else:
            print(f"TIME_DELAY fetch_data: {diff}")

# Function to update plot in the main thread
def update_plot():
    # Initialize plot lines with empty data
    respiration_line, = ax.plot([], [], marker="o", color="b", label="Respiration")
    pulse_line, = ax2.plot([], [], marker="x", color="r", label="Pulse")

    while True:
        start_time = time.time()
        # Update respiration data line
        respiration_line.set_data(time_values_r, respiration_values)

        # Update pulse data line
        pulse_line.set_data(time_values_p, pulse_values)

        # Update plot
        ax.relim()
        ax.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()

        diff = time.time() - start_time
        if diff < update_period:
            time.sleep(diff)
            # print(f"Updatet time plot: {diff}")
        else:
            print(f"TIME_DELAY plot: {diff}")

if __name__ == '__main__':
    update_period = 0.1 # seconds
    device = neulog.Device(port="COM11")
    res_connect = device.connect()
    if not res_connect:
        print("Connection failed")
        exit()

    # Plot real-time data
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.set_ylabel("Respiration", color="b")
    ax2.set_ylabel("Pulse Value", color="r")
    ax.tick_params(axis="y", labelcolor="b")
    ax2.tick_params(axis="y", labelcolor="r")
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    
    # Start background threads
    timerThread = threading.Thread(target=fetch_data)
    timerThread.daemon = True
    timerThread.start()

    plotThread = threading.Thread(target=update_plot)
    plotThread.daemon = True
    plotThread.start()

    plt.show()