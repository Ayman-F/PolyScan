#!/usr/bin/env python3
import boto3
import sys
import os
import time
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

# Initialize Bedrock client
bedrock = boto3.client(
    'bedrock-runtime',
    config=boto3.session.Config(
        read_timeout=300,
        connect_timeout=60,
        retries={'max_attempts': 2}
    )
)

def extract_sentences_from_text(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

def read_txt_sentences(txt_path: str):
    """Read sentences from TXT file"""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return extract_sentences_from_text(content)
    except Exception as e:
        print(f"❌ Error reading TXT file: {e}")
        return []

def read_html_sentences(html_path: str):
    """Read sentences from HTML file"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        return extract_sentences_from_text(text)
    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
        return []

def read_file_sentences(file_path: str):
    """Read sentences from any supported file type"""
    ext = file_path.lower().split('.')[-1]
    
    if ext == 'xml':
        return read_xml_sentences(file_path)
    elif ext == 'html':
        return read_html_sentences(file_path)
    elif ext == 'txt':
        return read_txt_sentences(file_path)
    else:
        print(f"❌ Unsupported file type: {ext}")
        return []

def read_xml_sentences(xml_path: str):
    sentences = []
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fast regex-based text extraction instead of XML parsing
        import re
        
        # Remove XML tags but keep text content
        text = re.sub(r'<[^>]+>', ' ', content)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove XML declarations and processing instructions
        text = re.sub(r'<\?[^>]*\?>', '', text)
        
        # Limit text size for faster processing
        if len(text) > 50000:  # Limit to 50k characters
            text = text[:50000] + "... [truncated for performance]"
        
        xml_sentences = extract_sentences_from_text(text)
        
        # Limit number of sentences for faster processing
        if len(xml_sentences) > 200:  # Limit to 200 sentences
            xml_sentences = xml_sentences[:200]
            sentences.extend([f"XML Phrase {i+1}: {sentence}" for i, sentence in enumerate(xml_sentences)])
            sentences.append("XML Phrase 201: [Additional content truncated for performance]")
        else:
            sentences.extend([f"XML Phrase {i+1}: {sentence}" for i, sentence in enumerate(xml_sentences)])
        
        return sentences
        
    except Exception as e:
        print(f"❌ Error reading XML: {e}")
        return []

def analyze_chunk(sentences, chunk_num, total_chunks):
    content = "\n".join(sentences)
    
    prompt = f"""Extract key information from this regulatory document chunk {chunk_num}/{total_chunks}:

{content}

Extract:
1. Key provisions and financial amounts
2. Affected sectors and companies
3. Implementation timelines
4. Economic impacts

Be concise and factual."""
    
    try:
        response = bedrock.converse(
            modelId="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 1500, "temperature": 0.1}
        )
        return response['output']['message']['content'][0]['text']
    except Exception as e:
        return f"Chunk {chunk_num} analysis failed: {e}"

def fusion_analysis(chunk_results):
    combined_content = "\n\n".join(chunk_results)
    
    prompt = f"""Based on these chunk analyses of a regulatory bill, provide a consolidated report:

{combined_content}

Provide EXACTLY this structure:

1. BILL SUMMARY:
[Key facts about the bill - what it does, main provisions, budget amounts]

2. TOP 5 IMPACTED SECTORS:
Sector 1: [Name] - Impact Score: [1-10] - [Description]
Sector 2: [Name] - Impact Score: [1-10] - [Description] 
Sector 3: [Name] - Impact Score: [1-10] - [Description]
Sector 4: [Name] - Impact Score: [1-10] - [Description]
Sector 5: [Name] - Impact Score: [1-10] - [Description]

3. TOP 3 STOCKS PER SECTOR:
Sector 1 Stocks:
- [TICKER]: [Company] - [Impact description]
- [TICKER]: [Company] - [Impact description]
- [TICKER]: [Company] - [Impact description]

Sector 2 Stocks:
- [TICKER]: [Company] - [Impact description]
- [TICKER]: [Company] - [Impact description] 
- [TICKER]: [Company] - [Impact description]

[Continue for all 5 sectors]

4. MARKET PREDICTIONS:
Mid-term (6-18 months): [Predictions]
Long-term (2-5 years): [Predictions]

Be specific with company names and stock tickers."""
    
    try:
        response = bedrock.converse(
            modelId="global.anthropic.claude-sonnet-4-5-20250929-v1:0",
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 3000, "temperature": 0.1}
        )
        return response['output']['message']['content'][0]['text']
    except Exception as e:
        return f"Fusion analysis failed: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python chunked_analyzer.py <file>")
        return
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"🚀 Starting Complete Document Analysis")
    print(f"📄 File: {file_path}")
    
    # print(f"🚀 Starting Complete Document Analysis")
    # print(f"📄 File: {file_path}")
    
    sentences = read_file_sentences(file_path)
    if not sentences:
        return
    
    # Smaller chunks for faster processing
    chunk_size = 400  # Reduced from 800
    chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]
    
    # print(f"\n⏱️ Analysis will take approximately {len(chunks) * 30} seconds...")
    # print(f"📊 Processing {len(sentences)} sentences in {len(chunks)} chunks")
    
    results = []
    
    for i, chunk in enumerate(chunks, 1):
        # print(f"\n🔄 Analyzing chunk {i}/{len(chunks)}...")
        start_time = time.time()
        
        result = analyze_chunk(chunk, i, len(chunks))
        results.append(f"CHUNK {i}:\n{result}")
        
        elapsed = int(time.time() - start_time)
        # print(f"✅ Chunk {i} completed in {elapsed}s")
    
    # print("\n🔄 Consolidating analysis...")
    start_time = time.time()
    
    final_report = fusion_analysis(results)
    
    elapsed = int(time.time() - start_time)
    # print(f"✅ Consolidation completed in {elapsed}s")
    
    print("="*80)
    print("📊 CONSOLIDATED FINANCIAL IMPACT ANALYSIS")
    print("="*80)
    print(final_report)
    print("="*80)
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"consolidated_analysis_{base_name}.txt"
    with open(output_file, 'w') as f:
        f.write(final_report)
    # print(f"\n💾 Consolidated analysis saved to: {output_file}")

if __name__ == "__main__":
    main()