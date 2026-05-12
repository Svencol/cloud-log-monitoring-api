# Cloud Log Monitoring API

A small cloud engineering project that simulates log ingestion, health checks, and alert detection for application reliability.

## Overview

This project is a Dockerized FastAPI service that accepts logs from services, stores them in memory, exposes a health check endpoint, and detects a basic high-error-rate alert condition.

I built this project to practice cloud engineering fundamentals: API deployment, containerization, health checks, cloud runtime configuration, and reliability thinking.

## Architecture

Client → FastAPI API → In-memory log store → Alert detection

## Features

- REST API built with FastAPI
- Log ingestion endpoint
- Health check endpoint
- Basic alert detection
- Dockerized application
- Ready for deployment to a cloud container runtime

## Endpoints

### GET /

Returns basic project information.

### GET /health

Returns service health and current log count.

### POST /logs

Ingests a log entry.

Example request:

```json
{
  "service": "payment-api",
  "level": "ERROR",
  "message": "Database timeout"
}
