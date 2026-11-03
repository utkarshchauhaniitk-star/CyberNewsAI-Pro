import React from 'react';
import { 
  Search, 
  ExternalLink, 
  Sparkles, 
  Pin, 
  PinOff,
  ChevronLeft, 
  ChevronRight,
  ShieldAlert,
  Bug,
  RefreshCw,
  RotateCcw,
  Zap,
  Globe,
  Radio,
  Flame,
  Check
} from 'lucide-react';

export default function NewsFeedView({
  articles = [],
  total = 0,
  page = 1,
  totalPages = 1,
  onPageChange,
  searchQuery,
  onSearchChange,
  selectedCategory,
  onCategoryChange,
  selectedSource,
  onSourceChange,
  selectedSeverity,
  onSeverityChange,
  hasCveFilter,
  onCveFilterChange,
  pinnedOnlyFilter,
  onPinnedOnlyChange,
  categories = [],
  sources = [],
  onOpenArticle,
  onTogglePin,
  onRefresh,
  isRefreshing = false,
  isLoading = false
}) {
  const severities = ['All', 'Critical', 'High', 'Medium', 'Low'];
  const hasActiveFilters = searchQuery || selectedCategory !== 'All' || selectedSource !== 'All' || selectedSeverity !== 'All' || hasCveFilter !== null || pinnedOnlyFilter === true;

  const handleResetFilters = () => {
    onSearchChange('');
    onCategoryChange('All');
    onSourceChange('All');
    onSeverityChange('All');
    onCveFilterChange(null);
    if (onPinnedOnlyChange) onPinnedOnlyChange(null);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      
      {/* Real-time Ingestion Radar Bar & Live Refresh Banner */}
      <div className="hud-panel" style={{ padding: '1.25rem 1.5rem' }}>
        
        {/* Top Search & Live Triggers */}
        <div style={{ display: 'flex', gap: '0.85rem', flexWrap: 'wrap', marginBottom: '1rem', alignItems: 'center' }}>
          
          {/* Cyber Search Bar */}
          <div style={{ position: 'relative', flex: 1, minWidth: '280px' }}>
            <Search 
              size={17} 
              color="var(--neon-cyan)" 
              style={{ position: 'absolute', left: '0.9rem', top: '50%', transform: 'translateY(-50%)' }} 
            />
            <input
              type="text"
              className="cyber-input"
              placeholder="SEARCH THREAT DISCLOSURES, ZERO-DAYS, RANSOMWARE, CVEs..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              style={{ paddingLeft: '2.6rem', fontFamily: 'var(--font-mono)', fontSize: '0.82rem' }}
            />
          </div>

          {/* Clickable Source Dropdown */}
          <div style={{ minWidth: '170px' }}>
            <select
              className="cyber-input"
              value={selectedSource}
              onChange={(e) => onSourceChange(e.target.value)}
              style={{ cursor: 'pointer', fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}
            >
              {sources.map(src => (
                <option key={src} value={src} style={{ background: '#091120' }}>
                  SOURCE: {src.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Clickable Severity Dropdown */}
          <div style={{ minWidth: '150px' }}>
            <select
              className="cyber-input"
              value={selectedSeverity}
              onChange={(e) => onSeverityChange(e.target.value)}
              style={{ cursor: 'pointer', fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}
            >
              {severities.map(sev => (
                <option key={sev} value={sev} style={{ background: '#091120' }}>
                  SEVERITY: {sev.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          {/* Clickable CVE Filter Toggle */}
          <button
            onClick={() => onCveFilterChange(hasCveFilter === true ? null : true)}
            className={`btn-cyber btn-cyber-sm ${hasCveFilter === true ? 'btn-cyber-primary' : 'btn-cyber-ghost'}`}
            title="Filter feed exclusively for stories with CVE identifiers"
          >
            <Bug size={14} />
            CVE ONLY
          </button>

          {/* Clickable Pinned Filter Toggle */}
          <button
            onClick={() => onPinnedOnlyChange(pinnedOnlyFilter === true ? null : true)}
            className={`btn-cyber btn-cyber-sm ${pinnedOnlyFilter === true ? 'btn-cyber-primary' : 'btn-cyber-ghost'}`}
            title="Show only bookmarked / pinned threats"
          >
            <Pin size={14} />
            PINNED
          </button>

          {/* Reset Filters Button */}
          {hasActiveFilters && (
            <button
              onClick={handleResetFilters}
              className="btn-cyber btn-cyber-sm btn-cyber-crimson"
              title="Reset all active filters"
            >
              <RotateCcw size={13} />
              RESET
            </button>
          )}

          {/* Live Ingestion Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="btn-cyber btn-cyber-live"
            style={{ padding: '0.55rem 1rem' }}
            title="Fetch live news directly from 5 RSS sources right now"
          >
            <RefreshCw 
              size={15} 
              style={{ animation: isRefreshing ? 'spin 0.8s linear infinite' : 'none' }} 
            />
            {isRefreshing ? 'STREAMING...' : 'LIVE REFRESH'}
          </button>
        </div>

        {/* Clickable Category Filter Chips */}
        <div style={{
          display: 'flex',
          gap: '0.5rem',
          overflowX: 'auto',
          paddingBottom: '0.2rem',
          scrollbarWidth: 'none'
        }}>
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => onCategoryChange(cat)}
                style={{
                  padding: '0.4rem 0.85rem',
                  borderRadius: 'var(--radius-full)',
                  fontSize: '0.74rem',
                  fontFamily: 'var(--font-mono)',
                  fontWeight: 600,
                  whiteSpace: 'nowrap',
                  cursor: 'pointer',
                  background: isSelected ? 'var(--neon-cyan)' : 'rgba(255, 255, 255, 0.03)',
                  color: isSelected ? '#030814' : 'var(--text-secondary)',
                  border: isSelected ? '1px solid var(--neon-cyan)' : '1px solid var(--border-dim)',
                  boxShadow: isSelected ? '0 0 15px rgba(0, 242, 254, 0.5)' : 'none',
                  transition: 'all 0.18s cubic-bezier(0.16, 1, 0.3, 1)',
                  userSelect: 'none'
                }}
                onMouseEnter={(e) => {
                  if (!isSelected) {
                    e.currentTarget.style.color = '#fff';
                    e.currentTarget.style.borderColor = 'var(--neon-cyan)';
                    e.currentTarget.style.boxShadow = '0 0 10px rgba(0, 242, 254, 0.25)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isSelected) {
                    e.currentTarget.style.color = 'var(--text-secondary)';
                    e.currentTarget.style.borderColor = 'var(--border-dim)';
                    e.currentTarget.style.boxShadow = 'none';
                  }
                }}
              >
                {cat.toUpperCase()}
              </button>
            );
          })}
        </div>

      </div>

      {/* Stream Metrics Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <span className="live-beacon"></span>
          <span style={{ fontSize: '0.82rem', fontFamily: 'var(--font-mono)', color: 'var(--neon-cyan)' }}>
            LIVE STREAM: <strong style={{ color: '#fff' }}>{articles.length}</strong> ACTIVE INCIDENTS (TOTAL INDEXED: {total})
          </span>
        </div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
          PAGE {page} OF {totalPages}
        </div>
      </div>

      {/* Live Cyber News Grid */}
      {isLoading ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
          gap: '1.35rem'
        }}>
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="skeleton-cyber" style={{ height: '260px' }} />
          ))}
        </div>
      ) : articles.length > 0 ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
          gap: '1.35rem'
        }}>
          {articles.map((art) => {
            const severityClass = 
              art.severity === 'Critical' ? 'badge-critical' :
              art.severity === 'High' ? 'badge-high' :
              art.severity === 'Low' ? 'badge-low' : 'badge-medium';

            return (
              <div
                key={art.id}
                className="cyber-card"
                style={{
                  borderLeft: art.severity === 'Critical' ? '3px solid var(--neon-crimson)' : '1px solid var(--border-dim)',
                  boxShadow: art.is_pinned ? '0 0 18px rgba(168, 85, 247, 0.25)' : undefined
                }}
              >
                <div>
                  {/* Top Badges Row (All Clickable!) */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.85rem' }}>
                    <div style={{ display: 'flex', gap: '0.45rem', flexWrap: 'wrap', alignItems: 'center' }}>
                      
                      {/* Clickable Severity Badge -> Filters by this severity */}
                      <span 
                        className={`clickable-badge ${severityClass}`}
                        onClick={() => onSeverityChange(art.severity)}
                        title={`Filter feed by ${art.severity} severity`}
                      >
                        {art.severity === 'Critical' && <Flame size={12} />}
                        {art.severity}
                      </span>

                      {/* Clickable Source Badge -> Filters by this source */}
                      <span 
                        className="clickable-badge badge-source"
                        onClick={() => onSourceChange(art.source)}
                        title={`Filter feed by source: ${art.source}`}
                      >
                        {art.source}
                      </span>

                      {/* Clickable Category Badge -> Filters by this category */}
                      <span 
                        className="clickable-badge"
                        style={{ background: 'rgba(0, 242, 254, 0.08)', color: 'var(--neon-cyan)', borderColor: 'rgba(0, 242, 254, 0.25)' }}
                        onClick={() => onCategoryChange(art.category)}
                        title={`Filter feed by category: ${art.category}`}
                      >
                        {art.category}
                      </span>

                      {/* Clickable CVE Badges -> Filters by this exact CVE */}
                      {art.cves?.map(cve => (
                        <span 
                          key={cve} 
                          className="clickable-badge badge-cve"
                          onClick={() => onSearchChange(cve)}
                          title={`Click to filter news for ${cve}`}
                        >
                          <Bug size={11} />
                          {cve}
                        </span>
                      ))}
                    </div>

                    {/* Clickable Pin Threat Button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onTogglePin(art.id);
                      }}
                      className="btn-cyber btn-cyber-sm"
                      style={{
                        padding: '0.25rem 0.45rem',
                        background: art.is_pinned ? 'var(--neon-purple-glow)' : 'transparent',
                        borderColor: art.is_pinned ? 'var(--neon-purple)' : 'var(--border-dim)',
                        color: art.is_pinned ? '#fff' : 'var(--text-muted)'
                      }}
                      title={art.is_pinned ? 'Unpin this threat' : 'Pin / Bookmark this threat'}
                    >
                      {art.is_pinned ? <Pin size={15} color="var(--neon-purple)" /> : <Pin size={15} />}
                    </button>
                  </div>

                  {/* Clickable Article Title -> Opens Analysis Modal */}
                  <h3 
                    onClick={() => onOpenArticle(art)}
                    style={{
                      fontSize: '1.02rem',
                      fontWeight: 700,
                      color: 'var(--text-primary)',
                      lineHeight: 1.42,
                      marginBottom: '0.65rem',
                      cursor: 'pointer',
                      transition: 'color 0.15s ease'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.color = 'var(--neon-cyan)'}
                    onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-primary)'}
                  >
                    {art.title}
                  </h3>

                  {/* Summary Snippet */}
                  <p style={{
                    fontSize: '0.82rem',
                    color: 'var(--text-secondary)',
                    lineHeight: 1.55,
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden'
                  }}>
                    {art.ai_summary || art.summary || 'Click to view technical threat intelligence assessment.'}
                  </p>
                </div>

                {/* Card Footer Actions (All Clickable!) */}
                <div style={{
                  borderTop: '1px solid rgba(255, 255, 255, 0.06)',
                  paddingTop: '0.85rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '0.5rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <button
                      onClick={() => onOpenArticle(art)}
                      className="btn-cyber btn-cyber-sm btn-cyber-primary"
                      title="Inspect full advisory telemetry"
                    >
                      TELEMETRY
                    </button>

                    <button
                      onClick={() => onOpenArticle(art)}
                      className="btn-cyber btn-cyber-sm btn-cyber-ghost"
                      title="View AI Threat Analysis"
                    >
                      <Sparkles size={13} color="var(--neon-cyan)" />
                      AI INTEL
                    </button>
                  </div>

                  {/* Clickable Safe External Link */}
                  <a
                    href={art.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="clickable-badge badge-source"
                    style={{ textDecoration: 'none', gap: '0.3rem', fontSize: '0.74rem' }}
                    title={`Open original report on ${art.source}`}
                  >
                    ORIGINAL <ExternalLink size={12} />
                  </a>
                </div>

              </div>
            );
          })}
        </div>
      ) : (
        <div className="hud-panel" style={{ padding: '3.5rem 2rem', textAlign: 'center' }}>
          <ShieldAlert size={42} color="var(--neon-cyan)" style={{ margin: '0 auto 1.25rem' }} />
          <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '0.5rem', fontFamily: 'var(--font-mono)' }}>
            NO INCIDENTS MATCH CURRENT RADAR FILTER
          </h3>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Adjust your search keywords, clear category selections, or trigger a live refresh.
          </p>
          <button onClick={handleResetFilters} className="btn-cyber btn-cyber-primary">
            RESET ALL FILTERS
          </button>
        </div>
      )}

      {/* Clickable Pagination Controls */}
      {totalPages > 1 && (
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '1rem',
          padding: '1.75rem 0'
        }}>
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className="btn-cyber btn-cyber-ghost"
          >
            <ChevronLeft size={16} /> PREV
          </button>

          <span style={{ fontSize: '0.85rem', fontFamily: 'var(--font-mono)', color: 'var(--neon-cyan)' }}>
            // PAGE {page} OF {totalPages}
          </span>

          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages}
            className="btn-cyber btn-cyber-ghost"
          >
            NEXT <ChevronRight size={16} />
          </button>
        </div>
      )}

    </div>
  );
}
