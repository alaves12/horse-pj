FROM ubuntu:18.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Remove some useless errors which appear when installing packages with apt
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NOWARNINGS yes
ENV TERM linux

WORKDIR /app

# Install package
COPY ./requirements/apt.txt /app/
RUN rm -rf /var/lib/apt/lists/* && \
	apt-get autoclean && \
	apt-get clean && \
	apt-get update && \
	apt-get -y --no-install-recommends install software-properties-common && \
    xargs apt-get -y --no-install-recommends install < apt.txt && \
	apt-get clean && \
	rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install

# Install pyenv
ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
COPY ./.python-version /app/
RUN curl https://pyenv.run | bash && \
    eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc && \
    pyenv update && \
    cat .python-version | xargs -I{} pyenv install -v {} && \
    cat .python-version | xargs -I{} pyenv global {} && \
    pyenv rehash

# Install python packages
ENV PATH $HOME/.local/bin:$PATH
COPY ./pyproject.toml ./poetry.lock /app/
RUN eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root

# Copy local data
COPY . /app