import os
import json
import uuid
import datetime
from typing import List, Dict, Optional

# Attempt to load Gemini client if configured
try:
    from app.ai.gemini_client import ask_gemini
    HAS_GEMINI = True
except Exception as e:
    HAS_GEMINI = False


def generate_article_summary(article: Dict, max_words: int = 150) -> Dict:
    """
    Generates a concise, fact-based summary for a cybersecurity article.
    Falls back gracefully if AI service is temporarily unavailable.
    """
    title = article.get("title", "")
    content = article.get("content") or article.get("summary") or ""
    source = article.get("source", "Cybersecurity Feed")

    prompt = f"""
You are a senior cybersecurity intelligence analyst.
Summarize the following verified news story in {max_words} words or fewer.

Rules:
- State the exact threat actor, affected software/infrastructure, and impact.
- Do NOT invent CVE numbers or details not present in the text.
- Use professional, objective threat intelligence language.
- Provide 1 actionable mitigation if mentioned.

Article Source: {source}
Title: {title}
Content:
{content[:2500]}
"""

    summary_text = ""
    is_gemini_used = False

    if HAS_GEMINI and os.getenv("GEMINI_API_KEY"):
        try:
            summary_text = ask_gemini(prompt).strip()
            is_gemini_used = True
        except Exception as e:
            print(f"[AIService] Gemini call failed: {e}. Falling back to structured extractor.")

    if not summary_text:
        # High quality factual extractive fallback
        raw_summary = article.get("summary", "")
        if raw_summary:
            sentences = [s.strip() for s in raw_summary.replace("\n", " ").split(". ") if s.strip()]
            summary_text = ". ".join(sentences[:3]) + "."
        else:
            summary_text = f"Security report from {source} highlighting critical developments regarding {title}."

    return {
        "article_id": article.get("id", ""),
        "summary": summary_text,
        "is_ai_generated": True,
        "model_used": "Gemini-3.5-Flash" if is_gemini_used else "Heuristic Extractor",
        "source_disclaimer": "AI-generated summary based strictly on reported vendor and news advisories."
    }


def generate_video_script(articles: List[Dict], duration_minutes: int = 5, video_style: str = "briefing") -> Dict:
    """
    Synthesizes a complete YouTube / video narration script from selected articles.
    """
    script_id = str(uuid.uuid4())
    now_str = datetime.datetime.now().strftime("%B %d, %Y")

    # Format article briefing blocks
    briefing_blocks = []
    for idx, art in enumerate(articles, 1):
        cves_str = ", ".join(art.get("cves", [])) if art.get("cves") else "N/A"
        briefing_blocks.append(
            f"STORY {idx}:\n"
            f"Title: {art.get('title')}\n"
            f"Source: {art.get('source')}\n"
            f"Category: {art.get('category', 'General')}\n"
            f"CVEs: {cves_str}\n"
            f"Summary: {art.get('summary') or art.get('content', '')[:500]}\n"
        )

    briefing_text = "\n---\n".join(briefing_blocks)

    prompt = f"""
You are an elite cybersecurity broadcaster and YouTube creator.
Create a {duration_minutes}-minute video narration script based strictly on the following verified cyber news stories.

Selected Stories:
{briefing_text}

Instructions:
1. [00:00 - 00:30] HOOK: A high-impact opening highlighting today's most critical zero-day or breach.
2. [00:30 - END-1:00] DEEP DIVE: Walk through each of the {len(articles)} stories in clear, compelling broadcast prose.
   - For each story, explain the vector, who is targeted, and the defensive takeaway.
   - Use speaker cues like [HOST NARRATION] and [ON-SCREEN GRAPHIC].
3. [WRAP-UP]: 3 practical security action items (e.g. patch cadence, MFA, audit logs).
4. [OUTRO]: Standard call to action to subscribe to CyberNewsAI.
5. Provide a clickable SEO title, a YouTube description, and 15 comma-separated tags.

Format the output strictly using these section headers:
=== YOUTUBE SCRIPT ===
(Full spoken script with stage directions)
=== SEO TITLE ===
(Clickable professional video title)
=== DESCRIPTION ===
(Video description with timestamps and story credits)
=== TAGS ===
(20 comma-separated tags)
"""

    script_content = ""
    seo_title = ""
    description = ""
    tags = []
    is_gemini_used = False

    if HAS_GEMINI and os.getenv("GEMINI_API_KEY"):
        try:
            raw_response = ask_gemini(prompt)
            is_gemini_used = True

            # Parse sections
            def extract_block(text: str, header: str, next_headers: List[str]) -> str:
                pos = text.find(f"=== {header} ===")
                if pos == -1:
                    return ""
                start = pos + len(f"=== {header} ===")
                end = len(text)
                for nh in next_headers:
                    npos = text.find(f"=== {nh} ===", start)
                    if npos != -1 and npos < end:
                        end = npos
                return text[start:end].strip()

            script_content = extract_block(raw_response, "YOUTUBE SCRIPT", ["SEO TITLE", "DESCRIPTION", "TAGS"])
            seo_title = extract_block(raw_response, "SEO TITLE", ["DESCRIPTION", "TAGS"])
            description = extract_block(raw_response, "DESCRIPTION", ["TAGS"])
            tags_raw = extract_block(raw_response, "TAGS", [])
            if tags_raw:
                tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        except Exception as e:
            print(f"[AIService] Script generation failed via Gemini: {e}")

    # Fallback script synthesizer if AI is unavailable or parsing failed
    if not script_content:
        first_title = articles[0].get("title", "Critical Cybersecurity Incidents") if articles else "Threat Alert"
        seo_title = f"Cyber Alert: {first_title[:60]} | Threat Intelligence Briefing"
        
        script_parts = [
            f"# CyberNewsAI Threat Intelligence Briefing — {now_str}",
            f"Target Runtime: ~{duration_minutes} minutes | Style: {video_style.title()}",
            "",
            "[HOST NARRATION - OPENING HOOK]",
            f"Welcome back to CyberNewsAI. Today is {now_str}, and we are tracking critical cybersecurity developments that security teams and IT professionals need to respond to immediately.",
            f"Leading today's briefing: {first_title}.",
            "",
            "Let's dive straight into the technical breakdown.",
            ""
        ]

        for i, art in enumerate(articles, 1):
            cves = ", ".join(art.get("cves", [])) if art.get("cves") else "Unassigned / General Threat"
            script_parts.extend([
                f"[ON-SCREEN GRAPHIC: Story #{i} - {art.get('source')} | Category: {art.get('category')} | Ref: {cves}]",
                f"[HOST NARRATION - STORY {i}]",
                f"Story number {i} comes from {art.get('source')}: '{art.get('title')}'.",
                f"{art.get('summary') or 'Researchers have flagged this active campaign as an urgent development requiring immediate defensive inspection.'}",
                f"Why this matters: In environments where defense-in-depth is critical, early detection of this pattern prevents lateral movement and unauthorized privilege escalation.",
                ""
            ])

        script_parts.extend([
            "[HOST NARRATION - STRATEGIC TAKEAWAYS & DEFENSE]",
            "To defend your organization against the attack vectors covered today:",
            "1. Audit edge-facing appliances and apply vendor patches immediately.",
            "2. Enforce phishing-resistant multi-factor authentication across all remote access gateways.",
            "3. Review endpoint detection telemetry for unexpected PowerShell or living-off-the-land utility activity.",
            "",
            "[HOST NARRATION - OUTRO]",
            "If you found this threat briefing valuable, hit like, share this with your security team, and subscribe to CyberNewsAI for real-time cybersecurity intelligence updates. Stay safe, stay patched, and we'll see you in the next briefing."
        ])

        script_content = "\n".join(script_parts)
        description = (
            f"Today's CyberNewsAI Threat Briefing ({now_str}) covers top security stories including:\n"
            + "\n".join([f"• {a.get('title')} ({a.get('source')})" for a in articles])
            + "\n\nSources:\n"
            + "\n".join([f"- {a.get('link')}" for a in articles])
        )
        tags = ["cybersecurity", "threat intelligence", "infosec", "cve", "ransomware", "hacker news", "cisa", "cve-alert"]

    if not seo_title:
        seo_title = f"Cyber Threat Briefing: {articles[0].get('title', 'Latest Breaches')[:50]}"
    if not description:
        description = f"CyberNewsAI briefing covering {len(articles)} critical stories."
    if not tags:
        tags = ["cybersecurity", "infosec", "threat-intel"]

    return {
        "id": script_id,
        "title": seo_title,
        "target_duration": f"{duration_minutes} min",
        "script_content": script_content,
        "seo_title": seo_title,
        "description": description,
        "tags": tags,
        "article_ids": [a.get("id") for a in articles if a.get("id")],
        "article_titles": [a.get("title") for a in articles],
        "is_ai_generated": True,
        "created_at": datetime.datetime.now().isoformat()
    }


def export_script_as_text(script: Dict) -> str:
    """Formats a script into a clean downloadable plaintext document."""
    divider = "=" * 80
    sub_divider = "-" * 80

    text = f"""{divider}
CYBERNEWSAI — THREAT INTELLIGENCE VIDEO SCRIPT
Generated: {script.get('created_at', 'N/A')}
Target Runtime: {script.get('target_duration', 'N/A')}
AI Verified Content: Yes (Review against original vendor advisories before broadcast)
{divider}

TITLE: {script.get('title', '')}

{sub_divider}
YOUTUBE SEO METADATA
{sub_divider}
SEO Title:
{script.get('seo_title', '')}

Description:
{script.get('description', '')}

Tags:
{', '.join(script.get('tags', []))}

{sub_divider}
REFERENCED THREAT ARTICLES
{sub_divider}
"""
    for title in script.get("article_titles", []):
        text += f"- {title}\n"

    text += f"""
{divider}
NARRATION SCRIPT (BROADCAST COPY)
{divider}

{script.get('script_content', '')}

{divider}
END OF SCRIPT — CYBERNEWSAI PORTFOLIO ENGINE
{divider}
"""
    return text.strip()
