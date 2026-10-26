import os
import sys
import logging

logging_str="[ %(levelname)s: %(module)s: %(message)s]"

log_dir="logs"
filepath=os.path.join(log_dir,"logging.log")
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger=logging.getLogger("warranty_claim_logger")