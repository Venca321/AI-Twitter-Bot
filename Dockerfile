
FROM python:3.11.8 as base

WORKDIR /app

# Python requirements
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Firefox
RUN wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
RUN echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
RUN echo 'Package: * Pin: origin packages.mozilla.org Pin-Priority: 1000' | tee /etc/apt/preferences.d/mozilla 
RUN apt-get update && apt-get install firefox -y

# Install selenium
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
RUN mkdir /opt/geckodriver && tar -xvf geckodriver-v0.34.0-linux64.tar.gz -C /opt/geckodriver
RUN echo 'export PATH="/opt/geckodriver:$PATH"' >> ~/.bashrc && rm geckodriver-v0.34.0-linux64.tar.gz

COPY . .

CMD ["python3", "-u", "main.py"]
