# Routing Optimizer
# Advanced keyword matching and routing optimization
# Thesis Specialist Platform v2.2

import re
from typing import List, Dict, Tuple, Optional
from collections import Counter

class RoutingOptimizer:
    """Advanced routing optimization with multiple matching strategies"""

    def __init__(self):
        self.keyword_cache = {}
        self.match_history = []

    def calculate_match_score(self, user_input: str, keywords: List[str]) -> float:
        """
        Calculate matching score using multiple strategies:
        - Exact match (40%)
        - Partial match (30%)
        - Semantic similarity (20%)
        - Context relevance (10%)
        """
        input_lower = user_input.lower()
        score = 0.0

        for keyword in keywords:
            keyword_lower = keyword.lower()

            if keyword_lower == input_lower:
                score += 0.4
            elif keyword_lower in input_lower:
                score += 0.3

            input_words = input_lower.split()
            keyword_words = keyword_lower.split()
            for word in keyword_words:
                if any(word in input_word for input_word in input_words):
                    score += 0.1

            if len(keyword_lower) > 3:
                if keyword_lower[:3] in input_lower or keyword_lower[-3:] in input_lower:
                    score += 0.05

        return min(score, 1.0)

    def fuzzy_match(self, user_input: str, keywords: List[str], threshold: float = 0.3) -> Tuple[bool, float]:
        """Fuzzy keyword matching with threshold"""
        score = self.calculate_match_score(user_input, keywords)
        return (score >= threshold, score)

    def prioritize_rules(self, user_input: str, rules: List[Dict]) -> List[Tuple[Dict, float]]:
        """Prioritize routing rules based on match quality"""
        scored_rules = []

        for rule in rules:
            keywords = rule.get('keywords', [])
            _, score = self.fuzzy_match(user_input, keywords)
            if score > 0:
                priority = rule.get('priority', 1)
                final_score = score * priority
                scored_rules.append((rule, final_score))

        scored_rules.sort(key=lambda x: x[1], reverse=True)
        return scored_rules

    def smart_route(self, user_input: str, rules: List[Dict]) -> Optional[Dict]:
        """Smart routing with context awareness"""
        if user_input in self.keyword_cache:
            return self.keyword_cache[user_input]

        scored_rules = self.prioritize_rules(user_input, rules)

        if scored_rules:
            best_rule = scored_rules[0][0]
            self.keyword_cache[user_input] = best_rule
            self.match_history.append({
                'input': user_input,
                'rule': best_rule['target'],
                'score': scored_rules[0][1]
            })

            if len(self.match_history) > 1000:
                self.match_history = self.match_history[-500:]

            return best_rule

        return None

    def batch_route(self, inputs: List[str], rules: List[Dict]) -> List[Optional[Dict]]:
        """Batch routing for efficiency"""
        results = []
        for input_str in inputs:
            result = self.smart_route(input_str, rules)
            results.append(result)
        return results

    def analyze_patterns(self) -> Dict:
        """Analyze routing patterns from history"""
        if not self.match_history:
            return {'patterns': [], 'most_common': None}

        target_counts = Counter(entry['rule'] for entry in self.match_history)
        most_common = target_counts.most_common(1)[0] if target_counts else None

        pattern_groups = {}
        for entry in self.match_history:
            input_len = len(entry['input'].split())
            key = f"{input_len}_words"
            if key not in pattern_groups:
                pattern_groups[key] = []
            pattern_groups[key].append(entry)

        return {
            'total_matches': len(self.match_history),
            'most_common_target': most_common,
            'pattern_distribution': {k: len(v) for k, v in pattern_groups.items()},
            'average_score': sum(e['score'] for e in self.match_history) / len(self.match_history)
        }

    def clear_cache(self):
        """Clear routing cache"""
        self.keyword_cache.clear()

    def get_stats(self) -> Dict:
        """Get routing statistics"""
        return {
            'cache_size': len(self.keyword_cache),
            'history_size': len(self.match_history),
            'patterns': self.analyze_patterns()
        }

if __name__ == '__main__':
    optimizer = RoutingOptimizer()

    sample_rules = [
        {'keywords': ['topic', 'research question', 'idea'], 'target': 'topic-expert', 'priority': 3},
        {'keywords': ['literature', 'review', 'references'], 'target': 'literature-expert', 'priority': 2},
        {'keywords': ['structure', 'outline', 'framework'], 'target': 'structure-expert', 'priority': 2},
        {'keywords': ['writing', 'draft', 'chapter'], 'target': 'writing-expert', 'priority': 1},
    ]

    test_inputs = [
        'Help me find a good research topic',
        'Write a literature review',
        'Create thesis outline',
        'Draft chapter 3',
        'Hello world'
    ]

    for input_str in test_inputs:
        result = optimizer.smart_route(input_str, sample_rules)
        if result:
            print(f"Input: '{input_str}' -> Target: {result['target']}")
        else:
            print(f"Input: '{input_str}' -> Target: No match")

    print("\nRouting Statistics:")
    print(optimizer.get_stats())
