# VAMU AI Service - Project Summary

## What We Built

A Python FastAPI microservice providing AI-powered features for the VAMU event platform:
- **Venue suggestions** using Google Places API
- **Item suggestions** using Groq LLM API

## Technology Stack
- Language: Python 3.11+
- Framework: FastAPI
- HTTP Client: httpx
- Validation: Pydantic
- APIs: Google Places, Groq LLM
- Deployment: Docker

## Architecture Pattern
Feature-Based Clean Architecture with 4 layers

## Status
✅ Two features implemented and tested:
- WHERE endpoint - Venue suggestions
- WISHLIST endpoint - Item suggestions

## Current Endpoints
- POST `/api/v1/inspiration/where` - Venue suggestions
- POST `/api/v1/inspiration/wishlist` - Item suggestions

For detailed information, see README.md
