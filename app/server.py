import os
import json
import threading
import datetime
import traceback
from flask import Flask, jsonify, request, render_template_string

from main import run_pipeline
from news.rss_fetcher import fetch_all_news
from news.deduplicator import remove_duplicates

app = Flask(__name__)

# State management
state_lock = threading.Lock()
pipeline_state = {
    "status": "idle",       # "idle", "running", "completed", "failed"
    "started_at": None,
    "finished_at": None,
    "error": None,
    "logs": []
}

# Live log file
LOG_FILE = "output/logs/pipeline.log"


def log_progress(message):
    """
    Callback function passed to run_pipeline to capture progress logs.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    with state_lock:
        pipeline_state["logs"].append(formatted_message)
        # Keep logs list size reasonable in memory
        if len(pipeline_state["logs"]) > 1000:
            pipeline_state["logs"].pop(0)
            
    # Append to log file
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
    except Exception:
        pass


def run_pipeline_thread():
    """
    Target function to execute the pipeline in a background thread.
    """
    global pipeline_state
    
    with state_lock:
        pipeline_state["status"] = "running"
        pipeline_state["started_at"] = datetime.datetime.now().isoformat()
        pipeline_state["finished_at"] = None
        pipeline_state["error"] = None
        pipeline_state["logs"] = []

    # Clear previous log file
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        pass

    log_progress("Initializing background execution thread...")
    
    try:
        run_pipeline(progress_callback=log_progress)
        
        with state_lock:
            pipeline_state["status"] = "completed"
            pipeline_state["finished_at"] = datetime.datetime.now().isoformat()
            
    except Exception as e:
        error_details = traceback.format_exc()
        log_progress(f"❌ CRITICAL ERROR IN PIPELINE:\n{error_details}")
        
        with state_lock:
            pipeline_state["status"] = "failed"
            pipeline_state["finished_at"] = datetime.datetime.now().isoformat()
            pipeline_state["error"] = str(e)


# -------------------------------------------------
# Web Routes
# -------------------------------------------------

@app.route("/")
def index():
    """
    Serves the Single Page Application.
    Since we have a beautiful dashboard, we serve index.html.
    We will create index.html in app/templates/index.html.
    """
    # Fallback to absolute template path if Flask cannot resolve it
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    return "Error: app/templates/index.html not found.", 404


@app.route("/api/status", methods=["GET"])
def get_status():
    """
    Returns the current state of the pipeline.
    """
    with state_lock:
        return jsonify(pipeline_state)


@app.route("/api/run", methods=["POST"])
def trigger_run():
    """
    Triggers a run of the pipeline if it is not currently running.
    """
    with state_lock:
        if pipeline_state["status"] == "running":
            return jsonify({"success": False, "message": "Pipeline is already running."}), 400
            
    thread = threading.Thread(target=run_pipeline_thread, daemon=True)
    thread.start()
    return jsonify({"success": True, "message": "Pipeline run started in the background."})


@app.route("/api/articles", methods=["GET"])
def get_articles():
    """
    Returns all fetched articles from the database (articles.json).
    If articles.json does not exist, trigger a quick live fetch in-memory.
    """
    refresh = request.args.get("refresh", "false").lower() == "true"
    articles_file = "output/articles.json"
    
    if not refresh and os.path.exists(articles_file):
        try:
            with open(articles_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
                return jsonify(articles)
        except Exception as e:
            # Fallback to fetch on error
            pass
            
    # Fetch live
    try:
        raw_articles = fetch_all_news()
        articles = remove_duplicates(raw_articles)
        # Cache it
        os.makedirs(os.path.dirname(articles_file), exist_ok=True)
        with open(articles_file, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, default=str)
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch articles: {str(e)}"}), 500


@app.route("/api/latest", methods=["GET"])
def get_latest():
    """
    Parses and returns all generated content (summaries, script, seo, shorts, thumbnail).
    """
    output = {
        "articles": [],
        "youtube_script": "",
        "seo": {"raw": "", "title": "", "description": "", "hashtags": [], "keywords": []},
        "shorts": "",
        "thumbnail": {"raw": "", "title": "", "text": "", "prompt": ""}
    }

    # 1. Load summaries (articles)
    articles_dir = "output/articles"
    if os.path.exists(articles_dir):
        for filename in sorted(os.listdir(articles_dir)):
            if filename.startswith("article_") and filename.endswith(".md"):
                file_path = os.path.join(articles_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Parse title from markdown "# Title"
                    title = "Story"
                    lines = content.split("\n")
                    if lines and lines[0].startswith("# "):
                        title = lines[0][2:].strip()
                        
                    # Parse source
                    source = "Unknown"
                    for line in lines:
                        if line.startswith("Source:"):
                            source = line.split(":", 1)[1].strip()
                            break
                            
                    # Parse link
                    link = ""
                    for line in lines:
                        if line.startswith("Link:"):
                            link = line.split(":", 1)[1].strip()
                            break

                    output["articles"].append({
                        "filename": filename,
                        "title": title,
                        "source": source,
                        "link": link,
                        "content": content
                    })
                except Exception:
                    pass

    # 2. Load YouTube Script
    script_path = "output/scripts/youtube_script.txt"
    if os.path.exists(script_path):
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                output["youtube_script"] = f.read()
        except Exception:
            pass

    # 3. Load SEO and parse it
    seo_path = "output/seo/seo.txt"
    if os.path.exists(seo_path):
        try:
            with open(seo_path, "r", encoding="utf-8") as f:
                raw_seo = f.read()
                output["seo"]["raw"] = raw_seo
                
                # Parse fields
                # Simple parser based on headers
                title_marker = "TITLE:"
                desc_marker = "DESCRIPTION:"
                tags_marker = "HASHTAGS:"
                keywords_marker = "KEYWORDS:"
                
                content_lower = raw_seo.lower()
                
                # Title
                t_start = content_lower.find(title_marker.lower())
                d_start = content_lower.find(desc_marker.lower())
                h_start = content_lower.find(tags_marker.lower())
                k_start = content_lower.find(keywords_marker.lower())
                
                indices = sorted([i for i in [t_start, d_start, h_start, k_start] if i != -1])
                
                def extract_section(start_idx, marker):
                    if start_idx == -1:
                        return ""
                    next_indices = [i for i in indices if i > start_idx]
                    end_idx = next_indices[0] if next_indices else len(raw_seo)
                    
                    val = raw_seo[start_idx + len(marker):end_idx].strip()
                    # Clean leading/trailing quotes or markdown
                    val = val.strip('`*"\n ')
                    return val

                if t_start != -1:
                    output["seo"]["title"] = extract_section(t_start, title_marker)
                if d_start != -1:
                    output["seo"]["description"] = extract_section(d_start, desc_marker)
                if h_start != -1:
                    tags_raw = extract_section(h_start, tags_marker)
                    output["seo"]["hashtags"] = [t.strip() for t in tags_raw.replace("\n", " ").split(" ") if t.strip()]
                if k_start != -1:
                    keywords_raw = extract_section(k_start, keywords_marker)
                    output["seo"]["keywords"] = [k.strip() for k in keywords_raw.split(",") if k.strip()]
        except Exception:
            pass

    # 4. Load Shorts
    shorts_path = "output/shorts/shorts.txt"
    if os.path.exists(shorts_path):
        try:
            with open(shorts_path, "r", encoding="utf-8") as f:
                output["shorts"] = f.read()
        except Exception:
            pass

    # 5. Load Thumbnail and parse it
    thumb_path = "output/thumbnails/thumbnail.txt"
    if os.path.exists(thumb_path):
        try:
            with open(thumb_path, "r", encoding="utf-8") as f:
                raw_thumb = f.read()
                output["thumbnail"]["raw"] = raw_thumb
                
                # Parse fields
                lines = raw_thumb.split("\n")
                current_section = None
                title_lines = []
                text_lines = []
                prompt_lines = []
                
                for line in lines:
                    line_stripped = line.strip()
                    line_lower = line_stripped.lower()
                    
                    if "thumbnail title:" in line_lower:
                        current_section = "title"
                        # Extract rest of line if any
                        part = line_stripped.split(":", 1)[1].strip()
                        if part:
                            title_lines.append(part)
                    elif "thumbnail text:" in line_lower:
                        current_section = "text"
                        part = line_stripped.split(":", 1)[1].strip()
                        if part:
                            text_lines.append(part)
                    elif "ai image prompt:" in line_lower or "image prompt:" in line_lower:
                        current_section = "prompt"
                        part = line_stripped.split(":", 1)[1].strip()
                        if part:
                            prompt_lines.append(part)
                    elif line_stripped:
                        if current_section == "title":
                            title_lines.append(line_stripped)
                        elif current_section == "text":
                            text_lines.append(line_stripped)
                        elif current_section == "prompt":
                            prompt_lines.append(line_stripped)
                            
                output["thumbnail"]["title"] = " ".join(title_lines).strip('`*"\n ')
                output["thumbnail"]["text"] = " ".join(text_lines).strip('`*"\n ')
                output["thumbnail"]["prompt"] = "\n".join(prompt_lines).strip('`*"\n ')
        except Exception:
            pass

    return jsonify(output)


@app.route("/api/save_script", methods=["POST"])
def save_script():
    """
    Saves edited YouTube script content back to file.
    """
    data = request.json
    script_content = data.get("content")
    
    if not script_content:
        return jsonify({"success": False, "message": "Content is required."}), 400
        
    script_path = "output/scripts/youtube_script.txt"
    try:
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        return jsonify({"success": True, "message": "Script saved successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to save script: {str(e)}"}), 500


@app.route("/api/schedule", methods=["GET", "POST"])
def handle_schedule():
    """
    Gets or sets the automated scheduler configuration.
    """
    config_file = "output/scheduler_config.json"
    
    if request.method == "POST":
        data = request.json
        enabled = data.get("enabled", False)
        time_str = data.get("time", "09:00")
        
        # Validate time format HH:MM
        try:
            parts = time_str.split(":")
            if len(parts) != 2 or not (0 <= int(parts[0]) <= 23) or not (0 <= int(parts[1]) <= 59):
                raise ValueError()
        except Exception:
            return jsonify({"success": False, "message": "Invalid time format. Use HH:MM."}), 400
            
        config = {"enabled": enabled, "time": time_str}
        
        try:
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
                
            # Trigger reload signal or file watch reload in scheduler process
            # In our scheduler.py, we can read this config on jobs check or watch it
            return jsonify({"success": True, "message": "Scheduler configuration updated.", "config": config})
        except Exception as e:
            return jsonify({"success": False, "message": f"Failed to write configuration: {str(e)}"}), 500
            
    else:  # GET
        default_config = {"enabled": False, "time": "09:00"}
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return jsonify(config)
            except Exception:
                pass
        return jsonify(default_config)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
