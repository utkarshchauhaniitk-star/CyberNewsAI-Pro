import React from 'react';
import { RefreshCw, Radio, Flame, Globe2, ShieldCheck, Zap } from 'lucide-react';

export default function Header({ 
  title, 
  subtitle, 
  onRefresh, 
  isRefreshing, 
  lastSyncTime,
  autoPoll,
  onToggleAutoPoll,
  latestAlert = null 
}) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border-neon)',
      background: 'rgba(3, 7, 15, 0.92)',
      backdropFilter: 'blur(16px)',
      position: 'sticky',
      top: 0,
      zIndex: 40,
      padding: '0.9rem 2.25rem'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '1.5rem',
        flexWrap: 'wrap'
      }}>
        {/* Title and Telemetry Subtitle */}
        <div>
          <h1 style={{
            fontSize: '1.4rem',
            fontWeight: 800,
            color: 'var(--text-primary)',
            letterSpacing: '0.02em',
            display: 'flex',
            alignItems: 'center',
            gap: '0.65rem'
          }}>
            <span style={{ color: 'var(--neon-cyan)', fontFamily: 'var(--font-mono)' }}>//</span>
            {title}
          </h1>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>
            {subtitle}
          </p>
        </div>

        {/* Real-time Threat Ticker */}
        {latestAlert && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.65rem',
            background: 'rgba(255, 51, 102, 0.12)',
            border: '1px solid rgba(255, 51, 102, 0.4)',
            padding: '0.45rem 0.95rem',
            borderRadius: 'var(--radius-full)',
            maxWidth: '480px',
            overflow: 'hidden',
            boxShadow: '0 0 15px rgba(255, 51, 102, 0.2)'
          }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--neon-crimson)', fontWeight: 800, fontSize: '0.74rem', whiteSpace: 'nowrap', fontFamily: 'var(--font-mono)' }}>
              <span className="live-beacon red"></span>
              ALERT:
            </span>
            <span style={{
              fontSize: '0.76rem',
              color: '#fecdd3',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              fontFamily: 'var(--font-sans)'
            }}>
              {latestAlert.title}
            </span>
          </div>
        )}

        {/* Action Controls & Real-Time Sync Button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          
          {/* Auto-Poll Toggle */}
          <button
            onClick={onToggleAutoPoll}
            className={`btn-cyber btn-cyber-sm ${autoPoll ? 'btn-cyber-live' : 'btn-cyber-ghost'}`}
            title="Toggle background auto-refresh every 60 seconds"
          >
            <Zap size={14} color={autoPoll ? 'var(--neon-green)' : 'currentColor'} />
            AUTO-SYNC: {autoPoll ? 'ON' : 'OFF'}
          </button>

          {/* Futuristic Live Sync Button */}
          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="btn-cyber btn-cyber-primary"
            style={{ padding: '0.55rem 1.25rem' }}
          >
            <RefreshCw 
              size={16} 
              style={{ animation: isRefreshing ? 'spin 0.8s linear infinite' : 'none' }} 
            />
            {isRefreshing ? 'STREAMING FEEDS...' : 'LIVE RADAR SYNC'}
          </button>

          {/* Active Feeds Badge */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.45rem 0.75rem',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(0, 242, 254, 0.08)',
            border: '1px solid var(--border-neon)',
            fontSize: '0.74rem',
            fontFamily: 'var(--font-mono)'
          }}>
            <Globe2 size={14} color="var(--neon-cyan)" />
            <span style={{ color: 'var(--neon-cyan)' }}>5 FEEDS</span>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </header>
  );
}
