"""Boilerplate Generator Tool - Generate project boilerplate code"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class BoilerplateGeneratorTool(MCPTool):
    PROJECT_TEMPLATES = {
        "python": {
            "fastapi": {
                "description": "FastAPI REST API project",
                "structure": [
                    "main.py",
                    "requirements.txt",
                    "app/__init__.py",
                    "app/main.py",
                    "app/config.py",
                    "app/models.py",
                    "app/schemas.py",
                    "app/crud.py",
                    "app/api/",
                    "tests/"
                ],
                "main_content": '''"""FastAPI application entry point"""
from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="API", version="1.0.0")

app.include_router(routes.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
'''
            },
            "flask": {
                "description": "Flask web application",
                "structure": [
                    "app.py",
                    "requirements.txt",
                    "config.py",
                    "models.py",
                    "templates/",
                    "static/"
                ],
                "main_content": '''"""Flask application entry point"""
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object("config.Config")


@app.route("/")
def root():
    return jsonify({"message": "App is running"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(debug=True)
'''
            },
            "cli": {
                "description": "Python CLI application with argparse",
                "structure": [
                    "main.py",
                    "requirements.txt",
                    "commands/",
                    "utils/"
                ],
                "main_content": '''"""CLI application entry point"""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("run", help="Run the application")
    subparsers.add_parser("init", help="Initialize configuration")

    args = parser.parse_args()

    if args.command == "run":
        print("Running application...")
    elif args.command == "init":
        print("Initializing...")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
            }
        },
        "javascript": {
            "express": {
                "description": "Express.js REST API",
                "structure": [
                    "package.json",
                    "src/index.js",
                    "src/routes/",
                    "src/controllers/",
                    "src/models/",
                    "src/middleware/",
                    "tests/"
                ],
                "main_content": '''const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/health", (req, res) => {
    res.json({ status: "healthy" });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
'''
            },
            "react": {
                "description": "React application",
                "structure": [
                    "package.json",
                    "src/App.jsx",
                    "src/index.js",
                    "src/components/",
                    "src/pages/",
                    "src/utils/",
                    "public/"
                ],
                "main_content": '''import React from "react";

function App() {
    return (
        <div className="app">
            <h1>React Application</h1>
        </div>
    );
}

export default App;
'''
            }
        },
        "typescript": {
            "node": {
                "description": "Node.js TypeScript project",
                "structure": [
                    "package.json",
                    "tsconfig.json",
                    "src/index.ts",
                    "src/routes/",
                    "src/controllers/",
                    "tests/"
                ],
                "main_content": '''import express, { Request, Response } from "express";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/health", (req: Request, res: Response) => {
    res.json({ status: "healthy" });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
'''
            }
        }
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="boilerplate_generator",
            description="Generates project boilerplate code for various frameworks including FastAPI, Flask, Express, React, and more. Creates complete project structure with essential files.",
            input_schema={
                "type": "object",
                "properties": {
                    "project_type": {
                        "type": "string",
                        "description": "Type of project to generate",
                        "enum": ["fastapi", "flask", "cli", "express", "react", "node"]
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Name of the project"
                    },
                    "include_tests": {
                        "type": "boolean",
                        "description": "Include test directory structure",
                        "default": True
                    },
                    "include_docker": {
                        "type": "boolean",
                        "description": "Include Docker configuration",
                        "default": False
                    }
                },
                "required": ["project_type", "project_name"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "object",
                        "description": "Generated files with path as key and content as value"
                    },
                    "structure": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "instructions": {"type": "string"}
                }
            },
            tags={"code", "generation", "boilerplate", "project", "template", "scaffold"},
            category="generators",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        project_type = params["project_type"]
        project_name = params["project_name"]
        include_tests = params.get("include_tests", True)
        include_docker = params.get("include_docker", False)

        try:
            template = self.PROJECT_TEMPLATES.get(
                params.get("language", "python"), {}
            ).get(project_type)

            if not template:
                return ToolResult(
                    tool_name="boilerplate_generator",
                    success=False,
                    error=f"Unknown project type: {project_type}",
                    execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
                )

            files = self._generate_boilerplate(
                project_name, template, include_tests, include_docker
            )

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="boilerplate_generator",
                success=True,
                data={
                    "files": files,
                    "structure": template["structure"],
                    "instructions": self._generate_instructions(project_name, project_type)
                },
                execution_time_ms=execution_time,
                metadata={"project_type": project_type, "project_name": project_name}
            )

        except Exception as e:
            return ToolResult(
                tool_name="boilerplate_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_boilerplate(
        self,
        project_name: str,
        template: Dict[str, Any],
        include_tests: bool,
        include_docker: bool
    ) -> Dict[str, str]:
        files = {}
        project_name_safe = project_name.replace("-", "_").replace(" ", "_")

        files["main.py" if "python" in template["main_content"] else "index.js"] = template["main_content"]

        if "python" in template["main_content"]:
            files["requirements.txt"] = self._generate_python_requirements(project_name)
            files["config.py"] = self._generate_python_config()
            files["models.py"] = self._generate_python_models()
        else:
            files["package.json"] = self._generate_package_json(project_name)

        if include_tests:
            if "python" in template["main_content"]:
                files["tests/__init__.py"] = ""
                files["tests/test_main.py"] = self._generate_python_test()
            else:
                files["tests/test.js"] = self._generate_js_test()

        if include_docker:
            files["Dockerfile"] = self._generate_dockerfile(project_name)
            files["docker-compose.yml"] = self._generate_docker_compose(project_name)

        return files

    def _generate_python_requirements(self, project_name: str) -> str:
        return f'''# {project_name}
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pytest>=7.0.0
httpx>=0.24.0
'''

    def _generate_python_config(self) -> str:
        return '''"""Application configuration"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
'''

    def _generate_python_models(self) -> str:
        return '''"""Database models"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''

    def _generate_python_test(self) -> str:
        return '''"""Tests for main application"""
import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
'''

    def _generate_package_json(self, project_name: str) -> str:
        return f'''{{
    "name": "{project_name}",
    "version": "1.0.0",
    "description": "{project_name} application",
    "main": "src/index.js",
    "scripts": {{
        "start": "node src/index.js",
        "dev": "nodemon src/index.js",
        "test": "jest"
    }},
    "dependencies": {{
        "express": "^4.18.0",
        "dotenv": "^16.0.0"
    }},
    "devDependencies": {{
        "nodemon": "^3.0.0",
        "jest": "^29.0.0"
    }}
}}
'''

    def _generate_js_test(self) -> str:
        return '''const request = require("supertest");
const app = require("../src/index");

describe("API Tests", () => {
    test("GET /health should return healthy status", async () => {
        const response = await request(app).get("/health");
        expect(response.status).toBe(200);
        expect(response.body.status).toBe("healthy");
    });
});
'''

    def _generate_dockerfile(self, project_name: str) -> str:
        return f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    def _generate_docker_compose(self, project_name: str) -> str:
        return f'''version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/{project_name}
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: {project_name}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
'''

    def _generate_instructions(self, project_name: str, project_type: str) -> str:
        return f'''
# {project_name}

Generated {project_type} project.

## Setup

1. Install dependencies:
   - Python: `pip install -r requirements.txt`
   - Node.js: `npm install`

2. Run the application:
   - Python: `uvicorn main:app --reload`
   - Node.js: `npm run dev`

3. Run tests:
   - Python: `pytest`
   - Node.js: `npm test`
'''
