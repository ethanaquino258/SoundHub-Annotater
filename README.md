# SoundHub-Annotater

**Instructions**
1. install [Python](https://www.python.org/downloads/)
    - be sure to check the box that says Add Python to PATH during installation
2. install [pip](https://pip.pypa.io/en/stable/installation/)
3. Clone the repository (if you have Git installed)
    - open your terminal/command prompt and run:
    - `git clone https://github.com/ethanaquino258/SoundHub-Annotater.git`
    - or download the zip here
        - click **Code > Download ZIP**
4. Set up virtual environment (recommended)
    - A virtual environment isolates your project’s dependencies, ensuring the app runs smoothly and doesn't conflict with other Python projects you may have.
    - create a virtual environment by running:
        - `python -m venv soundhub-annotater`
    - activate the virtual environment
        - On Windows:
            - `.\venv\Scripts\activate.bat`
        - On macOS/Linux:
            - `source venv/bin/activate`
5. Install dependencies
    - run the following command
        - `pip install -r requirements.txt`
    - if you see errors or have trouble installing the packages, make sure that you have the latest version of pip:
        - `python -m pip install --upgrade pip`
    - if you don’t have a requirements.txt file, you can manually install the required dependencies using:
        - `pip install PyQt5 matplotlib librosa sounddevice`
6. Run it
    - enter the following command and wait for the GUI to appear
        - `python main.py`