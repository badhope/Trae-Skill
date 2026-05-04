#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Validator - Validates agent.yaml configuration
Thesis Specialist Platform v2.2
"""

import yaml
import os
import sys
import json
from typing import Dict, List, Any

class ConfigValidator:
    def __init__(self, config_path: str = "agent.yaml"):
        self.config_path = config_path
        self.errors = []
        self.warnings = []
        self.config = {}

    def load_config(self) -> bool:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents = content.split('---')

                for doc in documents:
                    if doc.strip():
                        try:
                            doc_config = yaml.safe_load(doc)
                            if doc_config:
                                self.config.update(doc_config)
                        except yaml.YAMLError as e:
                            self.errors.append(f"YAML parsing error: {e}")
            return True
        except FileNotFoundError:
            self.errors.append(f"Configuration file not found: {self.config_path}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to load configuration: {e}")
            return False

    def validate_structure(self) -> bool:
        """Validate configuration structure"""
        required_sections = [
            'name', 'role', 'version', 'description',
            'executionFlow', 'expertEngines', 'metaAgents',
            'routingStrategy', 'memorySystem', 'checklists',
            'usageGuide', 'compatibility'
        ]

        for section in required_sections:
            if section not in self.config:
                self.errors.append(f"Missing required configuration section: {section}")

        return len(self.errors) == 0

    def validate_execution_flow(self) -> bool:
        """Validate execution flow"""
        flow = self.config.get('executionFlow', {})
        required_steps = [
            'step1_intentRecognition',
            'step2_expertMatching',
            'step3_taskPlanning',
            'step4_expertExecution',
            'step5_toolCalling',
            'step6_resultIntegration',
            'step7_qualityCheck',
            'step8_finalOutput'
        ]

        for step in required_steps:
            if step not in flow:
                self.errors.append(f"Execution flow missing step: {step}")
            else:
                step_config = flow[step]
                if 'name' not in step_config:
                    self.warnings.append(f"Step {step} missing name")
                if 'steps' not in step_config:
                    self.warnings.append(f"Step {step} missing steps")

        return len(self.errors) == 0

    def validate_expert_engines(self) -> bool:
        """Validate expert engines configuration"""
        engines = self.config.get('expertEngines', [])

        if not isinstance(engines, list):
            self.errors.append("expertEngines must be a list")
            return False

        for idx, engine in enumerate(engines):
            required_fields = ['id', 'name', 'description', 'keywords']

            for field in required_fields:
                if field not in engine:
                    self.errors.append(f"Expert engine [{idx}] missing field: {field}")

            if 'keywords' in engine and not isinstance(engine['keywords'], list):
                self.errors.append(f"Expert engine [{idx}] keywords must be a list")

            if 'id' in engine:
                skill_path = f"skills/engines/{engine['id']}/SKILL.md"
                if not os.path.exists(skill_path):
                    self.warnings.append(f"Expert engine {engine['id']} SKILL file missing: {skill_path}")

        return len(self.errors) == 0

    def validate_meta_agents(self) -> bool:
        """Validate meta agents configuration"""
        agents = self.config.get('metaAgents', [])

        if not isinstance(agents, list):
            self.errors.append("metaAgents must be a list")
            return False

        for idx, agent in enumerate(agents):
            required_fields = ['id', 'name', 'description', 'keywords']

            for field in required_fields:
                if field not in agent:
                    self.errors.append(f"Meta agent [{idx}] missing field: {field}")

        return len(self.errors) == 0

    def validate_routing(self) -> bool:
        """Validate routing strategy"""
        routing = self.config.get('routingStrategy', {})

        if 'defaultEngine' not in routing:
            self.errors.append("routingStrategy missing defaultEngine")

        if 'routingRules' not in routing:
            self.errors.append("routingStrategy missing routingRules")
        else:
            rules = routing['routingRules']
            for idx, rule in enumerate(rules):
                required_fields = ['keywords', 'targetType', 'target']
                for field in required_fields:
                    if field not in rule:
                        self.errors.append(f"Routing rule [{idx}] missing field: {field}")

        return len(self.errors) == 0

    def validate_memory_system(self) -> bool:
        """Validate memory system configuration"""
        memory = self.config.get('memorySystem', {})

        if 'enabled' not in memory:
            self.errors.append("memorySystem missing enabled field")

        if 'memoryTypes' not in memory:
            self.errors.append("memorySystem missing memoryTypes")

        return len(self.errors) == 0

    def validate_checklists(self) -> bool:
        """Validate checklists configuration"""
        checklists = self.config.get('checklists', {})

        required_checklists = ['inputCheck', 'executionCheck', 'outputCheck', 'qualityCheck']

        for checklist in required_checklists:
            if checklist not in checklists:
                self.errors.append(f"Missing checklist: {checklist}")

        return len(self.errors) == 0

    def validate_compatibility(self) -> bool:
        """Validate platform compatibility configuration"""
        compatibility = self.config.get('compatibility', {})

        if 'platforms' not in compatibility:
            self.errors.append("compatibility missing platforms")

        return len(self.errors) == 0

    def validate_version(self) -> bool:
        """Validate version format"""
        version = self.config.get('version', '')

        if not version:
            self.errors.append("Missing version number")
            return False

        parts = version.split('.')
        if len(parts) != 3:
            self.warnings.append(f"Version number format should be X.Y.Z, current: {version}")

        return len(self.errors) == 0

    def run_all_checks(self) -> bool:
        """Run all validation checks"""
        print("Starting configuration validation...")

        if not self.load_config():
            return False

        validations = [
            ('Structure validation', self.validate_structure),
            ('Execution flow validation', self.validate_execution_flow),
            ('Expert engines validation', self.validate_expert_engines),
            ('Meta agents validation', self.validate_meta_agents),
            ('Routing strategy validation', self.validate_routing),
            ('Memory system validation', self.validate_memory_system),
            ('Checklists validation', self.validate_checklists),
            ('Compatibility validation', self.validate_compatibility),
            ('Version validation', self.validate_version)
        ]

        for name, validator in validations:
            print(f"  Validating: {name}...")
            validator()

        return True

    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("# Configuration Validation Report")
        report.append("")
        report.append(f"## Validation Time: {self._get_timestamp()}")
        report.append(f"## Configuration File: {self.config_path}")
        report.append("")

        if self.errors:
            report.append("### Errors (Total: {})".format(len(self.errors)))
            for i, error in enumerate(self.errors, 1):
                report.append("{}. {}".format(i, error))
        else:
            report.append("### Errors: None")

        report.append("")

        if self.warnings:
            report.append("### Warnings (Total: {})".format(len(self.warnings)))
            for i, warning in enumerate(self.warnings, 1):
                report.append("{}. {}".format(i, warning))
        else:
            report.append("### Warnings: None")

        report.append("")

        if not self.errors:
            report.append("## Validation Passed!")
            report.append("")
            report.append("Configuration file format is correct and ready to use.")
        else:
            report.append("## Validation Failed")
            report.append("")
            report.append("Please fix the above errors and re-validate.")

        return "\n".join(report)

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """Main function"""
    validator = ConfigValidator()

    if validator.run_all_checks():
        report = validator.generate_report()
        print("\n" + "="*60)
        print(report)
        print("="*60 + "\n")

        with open("config-validation-report.md", 'w', encoding='utf-8') as f:
            f.write(report)
        print("Report saved to: config-validation-report.md")

        if validator.errors:
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    main()
