from flask import Flask, jsonify, request, abort, render_template_string
import platform
import os
import subprocess
import json

app = Flask(__name__)

HOME_HTML = """
<!doctype html>
<title>Local AI Hardware Scanner</title>
<h1>Local AI Hardware Scanner</h1>
<p>Use the <code>/api/scan</code> endpoint to get a hardware report and model recommendations.</p>
<p>Example: <code>GET /api/scan?task=vision</code></p>
"""

def get_cpu_info():
    try:
        cpu = platform.processor()
        if not cpu:
            cpu = "Unknown CPU"
        cores = os.cpu_count()
        return {"name": cpu, "cores": cores}
    except Exception:
        return {"name": "Error", "cores": None}

def get_ram_info():
    try:
        if os.name == "posix":
            with open("/proc/meminfo") as f:
                meminfo = f.read()
            total_kb = int([line for line in meminfo.splitlines() if "MemTotal:" in line][0].split()[1])
            total_gb = round(total_kb / 1024 / 1024, 2)
        else:
            total_gb = round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1024**3, 2)
        return {"total_gb": total_gb}
    except Exception:
        return {"total_gb": None}

def get_gpu_info():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return []
        lines = result.stdout.strip().splitlines()
        gpus = []
        for line in lines:
            name, mem = [x.strip() for x in line.split(",")]
            mem_gb = int(mem.split()[0]) // 1024
            gpus.append({"name": name, "memory_gb": mem_gb})
        return gpus
    except FileNotFoundError:
        return []  # nvidia-smi not installed
    except Exception:
        return []

def recommend_models(cpu, ram, gpus, task):
    # Very simple heuristic
    recommendations = []
    if task == "vision":
        if any(g["memory_gb"] >= 8 for g in gpus):
            recommendations.append("Stable Diffusion 1.5")
        if cpu["cores"] and cpu["cores"] >= 8 and ram["total_gb"] and ram["total_gb"] >= 16:
            recommendations.append("YOLOv5")
    elif task == "nlp":
        if any(g["memory_gb"] >= 12 for g in gpus):
            recommendations.append("LLaMA 7B")
        if cpu["cores"] and cpu["cores"] >= 12 and ram["total_gb"] and ram["total_gb"] >= 32:
            recommendations.append("GPT-J 6B")
    else:
        recommendations.append("No specific model for task '{}'".format(task))
    return recommendations

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/api/scan", methods=["GET"])
def api_scan():
    task = request.args.get("task", "").lower()
    if not task:
        return jsonify({"error": "Missing required query parameter 'task'"}), 400

    # Input validation: allow only known tasks
    allowed_tasks = {"vision", "nlp"}
    if task not in allowed_tasks:
        return jsonify({"error": f"Invalid task '{task}'. Allowed: {', '.join(allowed_tasks)}"}), 400

    try:
        cpu = get_cpu_info()
        ram = get_ram_info()
        gpus = get_gpu_info()
        models = recommend_models(cpu, ram, gpus, task)

        response = {
            "hardware": {
                "cpu": cpu,
                "ram": ram,
                "gpus": gpus,
            },
            "task": task,
            "recommended_models": models,
        }
        return jsonify(response)
    except Exception as e:
        # Generic error handling
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
