"""Mock Data Generator Tool - Generate mock data for testing"""

import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class MockDataGeneratorTool(MCPTool):
    DATA_TYPES = {
        "first_name": lambda: random.choice(["John", "Jane", "Bob", "Alice", "Charlie", "Diana", "Edward", "Fiona", "George", "Helen"]),
        "last_name": lambda: random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]),
        "email": lambda: f"{random.choice(['john', 'jane', 'bob', 'alice'])}.{random.choice(['smith', 'jones', 'brown'])}@example.com",
        "phone": lambda: f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "address": lambda: f"{random.randint(1,9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln'])}",
        "city": lambda: random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]),
        "state": lambda: random.choice(["NY", "CA", "TX", "FL", "IL", "PA", "OH", "GA"]),
        "zip_code": lambda: f"{random.randint(10000, 99999)}",
        "country": lambda: random.choice(["United States", "Canada", "United Kingdom", "Germany", "France"]),
        "company": lambda: random.choice(["Acme Corp", "Globex", "Initech", "Umbrella", "Stark Industries", "Wayne Enterprises"]),
        "job_title": lambda: random.choice(["Software Engineer", "Product Manager", "Designer", "Data Analyst", "DevOps Engineer"]),
        "username": lambda: f"{random.choice(['user', 'admin', 'test'])}{random.randint(1, 9999)}",
        "password": lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
        "url": lambda: f"https://www.example{random.randint(1,100)}.com",
        "ipv4": lambda: f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "ipv6": lambda: "::".join([f"{random.randint(0,65535):x}" for _ in range(4)]),
        "credit_card": lambda: f"{random.randint(4000,4999)}-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "currency": lambda: random.choice(["USD", "EUR", "GBP", "JPY", "CNY"]),
        "amount": lambda: round(random.uniform(1.00, 10000.00), 2),
        "date": lambda: (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
        "datetime": lambda: (datetime.now() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))).isoformat(),
        "timestamp": lambda: int((datetime.now() - timedelta(days=random.randint(0, 365))).timestamp()),
        "boolean": lambda: random.choice([True, False]),
        "integer": lambda: random.randint(1, 1000),
        "float": lambda: round(random.uniform(0.0, 1000.0), 2),
        "uuid": lambda: str(random.randint(10**35, 10**36-1)),
        "hex_color": lambda: f"#{random.randint(0, 0xFFFFFF):06x}",
        "paragraph": lambda: " ".join(["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit."]),
        "article_title": lambda: random.choice(["Breaking News:", "Analysis:", "Review:", "Guide:"]) + " " + random.choice(["Python Tips", "JavaScript Trends", "AI Advances", "Cloud Computing"]),
        "product_name": lambda: random.choice(["Laptop", "Phone", "Tablet", "Watch", "Headphones"]) + " " + random.choice(["Pro", "Plus", "Max", "Ultra", "Mini"]),
        "price": lambda: round(random.uniform(9.99, 999.99), 2),
        "sku": lambda: "".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        "order_id": lambda: f"ORD-{random.randint(100000, 999999)}",
        "status": lambda: random.choice(["pending", "processing", "shipped", "delivered", "cancelled"]),
        "image_url": lambda: f"https://picsum.photos/{random.randint(200,800)}/{random.randint(200,800)}",
        "avatar_url": lambda: f"https://api.dicebear.com/7.x/avataaars/svg?seed={random.randint(1,1000)}",
        "description": lambda: "Product description with details about features and specifications.",
        "latitude": lambda: round(random.uniform(-90, 90), 6),
        "longitude": lambda: round(random.uniform(-180, 180), 6),
        "coordinates": lambda: f"{round(random.uniform(-90, 90), 6)}, {round(random.uniform(-180, 180), 6)}",
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mock_data_generator",
            description="Generates realistic mock data for testing and development. Supports various data types including names, emails, addresses, companies, and more.",
            input_schema={
                "type": "object",
                "properties": {
                    "schema": {
                        "type": "object",
                        "description": "Schema defining fields and types",
                        "properties": {
                            "fields": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string"},
                                        "format": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of records to generate",
                        "default": 10
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format",
                        "enum": ["json", "python", "typescript", "csv"]
                    }
                },
                "required": ["schema"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "data": {"type": "array", "description": "Generated mock data records"},
                    "count": {"type": "integer"},
                    "format": {"type": "string"}
                }
            },
            tags={"code", "generation", "mock", "testing", "data", "faker"},
            category="generators",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        schema = params["schema"]
        count = params.get("count", 10)
        output_format = params.get("format", "json")

        try:
            fields = schema.get("fields", [])
            data = self._generate_mock_data(fields, count)

            formatted_data = self._format_data(data, output_format)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="mock_data_generator",
                success=True,
                data={
                    "data": formatted_data,
                    "count": count,
                    "format": output_format
                },
                execution_time_ms=execution_time,
                metadata={"count": count, "format": output_format}
            )

        except Exception as e:
            return ToolResult(
                tool_name="mock_data_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_mock_data(self, fields: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        results = []

        for _ in range(count):
            record = {}
            for field in fields:
                field_name = field["name"]
                field_type = field.get("type", "string")
                field_format = field.get("format")

                if field_format and field_format in self.DATA_TYPES:
                    record[field_name] = self.DATA_TYPES[field_format]()
                elif field_type in self.DATA_TYPES:
                    record[field_name] = self.DATA_TYPES[field_type]()
                else:
                    record[field_name] = self._generate_based_on_name(field_name)

            results.append(record)

        return results

    def _generate_based_on_name(self, name: str) -> str:
        name_lower = name.lower()

        for key in self.DATA_TYPES:
            if key in name_lower:
                return self.DATA_TYPES[key]()

        if "id" in name_lower:
            return random.randint(1, 10000)
        elif "count" in name_lower or "num" in name_lower:
            return random.randint(0, 100)
        elif "price" in name_lower or "cost" in name_lower:
            return round(random.uniform(10.0, 500.0), 2)
        elif "is_" in name_lower or "has_" in name_lower or "enabled" in name_lower:
            return random.choice([True, False])
        elif "date" in name_lower or "created" in name_lower or "updated" in name_lower:
            return (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        else:
            return f"mock_{name}_{random.randint(1, 100)}"

    def _format_data(self, data: List[Dict[str, Any]], format: str) -> Any:
        if format == "json":
            import json
            return json.dumps(data, indent=2)
        elif format == "python":
            lines = ["[", ",".join([f"\n    {repr(item)}" for item in data]), "\n]"]
            return "".join(lines)
        elif format == "typescript":
            if data:
                fields = list(data[0].keys())
                type_def = f"interface MockData {{\n" + "\n".join([f"  {f}: string | number | boolean;" for f in fields]) + "\n}"
                data_str = ",\n".join([str(item) for item in data])
                return f"{type_def}\n\nexport const mockData: MockData[] = [{data_str}];"
            return ""
        elif format == "csv":
            if not data:
                return ""
            import csv
            import io
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            return output.getvalue()
        return str(data)
