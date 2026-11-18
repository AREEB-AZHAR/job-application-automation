import json
import re
from typing import Dict, Any, Tuple, Optional

def load_profile(profile_path: str) -> Dict[str, Any]:
    with open(profile_path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_job(job: Dict[str, Any], profile: Dict[str, Any]) -> Tuple[bool, str, Optional[str], Optional[str]]:
    """
    Evaluates whether a job matches Areeb Azhar's criteria:
    - Must require <= 1 year experience (or entry level/fresh graduate/junior).
    - Must match one of the target tech domains.
    Returns:
    (is_match, reason, matched_domain, cv_path)
    """
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    full_text = f"{title} {description}"

    # 1. Experience check
    # Check for senior / lead / principal keywords
    disqualifying_titles = ["senior", "lead", "principal", "staff", "director", "architect", "head of", "vp", "manager"]
    for keyword in disqualifying_titles:
        if keyword in title:
            return False, f"Disqualified: Title contains senior keyword '{keyword}'", None, None

    # Check for experience years requirement (e.g. "3+ years", "2-4 years", "5 years")
    exp_matches = re.findall(r"(\d+)\+?\s*(?:-\s*(\d+))?\s*(?:years?|yrs?)\s*(?:of)?\s*experience", full_text)
    for min_exp, max_exp in exp_matches:
        min_years = int(min_exp)
        if min_years > 1:
            return False, f"Disqualified: Requires {min_years}+ years of experience (criteria is <= 1 year)", None, None

    # Check for acceptable levels
    entry_indicators = [
        "junior", "entry level", "fresh", "graduate", "associate", "intern", 
        "0-1", "0 to 1", "less than 1", "1 year", "1+ year", "no experience required"
    ]
    is_entry_level = any(indicator in full_text for indicator in entry_indicators)

    # 2. Domain matching
    mappings = profile.get("cv_mappings", {})
    if any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["react", "node", "typescript", "frontend", "web developer", "full stack", "fullstack"]):
        domain = "full_stack"
        cv_path = mappings.get("full_stack")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["rust", "blockchain", "solidity", "hyperledger", "web3", "smart contract"]):
        domain = "rust_blockchain"
        cv_path = mappings.get("rust_blockchain")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["flutter", "dart", "mobile developer", "android", "ios"]):
        domain = "flutter"
        cv_path = mappings.get("flutter")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["unity", "game developer", "c#", "unreal", "game programmer"]):
        domain = "game_dev"
        cv_path = mappings.get("game_dev")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["machine learning", "ai", "artificial intelligence", "deep learning", "nlp", "llm", "data science"]):
        domain = "ai_ml"
        cv_path = mappings.get("ai_ml")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["software engineer", "software developer", "programmer", "trainee"]):
        # Default software engineering maps to full-stack
        domain = "full_stack"
        cv_path = mappings.get("full_stack")
    else:
        return False, "Disqualified: Tech stack does not match software engineering domains", None, None

    match_reason = "Accepted: Matches domain and experience criteria (< 1 year)"
    return True, match_reason, domain, cv_path

def generate_cover_letter(job: Dict[str, Any], domain: str, profile: Dict[str, Any]) -> str:
    """
    Generates a tailored cover letter referencing Areeb Azhar's real projects and education.
    """
    company = job.get("company", "Hiring Team")
    title = job.get("title", "Software Engineer")
    
    project_highlights = {
        "full_stack": (
            "During my BS in Software Engineering at Iqra University, I developed CryptoTrader, "
            "a responsive market dashboard and virtual trading simulator with React 19, Vite, and Zustand, "
            "as well as IqraDegreeChain, a verification portal using a TypeScript Express API gateway and Hyperledger Fabric."
        ),
        "ai_ml": (
            "With my background in Software Engineering and strong foundations in algorithms and Python, "
            "I have built data-driven solutions and evaluated model workflows, focusing on clean architecture and performance."
        ),
        "flutter": (
            "I specialize in cross-platform mobile development with Flutter and Dart, building clean, responsive UI "
            "with state management and REST API integrations."
        ),
        "game_dev": (
            "I have hands-on experience designing gameplay mechanics, physics interactions, and UI architectures "
            "using Unity and C#."
        ),
        "rust_blockchain": (
            "I completed a specialized 9-week internship with Rockstable x Hazara University in Blockchain Technology "
            "& Rust programming, and engineered IqraDegreeChain with Hyperledger Fabric."
        )
    }

    highlight = project_highlights.get(domain, project_highlights["full_stack"])

    cover_letter = f"""Dear Hiring Team at {company},

I am writing to express my strong interest in the {title} position. As a Software Engineering graduate from Iqra University, Karachi (completed September 2026, scoring in the 88.1st percentile on the National Student Competency Test), I bring practical project experience and an eagerness to contribute immediately.

{highlight}

I am adaptable, proactive, and ready to contribute to your team. Whether collaborating remotely, in hybrid setups, or on-site, I take ownership of clean code and responsive problem-solving.

Thank you for your time and consideration. I welcome the opportunity to discuss how my background aligns with your engineering goals.

Sincerely,
Areeb Azhar
+92 301 2343423 | areebazhar3@gmail.com | github.com/AREEB-AZHAR
"""
    return cover_letter
