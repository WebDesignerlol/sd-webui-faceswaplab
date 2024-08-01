import subprocess
import os
import sys
import importlib.metadata as metadata
from packaging import version as pv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pip_install(*args):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", *args], check=True)
        logging.info(f"Successfully installed: {' '.join(args)}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install: {' '.join(args)}")
        raise e

def pip_uninstall(*args):
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", *args], check=True)
        logging.info(f"Successfully uninstalled: {' '.join(args)}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to uninstall: {' '.join(args)}")
        raise e

def is_installed(package: str) -> bool:
    package_name = package.split("==")[0].split(">=")[0].strip()
    try:
        installed_version = metadata.version(package_name)
        installed_version = pv.parse(installed_version)
    except metadata.PackageNotFoundError:
        return False

    if "==" in package:
        required_version = pv.parse(package.split("==")[1])
        return installed_version == required_version
    elif ">=" in package:
        required_version = pv.parse(package.split(">=")[1])
        return installed_version >= required_version
    else:
        return True  # Assume it's installed if no specific version check needed

def check_install() -> None:
    use_gpu = True

    if use_gpu and sys.platform != "darwin":
        logging.info("Faceswaplab: Use GPU requirements")
        req_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "requirements-gpu.txt"
        )
    else:
        logging.info("Faceswaplab: Use CPU requirements")
        req_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "requirements.txt"
        )

    logging.info("Checking faceswaplab requirements")
    with open(req_file) as file:
        for package in file:
            try:
                package = package.strip()

                if not is_installed(package):
                    logging.info(f"Install {package}")
                    pip_install(package)

            except Exception as e:
                logging.error(f"Failed to install {package}: {e}")
                logging.error(
                    f"Warning: Failed to install {package}, faceswaplab may not work. Try to restart the server or install dependencies manually."
                )
                raise e

try:
    check_install()
except Exception as e:
    logging.error("FaceswapLab install failed:", e)
    logging.error(
        "You can try to install dependencies manually by activating the virtual environment and installing requirements.txt or requirements-gpu.txt"
    )
