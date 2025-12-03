FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install the project in development mode
COPY pyproject.toml .
COPY src/ ./src/

# Install the project in development mode (-e means editable)
RUN pip install --no-cache-dir -e ".[mqtt_logger,shared]"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Make sure scripts in .local are usable
ENV DB_PATH=/app/data/app.db

# Verify installation
RUN python -c "import shared.config; print('Shared imports work!')"

# Set ownership
RUN chown -R appuser:appuser /app


USER appuser
RUN chmod -R 755 /app
RUN mkdir -p /app/data
RUN chmod -R 770 /app/data

CMD ["python", "-m", "src.mqtt_logger.main"]