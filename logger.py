import logging

class TrafficLog:
    def __init__(self, log_file):
        self.log_file = log_file
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log_traffic(self, data):
        logging.info(f'Traffic: {data}')

    def log_rejected_traffic(self, data):
        logging.warning(f'Rejected Access Attempt: {data}')
