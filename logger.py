#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger System - Agent execution logging
Thesis Specialist Platform v2.2
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AgentLogger:
    def __init__(self, name: str = "ThesisSpecialist", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)

            log_file = os.path.join(
                self.log_dir,
                f"ThesisSpecialist_{datetime.now().strftime('%Y%m%d')}.log"
            )

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    def debug(self, message: str, **kwargs):
        self.logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs):
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        self.logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs):
        self.logger.critical(message, extra=kwargs)

    def log_execution(self, phase: str, expert: str, input_text: str):
        self.info(f"[EXECUTION] Phase: {phase} | Expert: {expert} | Input: {input_text[:100]}...")

    def log_result(self, phase: str, expert: str, success: bool, duration: float):
        status = "SUCCESS" if success else "FAILED"
        self.info(f"[RESULT] Phase: {phase} | Expert: {expert} | Status: {status} | Duration: {duration:.2f}s")

def get_logger(name: str = "ThesisSpecialist") -> AgentLogger:
    return AgentLogger(name)

if __name__ == "__main__":
    logger = get_logger()
    logger.info("Logger initialized for Thesis Specialist Platform")
