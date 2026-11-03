import React, { useState } from 'react';
import { 
  BarChart3, 
  Flame, 
  ShieldAlert, 
  Bug, 
  Rss, 
  Check, 
  Copy,
  ExternalLink,
  Activity,
  Zap,
  Layers
} from 'lucide-react';

export default function ThreatStatsView({ stats, onFilterCategory, onFilterSeverity, onFilterCve }) {
  const [copiedCve, setCopiedCve] = useState(null);

  if (!stats) {
    return (
      <div className="hud-panel" style={{ padding: '3rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>// COMPUTING THREAT INTELLIGENCE TELEMETRY...</p>
      </div>
    );
  }

  const handleCopyCve = (cve) => {
    navigator.clipboard.writeText(cve);
    setCopiedCve(cve);
    setTimeout(() => setCopiedCve(null), 1800);
  };

  const total = stats.total_articles || 1;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      
      {/* Top Posture Banner */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))',
        gap: '1.25rem'
      }}>
        <div className="hud-panel" style={{ padding: '1.35rem' }}>
          <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
            // GLOBAL INCIDENT COUNT
          </div>
          <div style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--neon-cyan)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
            {stats.total_articles}
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '0.4rem', fontFamily: 'var(--font-mono)' }}>
            Persisted in SQLite database
          </div>
        </div>

        <div className="hud-panel" style={{ padding: '1.35rem' }}>
          <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
            // CRITICAL & HIGH THREATS
          </div>
          <div style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--neon-crimson)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
            {stats.critical_threats + stats.high_threats}
          </div>
          <div style={{ fontSize: '0.74rem', color: '#ff85a2', marginTop: '0.4rem', fontFamily: 'var(--font-mono)' }}>
            {Math.round(((stats.critical_threats + stats.high_threats) / total) * 100)}% of total indexed threat posture
          </div>
        </div>

        <div className="hud-panel" style={{ padding: '1.35rem' }}>
          <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
            // EXTRACTED CVE IDENTIFIERS
          </div>
          <div style={{ fontSize: '2.4rem', fontWeight: 800, color: 'var(--neon-purple)', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>
            {stats.cve_count}
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '0.4rem', fontFamily: 'var(--font-mono)' }}>
            Unique vulnerability designations
          </div>
        </div>

        <div className="hud-panel" style={{ padding: '1.35rem' }}>
          <div style={{ fontSize: '0.72rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
            // TELEMETRY REFRESH STATUS
          </div>
          <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--neon-green)', marginTop: '0.75rem', fontFamily: 'var(--font-mono)' }}>
            SYNCHRONIZED
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '0.4rem', fontFamily: 'var(--font-mono)' }}>
            Real-time multi-threaded ingestion
          </div>
        </div>
      </div>

      {/* Grid: Severity Distribution & Category Breakdown */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))',
        gap: '1.5rem'
      }}>
        
        {/* Severity Breakdown (Clickable rows!) */}
        <div className="hud-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '1.25rem', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Flame size={18} color="var(--neon-crimson)" /> // SEVERITY RISK PROFILE (CLICKABLE)
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { label: 'Critical', count: stats.critical_threats, color: 'var(--neon-crimson)' },
              { label: 'High', count: stats.high_threats, color: 'var(--neon-amber)' },
              { label: 'Medium', count: stats.medium_threats, color: 'var(--neon-cyan)' },
              { label: 'Low', count: stats.low_threats, color: 'var(--neon-green)' }
            ].map(item => {
              const pct = Math.round((item.count / total) * 100);
              return (
                <div 
                  key={item.label}
                  onClick={() => onFilterSeverity && onFilterSeverity(item.label)}
                  style={{ cursor: 'pointer', padding: '0.2rem 0' }}
                  title={`Click to filter feed for ${item.label} incidents`}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '0.4rem' }}>
                    <span style={{ fontWeight: 700, color: item.color, fontFamily: 'var(--font-mono)' }}>
                      {item.label.toUpperCase()}
                    </span>
                    <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-primary)' }}>
                      {item.count} incidents ({pct}%)
                    </span>
                  </div>
                  <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${pct}%`,
                      height: '100%',
                      background: item.color,
                      boxShadow: `0 0 10px ${item.color}`,
                      borderRadius: '4px'
                    }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Source Contribution Breakdown */}
        <div className="hud-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '1.25rem', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Rss size={18} color="var(--neon-cyan)" /> // MONITORED STREAM INGESTION METRICS
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {Object.entries(stats.source_counts || {}).map(([src, count]) => {
              const pct = Math.round((count / total) * 100);
              return (
                <div 
                  key={src} 
                  style={{
                    padding: '0.75rem 1rem',
                    borderRadius: 'var(--radius-sm)',
                    background: 'rgba(3, 6, 12, 0.65)',
                    border: '1px solid var(--border-neon)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <span className="live-beacon"></span>
                    <span style={{ fontSize: '0.86rem', fontWeight: 700, color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>
                      {src}
                    </span>
                  </div>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--neon-cyan)', fontWeight: 700 }}>
                    {count} stories ({pct}%)
                  </span>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Detected CVE Registry (All Clickable!) */}
      <div className="hud-panel" style={{ padding: '1.5rem' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '0.5rem', fontFamily: 'var(--font-mono)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Bug size={18} color="var(--neon-purple)" /> // EXTRACTED CVE IDENTIFIERS (CLICK TO FILTER OR COPY)
        </h3>
        <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', fontFamily: 'var(--font-mono)' }}>
          Click any CVE pill to immediately filter the news stream or use copy button:
        </p>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.55rem' }}>
          {(stats.recent_cves || []).map((cve) => (
            <div
              key={cve}
              className="clickable-badge badge-cve"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.35rem 0.75rem'
              }}
            >
              <span 
                onClick={() => onFilterCve && onFilterCve(cve)} 
                title={`Filter news stream for ${cve}`}
              >
                {cve}
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleCopyCve(cve);
                }}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  color: 'var(--neon-purple)',
                  display: 'flex'
                }}
                title="Copy CVE identifier"
              >
                {copiedCve === cve ? <Check size={13} color="var(--neon-green)" /> : <Copy size={13} />}
              </button>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
