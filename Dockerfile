FROM python:3.12 as python-base

# Make a new directory and set it as work dir
RUN mkdir /backend
WORKDIR /backend

# Copy all files
COPY . .

#COPY pyproject.toml .
RUN pip install -e .

# Make scripts executable
RUN chmod a+x docker/*.sh
