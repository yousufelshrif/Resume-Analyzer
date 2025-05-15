"""
LinkExtractor Module

This module provides the LinkExtractor class for extracting and classifying hyperlinks from 
unstructured text data such as resumes, emails, or web content. It intelligently handles various 
URL formats including:

- Fully-qualified URLs (http, https)
- www-prefixed domains
- Bare domains (e.g., linkedin.com), with optional strict filtering
- Obfuscated formats like [dot], (dot), [at], and (at)

It also supports optional classification of links into predefined or user-defined categories 
such as LinkedIn, GitHub, Portfolio, and custom labels.

Classes:
    LinkExtractor: Extracts and optionally classifies links from text.
    
Dependencies:
    - re: for efficient regex matching
    - collections: for efficient data structures and operations
    - typing: for type hints and annotations

Typical Use Cases:
    - Resume parsing and enrichment
    - Candidate sourcing and contact extraction
    - Lead generation and scraping
    - Text mining and NLP pipelines
"""


import re
from typing import List, Dict, Optional, Union


class LinkExtractor:
    """
    A utility class to extract and optionally classify hyperlinks from unstructured text such as resumes.
    It can handle standard URLs, www-prefixed domains, and bare domains, including common obfuscations
    like '[dot]' and '(at)'.

    Attributes:
        custom_domains (Optional[Dict[str, List[str]]]): Optional custom domain mappings for classification.
        strict_mode (bool): If True, excludes bare domains (e.g., 'linkedin.com') from results.
    """

    def __init__(self, custom_domains: Optional[Dict[str, List[str]]] = None, strict_mode: bool = False):
        """
        Initializes the LinkExtractor.

        Args:
            custom_domains (Optional[Dict[str, List[str]]]): Custom domain classification mappings.
            strict_mode (bool): Whether to exclude bare domains from results.
        """
        self.custom_domains = custom_domains or {}
        self.strict_mode = strict_mode

    def extract(self, text: str, classify: bool = False) -> Union[List[str], Dict[str, List[str]]]:
        """
        Extract and optionally classify links from the input text.

        Args:
            text (str): The unstructured text (e.g., resume content).
            classify (bool): If True, categorize the links by type.

        Returns:
            Union[List[str], Dict[str, List[str]]]: A list of extracted links, or a categorized dictionary.
        """
        raw_links = set()

        # Normalize obfuscations
        text = text.replace("[dot]", ".").replace("(dot)", ".").replace(" dot ", ".")
        text = text.replace("[at]", "@").replace("(at)", "@").replace(" at ", "@")

        # --- 1. Full http/https links ---
        full_links = re.findall(r'https?://[^\s\)\]\>\.,;]+', text)
        raw_links.update(link.strip(".,);>]") for link in full_links)

        # --- 2. www-prefixed domains ---
        www_links = re.findall(r'www\.[\w\-\.]+\.\w+', text)
        raw_links.update(f"https://{link.strip('.,);>]')}" for link in www_links)

        # --- 3. Bare domains (only if strict_mode is False) ---
        if not self.strict_mode:
            bare_domains = re.findall(r'\b(?:[\w\-]+\.)+(?:com|org|io|net|co|ai|dev|info)\b', text, re.IGNORECASE)
            raw_links.update(f"https://{domain.strip('.,);>]')}" for domain in bare_domains)

        clean_links = sorted(set(raw_links))

        if not classify:
            return clean_links

        # --- 4. Classification ---
        categories = {
            "LinkedIn": [],
            "GitHub": [],
            "Portfolio": [],
            "Other": []
        }

        for cat in self.custom_domains:
            categories.setdefault(cat, [])

        for link in clean_links:
            l = link.lower()
            if "linkedin.com" in l:
                categories["LinkedIn"].append(link)
            elif "github.com" in l:
                categories["GitHub"].append(link)
            elif any(sub in l for sub in ["about.me", "portfolio", "my.site", "personal", "me."]):
                categories["Portfolio"].append(link)
            elif self.custom_domains:
                matched = False
                for label, domains in self.custom_domains.items():
                    if any(domain in l for domain in domains):
                        categories[label].append(link)
                        matched = True
                        break
                if not matched:
                    categories["Other"].append(link)
            else:
                categories["Other"].append(link)

        return categories
