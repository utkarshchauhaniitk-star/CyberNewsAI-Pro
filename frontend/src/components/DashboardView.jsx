import React from 'react';
import { 
  ShieldAlert, 
  Flame, 
  Bug, 
  Layers, 
  ArrowRight, 
  Radio, 
  Zap, 
  Clock, 
  ExternalLink,
  ChevronRight,
  Pin,
  RefreshCw
} from 'lucide-react';

export default function DashboardView({ 
  stats, 
  latestArticles = [], 
  onSelectTab, 
  onOpenArticle,
  onFilterCategory,
  onFilterSeverity,
  onFilterCveOnly,
  onRefresh,
  isRefreshing
}) {
  const criticalStories = latestArticles.filter(a => a.severity === 'Critical').slice(0, 5);
  const total = stats?.total_articles || 1;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      
      {/* Top Futuristic KPI Metric Cards (All Clickable!) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))',
        gap: '1.25rem'
      }}>
        
        {/* Total Stories -> Click to view Feed */}
        <div 
          onClick={() => onSelectTab('feed')}
          className="hud-panel" 
          style={{ padding: '1.35rem', cursor: 'pointer', transition: 'all 0.2s ease' }}
          title="Click to view all live stories in feed"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                // TOTAL THREATS INDEXED
              </div>
              <div style={{ fontSize: '2.3rem', fontWeight: 800, color: 'var(--neon-cyan)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
                {stats?.total_articles ?? '—'}
              </div>
            </div>
            <div style={{
              padding: '0.65rem',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--neon-cyan-glow)',
              border: '1px solid var(--neon-cyan)'
            }}>
              <Radio size={20} color="var(--neon-cyan)" />
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--neon-cyan)', marginTop: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <span>Click to explore live stream</span> <ArrowRight size={13} />
          </div>
        </div>

        {/* Critical Alerts -> Click to filter by Critical */}
        <div 
          onClick={() => {
            onFilterSeverity('Critical');
            onSelectTab('feed');
          }}
          className="hud-panel" 
          style={{ padding: '1.35rem', cursor: 'pointer', transition: 'all 0.2s ease' }}
          title="Click to filter feed by Critical zero-days"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                // CRITICAL ZERO-DAYS
              </div>
              <div style={{ fontSize: '2.3rem', fontWeight: 800, color: 'var(--neon-crimson)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
                {stats?.critical_threats ?? '—'}
              </div>
            </div>
            <div style={{
              padding: '0.65rem',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--neon-crimson-glow)',
              border: '1px solid var(--neon-crimson)'
            }}>
              <Flame size={20} color="var(--neon-crimson)" />
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--neon-crimson)', marginTop: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <span className="live-beacon red"></span> Filter by Critical Threats <ArrowRight size={13} />
          </div>
        </div>

        {/* Detected CVEs -> Click to toggle CVE filter */}
        <div 
          onClick={() => {
            onFilterCveOnly(true);
            onSelectTab('feed');
          }}
          className="hud-panel" 
          style={{ padding: '1.35rem', cursor: 'pointer', transition: 'all 0.2s ease' }}
          title="Click to filter feed for stories with CVE IDs"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                // TRACKED CVE IDENTIFIERS
              </div>
              <div style={{ fontSize: '2.3rem', fontWeight: 800, color: 'var(--neon-purple)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
                {stats?.cve_count ?? '—'}
              </div>
            </div>
            <div style={{
              padding: '0.65rem',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--neon-purple-glow)',
              border: '1px solid var(--neon-purple)'
            }}>
              <Bug size={20} color="var(--neon-purple)" />
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--neon-purple)', marginTop: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <span>Filter for CVE Disclosures</span> <ArrowRight size={13} />
          </div>
        </div>

        {/* Active Feeds / Refresh */}
        <div 
          onClick={onRefresh}
          className="hud-panel" 
          style={{ padding: '1.35rem', cursor: 'pointer', transition: 'all 0.2s ease' }}
          title="Click to trigger live news sync now"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                // LIVE INGESTION FEEDS
              </div>
              <div style={{ fontSize: '2.3rem', fontWeight: 800, color: 'var(--neon-green)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
                5 FEEDS
              </div>
            </div>
            <div style={{
              padding: '0.65rem',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--neon-green-glow)',
              border: '1px solid var(--neon-green)'
            }}>
              <RefreshCw size={20} color="var(--neon-green)" style={{ animation: isRefreshing ? 'spin 0.8s linear infinite' : 'none' }} />
            </div>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--neon-green)', marginTop: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <span className="live-beacon"></span> Click to Sync Now <ArrowRight size={13} />
          </div>
        </div>

      </div>

      {/* Main Split: Urgent Zero-Day Stream vs Interactive Threat Matrix */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))',
        gap: '1.5rem'
      }}>
        
        {/* Urgent Critical Incident Stream */}
        <div className="hud-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1.25rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <ShieldAlert size={18} color="var(--neon-crimson)" />
              <h2 style={{ fontSize: '1.1rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                // PRIORITY ZERO-DAYS & CRITICAL THREATS
              </h2>
            </div>
            <button
              onClick={() => {
                onFilterSeverity('Critical');
                onSelectTab('feed');
              }}
              className="btn-cyber btn-cyber-sm btn-cyber-ghost"
            >
              VIEW ALL <ArrowRight size={13} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', flex: 1 }}>
            {criticalStories.length > 0 ? (
              criticalStories.map((story) => (
                <div
                  key={story.id}
                  onClick={() => onOpenArticle(story)}
                  className="cyber-card"
                  style={{
                    padding: '1rem 1.15rem',
                    cursor: 'pointer',
                    borderLeft: '3px solid var(--neon-crimson)'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', gap: '0.45rem', flexWrap: 'wrap' }}>
                      <span className="clickable-badge badge-critical">CRITICAL</span>
                      <span className="clickable-badge badge-source">{story.source}</span>
                      {story.cves?.map(cve => (
                        <span key={cve} className="clickable-badge badge-cve">{cve}</span>
                      ))}
                    </div>
                    <ChevronRight size={16} color="var(--text-muted)" />
                  </div>

                  <h3 style={{ fontSize: '0.94rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.4 }}>
                    {story.title}
                  </h3>

                  <p style={{
                    fontSize: '0.78rem',
                    color: 'var(--text-secondary)',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden'
                  }}>
                    {story.summary}
                  </p>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-muted)' }}>
                No active critical incidents right now. Telemetry nominal.
              </div>
            )}
          </div>
        </div>

        {/* Threat Distribution & Interactive Vectors */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Category Distribution Bars (Clickable!) */}
          <div className="hud-panel" style={{ padding: '1.5rem', flex: 1 }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, marginBottom: '0.4rem', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers size={18} color="var(--neon-cyan)" /> // THREAT CATEGORY SPECTRUM
            </h3>
            <p style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', fontFamily: 'var(--font-mono)' }}>
              Click any vector to immediately filter the real-time news radar:
            </p>

            {stats?.category_counts && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                {Object.entries(stats.category_counts)
                  .sort((a, b) => b[1] - a[1])
                  .map(([cat, count]) => {
                    const pct = Math.round((count / total) * 100);
                    return (
                      <div 
                        key={cat}
                        onClick={() => {
                          onFilterCategory(cat);
                          onSelectTab('feed');
                        }}
                        style={{ cursor: 'pointer', padding: '0.2rem 0' }}
                        title={`Filter feed for ${cat}`}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                          <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{cat}</span>
                          <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--neon-cyan)', fontWeight: 700 }}>
                            {count} ({pct}%)
                          </span>
                        </div>
                        <div style={{ height: '7px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                          <div style={{
                            width: `${pct}%`,
                            height: '100%',
                            background: 'linear-gradient(90deg, var(--neon-cyan), var(--neon-purple))',
                            boxShadow: '0 0 10px rgba(0, 242, 254, 0.5)',
                            borderRadius: '4px'
                          }} />
                        </div>
                      </div>
                    );
                  })}
              </div>
            )}
          </div>

        </div>

      </div>

    </div>
  );
}
