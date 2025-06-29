from agent_data import AGENTS
from collections import Counter

# Simple keyword-based task analysis
TASK_TYPES = {
    'code generation': ['generate', 'write', 'create', 'code'],
    'bug fix': ['fix', 'bug', 'error', 'issue', 'debug'],
    'refactoring': ['refactor', 'improve', 'clean', 'restructure'],
    'test': ['test', 'unit test', 'testing'],
    'documentation': ['document', 'docs', 'documentation'],
}

LANGUAGES = [
    'python', 'javascript', 'typescript', 'go', 'java', 'c++', 'c#', 'ruby'
]

PLATFORMS = [
    'vscode', 'jetbrains', 'neovim', 'replit', 'cloud9', 'cursor'
]

def analyze_task(task_desc):
    desc = task_desc.lower()
    task_type = None
    for ttype, keywords in TASK_TYPES.items():
        if any(kw in desc for kw in keywords):
            task_type = ttype
            break
    language = None
    for lang in LANGUAGES:
        if lang in desc:
            language = lang.capitalize() if lang != 'c++' else 'C++'
            break
    platform = None
    for plat in PLATFORMS:
        if plat in desc:
            platform = plat.capitalize() if plat != 'vscode' else 'VSCode'
            break
    return {
        'task_type': task_type,
        'language': language,
        'platform': platform
    }

def score_agent(agent, analysis):
    score = 0
    justifications = []
    # Language match
    if analysis['language'] and analysis['language'] in agent['languages']:
        score += 2
        justifications.append(f"Supports {analysis['language']}")
    # Platform match
    if analysis['platform'] and any(analysis['platform'] in p for p in agent['platforms']):
        score += 2
        justifications.append(f"Available on {analysis['platform']}")
    # Task type/feature match
    if analysis['task_type']:
        for feature in agent['features']:
            if analysis['task_type'].split()[0] in feature.lower():
                score += 2
                justifications.append(f"Good for {analysis['task_type']}")
    # Strengths
    if agent['strengths']:
        score += 1
        justifications.append(agent['strengths'][0])
    # Unique selling point
    if agent['unique']:
        justifications.append(agent['unique'])
    return score, justifications

def recommend_agents(task_desc):
    analysis = analyze_task(task_desc)
    scored = []
    for agent in AGENTS:
        score, justifications = score_agent(agent, analysis)
        scored.append({
            'agent': agent,
            'score': score,
            'justifications': justifications
        })
    top = sorted(scored, key=lambda x: x['score'], reverse=True)[:3]
    recommendations = []
    for item in top:
        recommendations.append({
            'name': item['agent']['name'],
            'description': item['agent']['description'],
            'score': item['score'],
            'justifications': item['justifications'],
            'platforms': item['agent']['platforms'],
            'languages': item['agent']['languages'],
            'features': item['agent']['features'],
            'strengths': item['agent']['strengths'],
            'weaknesses': item['agent']['weaknesses'],
            'unique': item['agent']['unique']
        })
    return recommendations
