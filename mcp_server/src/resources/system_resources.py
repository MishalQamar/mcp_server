import os

import psutil


async def get_memory_resource() -> dict:
    """Return memory usage statistics for the current server process."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    return {
        "pid": process.pid,
        "rss_bytes": memory_info.rss,
        "vms_bytes": memory_info.vms,
        "memory_percent": process.memory_percent(),
    }
