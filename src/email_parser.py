import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup

def parse_job_alert_email(subject: str, sender: str, html_content: str, snippet: str = "") -> List[Dict[str, Any]]:
    """
    Parses incoming job alert emails from LinkedIn, Indeed, Glassdoor, Rozee.pk, and PakTechJobs
    into structured opportunity dictionaries.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    jobs = []

    # Identify source platform from sender/subject
    source = "Email Job Alert"
    sender_lower = sender.lower()
    if "linkedin" in sender_lower or "linkedin" in subject.lower():
        source = "LinkedIn Alerts"
    elif "indeed" in sender_lower or "indeed" in subject.lower():
        source = "Indeed Alerts"
    elif "glassdoor" in sender_lower or "glassdoor" in subject.lower():
        source = "Glassdoor Alerts"
    elif "rozee" in sender_lower or "rozee" in subject.lower():
        source = "Rozee.pk Alerts"
    elif "paktechjobs" in sender_lower:
        source = "PakTechJobs Alerts"

    # Extract all links that look like job postings
    links = soup.find_all("a", href=True)
    seen_urls = set()

    for a in links:
        href = a["href"]
        text = a.get_text(strip=True)
        
        # Filter for job URLs
        is_job_link = any(pattern in href.lower() for pattern in [
            "/jobs/view/", "/viewjob", "/job-listing/", "/job/", "/careers/", "gh_jid=", "lever.co"
        ])

        if is_job_link and href not in seen_urls and len(text) > 4:
            seen_urls.add(href)
            
            # Find surrounding text/context for company & location
            parent = a.find_parent(["td", "div", "li", "tr"])
            context_text = parent.get_text(separator=" ", strip=True) if parent else text

            # Heuristic for title vs company
            title = text
            company = "Hiring Company"
            location = "Pakistan / Remote"

            # Parse lines from context
            parts = [p.strip() for p in context_text.split("·") if p.strip()]
            if len(parts) >= 2:
                company = parts[0]
            
            jobs.append({
                "source": source,
                "title": title,
                "company": company,
                "location": location,
                "url": href,
                "description": context_text
            })

    # Fallback if no specific links matched
    if not jobs and snippet:
        jobs.append({
            "source": source,
            "title": subject,
            "company": "Employer",
            "location": "Pakistan / Remote",
            "url": "",
            "description": snippet
        })

    return jobs
