import React from 'react';
import { Rss, ExternalLink, ShieldCheck, CheckCircle2, Globe, Radio, Zap } from 'lucide-react';

export default function SourcesView({ onRefresh, isRefreshing }) {
  const feeds = [
    {
      name: 'BleepingComputer',
      url: 'https://www.bleepingcomputer.com/feed/',
      focus: 'Ransomware syndicates, malware strains, data leaks, active exploits',
      cadence: 'Live (~20 stories/day)',
      latency: '~240ms',
      status: 'STREAM ACTIVE'
    },
    {
      name: 'The Hacker News',
      url: 'https://feeds.feedburner.com/TheHackersNews',
      focus: 'Zero-day vulnerability disclosures, APT espionage, remote code execution',
      cadence: 'Live (~50 stories/day)',
      latency: '~190ms',
      status: 'STREAM ACTIVE'
    },
    {
      name: 'SecurityWeek',
      url: 'https://securityweek.com/feed/',
      focus: 'Critical infrastructure, enterprise defense, industrial ICS/SCADA attacks',
      cadence: 'Live (~15 stories/day)',
      latency: '~320ms',
      status: 'STREAM ACTIVE'
    },
    {
      name: 'CISA Alerts (US Cybersecurity Agency)',
      url: 'https://www.cisa.gov/news.xml',
      focus: 'Official governmental KEV alerts, emergency directives, federal mitigations',
      cadence: 'Authoritative (~5-10/day)',
      latency: '~180ms',
      status: 'STREAM ACTIVE'
    },
    {
      name: 'KrebsOnSecurity',
      url: 'https://krebsonsecurity.com/feed/',
      focus: 'Investigative cybersecurity journalism, cybercrime networks, banking breaches',
      cadence: 'In-Depth Weekly',
      latency: '~210ms',
      status: 'STREAM ACTIVE'
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      
      {/* Intro HUD */}
      <div className="hud-panel" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.4rem' }}>
              <Rss size={22} color="var(--neon-cyan)" />
              <h2 style={{ fontSize: '1.25rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                // LIVE INGESTION PIPELINES (5 CONCURRENT STREAMS)
              </h2>
            </div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
              All 5 feeds are queried concurrently using Python ThreadPool workers, completing in under 2 seconds upon refresh.
            </p>
          </div>

          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="btn-cyber btn-cyber-live"
          >
            <Zap size={15} />
            {isRefreshing ? 'STREAMING ALL FEEDS...' : 'TEST ALL PIPELINES'}
          </button>
        </div>
      </div>

      {/* Feed Cards (All Clickable!) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
        gap: '1.35rem'
      }}>
        {feeds.map((feed) => (
          <div
            key={feed.name}
            className="cyber-card"
            style={{
              padding: '1.5rem',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: '1.15rem'
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
                <span className="clickable-badge badge-source" style={{ color: 'var(--neon-cyan)', borderColor: 'var(--border-neon)' }}>
                  {feed.name}
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.74rem', color: 'var(--neon-green)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                  <span className="live-beacon"></span> {feed.status}
                </span>
              </div>

              <div style={{ fontSize: '0.86rem', color: 'var(--text-primary)', marginBottom: '0.6rem', lineHeight: 1.45 }}>
                <strong style={{ color: 'var(--neon-cyan)' }}>Focus:</strong> {feed.focus}
              </div>

              <div style={{ display: 'flex', gap: '1rem', fontSize: '0.76rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                <span>CADENCE: {feed.cadence}</span>
                <span>LATENCY: {feed.latency}</span>
              </div>
            </div>

            <div style={{
              borderTop: '1px solid rgba(255, 255, 255, 0.06)',
              paddingTop: '0.85rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '220px' }}>
                {feed.url}
              </span>
              <a
                href={feed.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-cyber btn-cyber-sm btn-cyber-ghost"
                style={{ textDecoration: 'none' }}
              >
                FEED XML <ExternalLink size={12} />
              </a>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
