---
title: Demo Gallery
description: Explore hands-on demos showcasing how TiDB empowers AI applications. Get started quickly with TiDB Cloud Starter to build your own AI-powered solutions.
hide:
  - navigation
  - toc
  - pageTitle
  - editButton 
---

<style>

/* CSS Variables */
:root {
  --brand-color: #de243d;
  --brand-hover: #b71e34;
  --border-radius-sm: 0.5rem;
  --border-radius-md: 0.75rem;
  --border-radius-lg: 1rem;
  --spacing-sm: 1rem;
  --spacing-md: 2rem;
  --spacing-lg: 3rem;
  --transition-fast: 0.2s;
  --transition-normal: 0.3s;
  --dark-overlay: rgba(255, 255, 255, 0.08);
  --dark-border: rgba(255, 255, 255, 0.1);
  --dark-bg-subtle: rgba(255, 255, 255, 0.05);
}

/* Smooth scrolling for the entire page */
html {
  scroll-behavior: smooth;
}

/* Gallery Container */
.gallery-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--spacing-md) var(--spacing-sm);
}

/* Header */
.gallery-header {
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.gallery-title {
  font-size: 72px !important;
  font-weight: 800 !important;
  margin-bottom: 8px !important;
  line-height: 1 !important;
  color: var(--md-default-fg-color) !important;
}

.gallery-description {
  font-size: 22px !important;
  color: var(--md-default-fg-color--light) !important;
  padding: 0 120px;
  margin-bottom: 5rem !important;
}

/* Gallery CTA link styles */
.gallery-cta-link {
    position: relative;
    text-decoration: none;
    transition: all 0.3s ease-in-out;
}

.gallery-cta-link:hover {
    border-bottom: 3px solid var(--brand-color);
}


/* Layout */
.gallery-layout {
  display: flex;
  gap: var(--spacing-sm) !important;
}

/* Sidebar */
.gallery-sidebar {
  width: 8rem;
  flex-shrink: 0;
}

.sidebar-nav {
  position: sticky;
  top: 140px;
}

.sidebar-title {
  font-size: 14px !important;
  font-weight: 400 !important;
  color: var(--md-default-fg-color--light) !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.5rem 0 !important;
}

.sidebar-links {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-left: -12px;
}

.sidebar-link {
  display: block;
  padding: 8px 12px;
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  font-weight: 400 !important;
  color: var(--md-default-fg-color--light) !important;
  text-decoration: none !important;
  transition: all var(--transition-fast) ease;
  text-align: left;
  cursor: pointer;
}

.sidebar-link:hover {
  background-color: var(--md-default-fg-color--lightest) !important;
  color: var(--md-default-fg-color) !important;
  font-weight: 500 !important;
  transform: translateX(2px);
}

.sidebar-link:focus-visible {
  outline: 2px solid var(--brand-color);
  outline-offset: 2px;
}

/* Content */
.gallery-content {
  flex: 1;
  padding: 0 var(--spacing-lg);
}

.gallery-section {
  margin-bottom: var(--spacing-lg);
  scroll-margin-top: 120px;
}

.section-title {
  font-size: 24px !important;
  font-weight: 700 !important;
  color: var(--md-default-fg-color) !important;
  margin: 0 0 1.5rem 0 !important;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-sm) !important;
}

/* Cards */
.gallery-card {
  display: block;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  transition: all var(--transition-normal) ease;
  text-decoration: none !important;
  color: inherit;
}

.gallery-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--md-shadow-z2);
  text-decoration: none !important;
  outline: 2px solid var(--brand-color);
  outline-offset: 2px;
}


.gallery-card:hover .card-title {
  color: var(--brand-color) !important;
}

.card-image {
  height: 8rem;
  position: relative;
  overflow: hidden;
  background-color: var(--md-default-fg-color--lightest);
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-gradient {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
}

.card-badge {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.2rem 0.4rem;
  border-radius: 0.2rem;
  font-size: 0.5rem !important;
  font-weight: 500 !important;
}

.card-content {
  padding: 12px;
}

.card-title {
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  line-height: 1.5 !important;
  margin: 0 !important;
  color: var(--md-default-fg-color) !important;
}

.card-description {
  color: var(--md-default-fg-color--light) !important;
  font-size: 0.65rem !important;
  line-height: 1.5;
  display: -webkit-box;
  margin: 0;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* CTA */
.gallery-cta {
  background: linear-gradient(135deg, rgba(222, 36, 61, 0.08) 0%, rgba(99, 102, 241, 0.08) 100%);
  border: 1px solid rgba(222, 36, 61, 0.1);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-md);
  text-align: center;
  margin-top: var(--spacing-lg);
}

.cta-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--md-default-fg-color);
  margin-bottom: var(--spacing-sm);
}

.cta-description {
  color: var(--md-default-fg-color--light);
  margin: 0 auto var(--spacing-md);
  max-width: 42rem;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

/* Button shared styles */
.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  text-decoration: none !important;
  transition: all var(--transition-fast);
}

.btn-primary {
  background-color: var(--brand-color);
  color: white !important;
}

.btn-primary:hover {
  background-color: var(--brand-hover);
  color: white !important;
}

.btn-secondary {
  border: 1px solid var(--md-default-fg-color--lighter);
  background-color: var(--md-default-bg-color);
  color: var(--md-default-fg-color) !important;
}

.btn-secondary:hover {
  background-color: var(--md-default-fg-color--lightest);
  color: var(--md-default-fg-color) !important;
}

/* Dark mode styles */
[data-md-color-scheme="tidb-dark"] .sidebar-link:hover {
  background-color: var(--dark-overlay) !important;
}

[data-md-color-scheme="tidb-dark"] .gallery-card {
  border-color: var(--dark-border);
}

[data-md-color-scheme="tidb-dark"] .card-image {
  background-color: var(--dark-bg-subtle);
  border-bottom-color: var(--dark-border);
}

[data-md-color-scheme="tidb-dark"] .gallery-cta {
  background: linear-gradient(135deg, rgba(222, 36, 61, 0.12) 0%, rgba(99, 102, 241, 0.12) 100%);
  border-color: rgba(222, 36, 61, 0.2);
}

[data-md-color-scheme="tidb-dark"] .btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .gallery-layout { flex-direction: column; }
  .gallery-sidebar { width: 100%; }
  .sidebar-nav { position: static; }
  .sidebar-links { flex-direction: row; gap: 0.5rem; flex-wrap: wrap; }
  .sidebar-link { padding: 12px 16px !important; min-height: 44px; display: flex; align-items: center; }
  .gallery-content { padding: 0; }
  .gallery-description { padding: 0 20px; }
  .cards-grid { grid-template-columns: 1fr; }
  .gallery-title { font-size: 48px !important; }
}

@media (max-width: 1024px) and (min-width: 769px) {
  .cards-grid { grid-template-columns: repeat(2, 1fr); }
}

</style>



<div class="gallery-container">
  <div class="gallery-header">
    <h1 class="gallery-title">Demo Gallery</h1>
    <p class="gallery-description">
      Explore hands-on demos showcasing how TiDB empowers AI applications.<br>
Get started quickly with <a href='https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=demo_gallery' target='_blank' rel='noopener noreferrer' class='gallery-cta-link'><b>TiDB Cloud Starter</b></a> to build your own AI-powered solutions.

    </p>
  </div>

  <div class="gallery-layout">
    <div class="gallery-sidebar">
      <div class="sidebar-nav">
        <h6 class="sidebar-title">Categories</h6>
                          <nav class="sidebar-links">
            <a href="#featured" class="sidebar-link">Featured</a>
            <a href="#getting-started" class="sidebar-link">Getting Started</a>
            <a href="#search" class="sidebar-link">Search & Retrieval</a>
            <a href="#ai-apps" class="sidebar-link">AI Applications</a>
        </nav>
      </div>
    </div>
              <div class="gallery-content">
        <section id="featured" class="gallery-section">
        <h2 class="section-title">⭐ Featured</h2>
        <div class="cards-grid">
          <a href="image-search-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/7ba9733a-4d1f-4094-8edb-58731ebd08e9" alt="Image Search Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Image Search</h3>
              <p class="card-description">
                Build an image search application using multimodal embeddings for both text-to-image and image-to-image search.
              </p>
            </div>
          </a>
          <a href="rag-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/dfd85672-65ce-4a46-8dd2-9f77d826363e" alt="RAG Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">RAG</h3>
              <p class="card-description">
                Build a RAG application that combines document retrieval with language generation.
              </p>
            </div>
          </a>
          <a href="memory-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/74dee96b-ea20-49dc-ad27-679faa5bf9b8" alt="Memory Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Memory</h3>
              <p class="card-description">
                Implement conversation memory for chatbots and conversational AI applications.
              </p>
            </div>
          </a>
        </div>
      </section>
        <section id="getting-started" class="gallery-section">
        <h2 class="section-title">🚀 Getting Started</h2>
        <div class="cards-grid">
          <a href="basic-with-pytidb/" class="gallery-card">
            <div class="card-image card-gradient" style="background: linear-gradient(135deg, #10b981, var(--brand-color));">
              <div>⚙️</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">Basic Usage</h3>
              <p class="card-description">
                Learn fundamental PyTiDB operations including database connection, table creation, and data manipulation.
              </p>
            </div>
          </a>
          <a href="auto-embedding-with-pytidb/" class="gallery-card">
            <div class="card-image card-gradient" style="background: radial-gradient(circle at center, #8b5cf6 0%, var(--brand-color) 100%);">
              <div>🤖</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">Auto Embedding</h3>
              <p class="card-description">
                Automatically generate embeddings for your text data using built-in embedding models.
              </p>
            </div>
          </a>
        </div>
      </section>
        <section id="search" class="gallery-section">
        <h2 class="section-title">🔍 Search & Retrieval</h2>
        <div class="cards-grid">
          <a href="vector-search-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/6d7783a5-ce9c-4dcc-8b95-49d5f0ca735a" alt="Vector Search Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Vector Search</h3>
              <p class="card-description">
                Implement semantic search using vector embeddings to find similar content.
              </p>
            </div>
          </a>
          <a href="fulltext-search-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/c81ddad4-f996-4b1f-85c0-5cbb55bc2a3a" alt="Fulltext Search Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Fulltext Search</h3>
              <p class="card-description">
                Perform traditional text search using MySQL fulltext search capabilities.
              </p>
            </div>
          </a>
          <a href="hybrid-search-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/6e1c639d-2160-44c8-86b4-958913b9eca5" alt="Hybrid Search Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Hybrid Search</h3>
              <p class="card-description">
                Combine vector search and fulltext search for more comprehensive results.
              </p>
            </div>
          </a>
          <a href="image-search-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/7ba9733a-4d1f-4094-8edb-58731ebd08e9" alt="Image Search Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Image Search</h3>
              <p class="card-description">
                Build an image search application using multimodal embeddings for both text-to-image and image-to-image search.
              </p>
            </div>
          </a>
        </div>
      </section>
        <section id="ai-apps" class="gallery-section">
        <h2 class="section-title">🤖 AI Applications</h2>
        <div class="cards-grid">
          <a href="rag-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/dfd85672-65ce-4a46-8dd2-9f77d826363e" alt="RAG Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">RAG</h3>
              <p class="card-description">
                Build a RAG application that combines document retrieval with language generation.
              </p>
            </div>
          </a>
          <a href="memory-with-pytidb/" class="gallery-card">
            <div class="card-image">
              <img src="https://github.com/user-attachments/assets/74dee96b-ea20-49dc-ad27-679faa5bf9b8" alt="Memory Demo">
            </div>
            <div class="card-content">
              <h3 class="card-title">Memory</h3>
              <p class="card-description">
                Implement conversation memory for chatbots and conversational AI applications.
              </p>
            </div>
          </a>
          <a href="text2sql-with-pytidb/" class="gallery-card">
            <div class="card-image card-gradient" style="background: linear-gradient(135deg, #06b6d4, var(--brand-color));">
              <div>💬</div>
            </div>
            <div class="card-content">
              <h3 class="card-title">Text2SQL</h3>
              <p class="card-description">
                Convert natural language queries into SQL statements using AI models.
              </p>
            </div>
          </a>
        </div>
      </section>
      <div class="gallery-cta">
        <h3 class="cta-title">Ready to build your AI application?</h3>
        <p class="cta-description">
          Start your AI journey with TiDB Cloud Starter. Follow our quickstart guide to build your first AI-powered application in minutes, or explore specific examples for your use case.
        </p>
        <div class="cta-buttons">
          <a href="https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme" target="_blank" rel="noopener noreferrer" class="btn-primary">Try TiDB Cloud Starter</a>
          <a href="/ai/quickstart/" class="btn-secondary">View Quickstart Guide</a>
        </div>
      </div>
    </div>
  </div>
</div> 