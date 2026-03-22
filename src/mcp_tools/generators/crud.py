"""CRUD Generator Tool - Generate CRUD (Create, Read, Update, Delete) operations"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CRUDGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="crud_generator",
            description="Generates CRUD (Create, Read, Update, Delete) operations for database models. Supports SQLAlchemy, Django ORM, Prisma, and other ORMs.",
            input_schema={
                "type": "object",
                "properties": {
                    "model_definition": {
                        "type": "string",
                        "description": "Model definition in YAML, JSON, or natural language"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "framework": {
                        "type": "string",
                        "description": "ORM or database framework",
                        "enum": ["sqlalchemy", "django", "prisma", "sequelize"]
                    },
                    "include_api": {
                        "type": "boolean",
                        "description": "Generate REST API endpoints",
                        "default": True
                    }
                },
                "required": ["model_definition", "language", "framework"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "model_code": {"type": "string"},
                    "crud_code": {"type": "string"},
                    "api_code": {"type": "string"},
                    "fields": {"type": "array"}
                }
            },
            tags={"code", "generation", "crud", "database", "api", "orm"},
            category="generators",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        model_definition = params["model_definition"]
        language = params["language"]
        framework = params["framework"]
        include_api = params.get("include_api", True)

        try:
            fields = self._parse_model_definition(model_definition)

            if framework == "sqlalchemy":
                model_code = self._generate_sqlalchemy_model(fields)
                crud_code = self._generate_sqlalchemy_crud(fields)
            elif framework == "django":
                model_code = self._generate_django_model(fields)
                crud_code = self._generate_django_crud(fields)
            elif framework == "prisma":
                model_code = self._generate_prisma_model(fields)
                crud_code = self._generate_prisma_crud(fields)
            else:
                model_code = crud_code = "// Unsupported framework"

            api_code = ""
            if include_api:
                api_code = self._generate_api_code(fields, language, framework)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="crud_generator",
                success=True,
                data={
                    "model_code": model_code,
                    "crud_code": crud_code,
                    "api_code": api_code,
                    "fields": [f["name"] for f in fields]
                },
                execution_time_ms=execution_time,
                metadata={"language": language, "framework": framework}
            )

        except Exception as e:
            return ToolResult(
                tool_name="crud_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _parse_model_definition(self, definition: str) -> List[Dict[str, Any]]:
        fields = []

        import re
        field_pattern = r'(\w+):\s*(\w+)(?:\((\d+)\))?(?:\s*=\s*(.+))?'

        for match in re.finditer(field_pattern, definition):
            field_name = match.group(1)
            field_type = match.group(2)
            field_length = match.group(3)
            field_default = match.group(4)

            type_mapping = {
                "str": "String", "string": "String",
                "int": "Integer", "integer": "Integer",
                "float": "Float", "double": "Float",
                "bool": "Boolean", "boolean": "Boolean",
                "date": "Date", "datetime": "DateTime",
                "text": "Text", "json": "JSON"
            }

            fields.append({
                "name": field_name,
                "type": type_mapping.get(field_type.lower(), "String"),
                "length": int(field_length) if field_length else None,
                "default": field_default.strip() if field_default else None,
                "nullable": field_default is None and field_name.lower() != "id"
            })

        if not fields:
            for line in definition.split('\n'):
                if ':' in line:
                    parts = line.split(':')
                    name = parts[0].strip()
                    type_part = parts[1].strip().split()[0]
                    fields.append({
                        "name": name,
                        "type": type_mapping.get(type_part.lower(), "String"),
                        "length": None,
                        "default": None,
                        "nullable": name.lower() != "id"
                    })

        return fields

    def _generate_sqlalchemy_model(self, fields: List[Dict[str, Any]]) -> str:
        model_name = "Item"
        lines = [
            "from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text",
            "from sqlalchemy.ext.declarative import declarative_base",
            "from datetime import datetime",
            "",
            "Base = declarative_base()",
            "",
            f"class {model_name}(Base):",
            '    __tablename__ = "items"',
            "",
            "    id = Column(Integer, primary_key=True, index=True)"
        ]

        for field in fields[1:]:
            col_type = field["type"]
            if field["length"]:
                col_type = f"{col_type}({field['length']})"

            nullable_str = "" if field["nullable"] else ", nullable=False"
            default_str = f", default={field['default']}" if field["default"] else ""

            lines.append(f"    {field['name']} = Column({col_type}{nullable_str}{default_str})")

        lines.append("    created_at = Column(DateTime, default=datetime.utcnow)")
        lines.append("    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)")

        return "\n".join(lines)

    def _generate_sqlalchemy_crud(self, fields: List[Dict[str, Any]]) -> str:
        model_name = "Item"
        pk_name = "id"

        return f'''
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

def create_{model_name.lower()}(db: Session, {", ".join(f"{f['name']}" for f in fields[1:])}) -> {model_name}:
    """Create a new {model_name}"""
    db_{model_name.lower()} = {model_name}(
        {", ".join(f"{f['name']}={f['name']}" for f in fields[1:])}
    )
    db.add(db_{model_name.lower()})
    db.commit()
    db.refresh(db_{model_name.lower()})
    return db_{model_name.lower()}


def get_{model_name.lower()}(db: Session, {pk_name}: int) -> Optional[{model_name}]:
    """Get {model_name} by ID"""
    return db.query({model_name}).filter({model_name}.{pk_name} == {pk_name}).first()


def get_all_{model_name.lower()}s(db: Session, skip: int = 0, limit: int = 100) -> List[{model_name}]:
    """Get all {model_name}s with pagination"""
    return db.query({model_name}).offset(skip).limit(limit).all()


def update_{model_name.lower()}(db: Session, {pk_name}: int, {", ".join(f"{f['name']}" for f in fields[1:])}) -> Optional[{model_name}]:
    """Update an existing {model_name}"""
    db_{model_name.lower()} = db.query({model_name}).filter({model_name}.{pk_name} == {pk_name}).first()
    if db_{model_name.lower()}:
        for field in fields[1:]:
            setattr(db_{model_name.lower()}, field['name'], {field['name']})
        db.commit()
        db.refresh(db_{model_name.lower()})
    return db_{model_name.lower()}


def delete_{model_name.lower()}(db: Session, {pk_name}: int) -> bool:
    """Delete a {model_name}"""
    db_{model_name.lower()} = db.query({model_name}).filter({model_name}.{pk_name} == {pk_name}).first()
    if db_{model_name.lower()}:
        db.delete(db_{model_name.lower()})
        db.commit()
        return True
    return False
'''

    def _generate_django_model(self, fields: List[Dict[str, Any]]) -> str:
        lines = [
            "from django.db import models",
            "",
            f"class {fields[0]['name'].title()}(models.Model):" if fields else "class Item(models.Model):"
        ]

        for field in fields[1:]:
            field_type = field["type"]
            field_name = field["name"]
            nullable_str = "blank=True, null=True" if field["nullable"] else ""
            default_str = f", default={field['default']}" if field["default"] else ""

            if field["type"] == "String":
                if field["length"]:
                    lines.append(f"    {field_name} = models.CharField(max_length={field['length']}{', ' + nullable_str if nullable_str else ''}{default_str})")
                else:
                    lines.append(f"    {field_name} = models.CharField(max_length=255{', ' + nullable_str if nullable_str else ''}{default_str})")
            elif field["type"] == "Text":
                lines.append(f"    {field_name} = models.TextField({nullable_str}{default_str})")
            elif field["type"] == "Integer":
                lines.append(f"    {field_name} = models.IntegerField({nullable_str}{default_str})")
            elif field["type"] == "Boolean":
                lines.append(f"    {field_name} = models.BooleanField(default=False)")
            elif field["type"] == "DateTime":
                lines.append(f"    {field_name} = models.DateTimeField(auto_now_add=True)")

        lines.append("")
        lines.append("    def __str__(self):")
        lines.append(f'        return f"{{self.{fields[1]['name'] if len(fields) > 1 else 'id'}}}\"')

        return "\n".join(lines)

    def _generate_django_crud(self, fields: List[Dict[str, Any]]) -> str:
        model_name = fields[0]['name'].title() if fields else 'Item'

        return f'''
from .models import {model_name}

def create_{model_name.lower()}({", ".join(f"{f['name']}" for f in fields[1:])}):
    """Create a new {model_name}"""
    return {model_name}.objects.create({", ".join(f"{f['name']}={f['name']}" for f in fields[1:])})


def get_{model_name.lower()}(id):
    """Get {model_name} by ID"""
    return {model_name}.objects.get(id=id)


def get_all_{model_name.lower()}s():
    """Get all {model_name}s"""
    return {model_name}.objects.all()


def update_{model_name.lower()}(id, {", ".join(f"{f['name']}" for f in fields[1:])}):
    """Update {model_name}"""
    obj = {model_name}.objects.get(id=id)
    {", ".join(f"obj.{f['name']} = {f['name']}" for f in fields[1:])}
    obj.save()
    return obj


def delete_{model_name.lower()}(id):
    """Delete {model_name}"""
    obj = {model_name}.objects.get(id=id)
    obj.delete()
'''

    def _generate_prisma_model(self, fields: List[Dict[str, Any]]) -> str:
        model_name = fields[0]['name'].title() if fields else 'Item'

        lines = [
            "generator client {",
            '    provider = "prisma-client-js"',
            "}",
            "",
            "datasource db {",
            '    provider = "postgresql"',
            '    url      = env("DATABASE_URL")',
            "}",
            "",
            f"model {model_name} {{",
            "    id        Int      @id @default(autoincrement())"
        ]

        for field in fields[1:]:
            field_name = field["name"]
            field_type = field["type"]

            type_mapping = {
                "String": "String",
                "Integer": "Int",
                "Float": "Float",
                "Boolean": "Boolean",
                "DateTime": "DateTime",
                "Text": "String"
            }

            prisma_type = type_mapping.get(field_type, "String")

            if field["nullable"]:
                lines.append(f"    {field_name}  {prisma_type}?")
            else:
                lines.append(f"    {field_name}  {prisma_type}")

        lines.append("    createdAt DateTime @default(now())")
        lines.append("    updatedAt DateTime @updatedAt")
        lines.append("}")

        return "\n".join(lines)

    def _generate_prisma_crud(self, fields: List[Dict[str, Any]]) -> str:
        model_name = fields[0]['name'].title() if fields else 'Item'

        return f'''
import {{ PrismaClient }} from '@prisma/client'
const prisma = new PrismaClient()

async function create{model_name}(data) {{
    return await prisma.{model_name.lower()}.create({{ data }})
}}

async function get{model_name}(id) {{
    return await prisma.{model_name.lower()}.findUnique({{ where: {{ id }} }})
}}

async function getAll{model_name}s(skip = 0, take = 100) {{
    return await prisma.{model_name.lower()}.findMany({{ skip, take }})
}}

async function update{model_name}(id, data) {{
    return await prisma.{model_name.lower()}.update({{ where: {{ id }}, data }})
}}

async function delete{model_name}(id) {{
    return await prisma.{model_name.lower()}.delete({{ where: {{ id }} }})
}}
'''

    def _generate_api_code(self, fields: List[Dict[str, Any]], language: str, framework: str) -> str:
        if language == "python":
            return self._generate_fastapi_crud(fields)
        elif language in ("javascript", "typescript"):
            return self._generate_express_crud(fields)

        return ""

    def _generate_fastapi_crud(self, fields: List[Dict[str, Any]]) -> str:
        model_name = "Item"

        return f'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=schemas.{model_name})
def create_item(item: schemas.{model_name}Create, db: Session = Depends(get_db)):
    return crud.create_{model_name.lower()}(db, item)


@router.get("/{{item_id}}", response_model=schemas.{model_name})
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_{model_name.lower()}(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/", response_model=List[schemas.{model_name}])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_{model_name.lower()}s(db, skip=skip, limit=limit)


@router.put("/{{item_id}}", response_model=schemas.{model_name})
def update_item(item_id: int, item: schemas.{model_name}Update, db: Session = Depends(get_db)):
    return crud.update_{model_name.lower()}(db, item_id, item)


@router.delete("/{{item_id}}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_{model_name.lower()}(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {{"message": "Deleted successfully"}}
'''

    def _generate_express_crud(self, fields: List[Dict[str, Any]]) -> str:
        return '''
const express = require("express");
const router = express.Router();

let items = [];
let idCounter = 1;

router.post("/", (req, res) => {
    const item = { id: idCounter++, ...req.body };
    items.push(item);
    res.status(201).json(item);
});

router.get("/", (req, res) => {
    const { skip = 0, limit = 100 } = req.query;
    res.json(items.slice(Number(skip), Number(skip) + Number(limit)));
});

router.get("/:id", (req, res) => {
    const item = items.find(i => i.id === Number(req.params.id));
    if (!item) return res.status(404).json({ error: "Item not found" });
    res.json(item);
});

router.put("/:id", (req, res) => {
    const index = items.findIndex(i => i.id === Number(req.params.id));
    if (index === -1) return res.status(404).json({ error: "Item not found" });
    items[index] = { ...items[index], ...req.body };
    res.json(items[index]);
});

router.delete("/:id", (req, res) => {
    const index = items.findIndex(i => i.id === Number(req.params.id));
    if (index === -1) return res.status(404).json({ error: "Item not found" });
    items.splice(index, 1);
    res.json({ message: "Deleted successfully" });
});

module.exports = router;
'''
