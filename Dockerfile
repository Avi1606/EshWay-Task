FROM public.ecr.aws/x8v8d7g8/mars-base:latest

WORKDIR /app

# Copy repository source
COPY . /app/

# Install project dependencies and test tools
RUN pip install -e ".[all]" pytest pytest-cov

CMD ["bash"]