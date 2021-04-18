from enum import Enum


class LogLevel(Enum):
    Info = 1
    Debug = 2
    Error = 3
    Critical = 4


def log(log_level, message):
    if log_level == LogLevel.Info:
        print("INFO: " + message)
    elif log_level == LogLevel.Debug:
        print("DEBUG: " + message)
    elif log_level == LogLevel.Error:
        print("ERROR: " + message)
    elif log_level == LogLevel.Critical:
        print("CRITICAL: " + message)
